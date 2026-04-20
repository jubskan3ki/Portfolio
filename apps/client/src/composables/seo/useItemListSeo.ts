import { SITE_CONFIG } from './useSeo';

import type { ItemListSeoOptions } from '@/types/composables/seo';

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
