// src/services/plugins/customDirectives.ts
import type { NuxtApp } from 'nuxt/app';
import { type Plugin } from 'vue';

import type { ClickOutsideElement, NuxtPluginCustomDirectives } from '@/types/services/plugins/customDirectives';

const customDirectives: Plugin = (app) => {
	app.directive('focus', {
		mounted(el: HTMLElement) {
			el.focus();
		},
	});

	app.directive('click-outside', {
		mounted(el: ClickOutsideElement, binding) {
			el._clickOutside = (event: Event) => {
				if (!(el === event.target || el.contains(event.target as Node))) {
					binding.value(event);
				}
			};
			document.body.addEventListener('click', el._clickOutside);
		},
		unmounted(el: ClickOutsideElement) {
			if (el._clickOutside) {
				document.body.removeEventListener('click', el._clickOutside);
			}
		},
	});

	app.directive('scroll-to', {
		mounted(el: HTMLElement, binding) {
			el.addEventListener('click', () => {
				const target = document.querySelector(binding.value);
				if (target) {
					target.scrollIntoView({ behavior: 'smooth' });
				}
			});
		},
	});
};

const customDirectivesPlugin: NuxtPluginCustomDirectives = defineNuxtPlugin((nuxtApp: NuxtApp) => {
	const app = (nuxtApp as any).vueApp;
	customDirectives(app);
});

export default customDirectivesPlugin;
