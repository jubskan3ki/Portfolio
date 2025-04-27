// Export all projects mock data
export * from './categories';
export * from './projects';

// Export a method to get all projects data
import { projectCategories } from './categories';
import { projects } from './projects';

export const getAllProjectsData = () => {
	return {
		projects,
		projectCategories,
	};
};

// Get a specific project by slug
export const getProjectBySlug = (slug: string) => {
	return projects.find((project) => project.slug === slug);
};

// Get related projects for a specific project
export const getRelatedProjects = (slug: string, limit = 3) => {
	const currentProject = getProjectBySlug(slug);
	if (!currentProject) return [];

	return projects
		.filter(
			(project) =>
				project.slug !== slug &&
				(project.category === currentProject.category ||
					project.technologies.some((tech) => currentProject.technologies.includes(tech)))
		)
		.slice(0, limit);
};
