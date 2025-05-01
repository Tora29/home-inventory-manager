<script lang="ts">
	/**
	 * 検索入力コンポーネント
	 * @component SearchInput
	 */
	import Button from './Button.svelte';
	import SearchIcon from '@lucide/svelte/icons/search';

	/**
	 * コンポーネントのプロパティ定義
	 * @typedef {Object} SearchInputProps
	 * @property {string} [placeholder='検索...'] - プレースホルダーテキスト
	 * @property {string} [value=''] - 入力値
	 * @property {string} [buttonText='検索'] - 検索ボタンのテキスト
	 * @property {string} [className=''] - 追加のCSSクラス
	 * @property {Function} [onSearch] - 検索実行時のコールバック関数
	 * @property {Function} [onInputChange] - 入力値変更時のコールバック関数
	 * @property {boolean} [disabled=false] - 無効状態の指定
	 * @property {('sm'|'base'|'lg')} [size='base'] - 検索入力のサイズ
	 */
	const {
		placeholder = '検索...',
		value = '',
		buttonText = '検索',
		className = '',
		onSearch = undefined,
		onInputChange = undefined,
		disabled = false,
		size = 'base'
	} = $props<{
		placeholder?: string;
		value?: string;
		buttonText?: string;
		className?: string;
		onSearch?: (value: string) => void;
		onInputChange?: (value: string) => void;
		disabled?: boolean;
		size?: 'sm' | 'base' | 'lg';
	}>();

	/**
	 * 検索値の内部状態
	 */
	let searchValue = $state(value);

	/**
	 * 入力イベントのハンドラ
	 * @param {Event} event - 入力イベント
	 */
	function handleInput(event: Event) {
		const target = event.target as HTMLInputElement;
		searchValue = target.value;

		// 入力ごとに親コンポーネントに通知
		if (onInputChange) {
			onInputChange(searchValue);
		}
	}

	/**
	 * 検索実行のハンドラ
	 */
	function handleSubmit() {
		if (onSearch) {
			onSearch(searchValue);
		}
	}

	/**
	 * キーボード入力のハンドラ
	 * @param {KeyboardEvent} event - キーボードイベント
	 */
	function handleKeyPress(event: KeyboardEvent) {
		if (event.key === 'Enter') {
			if (onSearch) {
				onSearch(searchValue);
			}
		}
	}

	/**
	 * 値が外部から変更された場合に内部状態を更新する
	 */
	$effect(() => {
		searchValue = value;
	});

	/**
	 * コンポーネントのスタイルクラスを取得する
	 * @returns {string} 適用するCSSクラス名の文字列
	 */
	function getContainerClasses(): string {
		// サイズのマッピング
		const sizeMap: Record<string, string> = {
			sm: 'input-group-sm',
			base: '',
			lg: 'input-group-lg'
		};

		// 状態クラス
		const disabledClass = disabled ? 'opacity-70 pointer-events-none' : '';

		return [
			'input-group',
			'grid-cols-[auto_1fr_auto]',
			sizeMap[size],
			disabledClass,
			className
		]
			.filter(Boolean)
			.join(' ')
			.trim();
	}
</script>

<div class={getContainerClasses()}>
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
		{disabled}
	/>
	<Button
		variant="filled"
		color="primary"
		size={size}
		type="button"
		className="ig-btn"
		onclick={handleSubmit}
		{disabled}
		children={buttonText}
	/>
</div>
