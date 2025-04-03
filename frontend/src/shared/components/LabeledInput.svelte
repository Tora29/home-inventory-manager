<script lang="ts">
	/**
	 * ラベル付きインプットコンポーネント
	 *
	 * @param type - 入力タイプ
	 * @param placeholder - プレースホルダーテキスト
	 * @param value - 入力値
	 * @param disabled - 無効状態
	 * @param required - 必須フィールド
	 * @param name - フィールド名
	 * @param id - 要素ID
	 * @param label - ラベルテキスト
	 * @param className - 追加のCSSクラス
	 * @param autocomplete - オートコンプリート設定
	 * @param min - 数値フィールドの最小値
	 * @param max - 数値フィールドの最大値
	 * @param step - 数値フィールドのステップ
	 */

	// props定義
	let {
		type = 'text',
		placeholder = '',
		value = $bindable(''),
		disabled = false,
		required = false,
		name = '',
		id = '',
		label = '',
		className = '',
		autocomplete = 'off',
		min = undefined,
		max = undefined,
		step = undefined
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
		min?: string | number;
		max?: string | number;
		step?: string | number;
	}>();

	// HTMLInputElement参照
	let inputElement: HTMLInputElement;

	// フォーカスメソッド
	export function focus() {
		inputElement?.focus();
	}

	// 入力要素を取得するためのメソッド
	export function getInputElement(): HTMLInputElement | undefined {
		return inputElement;
	}
</script>

<div>
	<label for={id} class="block mb-1 text-sm font-medium">
		{label}
		{#if required}
			<span class="text-error-500">*</span>
		{/if}
	</label>
	<input
		{type}
		{name}
		{id}
		{placeholder}
		{disabled}
		{required}
		{autocomplete}
		{min}
		{max}
		{step}
		bind:value
		bind:this={inputElement}
		class="input w-full {className}"
	/>
</div>
