import { useMutation, useQueryClient } from '@tanstack/vue-query';

import { API_ENDPOINTS } from '@/config/api';
import { useAuthStore } from '@/stores/auth';

import { httpClient, createKeys } from '../core';
import { createRealtimeQuery } from '../core/query';

import type {
    LoginCredentials,
    LoginResponse,
    UserProfile,
    UpdateProfileData,
    ChangePasswordData,
    RequestResetPasswordData,
    VerifyResetCodeData,
    ConfirmResetPasswordData,
    AuthMessageResponse,
    VerifyCodeResponse,
} from '@/types/api/auth';
import type { SessionsResponse } from '@/types/feature/admin';

export const authKeys = {
    ...createKeys('auth'),
    sessions: () => ['auth', 'sessions'] as const,
};

export const authApi = {
    login: (credentials: LoginCredentials): Promise<LoginResponse> =>
        httpClient.post(API_ENDPOINTS.USERS.LOGIN, credentials),

    logout: (): Promise<void> => httpClient.post(API_ENDPOINTS.USERS.LOGOUT, {}),

    refresh: (): Promise<AuthMessageResponse> => httpClient.post(API_ENDPOINTS.USERS.REFRESH, {}),

    getProfile: (): Promise<UserProfile> => httpClient.get(API_ENDPOINTS.USERS.PROFILE),

    updateProfile: (data: UpdateProfileData): Promise<UserProfile> => httpClient.put(API_ENDPOINTS.USERS.PROFILE, data),

    changePassword: (data: ChangePasswordData): Promise<AuthMessageResponse> =>
        httpClient.post(API_ENDPOINTS.USERS.PASSWORD_CHANGE, data),

    requestResetPassword: (data: RequestResetPasswordData): Promise<AuthMessageResponse> =>
        httpClient.post(API_ENDPOINTS.USERS.REQUEST_RESET_PASSWORD, data),

    verifyResetCode: (data: VerifyResetCodeData): Promise<VerifyCodeResponse> =>
        httpClient.post(API_ENDPOINTS.USERS.VERIFY_RESET_CODE, data),

    confirmResetPassword: (data: ConfirmResetPasswordData): Promise<AuthMessageResponse> =>
        httpClient.post(API_ENDPOINTS.USERS.CONFIRM_RESET_PASSWORD, data),

    getSessions: (): Promise<SessionsResponse> => httpClient.get(API_ENDPOINTS.USERS.SESSIONS),

    revokeSession: (sessionId: string): Promise<void> =>
        httpClient.delete(`${API_ENDPOINTS.USERS.SESSIONS}?session_id=${sessionId}`),

    revokeAllSessions: (): Promise<void> => httpClient.delete(`${API_ENDPOINTS.USERS.SESSIONS}?all=true`),

    uploadProfileForm: (formData: FormData, method: 'PUT' | 'PATCH' = 'PUT'): Promise<UserProfile> =>
        httpClient.uploadForm(API_ENDPOINTS.USERS.PROFILE, formData, method),
};

export function useSessions() {
    return createRealtimeQuery(authKeys.sessions(), () => authApi.getSessions());
}

export function useRevokeSession() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (sessionId: string) => authApi.revokeSession(sessionId),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: authKeys.sessions() });
        },
    });
}

export function useRevokeAllSessions() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: () => authApi.revokeAllSessions(),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: authKeys.sessions() });
        },
    });
}

export function useUpdateProfile() {
    const authStore = useAuthStore();

    return useMutation({
        mutationFn: (data: UpdateProfileData) => authApi.updateProfile(data),
        onSuccess: (updatedUser) => {
            authStore.setUser(updatedUser);
        },
    });
}

export function useUploadProfileAvatar() {
    const authStore = useAuthStore();

    return useMutation({
        mutationFn: (formData: FormData) => authApi.uploadProfileForm(formData, 'PUT'),
        onSuccess: (updatedUser) => {
            authStore.setUser(updatedUser);
        },
    });
}

export function useLogin() {
    const authStore = useAuthStore();

    return useMutation({
        mutationFn: (credentials: LoginCredentials) => authApi.login(credentials),
        onSuccess: (data) => {
            if (data.user) {
                authStore.setUser(data.user);
            }
        },
    });
}

export function useLogout() {
    const authStore = useAuthStore();
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: () => authApi.logout(),
        onSettled: () => {
            authStore.clearAuth();
            queryClient.clear();
        },
    });
}
