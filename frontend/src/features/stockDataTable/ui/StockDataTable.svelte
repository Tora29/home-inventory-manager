<script lang="ts">
	import type { Stock } from '$features/stockDataTable/model/stockModel';
	import type { Category } from '$features/stockDataTable/model/categoryModel';
	import type { Item } from '$features/stockDataTable/model/itemModel';
	import type { Location } from '$features/stockDataTable/model/locationModel';
	
	import DataTable, { type Column, type DataItem } from '$shared/components/DataTable.svelte';
	import SearchInput from '$shared/components/SearchInput.svelte';
	import DropdownSelect from '$shared/components/DropdownSelect.svelte';
	import Button from '$shared/components/Button.svelte';
	import AlertWithText from '$shared/components/AlertWithText.svelte';
	
	import { applyStockFilters } from '$shared/utils/utilFilters';

	const props = $props<{
		stocks: Stock[];
		items: Item[];
		locations: Location[];
		categories: Category[];
		selectedLocation?: string | null;
		onLocationChange?: (locationId: string | null) => void;
	}>();

	let selectedCategory = $state('');
	let filteredStocks = $state<Stock[]>([]);
	let searchKeyword = $state('');
	
	const selectedLocation = $derived(props.selectedLocation ?? null);
	
	// 初期データの設定
	$effect(() => {
		filteredStocks = [...props.stocks];
	});

	// フィルタリング条件が変更されたらフィルタリングを適用
	$effect(() => {
		applyFilters();
	});

	// テーブル列定義
	const stockColumns: Column[] = [
		{
			header: '商品名',
			key: 'itemName',
			width: '25%',
			sortable: true,
			formatter: (value: string, item: DataItem) => {
				const quantity = Number(item.quantity);
				if (quantity <= 1) {
					return {
						component: AlertWithText,
						props: {
							text: value,
							iconClass: 'text-error-500'
						}
					};
				}
				return value;
			}
		},
		{
			header: '保管場所',
			key: 'locationName',
			fallback: '未設定',
			width: '20%',
			sortable: true
		},
		{
			header: '数量',
			key: 'quantity',
			width: '10%',
			align: 'left',
			sortable: true
		},
		{
			header: 'カテゴリ',
			key: 'categoryName',
			fallback: '未分類',
			width: '20%',
			sortable: true
		},
		{
			header: '最新入荷日時',
			key: 'updated_at',
			formatter: (value: string) => new Date(value).toLocaleDateString('ja-JP'),
			width: '25%',
			sortable: true
		}
	];

	// 表示用データの加工
	function transformStock(stock: Stock) {
		const item = Array.isArray(props.items) ? props.items.find((i: Item) => i.id === stock.item_id) : null;
		const location = Array.isArray(props.locations) ? props.locations.find((l: Location) => l.id === stock.location_id) : null;
		
		// カテゴリ情報の取得
		let categoryName = '未分類';
		if (item?.category_id) {
			const category = Array.isArray(props.categories) 
				? props.categories.find((c: Category) => c.id === item.category_id)
				: null;
			if (category) {
				categoryName = category.name;
			}
		}
		
		return {
			...stock,
			itemName: item?.name || '不明な商品',
			locationName: location?.name || '不明な場所',
			categoryName
		};
	}

	// 検索とロケーションフィルターを組み合わせて適用
	function applyFilters() {
		filteredStocks = applyStockFilters(
			props.stocks,
			{
				location: selectedLocation,
				categoryId: selectedCategory,
				keyword: searchKeyword
			},
			props.items,
			props.locations
		);
	}

	// カテゴリの選択変更時
	function handleCategoryChange(categoryId: string) {
		selectedCategory = categoryId;
		applyFilters();
	}

	// 選択解除ボタンの処理
	function clearSelection() {
		if (props.onLocationChange) {
			props.onLocationChange(null);
		}
		applyFilters();
	}

	// 在庫数が少ない場合の行スタイル
	function getRowClass(item: DataItem): string {
		if (Number(item.quantity) <= 1) {
			return 'bg-error-500/10 font-bold';
		}
		return '';
	}

	// フィルターをすべてリセット
	function resetFilters() {
		selectedCategory = '';
		searchKeyword = '';
		if (props.onLocationChange) {
			props.onLocationChange(null);
		}
		applyFilters();
	}
</script>

<!-- 在庫一覧セクション -->
<div class="card p-4">
	<h2 class="h3 mb-4">
		{#if selectedLocation}
			{selectedLocation}の在庫一覧
			<button class="btn-sm variant-ghost-surface" onclick={clearSelection}> 選択解除 ✖ </button>
		{:else}
			全ての在庫一覧
		{/if}
	</h2>

	<!-- フィルタリングセクション -->
	<div class="flex flex-col sm:flex-row justify-end gap-4 mb-6">
		<!-- フィルター項目のコンテナ -->
		<div class="flex flex-wrap gap-4 items-center">
			<!-- 商品名検索 -->
			<div class="flex-1 min-w-[300px]">
				<div class="text-sm font-medium mb-1">商品名</div>
				<SearchInput
					placeholder="商品名で検索"
					value={searchKeyword}
					buttonText="検索"
					onInputChange={(value) => {
						searchKeyword = value;
					}}
					onSearch={(value) => {
						searchKeyword = value;
					}}
				/>
			</div>

			<!-- カテゴリ選択 -->
			<div class="flex-1 min-w-[150px]">
				<div class="text-sm font-medium mb-1">カテゴリ</div>
				<DropdownSelect
					options={props.categories.map((cat: Category) => ({ value: cat.id.toString(), label: cat.name }))}
					placeholder="カテゴリを選択"
					value={selectedCategory}
					onChange={handleCategoryChange}
					label=""
				/>
			</div>
		</div>

		<!-- リセットボタン -->
		<div class="self-end">
			<Button
				variant="tonal"
				color="surface"
				onclick={resetFilters}
				children="フィルターをリセット"
			/>
		</div>
	</div>

	<div class="mt-4">
		<DataTable
			data={filteredStocks.map(stock => transformStock(stock))}
			columns={stockColumns}
			showTotal={true}
			totalLabel="合計"
			emptyMessage="在庫データがありません"
			{getRowClass}
		/>
	</div>
</div>
