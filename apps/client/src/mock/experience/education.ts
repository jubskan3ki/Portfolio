import type { Experience } from '@/types/feature/experience';

export const educationExperiences: Experience[] = [
	{
		id: 'edu-1',
		title: 'Master CTO & Tech Lead',
		company: 'HETIC',
		location: 'Montreuil, Île-de-France, France',
		period: 'Octobre 2024 - Novembre 2026',
		startDate: '2024-10-01',
		endDate: '2026-11-30',
		description:
			"Mastère spécialisé en CTO & Tech Lead, axé sur l'architecture logicielle, les technologies backend, le Cloud, la sécurité et le leadership stratégique en projets numériques.",
		achievements: [
			'Expertise avancée en Go, Node.js, Python, React.js et Flutter',
			'Compétences en Cloud, DevOps, API Rest/GraphQL',
			'Gestion agile et pilotage de projets innovants',
		],
	},
	{
		id: 'edu-2',
		title: 'Bachelor Développement Web et Mobile',
		company: 'HETIC',
		location: 'Montreuil, Île-de-France, France',
		period: 'Septembre 2021 - Octobre 2024',
		startDate: '2021-09-01',
		endDate: '2024-10-31',
		description:
			'Formation complète en développement web, mobile et backend, combinant projets concrets, expertise technique avancée et alternance professionnelle.',
		achievements: [
			'Maîtrise de React.js, Next.js, TypeScript, Flask et Go',
			'Connaissances solides en UX/UI Design avec Figma et Adobe',
			'Approche agile et DevOps pour le développement de projets performants',
		],
	},
];
