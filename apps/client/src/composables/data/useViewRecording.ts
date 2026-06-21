import type { MaybeRefOrGetter } from 'vue';
import { ref, toValue, watch } from 'vue';
import type { UseViewRecordingReturn } from '@/types/composables/data';

export function useViewRecording(
    data: MaybeRefOrGetter<{ slug: string } | null | undefined>,
    recordFn: (slug: string) => void,
): UseViewRecordingReturn {
    const viewRecorded = ref(false);
    // Mémorise le dernier slug enregistré : permet de ré-enregistrer lors d'une
    // navigation client entre deux détails (le composant est réutilisé, un simple
    // booléen resterait bloqué à true).
    const recordedSlug = ref<string | null>(null);

    watch(
        () => toValue(data),
        (item) => {
            // Client uniquement : sur SSR le détail est déjà en cache, un watch immediate
            // déclencherait un POST côté serveur (sans CSRF, compteur de vues faussé).
            if (!import.meta.client || !item) {
                return;
            }
            if (recordedSlug.value === item.slug) {
                return;
            }
            Promise.resolve(recordFn(item.slug)).catch(() => {});
            recordedSlug.value = item.slug;
            viewRecorded.value = true;
        },
        { immediate: true },
    );

    return { viewRecorded };
}
