import type { ExpertiseCategory, StackCategory } from '@/types/feature/stacks';

export const stackCategories: StackCategory[] = [
	{ id: 'all', name: 'Toutes' },
	{ id: 'frontend', name: 'Front-End' },
	{ id: 'backend', name: 'Back-End' },
	{ id: 'devops', name: 'DevOps' },
	{ id: 'database', name: 'Base de données' },
	{ id: 'tools', name: 'Outils' },
];

export const expertiseCategories: ExpertiseCategory[] = [
	{
		name: 'Développement Front-End',
		description: "Création d'interfaces utilisateur modernes, réactives et accessibles.",
		skills: ['Vue.js', 'React', 'Svelte', 'TypeScript', 'SCSS', 'Vite', 'Jest'],
	},
	{
		name: 'Développement Back-End',
		description: "Conception et développement d'APIs RESTful et de services performants.",
		skills: ['Go', 'Node.js', 'Express', 'Django', 'Python', 'PostgreSQL', 'MongoDB'],
	},
	{
		name: 'DevOps & Cloud',
		description: 'Mise en place de CI/CD, conteneurisation et déploiement sur le cloud.',
		skills: ['Docker', 'Terraform', 'Ansible', 'Kubernetes', 'AWS', 'GitHub Actions', 'Nginx', 'Linux'],
	},
	{
		name: 'Outils & Design',
		description: "Création d'interfaces et gestion de projets avec des outils modernes.",
		skills: ['Figma', 'Git', 'Illustrator', 'Photoshop'],
	},
];

// Helper function to get category name by id
export const getCategoryName = (categoryId: string): string => {
	const category = stackCategories.find((cat) => cat.id === categoryId);
	return category ? category.name : categoryId;
};
