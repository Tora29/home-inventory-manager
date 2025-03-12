<script lang="ts">
	import { onMount } from 'svelte';
	import { getCategories } from '$entities/categories';
	import { getItems } from '$entities/items';
	import type { Category } from '$entities/categories';
	import type { Item } from '$entities/items';

	let categories: Category[] = [];
	let items: Item[] = [];
	let loading = true;
	let error: string | null = null;

	// ページ読み込み時にデータを取得
	onMount(async () => {
		try {
			loading = true;
			// 並行して取得
			const [categoriesData, itemsData] = await Promise.all([
				getCategories(), 
				getItems()
			]);
			
			categories = categoriesData;
			items = itemsData;
			error = null;
		} catch (e) {
			console.error('Error fetching data:', e);
			error = e instanceof Error ? e.message : '通信エラーが発生しました';
		} finally {
			loading = false;
		}
	});

	// カテゴリ名を取得する関数
	function getCategoryName(categoryId: number | null): string {
		if (categoryId === null) return '未分類';
		const category = categories.find(c => c.id === categoryId);
		return category ? category.category_name : '未分類';
	}
</script>

<svelte:head>
	<title>ホーム在庫管理アプリ</title>
	<meta name="description" content="家庭の在庫管理をサポートするアプリ" />
</svelte:head>

<div class="container mx-auto p-4">
	<h1 class="text-2xl font-bold mb-6">ホーム在庫管理アプリ</h1>

	{#if loading}
		<div class="flex justify-center items-center h-40">
			<div class="loading loading-spinner text-primary"></div>
		</div>
	{:else if error}
		<div class="alert alert-error">
			<p>{error}</p>
			<button class="btn btn-sm" on:click={() => window.location.reload()}>再読み込み</button>
		</div>
	{:else}
		<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
			<!-- カテゴリリスト -->
			<div class="card bg-base-100 shadow-xl">
				<div class="card-body">
					<h2 class="card-title">カテゴリ一覧</h2>
					{#if categories.length === 0}
						<p>カテゴリがありません。カテゴリを追加してください。</p>
					{:else}
						<ul class="list-disc pl-5 space-y-2">
							{#each categories as category}
								<li>{category.category_name}</li>
							{/each}
						</ul>
					{/if}
					<div class="card-actions justify-end mt-4">
						<a href="/categories" class="btn btn-primary">カテゴリ管理</a>
					</div>
				</div>
			</div>

			<!-- アイテムリスト -->
			<div class="card bg-base-100 shadow-xl">
				<div class="card-body">
					<h2 class="card-title">最近のアイテム</h2>
					{#if items.length === 0}
						<p>アイテムがありません。アイテムを追加してください。</p>
					{:else}
						<div class="overflow-x-auto">
							<table class="table table-zebra w-full">
								<thead>
									<tr>
										<th>名前</th>
										<th>カテゴリ</th>
									</tr>
								</thead>
								<tbody>
									{#each items.slice(0, 5) as item}
										<tr>
											<td>{item.item_name}</td>
											<td>{getCategoryName(item.category_id)}</td>
										</tr>
									{/each}
								</tbody>
							</table>
						</div>
					{/if}
					<div class="card-actions justify-end mt-4">
						<a href="/items" class="btn btn-primary">アイテム管理</a>
					</div>
				</div>
			</div>
		</div>

		<!-- クイックアクション -->
		<div class="mt-8 card bg-base-100 shadow-xl">
			<div class="card-body">
				<h2 class="card-title">クイックアクション</h2>
				<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-4">
					<a href="/items/new" class="btn btn-primary">アイテム追加</a>
					<a href="/inventory" class="btn btn-secondary">在庫確認</a>
					<a href="/transactions/in" class="btn btn-accent">入庫登録</a>
					<a href="/transactions/out" class="btn btn-info">出庫登録</a>
				</div>
			</div>
		</div>
	{/if}
</div>
