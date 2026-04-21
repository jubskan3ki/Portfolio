import type { ContactAvailabilityStatus } from '@/types/feature/contact';
import type { ComputedRef, Ref } from 'vue';

// useViewRecording

export interface UseViewRecordingReturn {
    viewRecorded: Ref<boolean>;
}

// useDetailSlug

export interface UseDetailSlugReturn {
    slug: ComputedRef<string>;
}

// useSiteSettings

export interface SiteSettings {
    email: string;
    phone: string;
    bio: string;
    addressCity: string;
    addressCountry: string;
    socialGithub: string;
    socialLinkedin: string;
    socialMedium: string;
    availabilityStatus: ContactAvailabilityStatus;
    availabilityMessage: string;
    isAvailable: boolean;
}
