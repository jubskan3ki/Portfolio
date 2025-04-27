// categories.ts
import type { Category } from '@/types/feature/blog';

export const categories: Category[] = [
	{ id: 'frontend', name: 'Frontend', count: 20 },
	{ id: 'backend', name: 'Backend', count: 18 },
	{ id: 'mobile', name: 'Mobile', count: 12 },
	{ id: 'devops', name: 'DevOps', count: 14 },
	{ id: 'cloud', name: 'Cloud Computing', count: 9 },
	{ id: 'security', name: 'Cybersecurity', count: 7 },
	{ id: 'api', name: 'API & Microservices', count: 10 },
	{ id: 'architecture', name: 'Architecture Logicielle', count: 6 },
];

export const getCategoryName = (categoryId: string): string => {
	const category = categories.find((cat) => cat.id === categoryId);
	return category ? category.name : categoryId;
};
