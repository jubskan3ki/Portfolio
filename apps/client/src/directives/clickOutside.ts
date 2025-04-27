// src/directives/clickOutside.ts
import type { NuxtApp } from 'nuxt/app';
import type { DirectiveBinding } from 'vue';

export default defineNuxtPlugin((nuxtApp: NuxtApp) => {
	nuxtApp.vueApp.directive('click-outside', {
		mounted(el: HTMLElement, binding: DirectiveBinding) {
			el._clickOutsideHandler = (event: Event) => {
				if (!(el === event.target || el.contains(event.target as Node))) {
					binding.value(event);
				}
			};
			document.addEventListener('click', el._clickOutsideHandler);
		},
		unmounted(el: HTMLElement) {
			document.removeEventListener('click', el._clickOutsideHandler);
		},
	});
});

// Augmenter HTMLElement pour TypeScript
declare global {
	interface HTMLElement {
		_clickOutsideHandler: (event: Event) => void;
	}
}
