import { useMutation } from '@tanstack/vue-query';

import { useAlert } from '@/composables/ui/useAlert';
import { API_ENDPOINTS } from '@/config/api';
import { parseError } from '@/services/utils/errors';

import { httpClient, createKeys, createStaticQuery } from '../core';

import type {
    FAQ,
    ContactForm,
    ContactInfo,
    ContactResponse,
    ContactStats,
    ContactMessage,
    ContactMessagesFilters,
    FAQCreateData,
    FAQUpdateData,
    ContactInfoCreateData,
    ContactInfoUpdateData,
    ContactMessageUpdateData,
} from '@/types/feature/contact';
import type { QueryOptions } from '@/types/services/api';

export const contactKeys = {
    ...createKeys('contact'),
    faqs: () => ['contact', 'faqs'] as const,
    faq: (id: string | number) => ['contact', 'faq', id] as const,
    info: () => ['contact', 'info'] as const,
    messages: () => ['contact', 'messages'] as const,
    message: (id: string | number) => ['contact', 'message', id] as const,
    stats: () => ['contact', 'stats'] as const,
};

export const contactApi = {
    submitForm: (data: ContactForm): Promise<ContactResponse> => httpClient.post(API_ENDPOINTS.CONTACT.BASE, data),

    getFaqs: (): Promise<FAQ[]> => httpClient.get(API_ENDPOINTS.CONTACT.FAQS),

    getInfo: (): Promise<ContactInfo | null> =>
        httpClient.get<ContactInfo[]>(API_ENDPOINTS.CONTACT.INFO).then((list) => list[0] ?? null),

    getMessages: async (filters?: ContactMessagesFilters): Promise<ContactMessage[]> => {
        const response = await httpClient.get<{ data: ContactMessage[] }>(
            API_ENDPOINTS.CONTACT.BASE,
            filters as Record<string, unknown>,
        );
        return response.data;
    },

    getMessage: (id: number | string): Promise<ContactMessage> => httpClient.get(API_ENDPOINTS.CONTACT.DETAIL(id)),

    updateMessage: (id: number | string, data: ContactMessageUpdateData): Promise<ContactMessage> =>
        httpClient.patch(API_ENDPOINTS.CONTACT.DETAIL(id), data),

    deleteMessage: (id: number | string): Promise<void> => httpClient.delete(API_ENDPOINTS.CONTACT.DETAIL(id)),

    getFaq: (id: number | string): Promise<FAQ> => httpClient.get(API_ENDPOINTS.CONTACT.FAQ_DETAIL(id)),

    createFaq: (data: FAQCreateData): Promise<FAQ> => httpClient.post(API_ENDPOINTS.CONTACT.FAQS, data),

    updateFaq: (id: number | string, data: FAQUpdateData): Promise<FAQ> =>
        httpClient.patch(API_ENDPOINTS.CONTACT.FAQ_DETAIL(id), data),

    deleteFaq: (id: number | string): Promise<void> => httpClient.delete(API_ENDPOINTS.CONTACT.FAQ_DETAIL(id)),

    getInfoDetail: (id: number | string): Promise<ContactInfo> => httpClient.get(API_ENDPOINTS.CONTACT.INFO_DETAIL(id)),

    createInfo: (data: ContactInfoCreateData): Promise<ContactInfo> =>
        httpClient.post(API_ENDPOINTS.CONTACT.INFO, data),

    updateInfo: (id: number | string, data: ContactInfoUpdateData): Promise<ContactInfo> =>
        httpClient.patch(API_ENDPOINTS.CONTACT.INFO_DETAIL(id), data),

    deleteInfo: (id: number | string): Promise<void> => httpClient.delete(API_ENDPOINTS.CONTACT.INFO_DETAIL(id)),

    getStats: (): Promise<ContactStats> => httpClient.get(API_ENDPOINTS.CONTACT.STATS),

    // Admin methods
    getAdminMessages: <T = unknown>(params: Record<string, unknown>): Promise<T> =>
        httpClient.get(API_ENDPOINTS.CONTACT.BASE, params),

    markAsRead: (id: number | string): Promise<ContactMessage> =>
        httpClient.patch(API_ENDPOINTS.CONTACT.DETAIL(id), { isRead: true }),
};

export function useFaqs() {
    return createStaticQuery(contactKeys.faqs(), contactApi.getFaqs);
}

export function useContactInfo(options?: QueryOptions<ContactInfo>) {
    return createStaticQuery(contactKeys.info(), contactApi.getInfo, options);
}

export function useSubmitContact() {
    const { success, error: showError } = useAlert();

    return useMutation({
        mutationFn: contactApi.submitForm,
        onSuccess: () => {
            success('Message envoyé avec succès!', 'Merci pour votre message');
        },
        onError: (err: unknown) => {
            const { message } = parseError(err);
            showError(message, 'Erreur');
        },
    });
}
