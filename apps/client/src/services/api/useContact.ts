import type { Ref } from 'vue';
import { ref } from 'vue';

import { API_ENDPOINTS } from '@/config/api';

import api from '../utils/httpClient';

// Types
export interface ContactMessage {
	id: number;
	name: string;
	email: string;
	subject: 'general' | 'job' | 'project' | 'other';
	message: string;
	phone_number?: string;
	created_at: string;
	is_read: boolean;
}

export interface ContactMessageInput {
	name: string;
	email: string;
	subject: 'general' | 'job' | 'project' | 'other';
	message: string;
	phone_number?: string;
}

export function useContact() {
	const messages: Ref<ContactMessage[]> = ref([]);
	const currentMessage: Ref<ContactMessage | null> = ref(null);
	const isLoading = ref(false);
	const error = ref<string | null>(null);

	// Fetch all contact messages
	const fetchMessages = async () => {
		isLoading.value = true;
		error.value = null;
		try {
			messages.value = await api.get<ContactMessage[]>(API_ENDPOINTS.CONTACT.BASE);
		} catch (err: any) {
			error.value = err.message || 'Failed to fetch contact messages';
			console.error(error.value);
		} finally {
			isLoading.value = false;
		}
	};

	// Fetch unread contact messages
	const fetchUnreadMessages = async () => {
		isLoading.value = true;
		error.value = null;
		try {
			messages.value = await api.get<ContactMessage[]>(API_ENDPOINTS.CONTACT.UNREAD);
		} catch (err: any) {
			error.value = err.message || 'Failed to fetch unread messages';
			console.error(error.value);
		} finally {
			isLoading.value = false;
		}
	};

	// Fetch a single contact message
	const fetchMessage = async (id: string | number) => {
		isLoading.value = true;
		error.value = null;
		try {
			currentMessage.value = await api.get<ContactMessage>(API_ENDPOINTS.CONTACT.DETAIL(id));
		} catch (err: any) {
			error.value = err.message || 'Failed to fetch contact message';
			console.error(error.value);
		} finally {
			isLoading.value = false;
		}
	};

	// Send a contact message
	const sendMessage = async (message: ContactMessageInput) => {
		isLoading.value = true;
		error.value = null;
		try {
			const response = await api.post<ContactMessage>(API_ENDPOINTS.CONTACT.BASE, message);
			return response;
		} catch (err: any) {
			error.value = err.message || 'Failed to send message';
			console.error(error.value);
			throw error.value;
		} finally {
			isLoading.value = false;
		}
	};

	// Mark a message as read
	const markAsRead = async (id: string | number) => {
		isLoading.value = true;
		error.value = null;
		try {
			const updatedMessage = await api.put<ContactMessage>(API_ENDPOINTS.CONTACT.MARK_AS_READ(id), {});

			// Update the message in the messages array
			const index = messages.value.findIndex((msg) => msg.id === updatedMessage.id);
			if (index !== -1) {
				messages.value[index] = updatedMessage;
			}

			if (currentMessage.value && currentMessage.value.id === updatedMessage.id) {
				currentMessage.value = updatedMessage;
			}

			return updatedMessage;
		} catch (err: any) {
			error.value = err.message || 'Failed to mark message as read';
			console.error(error.value);
			throw error.value;
		} finally {
			isLoading.value = false;
		}
	};

	return {
		messages,
		currentMessage,
		isLoading,
		error,
		fetchMessages,
		fetchUnreadMessages,
		fetchMessage,
		sendMessage,
		markAsRead,
	};
}
