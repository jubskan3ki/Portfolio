import { computed, ref, watch, onMounted, onBeforeUnmount } from 'vue';

import { slugify } from '@/services/utils/string';

import type { TocItem } from '@/types/composables/ui';
import type { ContentBlock } from '@/types/feature/blog';
import type { Ref } from 'vue';

export function useTableOfContents(blocks: Ref<ContentBlock[] | undefined>) {
    const activeId = ref('');

    const headings = computed<TocItem[]>(() => {
        if (!blocks.value) {
            return [];
        }
        return blocks.value
            .filter((b): b is ContentBlock & { type: 'heading' } => b.type === 'heading')
            .map((b) => ({
                id: slugify(b.content),
                text: b.content,
                level: b.level,
            }));
    });

    let observer: IntersectionObserver | null = null;

    function setupObserver() {
        if (observer) {
            observer.disconnect();
        }
        if (!headings.value.length) {
            return;
        }

        observer = new IntersectionObserver(
            (entries) => {
                for (const entry of entries) {
                    if (entry.isIntersecting) {
                        activeId.value = entry.target.id;
                    }
                }
            },
            { rootMargin: '-80px 0px -60% 0px', threshold: 0.1 },
        );

        for (const heading of headings.value) {
            const el = document.getElementById(heading.id);
            if (el) {
                observer.observe(el);
            }
        }
    }

    onMounted(() => {
        watch(headings, () => setupObserver(), { immediate: true });
    });

    onBeforeUnmount(() => {
        if (observer) {
            observer.disconnect();
        }
    });

    return { headings, activeId };
}
