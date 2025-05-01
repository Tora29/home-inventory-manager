<script lang="ts">
	/**
	 * インプットコンポーネント
	 * @component Input
	 */
	/**
	 * コンポーネントのプロパティ定義
	 * @typedef {Object} InputProps
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
	 */
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

	/**
	 * 入力値の内部状態
	 */
	let inputValue = $state(value);

	/**
	 * 入力イベントのハンドラ
	 * @param {Event} event - 入力イベント
	 */
	function handleInput(event: Event) {
		const target = event.target as HTMLInputElement;
		inputValue = target.value;
	}

	/**
	 * 値が外部から変更された場合に内部状態を更新する
	 */
	$effect(() => {
		inputValue = value;
	});

	/**
	 * インプットのスタイルクラスを取得する
	 * @returns {string} 適用するCSSクラス名の文字列
	 */
	function getInputClasses(): string {
		// 状態に応じたクラスを追加できるようにする
		const stateClasses = {
			disabled: disabled ? 'input-disabled' : '',
			required: required ? 'input-required' : ''
		};

		return [
			'input',
			stateClasses.disabled,
			stateClasses.required,
			className
		]
			.filter(Boolean)
			.join(' ')
			.trim();
	}
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
			class={getInputClasses()}
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
		class={getInputClasses()}
		value={inputValue}
		oninput={handleInput}
		onchange={() => {}}
	/>
{/if}
