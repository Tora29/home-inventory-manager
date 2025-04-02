import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import { dirname, resolve } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess(),
	compilerOptions: {
		runes: true
	},
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
			$entities: 'src/entities',
			$features: 'src/features',
			$shared: 'src/shared',
			$widgets: 'src/widgets'
		},
		prerender: {
			handleHttpError: ({ path, status }) => {
				// 404エラーなら無視する
				if (status === 404) {
					return;
				}

				// その他のエラーは通常通り処理する
				throw new Error(`${status} while prerendering ${path}`);
			}
		}
	}
};

export default config;
