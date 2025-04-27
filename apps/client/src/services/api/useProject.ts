import type { Ref } from 'vue';
import { ref } from 'vue';

import { API_ENDPOINTS } from '@/config/api';
import api from '@/services/utils/httpClient';

// Types
export interface Project {
	id: number;
	title: string;
	description: string;
	status: 'completed' | 'in_progress' | 'planned' | 'archived';
	priority: number;
	tags: string[];
	github_link?: string;
	live_demo?: string;
	image?: string;
	created_at: string;
	updated_at: string;
	slug: string;
}

export interface ProjectInput {
	title: string;
	description: string;
	status: 'completed' | 'in_progress' | 'planned' | 'archived';
	priority: number;
	tags: string[];
	github_link?: string;
	live_demo?: string;
	image?: File;
}

export function useProject() {
	const projects: Ref<Project[]> = ref([]);
	const currentProject: Ref<Project | null> = ref(null);
	const isLoading = ref(false);
	const error = ref<string | null>(null);

	// Fetch all projects
	const fetchProjects = async () => {
		isLoading.value = true;
		error.value = null;
		try {
			projects.value = await api.get<Project[]>(API_ENDPOINTS.PROJECT.BASE);
		} catch (err: any) {
			error.value = err.message || 'Failed to fetch projects';
			console.error(error.value);
		} finally {
			isLoading.value = false;
		}
	};

	// Fetch active projects
	const fetchActiveProjects = async () => {
		isLoading.value = true;
		error.value = null;
		try {
			projects.value = await api.get<Project[]>(API_ENDPOINTS.PROJECT.ACTIVE);
		} catch (err: any) {
			error.value = err.message || 'Failed to fetch active projects';
			console.error(error.value);
		} finally {
			isLoading.value = false;
		}
	};

	// Fetch recent projects
	const fetchRecentProjects = async () => {
		isLoading.value = true;
		error.value = null;
		try {
			projects.value = await api.get<Project[]>(API_ENDPOINTS.PROJECT.RECENT);
		} catch (err: any) {
			error.value = err.message || 'Failed to fetch recent projects';
			console.error(error.value);
		} finally {
			isLoading.value = false;
		}
	};

	// Fetch archived projects
	const fetchArchivedProjects = async () => {
		isLoading.value = true;
		error.value = null;
		try {
			projects.value = await api.get<Project[]>(API_ENDPOINTS.PROJECT.ARCHIVED);
		} catch (err: any) {
			error.value = err.message || 'Failed to fetch archived projects';
			console.error(error.value);
		} finally {
			isLoading.value = false;
		}
	};

	// Fetch projects by tag
	const fetchProjectsByTag = async (tag: string) => {
		isLoading.value = true;
		error.value = null;
		try {
			projects.value = await api.get<Project[]>(`${API_ENDPOINTS.PROJECT.BY_TAG}?tag=${tag}`);
		} catch (err: any) {
			error.value = err.message || 'Failed to fetch projects by tag';
			console.error(error.value);
		} finally {
			isLoading.value = false;
		}
	};

	// Fetch a single project
	const fetchProject = async (id: string | number) => {
		isLoading.value = true;
		error.value = null;
		try {
			currentProject.value = await api.get<Project>(API_ENDPOINTS.PROJECT.DETAIL(id));
		} catch (err: any) {
			error.value = err.message || 'Failed to fetch project';
			console.error(error.value);
		} finally {
			isLoading.value = false;
		}
	};

	// Create a new project
	const createProject = async (project: ProjectInput) => {
		isLoading.value = true;
		error.value = null;

		try {
			let data: Project;

			if (project.image) {
				const formData = new FormData();
				formData.append('title', project.title);
				formData.append('description', project.description);
				formData.append('status', project.status);
				formData.append('priority', String(project.priority));
				formData.append('tags', JSON.stringify(project.tags));
				if (project.github_link) formData.append('github_link', project.github_link);
				if (project.live_demo) formData.append('live_demo', project.live_demo);
				formData.append('image', project.image);

				data = await api.uploadForm<Project>(API_ENDPOINTS.PROJECT.BASE, formData);
			} else {
				data = await api.post<Project>(API_ENDPOINTS.PROJECT.BASE, project);
			}

			projects.value.push(data);
			currentProject.value = data;

			return data;
		} catch (err: any) {
			error.value = err.message || 'Failed to create project';
			console.error(error.value);
			throw error.value;
		} finally {
			isLoading.value = false;
		}
	};

	// Update a project
	const updateProject = async (id: string | number, project: Partial<ProjectInput>) => {
		isLoading.value = true;
		error.value = null;

		try {
			let data: Project;

			if (project.image) {
				const formData = new FormData();

				if (project.title) formData.append('title', project.title);
				if (project.description) formData.append('description', project.description);
				if (project.status) formData.append('status', project.status);
				if (project.priority !== undefined) formData.append('priority', String(project.priority));
				if (project.tags) formData.append('tags', JSON.stringify(project.tags));
				if (project.github_link !== undefined) formData.append('github_link', project.github_link || '');
				if (project.live_demo !== undefined) formData.append('live_demo', project.live_demo || '');
				formData.append('image', project.image);

				data = await api.uploadForm<Project>(API_ENDPOINTS.PROJECT.DETAIL(id), formData, 'PATCH');
			} else {
				data = await api.patch<Project>(API_ENDPOINTS.PROJECT.DETAIL(id), project);
			}

			// Update the project in the projects array
			const index = projects.value.findIndex((proj) => proj.id === data.id);
			if (index !== -1) {
				projects.value[index] = data;
			}

			if (currentProject.value && currentProject.value.id === data.id) {
				currentProject.value = data;
			}

			return data;
		} catch (err: any) {
			error.value = err.message || 'Failed to update project';
			console.error(error.value);
			throw error.value;
		} finally {
			isLoading.value = false;
		}
	};

	// Delete a project
	const deleteProject = async (id: string | number) => {
		isLoading.value = true;
		error.value = null;

		try {
			await api.delete(API_ENDPOINTS.PROJECT.DETAIL(id));

			// Remove the project from the projects array
			projects.value = projects.value.filter((proj) => proj.id !== id);

			if (currentProject.value && currentProject.value.id === id) {
				currentProject.value = null;
			}

			return true;
		} catch (err: any) {
			error.value = err.message || 'Failed to delete project';
			console.error(error.value);
			throw error.value;
		} finally {
			isLoading.value = false;
		}
	};

	return {
		projects,
		currentProject,
		isLoading,
		error,
		fetchProjects,
		fetchActiveProjects,
		fetchRecentProjects,
		fetchArchivedProjects,
		fetchProjectsByTag,
		fetchProject,
		createProject,
		updateProject,
		deleteProject,
	};
}
