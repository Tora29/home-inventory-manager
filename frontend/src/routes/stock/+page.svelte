<script lang="ts">
	import { onMount } from 'svelte';
	import {
		initializeWebSocket,
		scannedItems,
		stockInByBarcode,
		clearScannedItems,
		type BarcodeStockIn,
		type ScannedItem
	} from '$entities/stocks';
	import { createItem, type ItemCreate } from '$entities/items';
	import { fetchCategories, type Category } from '$entities/categories';
	import { fetchRooms, type Room } from '$entities/locations';
	import DropdownSelect from '$shared/components/DropdownSelect.svelte';
	import LabeledInput from '$shared/components/LabeledInput.svelte';
	import type { ComponentType, SvelteComponent } from 'svelte';

	// カテゴリリスト
	let categories = $state<Category[]>([]);
	let isLoadingCategories = $state(false);
	let lastScanTime = $state<Date | null>(null);

	// 部屋リスト
	let rooms = $state<{ value: string; label: string }[]>([]);
	let isLoadingRooms = $state(false);

	// 部屋一覧を取得
	const loadRooms = async () => {
		isLoadingRooms = true;
		try {
			const roomsData = await fetchRooms();
			rooms = roomsData.map((room) => ({
				value: room.name,
				label: room.name
			}));
			console.log('取得した部屋データ:', rooms);
		} catch (error) {
			console.error('部屋データ取得エラー:', error);
		} finally {
			isLoadingRooms = false;
		}
	};

	// カテゴリ一覧を取得
	const loadCategories = async () => {
		isLoadingCategories = true;
		try {
			categories = await fetchCategories();
		} catch (error) {
			console.error('カテゴリ取得エラー:', error);
		} finally {
			isLoadingCategories = false;
		}
	};

	// 新規商品登録用の状態
	let isNewItemFormVisible = $state(false);
	let newItemData = $state({
		barcode: '',
		name: '',
		category_id: '',
		location: '',
		quantity: 1
	});

	// スキャンに使用するフォーカス管理
	let barcodeInputComponent: SvelteComponent & { focus: () => void };

	// 履歴クリア確認用
	let showClearConfirm = $state(false);

	// バーコード読み取りデモ用の入力
	let barcodeInput = $state('');
	let itemNameInput = $state('');
	let locationInput = $state('');
	let categoryInput = $state('');
	let quantityInput = $state(1);

	// 新規商品登録関数
	const registerNewItem = async () => {
		if (!newItemData.name || !newItemData.barcode) {
			alert('商品名とバーコードは必須です');
			return;
		}

		try {
			// 新規商品を登録
			const itemData: ItemCreate = {
				barcode: newItemData.barcode,
				item_name: newItemData.name,
				category_id: newItemData.category_id ? parseInt(newItemData.category_id) : undefined
			};

			console.log('新規商品登録:', itemData);
			const createdItem = await createItem(itemData);

			console.log('商品登録完了:', createdItem);

			// 在庫登録
			if (createdItem) {
				const stockData: BarcodeStockIn = {
					barcode: newItemData.barcode,
					location: newItemData.location,
					quantity: newItemData.quantity
				};

				// 在庫登録APIを呼び出し
				await stockInByBarcode(stockData);

				// 最終スキャン時間を更新
				lastScanTime = new Date();
			}

			// フォームをリセット
			isNewItemFormVisible = false;
			newItemData = {
				barcode: '',
				name: '',
				category_id: '',
				location: '',
				quantity: 1
			};

			// バーコード入力にフォーカスを戻す
			if (barcodeInputComponent) {
				barcodeInputComponent.focus();
			}
		} catch (error) {
			console.error('商品登録エラー:', error);
			alert('商品登録に失敗しました');
		}
	};

	// バーコード送信ハンドラ
	async function handleSubmit() {
		try {
			if (!itemNameInput.trim()) {
				alert('商品名は必須です');
				return;
			}

			// 新規商品として直接登録
			const itemData: ItemCreate = {
				barcode: barcodeInput || undefined, // バーコードは任意
				item_name: itemNameInput,
				category_id: categoryInput ? parseInt(categoryInput) : undefined
			};

			console.log('送信する商品データ:', itemData);

			try {
				// 商品が存在しない場合は新規登録
				const createdItem = await createItem(itemData);
				console.log('商品登録完了:', createdItem);

				// カテゴリIDを数値として確保
				const categoryId = categoryInput ? parseInt(categoryInput) : null;

				// カテゴリ名を取得
				let categoryName = '未分類';
				if (categoryId) {
					const selectedCategory = categories.find((cat) => cat.id === categoryId);
					if (selectedCategory) {
						categoryName = selectedCategory.name;
					}
				}

				// 在庫登録
				const data: BarcodeStockIn = {
					barcode: createdItem.barcode || barcodeInput || createdItem.id.toString(), // バーコードがない場合はIDを使用
					location: locationInput || '入荷',
					quantity: quantityInput || 1
				};

				console.log('在庫登録データ:', data);
				const stockResponse = await stockInByBarcode(data);
				console.log('在庫登録レスポンス:', stockResponse);

				// 正しい商品名を使用（API応答から取得するのではなく、入力された商品名をそのまま使用）
				const newItem: ScannedItem = {
					id: Date.now().toString(),
					timestamp: new Date(),
					barcode: data.barcode,
					item_name: itemNameInput, // 入力した商品名をそのまま使用
					location: data.location || '入荷',
					quantity: data.quantity || 1,
					isNew: false,
					category_id: categoryId,
					category_name: categoryName
				};

				// スキャン履歴に一時的に追加（WebSocketで上書きされる）
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

				// 最終スキャン時間を更新
				lastScanTime = new Date();

				// 入力をリセット
				barcodeInput = '';
				itemNameInput = '';
				categoryInput = '';
				locationInput = '';
				quantityInput = 1;

				// 自動でフォーカス
				barcodeInputComponent?.focus();
			} catch (error) {
				console.error('商品登録エラー:', error);
				alert('商品登録に失敗しました: ' + error);
			}
		} catch (error) {
			console.error('処理エラー:', error);
			alert('エラーが発生しました: ' + error);
		}
	}

	// 履歴クリア確認画面を表示
	const showClearConfirmation = () => {
		showClearConfirm = true;
	};

	// 履歴クリアを実行
	const confirmClearHistory = () => {
		clearScannedItems();
		showClearConfirm = false;
	};

	// キャンセル
	const cancelClearHistory = () => {
		showClearConfirm = false;
	};

	// 日付フォーマット関数
	const formatDate = (date: Date) => {
		return new Intl.DateTimeFormat('ja-JP', {
			year: 'numeric',
			month: '2-digit',
			day: '2-digit'
		}).format(date);
	};

	// WebSocket接続とカテゴリ取得を開始
	onMount(() => {
		initializeWebSocket();
		loadCategories();
		loadRooms();

		// ページ読み込み時に自動でフォーカス
		if (barcodeInputComponent) {
			barcodeInputComponent.focus();
		}

		// クリーンアップ
		return () => {
			// WebSocketは共有リソースなのでクローズしない
		};
	});
