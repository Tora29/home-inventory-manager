import { API_BASE_URL } from '$shared/utils/apiConfig';
import type {
	BarcodeStockIn,
	StockInResponse,
	StockNotification,
	ScannedItem
} from '../model/types';
import { writable, get } from 'svelte/store';

// スキャン履歴を保持するストア
export const scannedItems = writable<ScannedItem[]>([]);

// ローカルストレージキー
const STORAGE_KEY = 'scanned_items_history';

// WebSocketコネクション
let socket: WebSocket | null = null;
let reconnectTimer: ReturnType<typeof setTimeout> | null = null;
let isConnecting = false;

// 初期データのロード
const loadInitialData = () => {
	try {
		const savedData = localStorage.getItem(STORAGE_KEY);
		if (savedData) {
			const parsedData = JSON.parse(savedData) as { items: ScannedItem[] };

			// 日付を文字列からDateオブジェクトに変換
			const itemsWithDateObjects = parsedData.items.map((item) => ({
				...item,
				timestamp: new Date(item.timestamp)
			}));

			scannedItems.set(itemsWithDateObjects);
			console.log(`${itemsWithDateObjects.length}件のスキャン履歴を読み込みました`);
		}
	} catch (error) {
		console.error('スキャン履歴の読み込みに失敗しました:', error);
		// エラーが発生した場合は空の配列を設定
		scannedItems.set([]);
	}
};

// スキャン履歴の保存
const saveScannedItems = (items: ScannedItem[]) => {
	try {
		// 最大100件までを保存
		const itemsToSave = items.slice(0, 100);
		localStorage.setItem(STORAGE_KEY, JSON.stringify({ items: itemsToSave }));
	} catch (error) {
		console.error('スキャン履歴の保存に失敗しました:', error);
	}
};

// ストアの変更を監視して保存
scannedItems.subscribe((items) => {
	if (items.length > 0) {
		saveScannedItems(items);
	}
});

// 初期ロード実行
loadInitialData();

/**
 * WebSocket接続を初期化し、在庫更新通知を受け取る
 */
export const initializeWebSocket = () => {
	// 既に接続中なら何もしない
	if (isConnecting) {
		console.log('WebSocketは接続処理中です');
		return;
	}

	const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
	const wsHost = API_BASE_URL.includes('localhost') ? 'localhost:8000' : window.location.host;

	const wsUrl = `${wsProtocol}//${wsHost}/v1/ws/stock`;

	// WebSocketが既に接続されていれば何もしない
	if (socket && socket.readyState === WebSocket.OPEN) {
		console.log('WebSocketは既に接続されています');
		return;
	}

	// 接続中フラグを設定
	isConnecting = true;

	console.log(`WebSocket接続開始: ${wsUrl}`);

	// 再接続タイマーがあればクリア
	if (reconnectTimer) {
		clearTimeout(reconnectTimer);
		reconnectTimer = null;
	}

	try {
		socket = new WebSocket(wsUrl);

		socket.onopen = () => {
			console.log('WebSocketに接続しました');
			isConnecting = false;
		};

		socket.onmessage = (event) => {
			try {
				const notification = JSON.parse(event.data) as StockNotification;
				console.log('在庫更新通知を受信:', notification);

				if (notification.type === 'stock_in') {
					// 現在のスキャン履歴を確認
					const currentItems = get(scannedItems);

					// 同じバーコードのアイテムがあるか確認（最新の登録情報がある可能性）
					const existingItem = currentItems.find(
						(item) =>
							item.barcode === notification.data.barcode &&
							item.location === notification.data.location
					);

					// スキャン履歴に追加
					const newItem: ScannedItem = {
						id: Date.now().toString(),
						timestamp: new Date(),
						barcode: notification.data.barcode,
						// 既存アイテムの商品名を優先して使用（存在すれば）
						item_name: existingItem ? existingItem.item_name : notification.data.item_name,
						location: notification.data.location,
						quantity: notification.data.quantity,
						isNew: false, // WebSocketからの通知は常に既存商品
						category_id: notification.data.category_id,
						category_name: notification.data.category_name
					};

					// デバッグログ
					console.log('WebSocket通知からのアイテム:', newItem);

					scannedItems.update((items) => {
						// 同じバーコードと場所の組み合わせがあるか確認
						const existingItemIndex = items.findIndex(
							(item) => item.barcode === newItem.barcode && item.location === newItem.location
						);

						// 新しいアイテムリストを作成
						let newItems = [...items];

						// 既存のアイテムがあれば更新、なければ追加
						if (existingItemIndex > -1) {
							// 既存のアイテムがあれば、それを削除
							newItems.splice(existingItemIndex, 1);
						}

						// 新しいアイテムを先頭に追加
						return [newItem, ...newItems];
					});
				}
			} catch (error) {
				console.error('WebSocketメッセージの解析エラー:', error);
			}
		};

		socket.onclose = (event) => {
			console.log(`WebSocket接続が閉じられました: コード=${event.code}, 理由=${event.reason}`);
			isConnecting = false;

			// 正常に閉じられた場合以外は再接続を試みる
			if (event.code !== 1000) {
				// 3秒後に再接続を試みる
				reconnectTimer = setTimeout(initializeWebSocket, 3000);
				console.log('3秒後に再接続を試みます');
			}
		};

		socket.onerror = (error) => {
			console.error('WebSocketエラー:', error);
			isConnecting = false;
		};
	} catch (error) {
		console.error('WebSocket接続エラー:', error);
		isConnecting = false;

		// 3秒後に再接続を試みる
		reconnectTimer = setTimeout(initializeWebSocket, 3000);
	}
};

/**
 * バーコードスキャンによる在庫追加
 * @param data バーコードデータ
 * @returns API応答
 */
export const stockInByBarcode = async (data: BarcodeStockIn): Promise<StockInResponse> => {
	try {
		console.log('バーコード在庫登録を開始:', data);
		const url = `${API_BASE_URL}/stock/in`;

		const response = await fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		});

		if (!response.ok) {
			let errorBody = '';
			try {
				errorBody = await response.text();
			} catch (e) {
				errorBody = 'レスポンス本文を取得できません';
			}

			throw new Error(`APIエラー: ${response.status} - ${response.statusText} - ${errorBody}`);
		}

		const result = (await response.json()) as StockInResponse;
		console.log('バーコード在庫登録成功:', result);

		return result;
	} catch (error) {
		console.error('バーコード在庫登録エラー:', error);
		throw error;
	}
};

/**
 * クライアントサイドでスキャン履歴に新規アイテムを追加
 * @param item 新規スキャンアイテム
 */
export const addScannedItem = (item: Omit<ScannedItem, 'id' | 'timestamp'>) => {
	const newItem: ScannedItem = {
		...item,
		id: Date.now().toString(),
		timestamp: new Date()
	};

	scannedItems.update((items) => [newItem, ...items]);
	return newItem;
};

/**
 * スキャン履歴をクリアする
 */
export const clearScannedItems = () => {
	scannedItems.set([]);
	localStorage.removeItem(STORAGE_KEY);
};
