import { computed } from 'vue';

import { contactApi } from '@/services/api/modules/contact';

import type { SiteSettings } from '@/types/composables/data';
import type { ContactInfo } from '@/types/feature/contact';

const SITE_SETTINGS_KEY = 'site-settings';

const EMPTY_SETTINGS: SiteSettings = {
    email: '',
    phone: '',
    bio: '',
    addressCity: '',
    addressCountry: '',
    socialGithub: '',
    socialLinkedin: '',
    socialTwitter: '',
    socialMedium: '',
    availabilityStatus: 'unavailable',
    availabilityMessage: '',
    isAvailable: false,
};

function toSettings(info: ContactInfo | null): SiteSettings {
    if (!info) {
        return { ...EMPTY_SETTINGS };
    }
    const status = info.availability?.status ?? 'unavailable';
    return {
        email: info.email ?? '',
        phone: info.phone ?? '',
        bio: info.bio ?? '',
        addressCity: info.address?.city ?? '',
        addressCountry: info.address?.country ?? '',
        socialGithub: info.socialMedia?.github ?? '',
        socialLinkedin: info.socialMedia?.linkedin ?? '',
        socialTwitter: info.socialMedia?.twitter ?? '',
        socialMedium: info.socialMedia?.medium ?? '',
        availabilityStatus: status,
        availabilityMessage: info.availability?.message ?? '',
        isAvailable: status === 'available',
    };
}

export async function useSiteSettings() {
    const { data, refresh, pending, error } = await useAsyncData(
        SITE_SETTINGS_KEY,
        () => contactApi.getInfo(),
        {
            default: () => null,
            transform: (info: ContactInfo | null) => toSettings(info),
        },
    );

    const settings = computed<SiteSettings>(() => data.value ?? { ...EMPTY_SETTINGS });

    return { settings, refresh, pending, error };
}
