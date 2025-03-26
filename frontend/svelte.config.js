import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import { dirname, resolve } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess(),
	kit: {
		files: {
			assets: 'src/shared/static'
		},
		adapter: adapter({
			pages: 'build',
			assets: 'build',
			fallback: null
		}),
		alias: {
			'@': resolve(__dirname, './src'),
			$lib: resolve(__dirname, './src/lib'),
			$shared: resolve(__dirname, './src/shared'),
			$entities: resolve(__dirname, './src/entities'),
			$features: resolve(__dirname, './src/features'),
			$widgets: resolve(__dirname, './src/widgets')
		}
	}
};

export default config;
