import type { MaybeRef } from 'vue';
import { computed, unref } from 'vue';
import { API_ENDPOINTS } from '@/config/api';

import type { ExperienceFilters, PaginatedResponse } from '@/types/api/common';
import type {
    Experience,
    ExperienceCreateData,
    ExperienceStats,
    ExperienceTimeline,
    ExperienceType,
    ExperienceTypeCreateData,
    ExperienceTypeUpdateData,
    ExperienceUpdateData,
} from '@/types/feature/experience';
import type { QueryOptions } from '@/types/services/api';
import {
    createDetailQuery,
    createKeys,
    createListQuery,
    createStaticQuery,
    createSubResourceMutations,
    httpClient,
} from '../core';

export const experienceKeys = {
    ...createKeys('experiences'),
    byType: (typeName: string) => ['experiences', 'by-type', typeName] as const,
    current: () => ['experiences', 'current'] as const,
    timeline: () => ['experiences', 'timeline'] as const,
    professional: () => ['experiences', 'professional'] as const,
    educational: () => ['experiences', 'educational'] as const,
    types: () => ['experiences', 'types'] as const,
    type: (id: string | number) => ['experiences', 'type', id] as const,
    stats: () => ['experiences', 'stats'] as const,
};

export const experiencesApi = {
    getAll: (filters?: ExperienceFilters, signal?: AbortSignal): Promise<PaginatedResponse<Experience>> =>
        httpClient.get(API_ENDPOINTS.EXPERIENCES.BASE, filters as Record<string, unknown>, signal),

    getById: (id: number | string, signal?: AbortSignal): Promise<Experience> =>
        httpClient.get(API_ENDPOINTS.EXPERIENCES.DETAIL(id), undefined, signal),

    getByType: async (typeName: string, filters?: ExperienceFilters, signal?: AbortSignal): Promise<Experience[]> => {
        const response: PaginatedResponse<Experience> = await httpClient.get(
            API_ENDPOINTS.EXPERIENCES.BY_TYPE(typeName),
            filters as Record<string, unknown>,
            signal,
        );
        return response.data;
    },

    getCurrent: (signal?: AbortSignal): Promise<Experience | null> =>
        httpClient.get(API_ENDPOINTS.EXPERIENCES.CURRENT, undefined, signal),

    getTimeline: (signal?: AbortSignal): Promise<ExperienceTimeline[]> =>
        httpClient.get(API_ENDPOINTS.EXPERIENCES.TIMELINE, undefined, signal),

    create: (data: ExperienceCreateData): Promise<Experience> => httpClient.post(API_ENDPOINTS.EXPERIENCES.BASE, data),

    update: (id: number | string, data: ExperienceUpdateData): Promise<Experience> =>
        httpClient.patch(API_ENDPOINTS.EXPERIENCES.DETAIL(id), data),

    delete: (id: number | string): Promise<void> => httpClient.delete(API_ENDPOINTS.EXPERIENCES.DETAIL(id)),

    getTypes: (signal?: AbortSignal): Promise<ExperienceType[]> =>
        httpClient.get(API_ENDPOINTS.EXPERIENCES.TYPES, undefined, signal),

    getType: (id: number | string): Promise<ExperienceType> =>
        httpClient.get(API_ENDPOINTS.EXPERIENCES.TYPE_DETAIL(id)),

    createType: (data: ExperienceTypeCreateData): Promise<ExperienceType> =>
        httpClient.post(API_ENDPOINTS.EXPERIENCES.TYPES, data),

    updateType: (id: number | string, data: ExperienceTypeUpdateData): Promise<ExperienceType> =>
        httpClient.patch(API_ENDPOINTS.EXPERIENCES.TYPE_DETAIL(id), data),

    deleteType: (id: number | string): Promise<void> => httpClient.delete(API_ENDPOINTS.EXPERIENCES.TYPE_DETAIL(id)),

    getStats: (signal?: AbortSignal): Promise<ExperienceStats> =>
        httpClient.get(API_ENDPOINTS.EXPERIENCES.STATS, undefined, signal),

    getAdminList: <T = unknown>(params: Record<string, unknown>): Promise<T> =>
        httpClient.get(API_ENDPOINTS.EXPERIENCES.BASE, params),

    createWithForm: <T = Experience>(formData: FormData): Promise<T> =>
        httpClient.uploadForm(API_ENDPOINTS.EXPERIENCES.BASE, formData, 'POST'),

    updateWithForm: <T = Experience>(id: number | string, formData: FormData): Promise<T> =>
        httpClient.uploadForm(API_ENDPOINTS.EXPERIENCES.DETAIL(id), formData, 'PATCH'),
};

export function useExperiences(filters?: MaybeRef<ExperienceFilters>) {
    return createListQuery(
        computed(() => experienceKeys.list(unref(filters))),
        ({ signal }) => experiencesApi.getAll(unref(filters), signal),
        { placeholderData: (prev: PaginatedResponse<Experience> | undefined) => prev },
    );
}

export function useExperienceDetail(id: MaybeRef<number | string>) {
    return createDetailQuery(
        computed(() => experienceKeys.detail(unref(id))),
        ({ signal }) => experiencesApi.getById(unref(id), signal),
        { enabled: computed(() => !!unref(id)) },
    );
}

export function useExperiencesByType(typeName: MaybeRef<string>) {
    return createStaticQuery(
        computed(() => experienceKeys.byType(unref(typeName))),
        ({ signal }) => experiencesApi.getByType(unref(typeName), undefined, signal),
        { enabled: computed(() => !!unref(typeName)) },
    );
}

export function useProfessionalExperiences(options?: QueryOptions<Experience[]>) {
    return createStaticQuery(
        experienceKeys.professional(),
        ({ signal }) => experiencesApi.getByType('professional', undefined, signal),
        options,
    );
}

export function useExperienceTypes() {
    return createStaticQuery(experienceKeys.types(), ({ signal }) => experiencesApi.getTypes(signal));
}

export function useExperienceStats() {
    return createStaticQuery(experienceKeys.stats(), ({ signal }) => experiencesApi.getStats(signal));
}

export function useCurrentExperience() {
    return createDetailQuery(experienceKeys.current(), ({ signal }) => experiencesApi.getCurrent(signal));
}

export function useExperienceTimeline() {
    return createStaticQuery(experienceKeys.timeline(), ({ signal }) => experiencesApi.getTimeline(signal));
}

const typeMutations = createSubResourceMutations<
    ExperienceType,
    ExperienceTypeCreateData,
    ExperienceTypeUpdateData,
    number | string
>(
    {
        create: experiencesApi.createType,
        update: experiencesApi.updateType,
        delete: experiencesApi.deleteType,
    },
    { all: experienceKeys.types },
    'id',
);

export const useCreateExperienceType = typeMutations.useCreate;
