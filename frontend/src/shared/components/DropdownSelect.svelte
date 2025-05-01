<script lang="ts">
	/**
	 * ドロップダウン選択コンポーネント
	 * @component DropdownSelect
	 */
	/**
	 * コンポーネントのプロパティ定義
	 * @typedef {Object} DropdownSelectProps
	 * @property {Array<{value: string, label: string}>} [options=[]] - 選択肢の配列
	 * @property {string} [value=''] - 現在選択されている値
	 * @property {string} [placeholder='選択してください'] - プレースホルダーテキスト
	 * @property {string} [label=''] - ラベルテキスト
	 * @property {Function} [onChange] - 値が変更されたときのコールバック関数
	 * @property {string} [id] - 要素のID（指定がない場合は自動生成）
	 * @property {string} [className=''] - 追加のCSSクラス
	 * @property {boolean} [disabled=false] - 無効状態の指定
	 * @property {boolean} [required=false] - 必須入力の指定
	 * @property {('sm'|'md'|'lg')} [size='md'] - セレクトボックスのサイズ
	 */
	const {
		options = [],
		value = '',
		placeholder = '選択してください',
		label = '',
		onChange,
		id = `dropdown-${Math.random().toString(36).substring(2, 9)}`,
		className = '',
		disabled = false,
		required = false,
		size = 'md'
	} = $props<{
		options: { value: string; label: string }[];
		value: string;
		placeholder: string;
		label: string;
		onChange?: (value: string) => void;
		id?: string;
		className?: string;
		disabled?: boolean;
		required?: boolean;
		size?: 'sm' | 'md' | 'lg';
	}>();

	/**
	 * 選択が変更されたときのハンドラー
	 * @param {Event} event - 変更イベント
	 */
	function handleChange(event: Event) {
		const target = event.target as HTMLSelectElement;
		const newValue = target.value;

		// コールバック関数が提供されている場合は呼び出す
		if (typeof onChange === 'function') {
			onChange(newValue);
		}
	}

	/**
	 * セレクトボックスのスタイルクラスを取得する
	 * @returns {string} 適用するCSSクラス名の文字列
	 */
	function getSelectClasses(): string {
		// サイズのマッピング
		const sizeMap: Record<string, string> = {
			sm: 'select-sm',
			md: '',
			lg: 'select-lg'
		};

		// 状態クラス
		const stateClasses = {
			disabled: disabled ? 'select-disabled' : '',
			required: required ? 'select-required' : ''
		};

		return [
			'select',
			'w-full',
			sizeMap[size],
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
	<label class="label" for={id}>
		<span class="label-text">{label}</span>
		{#if required}
			<span class="text-error">*</span>
		{/if}
	</label>
{/if}

<select 
	{id} 
	class={getSelectClasses()} 
	{value} 
	onchange={handleChange} 
	{disabled} 
	{required}
>
	<option value="" disabled selected={!value}>{placeholder}</option>
	{#each options as option}
		<option value={option.value} selected={value === option.value}>
			{option.label}
		</option>
	{/each}
</select>
