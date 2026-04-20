import { ref, watch, type Ref } from 'vue';

import { slugify } from '@/services/utils/string';

import type { UseSlugGeneratorOptions, UseSlugGeneratorReturn } from '@/types/composables/forms';

export function generateSlug(text: string): string {
    return slugify(text);
}

export function useSlugGenerator(source: Ref<string>, options: UseSlugGeneratorOptions = {}): UseSlugGeneratorReturn {
    const { auto = true, trackManualEdit = true } = options;

    const slug = ref('');
    const wasManuallyEdited = ref(false);

    const generate = () => {
        slug.value = generateSlug(source.value);
    };

    const setSlug = (value: string) => {
        slug.value = value;
        if (trackManualEdit && value !== generateSlug(source.value)) {
            wasManuallyEdited.value = true;
        }
    };

    if (auto) {
        watch(
            source,
            () => {
                if (!wasManuallyEdited.value) {
                    generate();
                }
            },
            { immediate: true },
        );
    }

    return {
        slug,
        generate,
        setSlug,
        wasManuallyEdited,
    };
}
