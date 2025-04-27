import { defineNuxtConfig } from 'nuxt/config';
import { fileURLToPath } from 'url';

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
	modules: ['@pinia/nuxt', '@vueuse/nuxt', '@nuxt/image', '@nuxtjs/sitemap'],

	// ⚡ Nitro (Backend Nuxt)
	nitro: {
		preset: 'node-server',
	},

	// 🔥 Auto-import des composants
	components: {
		dirs: [
			'src/components/base',
			'src/components/feature',
			'src/components/feedback',
			'src/components/layouts',
			'src/components/loaders',
			'src/components/navigation',
			'src/components/ui',
		],
	},

	// Activer le SSR et désactiver le mode statique
	ssr: true,

	// 🌟 Configuration globale
	app: {
		head: {
			title: 'Juba Ait-Adda | Développeur Full-Stack',
			meta: [
				{ name: 'viewport', content: 'width=device-width, initial-scale=1' },
				{ charset: 'utf-8' },
				{ name: 'description', content: 'Portfolio de Juba Ait-Adda, développeur full-stack et DevOps' },
			],
			link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
		},
		pageTransition: { name: 'page', mode: 'out-in' },
		rootId: 'app',
	},

	// 🎨 SCSS Configuration
	css: ['./src/styles/main.scss'],

	vite: {
		css: {
			preprocessorOptions: {
				scss: {
					// Retrait des imports additionnels car ils sont déjà inclus dans les fichiers
					additionalData: '',
				},
			},
		},
		resolve: {
			alias: {
				'@': fileURLToPath(new URL('./src', import.meta.url)),
				'~': fileURLToPath(new URL('./', import.meta.url)),
			},
		},
	},

	// Configure directory structure
	srcDir: './',
	dir: {
		pages: 'src/pages',
		layouts: 'src/layouts',
		public: 'public',
	},

	// Configure Nuxt to watch for SCSS changes
	watch: ['./src/styles/**/*.scss'],

	// Enable Nuxt DevTools
	devtools: {
		enabled: true,
	},

	// Router configuration
	router: {
		options: {
			strict: false,
		},
	},

	compatibilityDate: '2025-03-05',
});
