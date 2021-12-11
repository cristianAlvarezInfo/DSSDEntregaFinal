import { resolve } from "path";
import adapter from '@sveltejs/adapter-auto';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter(),

		// hydrate the <div id="svelte"> element in src/app.html
		target: '#svelte',
		vite: {
			resolve: {
				alias: {
					$component: resolve('./src/components'),
					$store: resolve('./src/store')
				}
			}
		}
	}
};

export default config;
