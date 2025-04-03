import type { Item, ItemCreate, ItemDetail, ItemUpdate } from '../model/types';
import { API_BASE_URL } from '$shared/utils/apiConfig';

/**
 * アイテム一覧を取得する
 * @param skip スキップする件数
 * @param limit 取得する上限件数
 * @returns アイテムのリスト
 */
export const fetchItems = async (skip: number = 0, limit: number = 100): Promise<Item[]> => {
	try {
		const url = `${API_BASE_URL}/items/?skip=${skip}&limit=${limit}`;

		const response = await fetch(url);

		if (!response.ok) {
			let errorBody = '';
			try {
				errorBody = await response.text();
			} catch (e) {
				errorBody = 'レスポンス本文を取得できません';
			}

			throw new Error(`APIエラー: ${response.status} - ${response.statusText} - ${errorBody}`);
		}

		const data = await response.json();
		return data;
	} catch (error) {
		console.error('アイテムデータの取得に失敗しました:', error);
		throw error;
	}
};

/**
 * アイテム一覧を取得する（getItemsは互換性のために残しています）
 * @param skip スキップする件数
 * @param limit 取得する上限件数
 * @returns アイテムのリスト
 */
export const getItems = fetchItems;

/**
 * ID指定でアイテムを取得する
 * @param id アイテムID
 * @returns アイテム情報
 */
export const getItem = async (id: number): Promise<ItemDetail> => {
	try {
		const url = `${API_BASE_URL}/items/${id}`;
		const response = await fetch(url);

		if (!response.ok) {
			throw new Error(`APIエラー: ${response.status} - ${response.statusText}`);
		}

		return await response.json();
	} catch (error) {
		console.error(`アイテム(ID: ${id})の取得に失敗しました:`, error);
		throw error;
	}
};

/**
 * バーコードでアイテムを検索する
 * @param barcode バーコード
 * @returns アイテム情報（見つからない場合はnull）
 */
export const getItemByBarcode = async (barcode: string): Promise<ItemDetail | null> => {
	try {
		const url = `${API_BASE_URL}/items/barcode/${barcode}`;
		const response = await fetch(url);

		if (response.status === 404) {
			return null;
		}

		if (!response.ok) {
			throw new Error(`APIエラー: ${response.status} - ${response.statusText}`);
		}

		return await response.json();
	} catch (error) {
		console.error(`バーコード(${barcode})でのアイテム検索に失敗しました:`, error);
		throw error;
	}
};

/**
 * 新規アイテムを作成する
 * @param data アイテム作成データ
 * @returns 作成されたアイテム
 */
export const createItem = async (data: ItemCreate): Promise<Item> => {
	try {
		const url = `${API_BASE_URL}/items/`;

		// バックエンドのスキーマに合わせてフィールド名を変換
		const convertedData = {
			name: data.item_name,
			barcode: data.barcode,
			category_id: data.category_id,
			note: data.note
		};

		console.log('API送信データ:', convertedData);

		const response = await fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(convertedData)
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

		return await response.json();
	} catch (error) {
		console.error('アイテムの作成に失敗しました:', error);
		throw error;
	}
};

/**
 * アイテムを更新する
 * @param id アイテムID
 * @param data 更新データ
 * @returns 更新されたアイテム
 */
export const updateItem = async (id: number, data: ItemUpdate): Promise<Item> => {
	try {
		const url = `${API_BASE_URL}/items/${id}`;
		const response = await fetch(url, {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		});

		if (!response.ok) {
			throw new Error(`APIエラー: ${response.status} - ${response.statusText}`);
		}

		return await response.json();
	} catch (error) {
		console.error(`アイテム(ID: ${id})の更新に失敗しました:`, error);
		throw error;
	}
};

/**
 * アイテムを削除する
 * @param id アイテムID
 * @returns 削除結果
 */
export const deleteItem = async (id: number): Promise<void> => {
	try {
		const url = `${API_BASE_URL}/items/${id}`;
		const response = await fetch(url, {
			method: 'DELETE'
		});

		if (!response.ok) {
			throw new Error(`APIエラー: ${response.status} - ${response.statusText}`);
		}
	} catch (error) {
		console.error(`アイテム(ID: ${id})の削除に失敗しました:`, error);
		throw error;
	}
};
