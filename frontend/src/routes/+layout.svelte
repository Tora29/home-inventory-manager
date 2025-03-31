<script lang="ts">
  import '../app.css';
	let { children } = $props();
	import Header from '$widgets/header/ui/header.svelte';
  import Sidebar from '$widgets/sidebar/sidebar.svelte';
</script>

<div class="flex flex-col h-screen w-full">
  <Header />
  <div class="flex flex-1 overflow-hidden">
    <Sidebar />
    <main class="flex-1 overflow-auto p-4">
      {@render children()}
    </main>
  </div>
</div>
