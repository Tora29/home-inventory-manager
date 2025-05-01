<script lang="ts">
	/**
	 * ラベル付きインプットコンポーネント
	 * @component LabeledInput
	 */
	/**
	 * コンポーネントのプロパティ定義
	 * @typedef {Object} LabeledInputProps
	 * @property {('text'|'password'|'email'|'number'|'search'|'tel'|'url')} [type='text'] - 入力フィールドのタイプ
	 * @property {string} [placeholder=''] - プレースホルダーテキスト
	 * @property {string|number} [value=''] - 入力値
	 * @property {boolean} [disabled=false] - 無効状態の指定
	 * @property {boolean} [required=false] - 必須入力の指定
	 * @property {string} [name=''] - フォーム送信時の名前
	 * @property {string} [id=''] - 要素のID
	 * @property {string} [label=''] - ラベルテキスト
	 * @property {string} [className=''] - 追加のCSSクラス
	 * @property {string} [autocomplete='off'] - オートコンプリートの設定
	 * @property {string|number} [min] - 数値フィールドの最小値
	 * @property {string|number} [max] - 数値フィールドの最大値
	 * @property {string|number} [step] - 数値フィールドのステップ
	 * @property {('sm'|'md'|'lg')} [size='md'] - 入力フィールドのサイズ
	 * @property {string} [error=''] - エラーメッセージ
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
		step = undefined,
		size = 'md',
		error = ''
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
		size?: 'sm' | 'md' | 'lg';
		error?: string;
	}>();

	/**
	 * HTMLInputElement参照
	 */
	let inputElement: HTMLInputElement;

	/**
	 * 入力フィールドにフォーカスするメソッド
	 */
	export function focus() {
		inputElement?.focus();
	}

	/**
	 * 入力要素を取得するためのメソッド
	 * @returns {HTMLInputElement|undefined} 入力要素のDOM参照
	 */
	export function getInputElement(): HTMLInputElement | undefined {
		return inputElement;
	}

	/**
	 * インプットのスタイルクラスを取得する
	 * @returns {string} 適用するCSSクラス名の文字列
	 */
	function getInputClasses(): string {
		// サイズのマッピング
		const sizeMap: Record<string, string> = {
			sm: 'input-sm',
			md: '',
			lg: 'input-lg'
		};

		// 状態クラス
		const stateClasses = {
			disabled: disabled ? 'input-disabled' : '',
			error: error ? 'input-error' : ''
		};

		return [
			'input',
			'w-full',
			sizeMap[size],
			stateClasses.disabled,
			stateClasses.error,
			className
		]
			.filter(Boolean)
			.join(' ')
			.trim();
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
		class={getInputClasses()}
	/>
	{#if error}
		<div class="text-error-500 text-sm mt-1">{error}</div>
	{/if}
</div>
