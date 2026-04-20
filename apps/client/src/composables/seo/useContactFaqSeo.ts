import { FAQ_ITEMS, useFaqPageSchema } from '@/composables/seo/useFaqSchema';
import { SITE_CONFIG } from '@/composables/seo/useSeo';

export { FAQ_ITEMS, HOME_FAQ_ITEMS, useFaqPageSchema } from '@/composables/seo/useFaqSchema';

export function useContactFaqSeo() {
    const contactUrl = `${SITE_CONFIG.url}/contact`;
    useFaqPageSchema(contactUrl, FAQ_ITEMS);
    return { items: FAQ_ITEMS };
}
