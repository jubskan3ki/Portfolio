import { defineNuxtConfig } from 'nuxt/config';

export default defineNuxtConfig({
	// ✅ TypeScript strict
	typescript: {
		shim: false,
		strict: true,
		typeCheck: true,
	},

	// ✅ Auto-import des modules et composants
	imports: {
		autoImport: true,
	},

	// 📦 Modules utiles
	modules: ['@vueuse/nuxt'],

	// 🌍 Alias propre pour éviter les imports relatifs
	alias: {
		'@': './src',
	},

	// ⚡ Nitro (Backend Nuxt)
	nitro: {
		preset: 'node-server',
	},

	// 🔥 Auto-import des composants
	components: true,

	// Activer le SSR et désactiver le mode statique
	ssr: true,

	// 🌟 Configuration globale
	app: {
		head: {
			title: 'Mon Projet Nuxt',
			meta: [{ name: 'viewport', content: 'width=device-width, initial-scale=1' }, { charset: 'utf-8' }],
		},
	},

	compatibilityDate: '2025-03-05',
});
