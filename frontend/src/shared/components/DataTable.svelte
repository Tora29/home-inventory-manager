<script lang="ts" module>
	/**
	 * DataTable コンポーネント用のモジュール定義
	 * @module DataTable
	 */
	import IconMoveVertical from '@lucide/svelte/icons/move-vertical';
	import IconMoveUp from '@lucide/svelte/icons/move-up';
	import IconMoveDown from '@lucide/svelte/icons/move-down';

	/**
	 * データ項目のインターフェース
	 * @interface DataItem
	 */
	export interface DataItem {
		[key: string]: any;
	}

	/**
	 * セル内容の型定義
	 * 文字列またはコンポーネントオブジェクト
	 * @typedef {string|Object} CellContent
	 */
	export type CellContent = string | { component: any; props?: any };

	/**
	 * テーブル列の設定インターフェース
	 * @interface Column
	 */
	export interface Column {
		/** カラムヘッダーのテキスト */
		header: string;
		/** データオブジェクトのプロパティキー */
		key: string;
		/** テキスト配置 */
		align?: 'left' | 'center' | 'right';
		/** セル内容のフォーマッター関数 */
		formatter?: (value: any, item: DataItem) => CellContent;
		/** 値がない場合のフォールバックテキスト */
		fallback?: string;
		/** 列の幅 */
		width?: string;
		/** ソート可能かどうか */
		sortable?: boolean;
	}

	/**
	 * ソート方向の型定義
	 * @typedef {'asc'|'desc'|null} SortDirection
	 */
	export type SortDirection = 'asc' | 'desc' | null;

	/**
	 * ソート状態のインターフェース
	 * @interface SortState
	 */
	export interface SortState {
		/** ソートするキー */
		key: string | null;
		/** ソート方向 */
		direction: SortDirection;
	}
</script>

<script lang="ts">
	/**
	 * データテーブルコンポーネント
	 * @component DataTable
	 */
	/**
	 * コンポーネントのプロパティ定義
	 * @typedef {Object} DataTableProps
	 * @property {DataItem[]} [data=[]] - 表示するデータ配列
	 * @property {Column[]} [columns=[]] - テーブル列の設定配列
	 * @property {boolean} [showTotal=false] - 合計行を表示するかどうか
	 * @property {string} [totalLabel='合計'] - 合計行のラベル
	 * @property {string} [emptyMessage='データがありません'] - データがない場合のメッセージ
	 * @property {boolean} [hoverEffect=true] - 行にホバーエフェクトを適用するかどうか
	 * @property {Function} [getRowClass] - 行のカスタムクラスを返す関数
	 * @property {Function} [getCellClass] - セルのカスタムクラスを返す関数
	 * @property {SortState} [initialSort] - 初期ソート状態
	 * @property {Function} [onSort] - ソート状態変更時のコールバック関数
	 */
	const props = $props<{
		data?: DataItem[];
		columns?: Column[];
		showTotal?: boolean;
		totalLabel?: string;
		emptyMessage?: string;
		hoverEffect?: boolean;
		getRowClass?: (item: DataItem) => string;
		getCellClass?: (item: DataItem, column: Column) => string;
		initialSort?: SortState;
		onSort?: (sortState: SortState) => void;
	}>();

	// デフォルト値の設定
	const data = $derived(props.data || []);
	const columns = $derived(props.columns || []);
	const showTotal = $derived(props.showTotal ?? false);
	const totalLabel = $derived(props.totalLabel ?? '合計');
	const emptyMessage = $derived(props.emptyMessage ?? 'データがありません');
	const hoverEffect = $derived(props.hoverEffect ?? true);
	const getRowClass = $derived(props.getRowClass || (() => ''));
	const getCellClass = $derived(props.getCellClass || (() => ''));
	const onSort = $derived(props.onSort);

	/**
	 * ソート状態の内部状態
	 */
	let sortState = $state<SortState>(props.initialSort || { key: null, direction: null });

	/**
	 * ソート可能な列をクリックしたときの処理
	 * @param {Column} column - クリックされた列
	 */
	function handleHeaderClick(column: Column) {
		if (!column.sortable) return;

		// 同じ列をクリックした場合は方向を切り替え、違う列の場合は昇順から開始
		if (sortState.key === column.key) {
			if (sortState.direction === 'asc') {
				sortState = { key: column.key, direction: 'desc' };
			} else if (sortState.direction === 'desc') {
				sortState = { key: null, direction: null };
			} else {
				sortState = { key: column.key, direction: 'asc' };
			}
		} else {
			sortState = { key: column.key, direction: 'asc' };
		}

		// 親コンポーネントにソート状態の変更を通知
		if (onSort) {
			onSort(sortState);
		}
	}

	/**
	 * ソートされたデータを取得
	 * @returns {DataItem[]} ソート後のデータ配列
	 */
	function getSortedData(): DataItem[] {
		if (!sortState.key || !sortState.direction) {
			return data;
		}

		return [...data].sort((a, b) => {
			const aValue = getNestedProperty(a, sortState.key as string);
			const bValue = getNestedProperty(b, sortState.key as string);

			// nullやundefinedは最後にソート
			if (aValue === undefined || aValue === null) return 1;
			if (bValue === undefined || bValue === null) return -1;

			// 数値の場合
			if (typeof aValue === 'number' && typeof bValue === 'number') {
				return sortState.direction === 'asc' ? aValue - bValue : bValue - aValue;
			}

			// 日付の場合
			if (aValue instanceof Date && bValue instanceof Date) {
				return sortState.direction === 'asc'
					? aValue.getTime() - bValue.getTime()
					: bValue.getTime() - aValue.getTime();
			}

			// 日付文字列の場合
			if (
				typeof aValue === 'string' &&
				typeof bValue === 'string' &&
				!isNaN(Date.parse(aValue)) &&
				!isNaN(Date.parse(bValue))
			) {
				const dateA = new Date(aValue).getTime();
				const dateB = new Date(bValue).getTime();
				return sortState.direction === 'asc' ? dateA - dateB : dateB - dateA;
			}

			// 文字列として比較
			const strA = String(aValue).toLowerCase();
			const strB = String(bValue).toLowerCase();
			return sortState.direction === 'asc'
				? strA.localeCompare(strB, 'ja')
				: strB.localeCompare(strA, 'ja');
		});
	}

	/**
	 * ネストされたプロパティを取得する関数
	 * @param {any} obj - 対象オブジェクト
	 * @param {string} path - プロパティパス（ドット記法）
	 * @returns {any} 取得した値
	 */
	function getNestedProperty(obj: any, path: string): any {
		// ドット記法でプロパティパスを分割
		const keys = path.split('.');
		let value = obj;

		// 各キーに沿って値を取得
		for (const key of keys) {
			if (value === undefined || value === null) {
				return undefined;
			}
			value = value[key];
		}

		return value;
	}

	/**
	 * セルの値を取得する関数
	 * @param {DataItem} item - データ項目
	 * @param {Column} column - 列設定
	 * @returns {CellContent} セルの内容
	 */
	function getCellValue(item: DataItem, column: Column): CellContent {
		// ドット記法に対応した値の取得
		const value = getNestedProperty(item, column.key);

		// 値が存在しない場合はフォールバック
		if (value === undefined || value === null) {
			return column.fallback || '';
		}

		// フォーマッタがある場合は適用
		if (column.formatter) {
			return column.formatter(value, item);
		}

		return String(value);
	}

	/**
	 * セル位置のクラスを取得
	 * @param {string} align - テキスト配置
	 * @returns {string} CSSクラス名
	 */
	function getAlignClass(align?: 'left' | 'center' | 'right'): string {
		const alignMap: Record<string, string> = {
			center: 'text-center',
			right: 'text-right',
			left: ''
		};
		
		return alignMap[align || 'left'] || '';
	}

	/**
	 * セルの内容が文字列かコンポーネントかを判定
	 * @param {CellContent} content - セルの内容
	 * @returns {boolean} コンポーネントであるかどうか
	 */
	function isComponent(content: CellContent): content is { component: any; props?: any } {
		return typeof content === 'object' && content !== null && 'component' in content;
	}

	/**
	 * 行にホバーエフェクトを適用するか判定する関数
	 * @param {DataItem} item - データ項目
	 * @returns {boolean} ホバーエフェクトを適用するかどうか
	 */
	function shouldApplyHoverEffect(item: DataItem): boolean {
		if (!hoverEffect) return false;
		// カスタムスタイルがある行には適用しない
		return getRowClass(item) === '';
	}

	/**
	 * ソートアイコンを取得する関数
	 * @param {Column} column - 列設定
	 * @returns {any} アイコンコンポーネント
	 */
	function getSortIconComponent(column: Column) {
		if (!column.sortable) return null;

		const iconMap = {
			notSorted: IconMoveVertical,
			asc: IconMoveUp,
			desc: IconMoveDown
		};

		if (sortState.key !== column.key) {
			return iconMap.notSorted;
		}

		return sortState.direction === 'asc' ? iconMap.asc : iconMap.desc;
	}
