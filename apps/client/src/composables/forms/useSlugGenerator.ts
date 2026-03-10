import { ref, watch, type Ref } from 'vue';

import { slugify } from '@/services/utils/string';

interface UseSlugGeneratorOptions {
    auto?: boolean;
    trackManualEdit?: boolean;
}

interface UseSlugGeneratorReturn {
    slug: Ref<string>;
    generate: () => void;
    setSlug: (value: string) => void;
    wasManuallyEdited: Ref<boolean>;
}

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
