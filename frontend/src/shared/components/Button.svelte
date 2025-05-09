<script lang="ts">
	/**
	 * ボタンコンポーネント
	 * @component Button
	 */
	
	/**
	 * コンポーネントのプロパティ定義
	 * @typedef {Object} ButtonProps
	 * @property {('filled'|'tonal'|'outlined')} [variant='filled'] - ボタンのバリエーション
	 * @property {('primary'|'secondary'|'tertiary'|'success'|'warning'|'error'|'surface')} [color='primary'] - ボタンの色
	 * @property {('sm'|'base'|'lg')} [size='base'] - ボタンのサイズ
	 * @property {boolean} [disabled=false] - 無効状態の指定
	 * @property {('button'|'submit'|'reset')} [type='button'] - ボタンのタイプ
	 * @property {string} [className=''] - 追加のCSSクラス
	 * @property {boolean} [iconOnly=false] - アイコンのみのボタンかどうか
	 * @property {string} [ariaLabel=''] - アクセシビリティ用のラベル
	 * @property {Function} [onclick] - クリック時のイベントハンドラ
	 * @property {string} [children=''] - ボタンの子要素（テキストなど）
	 */
	const {
		variant = 'filled',
		color = 'primary',
		size = 'base',
		disabled = false,
		type = 'button',
		className = '',
		iconOnly = false,
		ariaLabel = '',
		onclick = undefined,
		children = ''
	} = $props<{
		variant?: 'filled' | 'tonal' | 'outlined';
		color?: 'primary' | 'secondary' | 'tertiary' | 'success' | 'warning' | 'error' | 'surface';
		size?: 'sm' | 'base' | 'lg';
		disabled?: boolean;
		type?: 'button' | 'submit' | 'reset';
		className?: string;
		iconOnly?: boolean;
		ariaLabel?: string;
		onclick?: ((event: MouseEvent) => void);
		children?: string;
	}>();

	/**
	 * ボタンのスタイルクラスを取得する
	 * @returns {string} 適用するCSSクラス名の文字列
	 */
	function getClasses(): string {
		// ベースクラスのマッピング
		const baseClassMap: Record<string, string> = {
			true: 'btn-icon',
			false: 'btn'
		};
		
		// サイズのマッピング
		const sizeMap: Record<string, string> = {
			sm: 'btn-sm',
			base: '',
			lg: 'btn-lg'
		};
		
		// バリアントとカラーの組み合わせ
		const variantSuffix = variant === 'filled' ? '-500' : '';
		const variantClass = `preset-${variant}-${color}${variantSuffix}`;
		
		// 最終的なクラス名を生成
		return [
			baseClassMap[String(iconOnly)],
			sizeMap[size],
			variantClass,
			className
		]
			.filter(Boolean)
			.join(' ')
			.trim();
	}
</script>

<button {type} class={getClasses()} {disabled} aria-label={ariaLabel} {onclick}>
	{children}
</button>
