import { defineStore } from 'pinia';
import { computed, ref } from 'vue';

import type { UserProfile as User } from '@/types/api/auth';

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
    };

    const clearAuth = () => {
        user.value = null;
    };

    return {
        user,
        isAuthenticated,
        fullName,
        setUser,
        clearAuth,
    };
});
