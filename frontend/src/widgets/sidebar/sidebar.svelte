<script lang="ts">
	import { Navigation } from '@skeletonlabs/skeleton-svelte';

	import IconHome from '@lucide/svelte/icons/house';
	import IconLayoutDashboard from '@lucide/svelte/icons/layout-dashboard';
	import IconPackage from '@lucide/svelte/icons/package';
	import IconClipboardList from '@lucide/svelte/icons/clipboard-list';
	import IconSettings from '@lucide/svelte/icons/settings';
</script>

<div class="h-full border-r border-surface-100-900">
	<Navigation.Rail>
		{#snippet header()}
			<Navigation.Tile label="Home" href="/" title="Home"><IconHome /></Navigation.Tile>
		{/snippet}
		{#snippet tiles()}
			<Navigation.Tile label="Dashboard" href="/dashboard"><IconLayoutDashboard /></Navigation.Tile>
			<Navigation.Tile label="Stock" href="/stock"><IconPackage /></Navigation.Tile>
			<Navigation.Tile label="Items" href="/items"><IconClipboardList /></Navigation.Tile>
		{/snippet}
		{#snippet footer()}
			<Navigation.Tile label="Settings" href="/settings" title="settings"
				><IconSettings /></Navigation.Tile
			>
		{/snippet}
	</Navigation.Rail>
</div>
