<script lang="ts">
	import { onMount } from 'svelte';
	import { fetchStocks, type Stock } from '$entities/stocks';
	import { fetchCategories, type Category } from '$entities/categories';

	import DataTable, { type Column, type DataItem } from '$shared/components/DataTable.svelte';
	import SearchInput from '$shared/components/SearchInput.svelte';
	import DropdownSelect from '$shared/components/DropdownSelect.svelte';
	import Button from '$shared/components/Button.svelte';
	import AlertWithText from '$shared/components/AlertWithText.svelte';

	import CircleAlert from '@lucide/svelte/icons/circle-alert';

	import {
		loadFloorPlanJson,
		generateSvgFromJson,
		addRoomClickEvents
	} from '$shared/utils/jsonToSvgUtils';
	import type { FloorPlan } from '$shared/types/floorPlan';

	let svgContent = $state('');
	let stocks = $state<Stock[]>([]);
	let categories = $state<Category[]>([]);
	let selectedLocation = $state<string | null>(null);
	let selectedCategory = $state('');
	let filteredStocks = $state<Stock[]>([]);
	let floorPlan = $state<FloorPlan | null>(null);
	let searchKeyword = $state('');

	// フィルタリング条件が変更されたらフィルタリングを適用
	$effect(() => {
		applyFilters();
	});

	// テーブル列定義
	const stockColumns: Column[] = [
		{
			header: '商品名',
			key: 'item.name',
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
			key: 'location',
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
			key: 'item.category.name',
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

	// 場所によるフィルタリング
	function filterStocksByLocation(location: string): Stock[] {
		return stocks.filter((stock) => stock.location === location);
	}

	// キーワードによるフィルタリング
	function filterStocksByKeyword(keyword: string, stocksToFilter: Stock[]): Stock[] {
		if (!keyword) return stocksToFilter;

		const lowerKeyword = keyword.toLowerCase();
		return stocksToFilter.filter((stock) => stock.item?.name?.toLowerCase().includes(lowerKeyword));
	}

	// カテゴリによるフィルタリング
	function filterStocksByCategory(categoryId: string, stocksToFilter: Stock[]): Stock[] {
		if (!categoryId) return stocksToFilter;

		return stocksToFilter.filter((stock) => stock.item?.category?.id === parseInt(categoryId));
	}

	// 検索とロケーションフィルターを組み合わせて適用
	function applyFilters() {
		let result = stocks;

		// ロケーションフィルター適用
		if (selectedLocation) {
			result = filterStocksByLocation(selectedLocation);
		}

		// カテゴリフィルター適用
		if (selectedCategory) {
			result = filterStocksByCategory(selectedCategory, result);
		}

		// 検索キーワードフィルター適用（商品名のみ）
		if (searchKeyword) {
			result = filterStocksByKeyword(searchKeyword, result);
		}

		filteredStocks = result;
	}

	// カテゴリの選択変更時
	function handleCategoryChange(categoryId: string) {
		selectedCategory = categoryId;
		applyFilters();
	}

	// 部屋クリック時の処理
	function handleRoomClick(roomName: string) {
		// 同じ部屋が選択された場合は選択解除
		if (selectedLocation === roomName) {
			selectedLocation = null;
		} else {
			selectedLocation = roomName;
		}
		applyFilters();
	}

	// 選択解除ボタンの処理
	function clearSelection() {
		selectedLocation = null;
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
		selectedLocation = null;
		selectedCategory = '';
		searchKeyword = '';
		applyFilters();
	}

	onMount(async () => {
		try {
			// JSONから間取り図データを読み込む
			floorPlan = await loadFloorPlanJson('/floorPlan.json');

			// JSONデータからSVGを生成
			svgContent = generateSvgFromJson(floorPlan);

			// SVG生成後、部屋要素にクリックイベントを追加
			addRoomClickEvents(handleRoomClick);
		} catch (error) {
			console.error('間取り図データの読み込みに失敗しました:', error);
		}

		// カテゴリデータを取得
		try {
			categories = await fetchCategories();
		} catch (error) {
			console.error('カテゴリデータの取得に失敗しました:', error);
		}

		// 在庫データを取得
		try {
			stocks = await fetchStocks();
			// 初期表示時は全ての在庫を表示
			filteredStocks = [...stocks];
			console.log('取得した在庫データ:', stocks);
		} catch (error) {
			console.error('在庫データの取得に失敗しました:', error);
			// エラー詳細を表示
			if (error instanceof Error) {
				console.error('エラーの詳細:', error.message, error.stack);
			}
		}
	});
</script>

<!-- コンテンツコンテナ -->
<div class="flex flex-col gap-6">
	<!-- 間取り図セクション -->
	<div class="card p-4">
		<h2 class="h3 mb-4">
			間取り図
			<p class="text-sm font-normal">選択した部屋の在庫を表示します。</p>
		</h2>

		<!-- 間取り図を中央に配置 -->
		<div class="flex justify-center items-center my-4">
			{@html svgContent}
		</div>
	</div>

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
						options={categories.map((cat) => ({ value: cat.id.toString(), label: cat.name }))}
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
				data={filteredStocks}
				columns={stockColumns}
				showTotal={true}
				totalLabel="合計"
				emptyMessage="在庫データがありません"
				{getRowClass}
			/>
		</div>
	</div>
</div>

<style>
	:global(.room-element) {
		cursor: pointer;
		transition: fill 0.2s ease-in-out;
	}

	:global(.room-element:hover) {
		fill: #a8a8a8 !important;
	}
</style>
