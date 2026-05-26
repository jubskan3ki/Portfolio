import type { Pinia } from 'pinia';
import { onAuthFailure } from '@/services/api/core';
import { useAuthStore } from '@/stores/auth';

export default defineNuxtPlugin((nuxtApp) => {
    if (!import.meta.client) {
        return;
    }

    // 401 + refresh échoué -> clear store (redirection gérée layout/page)
    onAuthFailure(() => {
        const authStore = useAuthStore(nuxtApp.$pinia as Pinia);
        authStore.clearAuth();
    });
});
