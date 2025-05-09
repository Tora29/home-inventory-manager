<script lang="ts">
	import type { PageProps } from './$types';
	let { data }: PageProps = $props();

	import { onMount } from 'svelte';
	import type { Stock } from '$features/stockList/model/stockModel';
	import type { Category } from '$features/stockList/model/categoryModel';
	import type { Item } from '$features/stockList/model/itemModel';
	import type { Location } from '$features/stockList/model/locationModel';

	import FloorViewer from '$features/floorViewer/ui/FloorViewer.svelte';
	import StockDataTable from '$features/stockList/ui/StockList.svelte';

	let stocks = $state<Stock[]>([]);
	let categories = $state<Category[]>([]);
	let selectedLocation = $state<string | null>(null);
	let items = $state<Item[]>([]);
	let locations = $state<Location[]>([]);

	// 場所変更時のコールバック（FloorViewerとStockDataTableで共通利用）
	function handleLocationChange(locationId: string | null) {
		selectedLocation = locationId;
	}

	onMount(async () => {
		// カテゴリデータと在庫データを取得
		if (data) {
			// カテゴリデータをセット
			if (Array.isArray(data.categories)) {
				categories = data.categories;
			}
			
			// アイテムデータをセット
			if (Array.isArray(data.items)) {
				items = data.items;
			}
			
			// ロケーションデータをセット
			if (Array.isArray(data.locations)) {
				locations = data.locations;
			}
			
			// 在庫データをセット
			if (Array.isArray(data.stocks)) {
				stocks = data.stocks;
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

		<!-- 間取り図 -->
		<FloorViewer 
			onRoomClick={handleLocationChange} 
			selectedLocation={selectedLocation}
		/>
	</div>

	<!-- 在庫一覧テーブル -->
	<StockDataTable 
		stocks={stocks} 
		items={items} 
		locations={locations}
		categories={categories}
		selectedLocation={selectedLocation}
		onLocationChange={handleLocationChange}
	/>
</div>

