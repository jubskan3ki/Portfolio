import type { ItemListSeoOptions } from '@/types/composables/seo';
import { SITE_CONFIG } from './useSeo';

export function useItemListSeo(options: ItemListSeoOptions) {
    useSchemaOrg([
        defineItemList({
            // Getter réactif : l'ItemList suit les changements de liste côté client (pagination/filtre).
            itemListElement: () =>
                options.items.value.map((item, index) => ({
                    '@type': 'ListItem',
                    position: index + 1,
                    name: item.name,
                    url: `${SITE_CONFIG.url}${item.url}`,
                    ...(item.image && { image: item.image }),
                })),
        }),
    ]);
}
