// src/services/plugins/meta.ts
import type { NuxtApp } from 'nuxt/app';
import { useHead, useRoute } from 'nuxt/app';

import ROUTES from '@/config/routes';
import type { MetaConfig, NuxtPluginMeta, UpdateMetaFunction } from '@/types/services/plugins/meta';

const metaPlugin: NuxtPluginMeta = defineNuxtPlugin((nuxtApp: NuxtApp) => {
	// Exécuter à chaque changement de route
	nuxtApp.hook('app:mounted', () => {
		updateMeta();
	});

	nuxtApp.hook('page:finish', () => {
		updateMeta();
	});

	const updateMeta: UpdateMetaFunction = () => {
		// Obtenir la route actuelle
		const route = useRoute();

		// Configuration par défaut des méta-informations
		const defaultTitle = 'Juba Ait-Adda | Développeur Full-Stack';
		const defaultDescription = 'Portfolio de Juba Ait-Adda, développeur full-stack et DevOps';

		// Configuration des méta-informations par route
		const metaConfig: MetaConfig = {
			[ROUTES.HOME.path]: {
				title: 'Accueil | Juba Ait-Adda',
				description: 'Portfolio de Juba Ait-Adda, développeur full-stack et DevOps',
			},
			[ROUTES.BLOG.path]: {
				title: 'Blog | Juba Ait-Adda',
				description: 'Articles techniques et partage de connaissances sur le développement web et DevOps',
			},
			[ROUTES.PROJECTS.path]: {
				title: 'Projets | Juba Ait-Adda',
				description: 'Découvrez les projets réalisés par Juba Ait-Adda',
			},
			[ROUTES.STACKS.path]: {
				title: 'Technologies | Juba Ait-Adda',
				description: 'Les technologies maîtrisées par Juba Ait-Adda',
			},
			[ROUTES.CONTACT.path]: {
				title: 'Contact | Juba Ait-Adda',
				description: 'Contactez Juba Ait-Adda pour vos projets de développement',
			},
			[ROUTES.EXPERIENCE.path]: {
				title: 'Expérience | Juba Ait-Adda',
				description: 'Parcours professionnel et académique de Juba Ait-Adda',
			},
		};

		// Trouver la configuration pour la route actuelle
		const routeConfig = metaConfig[route.path] || {
			title: defaultTitle,
			description: defaultDescription,
		};

		// Mise à jour des méta-informations
		useHead({
			title: routeConfig.title,
			meta: [
				{
					name: 'description',
					content: routeConfig.description,
				},
			],
		});
	};
});

export default metaPlugin;
