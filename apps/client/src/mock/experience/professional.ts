import type { Experience } from '@/types/feature/experience';

export const professionalExperiences: Experience[] = [
	{
		id: 'job-1',
		title: 'Président',
		company: 'HeticTacToe',
		location: 'Montreuil, Île-de-France, France',
		period: 'Février 2025 - Présent',
		startDate: '2025-02-01',
		endDate: new Date().toISOString(),
		description:
			"Supervision de l'organisation d'événements, coordination d'équipe, communication interne et externe pour promouvoir le jeu de société sur le campus HETIC.",
		achievements: [
			'Organisation régulière de soirées, tournois et initiations',
			'Gestion d’une équipe projet et relations avec l’administration',
			'Développement d’une communication visuelle et rédactionnelle cohérente',
		],
	},
	{
		id: 'job-2',
		title: 'Développeur Full Stack',
		company: 'StudiMove',
		location: 'Bondy, Île-de-France, France',
		period: 'Octobre 2024 - Mars 2025',
		startDate: '2024-10-01',
		endDate: '2025-03-31',
		description:
			"Conception et développement d'une application mobile Flutter, d'un dashboard web React, et d'un backend en Go pour la réservation et gestion d'événements étudiants.",
		technologies: ['Go', 'React', 'Flutter', 'Docker', 'PostgreSQL', 'AWS S3'],
		achievements: [
			'Déploiement de l’infrastructure sur VPS avec Docker et Nginx',
			'Création d’un système de scoring et d’analyses de performances',
			'Mise en place d’une architecture sécurisée et optimisée',
		],
	},
	{
		id: 'job-3',
		title: 'Développeur Full Stack',
		company: 'Unboared',
		location: 'Paris, Île-de-France, France',
		period: 'Octobre 2023 - Septembre 2024',
		startDate: '2023-10-01',
		endDate: '2024-09-30',
		description:
			"Développement de jeux interactifs en React, création d'un framework interne de jeux, conception de dashboard B2B, et optimisation des applications existantes.",
		technologies: ['React', 'TypeScript', 'Pixi.js', 'Node.js'],
		achievements: [
			'Création d’un framework de jeux interne performant',
			'Refonte UX/UI de plusieurs jeux existants',
			'Développement d’un dashboard partenaire B2B sur-mesure',
		],
	},
	{
		id: 'job-4',
		title: 'Développeur Full Stack',
		company: 'Siko Mobility',
		location: 'Paris, Île-de-France, France',
		period: 'Octobre 2022 - Septembre 2023',
		startDate: '2022-10-01',
		endDate: '2023-09-30',
		description:
			'Développement du nouveau site web corporate en Next.js et TypeScript, création d’interfaces utilisateurs et d’un dashboard de gestion client en React.',
		technologies: ['Next.js', 'React', 'TypeScript', 'CSS', 'PHP'],
		achievements: [
			'Refonte complète du site et amélioration UX/UI',
			'Création d’un dashboard CRM temps réel',
			'Optimisation des formulaires de souscription clients',
		],
	},
	{
		id: 'job-5',
		title: 'Développeur Full Stack',
		company: 'CAHOUET',
		location: 'Montreuil, Île-de-France, France',
		period: 'Juillet 2022 - Octobre 2022',
		startDate: '2022-07-01',
		endDate: '2022-10-31',
		description:
			'Refonte intégrale du site web de l’entreprise Cahouet en HTML, CSS, JavaScript, PHP et MySQL pour moderniser leur présence digitale.',
		technologies: ['HTML', 'CSS', 'JavaScript', 'PHP', 'MySQL'],
		achievements: [
			'Conception d’une nouvelle vitrine web moderne et performante',
			'Amélioration de la visibilité digitale de l’entreprise',
			'Gestion du projet en autonomie complète',
		],
	},
];
