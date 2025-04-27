// types/services/plugins/meta.ts

import type { NuxtApp } from 'nuxt/app';

// Interface pour les méta-informations d'une page
export interface PageMetaInfo {
	title: string;
	description: string;
}

// Interface pour la configuration des méta-informations par route
export interface MetaConfig {
	[routePath: string]: PageMetaInfo;
}

// Fonction de mise à jour des méta-informations
export type UpdateMetaFunction = () => void;

// Type pour le plugin Nuxt
export type NuxtPluginMeta = (nuxtApp: NuxtApp) => void;
