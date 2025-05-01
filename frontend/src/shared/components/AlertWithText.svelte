<script lang="ts">
	/**
	 * アラートテキストコンポーネント
	 * @component AlertWithText
	 */
	import CircleAlert from '@lucide/svelte/icons/circle-alert';

	/**
	 * コンポーネントのプロパティ定義
	 * @typedef {Object} AlertWithTextProps
	 * @property {string} [text=''] - アラートテキスト
	 * @property {string} [iconClass='text-error-500'] - アイコンのCSSクラス
	 * @property {('error'|'warning'|'info'|'success')} [type='error'] - アラートのタイプ
	 * @property {string} [className=''] - 追加のCSSクラス
	 */
	const { 
		text = '', 
		iconClass = 'text-error-500',
		type = 'error',
		className = ''
	} = $props<{
		text: string;
		iconClass?: string;
		type?: 'error' | 'warning' | 'info' | 'success';
		className?: string;
	}>();

	/**
	 * アラートタイプに基づいたアイコンの色を取得する
	 * @returns {string} アイコンの色
	 */
	function getIconColor(): string {
		// タイプごとの色マッピング
		const colorMap: Record<string, string> = {
			error: 'red',
			warning: 'orange',
			info: 'blue',
			success: 'green'
		};

		return colorMap[type] || colorMap['error'];
	}

	/**
	 * コンテナのスタイルクラスを取得する
	 * @returns {string} 適用するCSSクラス名の文字列
	 */
	function getContainerClasses(): string {
		// タイプごとのクラスマッピング
		const typeClassMap: Record<string, string> = {
			error: 'text-error-500',
			warning: 'text-warning-500',
			info: 'text-info-500',
			success: 'text-success-500'
		};

		return [
			'flex',
			'items-center',
			'gap-2',
			typeClassMap[type],
			className
		]
			.filter(Boolean)
			.join(' ')
			.trim();
	}
</script>

<div class={getContainerClasses()}>
	<CircleAlert color={getIconColor()} size={16} class={iconClass} />
	<span>{text}</span>
</div>
