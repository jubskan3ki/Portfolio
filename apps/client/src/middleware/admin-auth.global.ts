import { refreshTokenManager } from '@/services/api/core/token';
import { authApi } from '@/services/api/modules/auth';
import { useAuthStore } from '@/stores/auth';

export default defineNuxtRouteMiddleware(async (to) => {
    // Only protect admin sub-routes (not the login page at /admin)
    if (!to.path.startsWith('/admin/')) {
        return;
    }

    // Skip on server — JWT is in HTTPOnly cookies, verified client-side
    if (!import.meta.client) {
        return;
    }

    const authStore = useAuthStore();

    // Already authenticated in this session
    if (authStore.isAuthenticated) {
        return;
    }

    // Try to verify with backend (imperative — outside component setup)
    try {
        const refreshed = await refreshTokenManager.refresh();
        if (!refreshed) {
            throw new Error('Token refresh failed');
        }
        const profile = await authApi.getProfile();
        authStore.setUser(profile);
    } catch {
        // Not authenticated — redirect to login
        const redirectTo = to.fullPath !== '/admin' ? to.fullPath : '/admin/dashboard';
        return navigateTo(`/admin?redirect=${encodeURIComponent(redirectTo)}`, {
            replace: true,
        });
    }
});
