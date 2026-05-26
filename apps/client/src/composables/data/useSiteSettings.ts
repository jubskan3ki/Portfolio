import { computed } from 'vue';

import { contactApi } from '@/services/api/modules/contact';

import type { SiteSettings } from '@/types/composables/data';
import type { ContactInfo } from '@/types/feature/contact';

const SITE_SETTINGS_KEY = 'site-settings';

export const DEFAULT_SETTINGS: SiteSettings = {
    email: 'contact@aitaddajuba.fr',
    phone: '+33 6 95 21 71 97',
    bio: 'Développeur fullstack et DevOps basé à Paris, spécialisé en Nuxt 3, Vue 3, TypeScript, Django/Python et infrastructure cloud.',
    addressCity: 'Paris',
    addressCountry: 'France',
    socialGithub: 'https://github.com/jubskan3ki',
    socialLinkedin: 'https://www.linkedin.com/in/juba-aitadda/',
    socialMedium: '',
    availabilityStatus: 'available',
    availabilityMessage: 'Ouvert aux opportunités CDI & missions freelance',
    isAvailable: true,
};

function toSettings(info: ContactInfo | null): SiteSettings {
    if (!info) {
        return { ...DEFAULT_SETTINGS };
    }
    const status = info.availability?.status ?? DEFAULT_SETTINGS.availabilityStatus;
    return {
        email: info.email || DEFAULT_SETTINGS.email,
        phone: info.phone || DEFAULT_SETTINGS.phone,
        bio: info.bio || DEFAULT_SETTINGS.bio,
        addressCity: info.address?.city || DEFAULT_SETTINGS.addressCity,
        addressCountry: info.address?.country || DEFAULT_SETTINGS.addressCountry,
        socialGithub: info.socialMedia?.github || DEFAULT_SETTINGS.socialGithub,
        socialLinkedin: info.socialMedia?.linkedin || DEFAULT_SETTINGS.socialLinkedin,
        socialMedium: info.socialMedia?.medium || DEFAULT_SETTINGS.socialMedium,
        availabilityStatus: status,
        availabilityMessage: info.availability?.message || DEFAULT_SETTINGS.availabilityMessage,
        isAvailable: status === 'available',
    };
}

export async function useSiteSettings(options: { lazy?: boolean } = {}) {
    const result = useAsyncData(SITE_SETTINGS_KEY, () => contactApi.getInfo(), {
        lazy: options.lazy ?? false,
        default: () => null,
        transform: (info: ContactInfo | null) => toSettings(info),
    });

    const { data, refresh, pending, error } = options.lazy ? result : await result;

    const settings = computed<SiteSettings>(() => data.value ?? { ...DEFAULT_SETTINGS });

    return { settings, refresh, pending, error };
}
