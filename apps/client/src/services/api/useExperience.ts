import type { Ref } from 'vue';
import { ref } from 'vue';

import { API_ENDPOINTS } from '@/config/api';
import api from '@/services/utils/httpClient';

// Types
export interface Experience {
	id: number;
	title: string;
	company_or_school: string;
	location: string;
	start_date: string;
	end_date?: string;
	description: string;
	skills_acquired: string[];
	experience_type: 'education' | 'professional';
	is_highlighted: boolean;
	website?: string;
	logo?: string;
	created_at: string;
	updated_at: string;
}

export interface ExperienceInput {
	title: string;
	company_or_school: string;
	location: string;
	start_date: string;
	end_date?: string;
	description: string;
	skills_acquired: string[];
	experience_type: 'education' | 'professional';
	is_highlighted: boolean;
	website?: string;
	logo?: File;
}

export function useExperience() {
	const experiences: Ref<Experience[]> = ref([]);
	const currentExperience: Ref<Experience | null> = ref(null);
	const isLoading = ref(false);
	const error = ref<string | null>(null);

	// Fetch all experiences
	const fetchExperiences = async () => {
		isLoading.value = true;
		error.value = null;
		try {
			experiences.value = await api.get<Experience[]>(API_ENDPOINTS.EXPERIENCE.BASE);
		} catch (err: any) {
			error.value = err.message || 'Failed to fetch experiences';
			console.error(error.value);
		} finally {
			isLoading.value = false;
		}
	};

	// Fetch current experiences
	const fetchCurrentExperiences = async () => {
		isLoading.value = true;
		error.value = null;
		try {
			experiences.value = await api.get<Experience[]>(API_ENDPOINTS.EXPERIENCE.CURRENT);
		} catch (err: any) {
			error.value = err.message || 'Failed to fetch current experiences';
			console.error(error.value);
		} finally {
			isLoading.value = false;
		}
	};

	// Fetch professional experiences
	const fetchProfessionalExperiences = async () => {
		isLoading.value = true;
		error.value = null;
		try {
			experiences.value = await api.get<Experience[]>(API_ENDPOINTS.EXPERIENCE.PROFESSIONAL);
		} catch (err: any) {
			error.value = err.message || 'Failed to fetch professional experiences';
			console.error(error.value);
		} finally {
			isLoading.value = false;
		}
	};

	// Fetch educational experiences
	const fetchEducationalExperiences = async () => {
		isLoading.value = true;
		error.value = null;
		try {
			experiences.value = await api.get<Experience[]>(API_ENDPOINTS.EXPERIENCE.EDUCATIONAL);
		} catch (err: any) {
			error.value = err.message || 'Failed to fetch educational experiences';
			console.error(error.value);
		} finally {
			isLoading.value = false;
		}
	};

	// Fetch highlighted experiences
	const fetchHighlightedExperiences = async () => {
		isLoading.value = true;
		error.value = null;
		try {
			experiences.value = await api.get<Experience[]>(API_ENDPOINTS.EXPERIENCE.HIGHLIGHTED);
		} catch (err: any) {
			error.value = err.message || 'Failed to fetch highlighted experiences';
			console.error(error.value);
		} finally {
			isLoading.value = false;
		}
	};

	// Fetch a single experience
	const fetchExperience = async (id: string | number) => {
		isLoading.value = true;
		error.value = null;
		try {
			currentExperience.value = await api.get<Experience>(API_ENDPOINTS.EXPERIENCE.DETAIL(id));
		} catch (err: any) {
			error.value = err.message || 'Failed to fetch experience';
			console.error(error.value);
		} finally {
			isLoading.value = false;
		}
	};

	// Create a new experience
	const createExperience = async (experience: ExperienceInput) => {
		isLoading.value = true;
		error.value = null;

		try {
			let data: any;

			if (experience.logo) {
				const formData = new FormData();
				formData.append('title', experience.title);
				formData.append('company_or_school', experience.company_or_school);
				formData.append('location', experience.location);
				formData.append('start_date', experience.start_date);
				if (experience.end_date) formData.append('end_date', experience.end_date);
				formData.append('description', experience.description);
				formData.append('skills_acquired', JSON.stringify(experience.skills_acquired));
				formData.append('experience_type', experience.experience_type);
				formData.append('is_highlighted', String(experience.is_highlighted));
				if (experience.website) formData.append('website', experience.website);
				formData.append('logo', experience.logo);

				data = await api.uploadForm<Experience>(API_ENDPOINTS.EXPERIENCE.BASE, formData);
			} else {
				data = await api.post<Experience>(API_ENDPOINTS.EXPERIENCE.BASE, experience);
			}

			experiences.value.push(data);
			currentExperience.value = data;

			return data;
		} catch (err: any) {
			error.value = err.message || 'Failed to create experience';
			console.error(error.value);
			throw error.value;
		} finally {
			isLoading.value = false;
		}
	};

	// Update an experience
	const updateExperience = async (id: string | number, experience: Partial<ExperienceInput>) => {
		isLoading.value = true;
		error.value = null;

		try {
			let data: Experience;

			if (experience.logo) {
				const formData = new FormData();

				if (experience.title) formData.append('title', experience.title);
				if (experience.company_or_school) formData.append('company_or_school', experience.company_or_school);
				if (experience.location) formData.append('location', experience.location);
				if (experience.start_date) formData.append('start_date', experience.start_date);
				if (experience.end_date) formData.append('end_date', experience.end_date);
				if (experience.description) formData.append('description', experience.description);
				if (experience.skills_acquired)
					formData.append('skills_acquired', JSON.stringify(experience.skills_acquired));
				if (experience.experience_type) formData.append('experience_type', experience.experience_type);
				if (experience.is_highlighted !== undefined)
					formData.append('is_highlighted', String(experience.is_highlighted));
				if (experience.website) formData.append('website', experience.website);
				formData.append('logo', experience.logo);

				data = await api.uploadForm<Experience>(API_ENDPOINTS.EXPERIENCE.DETAIL(id), formData, 'PATCH');
			} else {
				data = await api.patch<Experience>(API_ENDPOINTS.EXPERIENCE.DETAIL(id), experience);
			}

			// Update the experience in the experiences array
			const index = experiences.value.findIndex((exp) => exp.id === data.id);
			if (index !== -1) {
				experiences.value[index] = data;
			}

			if (currentExperience.value && currentExperience.value.id === data.id) {
				currentExperience.value = data;
			}

			return data;
		} catch (err: any) {
			error.value = err.message || 'Failed to update experience';
			console.error(error.value);
			throw error.value;
		} finally {
			isLoading.value = false;
		}
	};

	// Delete an experience
	const deleteExperience = async (id: string | number) => {
		isLoading.value = true;
		error.value = null;

		try {
			await api.delete(API_ENDPOINTS.EXPERIENCE.DETAIL(id));

			// Remove the experience from the experiences array
			experiences.value = experiences.value.filter((exp) => exp.id !== id);

			if (currentExperience.value && currentExperience.value.id === id) {
				currentExperience.value = null;
			}

			return true;
		} catch (err: any) {
			error.value = err.message || 'Failed to delete experience';
			console.error(error.value);
			throw error.value;
		} finally {
			isLoading.value = false;
		}
	};

	return {
		experiences,
		currentExperience,
		isLoading,
		error,
		fetchExperiences,
		fetchCurrentExperiences,
		fetchProfessionalExperiences,
		fetchEducationalExperiences,
		fetchHighlightedExperiences,
		fetchExperience,
		createExperience,
		updateExperience,
		deleteExperience,
	};
}
