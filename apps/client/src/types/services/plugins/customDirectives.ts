// types/services/plugins/customDirectives.ts

import type { NuxtApp } from 'nuxt/app';

// Type pour les éléments avec gestionnaire de clic extérieur
export interface ClickOutsideElement extends HTMLElement {
	_clickOutside?: (event: Event) => void;
}

// Type pour le plugin Nuxt
export type NuxtPluginCustomDirectives = (nuxtApp: NuxtApp) => void;
