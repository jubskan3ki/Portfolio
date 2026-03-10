import { computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import { isValidSlug } from '@/services/utils/validation';

import type { ComputedRef } from 'vue';
import type { RouteLocationRaw } from 'vue-router';

interface UseDetailSlugReturn {
    slug: ComputedRef<string>;
}

export function useDetailSlug(fallbackRoute: RouteLocationRaw): UseDetailSlugReturn {
    const route = useRoute();
    const router = useRouter();

    const rawSlug = computed(() => route.params.slug);

    const slug = computed(() => {
        const s = rawSlug.value;
        if (isValidSlug(s)) {
            return s;
        }
        return '';
    });

    watch(
        rawSlug,
        (s) => {
            if (s && !isValidSlug(s)) {
                router.replace(fallbackRoute);
            }
        },
        { immediate: true },
    );

    return { slug };
}
