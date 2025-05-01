<script lang="ts">
  import type { PageProps } from './$types';
  let { data }: PageProps = $props();
</script>
  
<h1>アイテム一覧</h1>

{#if 'error' in data.items}
  <p>エラー: {data.items.error}</p>
{:else if data.items.length === 0}
  <p>アイテムがありません</p>
{:else}
  <ul>
    {#each data.items as item}
      <li>商品名：{item.name}（バーコード: {item.barcode}）</li>
    {/each}
  </ul>
{/if}
  