import { onMounted, onUnmounted, ref } from 'vue';

export function useReducedMotion() {
    const prefersReducedMotion = ref(false);
    const isHydrated = ref(false);
    let mediaQuery: MediaQueryList | null = null;

    const checkMotionPreference = () => {
        if (typeof window !== 'undefined') {
            prefersReducedMotion.value = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        }
    };

    const handleChange = () => {
        checkMotionPreference();
    };

    onMounted(() => {
        isHydrated.value = true;
        checkMotionPreference();

        if (typeof window !== 'undefined') {
            mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
            mediaQuery.addEventListener('change', handleChange);
        }
    });

    onUnmounted(() => {
        if (mediaQuery) {
            mediaQuery.removeEventListener('change', handleChange);
        }
    });

    return { prefersReducedMotion, isHydrated };
}
