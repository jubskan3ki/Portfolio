import { computed } from 'vue';

import type { BreadcrumbSeoItem, BreadcrumbSeoOptions, BreadcrumbSeoReturn } from '@/types/composables/seo';

const ROUTE_LABELS: Record<string, string> = {
    '/': 'Accueil',
    '/blog': 'Blog',
    '/projects': 'Projets',
    '/stacks': 'Stacks',
    '/contact': 'À propos & Contact',
    '/experience': 'Mon Parcours',
};

const SITE_URL = 'https://juba-aitadda.dev';

export function useBreadcrumbSeo(options?: BreadcrumbSeoOptions): BreadcrumbSeoReturn {
    const route = useRoute();

    const items = computed<BreadcrumbSeoItem[]>(() => {
        const path = route.path;
        const crumbs: BreadcrumbSeoItem[] = [];
        const meta = options?.meta;

        crumbs.push({ label: ROUTE_LABELS['/'] ?? 'Accueil', to: '/' });

        if (path === '/') {
            return crumbs;
        }

        const segments = path.split('/').filter(Boolean);
        const sectionPath = `/${segments[0]}`;
        const sectionLabel = ROUTE_LABELS[sectionPath];

        if (sectionLabel) {
            crumbs.push({ label: sectionLabel, to: sectionPath });
        }

        if (segments.length >= 2 && meta) {
            if (meta.category) {
                const categoryTo = meta.categoryPath || `${sectionPath}?category=${encodeURIComponent(meta.category)}`;
                crumbs.push({ label: meta.category, to: categoryTo });
            }

            if (meta.title) {
                crumbs.push({ label: meta.title, to: path });
            }
        }

        return crumbs;
    });

    useSchemaOrg([
        defineBreadcrumb({
            itemListElement: items.value.map((item, index) => ({
                '@type': 'ListItem' as const,
                position: index + 1,
                name: item.label,
                item: `${SITE_URL}${item.to}`,
            })),
        }),
    ]);

    return { items };
}
