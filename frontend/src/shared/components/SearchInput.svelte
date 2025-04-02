<script lang="ts">
	import Button from './Button.svelte';

  import SearchIcon from '@lucide/svelte/icons/search';

	const {
		placeholder = '検索...',
		value = '',
		buttonText = '検索',
		className = '',
		onSearch = undefined,
		onInputChange = undefined
	} = $props<{
		placeholder?: string;
		value?: string;
		buttonText?: string;
		className?: string;
		onSearch?: (value: string) => void;
		onInputChange?: (value: string) => void;
	}>();

	let searchValue = $state(value);

	function handleInput(event: Event) {
		const target = event.target as HTMLInputElement;
		searchValue = target.value;

		// 入力ごとに親コンポーネントに通知
		if (onInputChange) {
			onInputChange(searchValue);
		}
	}

	function handleSubmit() {
		if (onSearch) {
			onSearch(searchValue);
		}
	}

	function handleKeyPress(event: KeyboardEvent) {
		if (event.key === 'Enter') {
			if (onSearch) {
				onSearch(searchValue);
			}
		}
	}

	$effect(() => {
		searchValue = value;
	});
</script>

<div class={`input-group grid-cols-[auto_1fr_auto] ${className}`}>
	<div class="ig-cell preset-tonal">
		<SearchIcon />
	</div>
	<input
		type="search"
		class="ig-input"
		{placeholder}
		value={searchValue}
		oninput={handleInput}
		onkeypress={handleKeyPress}
	/>
	<Button
		variant="filled"
		color="primary"
		size="base"
		type="button"
		className="ig-btn"
		onclick={handleSubmit}
		children={buttonText}
	/>
</div>
