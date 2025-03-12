<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchItems } from '../api/itemsApi';

  let items: Array<any> = [];
  let error: string | null = null;

  onMount(async () => {
      try {
          items = await fetchItems();
      } catch (e: unknown) {
          error = e instanceof Error ? e.message : 'Unknown error occurred';
      }
  });
</script>

{#if error}
  <p>エラーが発生しました: {error}</p>
{:else}
  <ul>
    {#each items as item}
        <li>{item.id}: {item.name} - {item.category} - {item.description}</li>
    {/each}
  </ul>
{/if}

<style>
p {
  color: red;
}
</style>