</script>

<div class="table-wrap w-full overflow-x-auto">
	<table class="table table-auto w-full">
		<thead class="bg-surface-700">
			<tr>
				{#each columns as column}
					<th
						class="{getAlignClass(column.align)} {column.sortable
							? 'cursor-pointer select-none'
							: ''} font-bold"
						style={column.width ? `width: ${column.width}; min-width: ${column.width};` : ''}
						onclick={() => handleHeaderClick(column)}
					>
						<div class="flex items-center justify-between gap-1 whitespace-nowrap">
							<span>{column.header}</span>
							{#if column.sortable}
								{@const IconComponent = getSortIconComponent(column)}
								{#if IconComponent}
									<IconComponent size={16} class="sort-icon" />
								{/if}
							{/if}
						</div>
					</th>
				{/each}
			</tr>
		</thead>
		<tbody>
			{#if data.length > 0}
				{#each getSortedData() as item}
					<tr
						class="{getRowClass(item)} {shouldApplyHoverEffect(item)
							? 'hover:preset-tonal-primary'
							: ''}"
					>
						{#each columns as column}
							<td
								class="{getAlignClass(column.align)} {getCellClass(item, column)}"
								style={column.width ? `width: ${column.width}; min-width: ${column.width};` : ''}
							>
								{#if isComponent(getCellValue(item, column))}
									{@const content = getCellValue(item, column) as { component: any; props?: any }}
									{@const Component = content.component}
									<Component {...content.props || {}} />
								{:else}
									{@html getCellValue(item, column)}
								{/if}
							</td>
						{/each}
					</tr>
				{/each}
			{:else}
				<tr>
					<td colspan={columns.length} class="text-center py-4">{emptyMessage}</td>
				</tr>
			{/if}
		</tbody>
		{#if showTotal}
			<tfoot>
				<tr>
					<td colspan={columns.length - 1}>{totalLabel}</td>
					<td class="text-right">{getSortedData().length} 件</td>
				</tr>
			</tfoot>
		{/if}
	</table>
</div>

<style>
	.table-wrap {
		border-radius: var(--theme-border-radius);
	}

	/* テーブルのレイアウトを固定に設定 */
	:global(.table) {
		table-layout: fixed;
	}

	/* ソート可能な列のヘッダーにホバーエフェクト */
	th.cursor-pointer:hover {
		background-color: rgba(var(--color-primary-500) / 0.1);
	}
</style>