</script>

<div class="flex flex-col gap-6">
	<!-- バーコードスキャナーセクション -->
	<div class="card p-4">
		<h2 class="h3 mb-4">バーコードスキャナー</h2>

		<!-- 商品登録フォーム -->
		<div class="p-4 rounded-lg mb-8 border border-surface-300-600-token">
			<h3 class="h4 mb-2">商品登録</h3>
			<form
				onsubmit={(e) => {
					e.preventDefault();
					handleSubmit();
				}}
				class="space-y-4"
			>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
					<div>
						<LabeledInput
							type="text"
							id="itemName"
							label="商品名"
							placeholder="商品名を入力"
							required={true}
							bind:value={itemNameInput}
							autocomplete="off"
						/>
					</div>
					<div>
						<LabeledInput
							type="text"
							id="barcode"
							label="バーコード"
							placeholder="バーコードを入力（任意）"
							bind:value={barcodeInput}
							bind:this={barcodeInputComponent}
							autocomplete="off"
						/>
					</div>
					<div>
						<label for="category" class="block mb-1 text-sm font-medium">カテゴリ</label>
						<DropdownSelect
							options={categories.map((cat) => ({ value: cat.id.toString(), label: cat.name }))}
							value={categoryInput}
							placeholder="カテゴリを選択"
							label=""
							onChange={(value) => (categoryInput = value)}
						/>
					</div>
					<div>
						<label for="location" class="block mb-1 text-sm font-medium">保管場所</label>
						<DropdownSelect
							options={rooms}
							value={locationInput}
							placeholder="保管場所を選択"
							label=""
							onChange={(value) => (locationInput = value)}
						/>
					</div>
					<div>
						<LabeledInput
							type="number"
							id="quantity"
							label="数量"
							bind:value={quantityInput}
							min="1"
							className="w-full"
						/>
					</div>
				</div>
				<button type="submit" class="btn variant-filled-primary"> 登録 </button>
			</form>
		</div>

		<!-- 直近のスキャン情報 -->
		{#if lastScanTime}
			<div class="alert variant-soft-primary p-3 rounded mb-4 flex items-center justify-between">
				<div>
					<span class="text-sm">最終スキャン: {formatDate(lastScanTime)}</span>
				</div>
				<button onclick={showClearConfirmation} class="btn-sm variant-soft-error">
					履歴をクリア
				</button>
			</div>
		{/if}
	</div>

	<!-- スキャン履歴セクション -->
	<div class="card p-4">
		<h2 class="h3 mb-4">スキャン履歴</h2>
		{#if $scannedItems.length === 0}
			<p class="italic text-sm opacity-70">まだ履歴がありません</p>
		{:else}
			<div class="table-container">
				<table class="table table-hover">
					<thead>
						<tr>
							<th>日時</th>
							<th>商品名</th>
							<th>バーコード</th>
							<th>収納場所</th>
							<th>数量</th>
							<th>カテゴリ</th>
							<th>状態</th>
						</tr>
					</thead>
					<tbody>
						{#each $scannedItems as item (item.id)}
							<tr>
								<td class="whitespace-nowrap text-sm">
									{formatDate(item.timestamp)}
								</td>
								<td class="whitespace-nowrap text-sm font-medium">
									{item.item_name}
								</td>
								<td class="whitespace-nowrap text-sm">
									{item.barcode}
								</td>
								<td class="whitespace-nowrap text-sm">
									{item.location}
								</td>
								<td class="whitespace-nowrap text-sm">
									{item.quantity}
								</td>
								<td class="whitespace-nowrap text-sm">
									{item.category_name || '未分類'}
								</td>
								<td class="whitespace-nowrap text-sm">
									{#if item.isNew}
										<span class="badge variant-soft-success"> 新規登録 </span>
									{:else}
										<span class="badge variant-soft-primary"> 入荷処理 </span>
									{/if}
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{/if}
	</div>
</div>

<!-- クリア確認ダイアログ -->
{#if showClearConfirm}
	<div
		class="modal-backdrop fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
	>
		<div class="modal-container bg-surface-100-800-token rounded-lg p-6 max-w-md w-full">
			<h3 class="h4 mb-4">履歴クリアの確認</h3>
			<p class="mb-4 text-sm opacity-70">
				スキャン履歴をすべて削除します。この操作は元に戻せません。
			</p>
			<div class="flex justify-end space-x-3">
				<button onclick={cancelClearHistory} class="btn variant-ghost"> キャンセル </button>
				<button onclick={confirmClearHistory} class="btn variant-filled-error"> 削除する </button>
			</div>
		</div>
	</div>
{/if}
