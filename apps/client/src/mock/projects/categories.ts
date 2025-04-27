import type { ProjectCategory } from '@/types/feature/project';

export const projectCategories: ProjectCategory[] = [
	{ id: '', name: 'Tous les projets', count: 0 },
	{ id: 'web', name: 'Applications Web', count: 5 },
	{ id: 'mobile', name: 'Applications Mobile', count: 1 },
	{ id: 'devops', name: 'Solutions DevOps', count: 2 },
];

export const getCategoryName = (categoryId: string): string => {
	const category = projectCategories.find((cat) => cat.id === categoryId);
	return category ? category.name : categoryId;
};
