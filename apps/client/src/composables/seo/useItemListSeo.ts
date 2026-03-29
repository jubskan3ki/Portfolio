import { SITE_CONFIG } from './useSeo';

import type { Ref, ComputedRef } from 'vue';

interface ItemListItem {
    name: string;
    url: string;
    image?: string;
}

interface ItemListSeoOptions {
    items: Ref<ItemListItem[]> | ComputedRef<ItemListItem[]>;
}

/**
 * Ajoute un Schema.org ItemList sur les pages listing (blog, projets, stacks).
 * Google peut l'utiliser pour des resultats enrichis en carrousel.
 */
export function useItemListSeo(options: ItemListSeoOptions) {
    useSchemaOrg([
        defineItemList({
            itemListElement: options.items.value.map((item, index) => ({
                '@type': 'ListItem',
                position: index + 1,
                name: item.name,
                url: `${SITE_CONFIG.url}${item.url}`,
                ...(item.image && { image: item.image }),
            })),
        }),
    ]);
}
