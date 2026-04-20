import { defineStore } from 'pinia';
import { computed, ref } from 'vue';

import type { UserProfile as User } from '@/types/api/auth';

const SESSION_HINT_KEY = 'portfolio.session.hint';

export const useAuthStore = defineStore('auth', () => {
    const user = ref<User | null>(null);

    const isAuthenticated = computed(() => !!user.value);
    const fullName = computed(() => {
        if (!user.value) {
            return '';
        }
        return `${user.value.firstName} ${user.value.lastName}`.trim();
    });

    const setUser = (profile: User) => {
        user.value = profile;
        if (import.meta.client) {
            localStorage.setItem(SESSION_HINT_KEY, '1');
        }
    };

    const clearAuth = () => {
        user.value = null;
        if (import.meta.client) {
            localStorage.removeItem(SESSION_HINT_KEY);
        }
    };

    return {
        user,
        isAuthenticated,
        fullName,
        setUser,
        clearAuth,
    };
});
