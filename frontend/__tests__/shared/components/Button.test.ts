import { render } from '@testing-library/svelte';
import { expect, describe, it } from 'vitest';
import Button from '$shared/components/Button.svelte';

describe('Button コンポーネント', () => {
  it('デフォルトプロパティで正しくレンダリングされること', () => {
    const { container } = render(Button, {
      props: {
        children: 'ボタン'
      }
    });
    
    const button = container.querySelector('button');
    expect(button).not.toBeNull();
    expect(button?.textContent).toBe('ボタン');
    expect(button?.className).toContain('btn');
    expect(button?.className).toContain('preset-filled-primary-500');
    expect(button?.disabled).toBe(false);
    expect(button?.type).toBe('button');
  });

  it('カスタムプロパティで正しくレンダリングされること', () => {
    const { container } = render(Button, {
      props: {
        variant: 'outlined',
        color: 'secondary',
        size: 'lg',
        disabled: true,
        type: 'submit',
        className: 'custom-class',
        iconOnly: true,
        ariaLabel: 'テストボタン',
        children: 'カスタムボタン'
      }
    });
    
    const button = container.querySelector('button');
    expect(button).not.toBeNull();
    expect(button?.textContent).toBe('カスタムボタン');
    expect(button?.className).toContain('btn-icon');
    expect(button?.className).toContain('btn-lg');
    expect(button?.className).toContain('preset-outlined-secondary');
    expect(button?.className).toContain('custom-class');
    expect(button?.disabled).toBe(true);
    expect(button?.type).toBe('submit');
    expect(button?.getAttribute('aria-label')).toBe('テストボタン');
  });
});
