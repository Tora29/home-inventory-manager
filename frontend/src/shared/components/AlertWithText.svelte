<script lang="ts">
	import CircleAlert from '@lucide/svelte/icons/circle-alert';

	const { text = '', iconClass = 'text-error-500' } = $props<{
		text: string;
		iconClass?: string;
	}>();
</script>

<div class="flex items-center gap-2">
	<CircleAlert color={'orange'} size={16} class={iconClass} />
	<span>{text}</span>
</div>
