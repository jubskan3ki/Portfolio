import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue';

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
    let pendingFrame: number | null = null;

    function teardown() {
        if (observer) {
            observer.disconnect();
            observer = null;
        }
    }

    function setupObserver() {
        teardown();
        if (!headings.value.length || typeof IntersectionObserver === 'undefined') {
            return;
        }

        if (pendingFrame !== null) {
            cancelAnimationFrame(pendingFrame);
        }
        pendingFrame = requestAnimationFrame(() => {
            pendingFrame = null;
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
        });
    }

    onMounted(() => {
        watch(headings, () => setupObserver(), { immediate: true });
    });

    onBeforeUnmount(() => {
        if (pendingFrame !== null) {
            cancelAnimationFrame(pendingFrame);
        }
        teardown();
    });

    return { headings, activeId };
}
