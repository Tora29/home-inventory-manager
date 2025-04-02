<script lang="ts">
	const {
		type = 'text',
		placeholder = '',
		value = '',
		disabled = false,
		required = false,
		name = '',
		id = '',
		label = '',
		className = '',
		autocomplete = 'off'
	} = $props<{
		type?: 'text' | 'password' | 'email' | 'number' | 'search' | 'tel' | 'url';
		placeholder?: string;
		value?: string | number;
		disabled?: boolean;
		required?: boolean;
		name?: string;
		id?: string;
		label?: string;
		className?: string;
		autocomplete?: string;
	}>();

	let inputValue = $state(value);

	function handleInput(event: Event) {
		const target = event.target as HTMLInputElement;
		inputValue = target.value;
	}

	$effect(() => {
		inputValue = value;
	});
</script>

{#if label}
	<label class="label">
		<span class="label-text">{label}</span>
		<input
			{type}
			{name}
			{id}
			{placeholder}
			{disabled}
			{required}
			{autocomplete}
			class={`input ${className}`}
			value={inputValue}
			oninput={handleInput}
			onchange={() => {}}
		/>
	</label>
{:else}
	<input
		{type}
		{name}
		{id}
		{placeholder}
		{disabled}
		{required}
		{autocomplete}
		class={`input ${className}`}
		value={inputValue}
		oninput={handleInput}
		onchange={() => {}}
	/>
{/if}
