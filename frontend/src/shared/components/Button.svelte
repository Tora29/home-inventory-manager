<script lang="ts">
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
		onclick?: (event: MouseEvent) => void;
		children?: string;
	}>();

	// クラスを動的に生成
	function getClasses(): string {
		const baseClass = iconOnly ? 'btn-icon' : 'btn';
		const sizeClass = size !== 'base' ? `btn-${size}` : '';
		const variantClass = `preset-${variant}-${color}${variant === 'filled' ? '-500' : ''}`;

		return `${baseClass} ${sizeClass} ${variantClass} ${className}`.trim();
	}
</script>

<button {type} class={getClasses()} {disabled} aria-label={ariaLabel} {onclick}>
	{children}
</button>
