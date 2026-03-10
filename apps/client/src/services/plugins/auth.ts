import { onAuthFailure } from '@/services/api/core';
import { useAuthStore } from '@/stores/auth';

import type { Pinia } from 'pinia';

export default defineNuxtPlugin((nuxtApp) => {
    // Only setup on client side
    if (!import.meta.client) {
        return;
    }

    // Register auth failure handler
    // This will be called when a 401 error occurs and token refresh fails
    // Only clears auth state - the layout/page handles redirection
    onAuthFailure(() => {
        const authStore = useAuthStore(nuxtApp.$pinia as Pinia);
        authStore.clearAuth();
    });
});
