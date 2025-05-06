import { svelteTesting } from '@testing-library/svelte/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
	plugins: [tailwindcss(), sveltekit(), svelteTesting()],
	server: {
		watch: {
			usePolling: true
		}
	},
	test: {
		coverage: {
			provider: 'v8',
			reporter: ['text', 'json', 'html', 'json-summary'],
			reportsDirectory: './coverage'
		},
		environment: 'jsdom',
		include: ['__tests__/**/*.{test,spec}.{js,ts}', 'src/**/*.{test,spec}.{js,ts}']
	}
});
