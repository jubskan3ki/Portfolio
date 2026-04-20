import { refreshTokenManager } from '@/services/api/core/token';
import { authApi } from '@/services/api/modules/auth';
import { useAuthStore } from '@/stores/auth';

const SESSION_HINT_KEY = 'portfolio.session.hint';

export default defineNuxtRouteMiddleware(async (to) => {
    // Protège /admin/* mais pas la page de login /admin
    if (!to.path.startsWith('/admin/')) {
        return;
    }

    // Skip SSR: JWT en HTTPOnly cookies, vérification côté client
    if (!import.meta.client) {
        return;
    }

    const authStore = useAuthStore();

    if (authStore.isAuthenticated) {
        return;
    }

    if (!localStorage.getItem(SESSION_HINT_KEY)) {
        const redirectTo = to.fullPath !== '/admin' ? to.fullPath : '/admin/dashboard';
        return navigateTo(`/admin?redirect=${encodeURIComponent(redirectTo)}`, { replace: true });
    }

    try {
        const refreshed = await refreshTokenManager.refresh();
        if (!refreshed) {
            throw new Error('Token refresh failed');
        }
        const profile = await authApi.getProfile();
        authStore.setUser(profile);
    } catch {
        localStorage.removeItem(SESSION_HINT_KEY);
        const redirectTo = to.fullPath !== '/admin' ? to.fullPath : '/admin/dashboard';
        return navigateTo(`/admin?redirect=${encodeURIComponent(redirectTo)}`, {
            replace: true,
        });
    }
});
