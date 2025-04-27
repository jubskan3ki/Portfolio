import type { Ref } from 'vue';
import { ref } from 'vue';

import { API_ENDPOINTS } from '@/config/api';
import api from '@/services/utils/httpClient';

// Types
export interface Stack {
	id: number;
	name: string;
	category: 'frontend' | 'backend' | 'database' | 'devops' | 'mobile' | 'design' | 'other';
	proficiency: number;
	experience_years: number;
	description?: string;
	official_website?: string;
	icon?: string;
	created_at: string;
	updated_at: string;
	slug: string;
}

export interface StackInput {
	name: string;
	category: 'frontend' | 'backend' | 'database' | 'devops' | 'mobile' | 'design' | 'other';
	proficiency: number;
	experience_years: number;
	description?: string;
	official_website?: string;
	icon?: File;
}

export function useStack() {
	const stacks: Ref<Stack[]> = ref([]);
	const currentStack: Ref<Stack | null> = ref(null);
	const isLoading = ref(false);
	const error = ref<string | null>(null);

	const fetchStacks = async () => {
		isLoading.value = true;
		error.value = null;
		try {
			stacks.value = await api.get<Stack[]>(API_ENDPOINTS.STACK.BASE);
		} catch (err: any) {
			error.value = err.message || 'Failed to fetch stacks';
			console.error(error.value);
		} finally {
			isLoading.value = false;
		}
	};

	// Fetch stacks by category
	const fetchStacksByCategory = async (category: string) => {
		isLoading.value = true;
		error.value = null;
		try {
			stacks.value = await api.get<Stack[]>(API_ENDPOINTS.STACK.BY_CATEGORY(category));
		} catch (err: any) {
			error.value = err.message || 'Failed to fetch stacks by category';
			console.error(error.value);
		} finally {
			isLoading.value = false;
		}
	};

	// Fetch most proficient stacks
	const fetchMostProficientStacks = async () => {
		isLoading.value = true;
		error.value = null;
		try {
			stacks.value = await api.get<Stack[]>(API_ENDPOINTS.STACK.MOST_PROFICIENT);
		} catch (err: any) {
			error.value = err.message || 'Failed to fetch most proficient stacks';
			console.error(error.value);
		} finally {
			isLoading.value = false;
		}
	};

	// Fetch a single stack
	const fetchStack = async (id: string | number) => {
		isLoading.value = true;
		error.value = null;
		try {
			currentStack.value = await api.get<Stack>(API_ENDPOINTS.STACK.DETAIL(id));
		} catch (err: any) {
			error.value = err.message || 'Failed to fetch stack';
			console.error(error.value);
		} finally {
			isLoading.value = false;
		}
	};

	// Create a new stack
	const createStack = async (stack: StackInput) => {
		isLoading.value = true;
		error.value = null;

		try {
			const formData = new FormData();
			formData.append('name', stack.name);
			formData.append('category', stack.category);
			formData.append('proficiency', String(stack.proficiency));
			formData.append('experience_years', String(stack.experience_years));
			if (stack.description) formData.append('description', stack.description);
			if (stack.official_website) formData.append('official_website', stack.official_website);
			if (stack.icon) formData.append('icon', stack.icon);

			const newStack = await api.uploadForm<Stack>(API_ENDPOINTS.STACK.BASE, formData);
			stacks.value.push(newStack);
			currentStack.value = newStack;

			return newStack;
		} catch (err: any) {
			error.value = err.message || 'Failed to create stack';
			console.error(error.value);
			throw error.value;
		} finally {
			isLoading.value = false;
		}
	};

	// Update a stack
	const updateStack = async (id: string | number, stack: Partial<StackInput>) => {
		isLoading.value = true;
		error.value = null;

		try {
			const formData = new FormData();

			if (stack.name) formData.append('name', stack.name);
			if (stack.category) formData.append('category', stack.category);
			if (stack.proficiency !== undefined) formData.append('proficiency', String(stack.proficiency));
			if (stack.experience_years !== undefined)
				formData.append('experience_years', String(stack.experience_years));
			if (stack.description !== undefined) formData.append('description', stack.description || '');
			if (stack.official_website !== undefined) formData.append('official_website', stack.official_website || '');
			if (stack.icon) formData.append('icon', stack.icon);

			const updatedStack = await api.uploadForm<Stack>(API_ENDPOINTS.STACK.DETAIL(id), formData, 'PATCH');

			// Update the stack in the stacks array
			const index = stacks.value.findIndex((s) => s.id === updatedStack.id);
			if (index !== -1) {
				stacks.value[index] = updatedStack;
			}

			if (currentStack.value && currentStack.value.id === updatedStack.id) {
				currentStack.value = updatedStack;
			}

			return updatedStack;
		} catch (err: any) {
			error.value = err.message || 'Failed to update stack';
			console.error(error.value);
			throw error.value;
		} finally {
			isLoading.value = false;
		}
	};

	// Delete a stack
	const deleteStack = async (id: string | number) => {
		isLoading.value = true;
		error.value = null;

		try {
			await api.delete(API_ENDPOINTS.STACK.DETAIL(id));

			// Remove the stack from the stacks array
			stacks.value = stacks.value.filter((s) => s.id !== id);

			if (currentStack.value && currentStack.value.id === id) {
				currentStack.value = null;
			}

			return true;
		} catch (err: any) {
			error.value = err.message || 'Failed to delete stack';
			console.error(error.value);
			throw error.value;
		} finally {
			isLoading.value = false;
		}
	};

	return {
		stacks,
		currentStack,
		isLoading,
		error,
		fetchStacks,
		fetchStacksByCategory,
		fetchMostProficientStacks,
		fetchStack,
		createStack,
		updateStack,
		deleteStack,
	};
}
