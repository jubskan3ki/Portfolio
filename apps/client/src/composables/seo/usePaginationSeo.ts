import { computed } from 'vue';

import { SITE_CONFIG } from './useSeo';

import type { PaginationSeoOptions } from '@/types/composables/seo';

export function usePaginationSeo({ basePath, currentPage, totalPages }: PaginationSeoOptions): void {
    const buildPageUrl = (page: number): string => {
        const path = page === 1 ? basePath : `${basePath}?page=${page}`;
        return `${SITE_CONFIG.url}${path}`;
    };

    const linkTags = computed(() => {
        const page = currentPage.value;
        const total = totalPages.value;
        const links: Array<{ rel: string; href: string; key?: string }> = [];

        links.push({
            rel: 'canonical',
            href: buildPageUrl(page),
            key: 'canonical',
        });

        if (page > 1) {
            links.push({
                rel: 'prev',
                href: buildPageUrl(page - 1),
            });
        }

        if (page < total) {
            links.push({
                rel: 'next',
                href: buildPageUrl(page + 1),
            });
        }

        return links;
    });

    useHead({
        link: linkTags,
    });
}
