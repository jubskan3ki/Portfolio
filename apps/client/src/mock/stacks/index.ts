// Export all stacks mock data
export * from './categories';
export * from './stacks';

// Export a method to get all stacks data
import { expertiseCategories, stackCategories } from './categories';
import { stacks } from './stacks';

export const getAllStacksData = () => {
	return {
		stacks,
		stackCategories,
		expertiseCategories,
	};
};

// Get a specific stack by slug
export const getStackBySlug = (slug: string) => {
	return stacks.find((stack) => stack.slug === slug);
};

// Get related stacks for a specific stack
export const getRelatedStacks = (slug: string, limit = 3) => {
	const currentStack = getStackBySlug(slug);
	if (!currentStack) return [];

	return stacks
		.filter(
			(stack) =>
				stack.slug !== slug &&
				(stack.category === currentStack.category || stack.tags.some((tag) => currentStack.tags.includes(tag)))
		)
		.slice(0, limit);
};
