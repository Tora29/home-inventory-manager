<script lang="ts">
	/**
	 * ドロップダウン選択コンポーネント
	 *
	 * @param options - 選択肢の配列 [{value: string, label: string}]
	 * @param value - 現在選択されている値
	 * @param placeholder - プレースホルダーテキスト
	 * @param label - ラベルテキスト
	 * @param onChange - 値が変更されたときのコールバック関数
	 */

	const {
		options = [],
		value = '',
		placeholder = '選択してください',
		label = '',
		onChange,
		id = `dropdown-${Math.random().toString(36).substring(2, 9)}`
	} = $props<{
		options: { value: string; label: string }[];
		value: string;
		placeholder: string;
		label: string;
		onChange?: (value: string) => void;
		id?: string;
	}>();

	// 選択が変更されたときのハンドラー
	function handleChange(event: Event) {
		const target = event.target as HTMLSelectElement;
		const newValue = target.value;

		// コールバック関数が提供されている場合は呼び出す
		if (typeof onChange === 'function') {
			onChange(newValue);
		}
	}
</script>

{#if label}
	<label class="label" for={id}>
		<span class="label-text">{label}</span>
	</label>
{/if}

<select {id} class="select w-full" {value} onchange={handleChange}>
	<option value="" disabled selected={!value}>{placeholder}</option>
	{#each options as option}
		<option value={option.value} selected={value === option.value}>
			{option.label}
		</option>
	{/each}
</select>
