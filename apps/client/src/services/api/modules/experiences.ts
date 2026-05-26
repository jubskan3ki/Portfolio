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
    getAll: (filters?: ExperienceFilters): Promise<PaginatedResponse<Experience>> =>
        httpClient.get(API_ENDPOINTS.EXPERIENCES.BASE, filters as Record<string, unknown>),

    getById: (id: number | string): Promise<Experience> => httpClient.get(API_ENDPOINTS.EXPERIENCES.DETAIL(id)),

    getByType: async (typeName: string, filters?: ExperienceFilters): Promise<Experience[]> => {
        const response: PaginatedResponse<Experience> = await httpClient.get(
            API_ENDPOINTS.EXPERIENCES.BY_TYPE(typeName),
            filters as Record<string, unknown>,
        );
        return response.data;
    },

    getCurrent: (): Promise<Experience | null> => httpClient.get(API_ENDPOINTS.EXPERIENCES.CURRENT),

    getTimeline: (): Promise<ExperienceTimeline[]> => httpClient.get(API_ENDPOINTS.EXPERIENCES.TIMELINE),

    create: (data: ExperienceCreateData): Promise<Experience> => httpClient.post(API_ENDPOINTS.EXPERIENCES.BASE, data),

    update: (id: number | string, data: ExperienceUpdateData): Promise<Experience> =>
        httpClient.patch(API_ENDPOINTS.EXPERIENCES.DETAIL(id), data),

    delete: (id: number | string): Promise<void> => httpClient.delete(API_ENDPOINTS.EXPERIENCES.DETAIL(id)),

    getTypes: (): Promise<ExperienceType[]> => httpClient.get(API_ENDPOINTS.EXPERIENCES.TYPES),

    getType: (id: number | string): Promise<ExperienceType> =>
        httpClient.get(API_ENDPOINTS.EXPERIENCES.TYPE_DETAIL(id)),

    createType: (data: ExperienceTypeCreateData): Promise<ExperienceType> =>
        httpClient.post(API_ENDPOINTS.EXPERIENCES.TYPES, data),

    updateType: (id: number | string, data: ExperienceTypeUpdateData): Promise<ExperienceType> =>
        httpClient.patch(API_ENDPOINTS.EXPERIENCES.TYPE_DETAIL(id), data),

    deleteType: (id: number | string): Promise<void> => httpClient.delete(API_ENDPOINTS.EXPERIENCES.TYPE_DETAIL(id)),

    getStats: (): Promise<ExperienceStats> => httpClient.get(API_ENDPOINTS.EXPERIENCES.STATS),

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
        () => experiencesApi.getAll(unref(filters)),
        { placeholderData: (prev: PaginatedResponse<Experience> | undefined) => prev },
    );
}

export function useExperienceDetail(id: MaybeRef<number | string>) {
    return createDetailQuery(
        computed(() => experienceKeys.detail(unref(id))),
        () => experiencesApi.getById(unref(id)),
        { enabled: computed(() => !!unref(id)) },
    );
}

export function useExperiencesByType(typeName: MaybeRef<string>) {
    return createStaticQuery(
        computed(() => experienceKeys.byType(unref(typeName))),
        () => experiencesApi.getByType(unref(typeName)),
        { enabled: computed(() => !!unref(typeName)) },
    );
}

export function useProfessionalExperiences(options?: QueryOptions<Experience[]>) {
    return createStaticQuery(experienceKeys.professional(), () => experiencesApi.getByType('professional'), options);
}

export function useExperienceTypes() {
    return createStaticQuery(experienceKeys.types(), experiencesApi.getTypes);
}

export function useExperienceStats() {
    return createStaticQuery(experienceKeys.stats(), experiencesApi.getStats);
}

export function useCurrentExperience() {
    return createDetailQuery(experienceKeys.current(), experiencesApi.getCurrent);
}

export function useExperienceTimeline() {
    return createStaticQuery(experienceKeys.timeline(), experiencesApi.getTimeline);
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
