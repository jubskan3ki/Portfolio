export interface FAQ {
    id: number;
    question: string;
    answer: string;
    isPublished: boolean;
    order: number;
}

// FAQ statique front-only (émis dans FAQPage JSON-LD)
export interface FaqItem {
    question: string;
    answer: string;
}

export interface ContactForm {
    name: string;
    email: string;
    subject: string;
    message: string;
    phone?: string;
    company?: string;
}

export interface ContactResponse {
    success: boolean;
    message: string;
    referenceId: string;
}

export interface ContactInfo {
    id: number;
    email: string;
    phone: string;
    bio?: string;
    address: {
        street: string;
        city: string;
        zipCode: string;
        country: string;
    };
    socialMedia: {
        linkedin: string;
        github: string;
        medium: string;
    };
    availability: {
        status: ContactAvailabilityStatus;
        message: string;
    };
}

export type ContactAvailabilityStatus = 'available' | 'limited' | 'unavailable';

export interface ContactStats {
    totalMessages: number;
    responseRate: number;
    averageResponseTime: string;
    popularSubjects: Array<{ subject: string; count: number }>;
}

export interface ContactMessage {
    id: number;
    name: string;
    email: string;
    subject: string;
    message: string;
    phone?: string;
    company?: string;
    isRead: boolean;
    isArchived: boolean;
    createdAt: string;
    updatedAt: string;
}

export interface ContactMessagesFilters {
    page?: number;
    limit?: number;
    search?: string;
    isRead?: boolean;
    isArchived?: boolean;
}

export interface FAQCreateData {
    question: string;
    answer: string;
    isPublished?: boolean;
    order?: number;
}

export type FAQUpdateData = Partial<FAQCreateData>;

export interface ContactInfoCreateData {
    email?: string;
    phone?: string;
    is_primary?: boolean;
    address?: {
        street?: string;
        city?: string;
        zipCode?: string;
        country?: string;
    };
    socialMedia?: {
        linkedin?: string;
        github?: string;
        medium?: string;
    };
    availability?: {
        status?: ContactAvailabilityStatus;
        message?: string;
    };
}

export type ContactInfoUpdateData = Partial<ContactInfoCreateData>;

export interface ContactMessageUpdateData {
    isRead?: boolean;
    isArchived?: boolean;
}

export interface ContactFormProps {
    title?: string;
    subtitle?: string;
    customClass?: string;
    formId?: string;
}

// ContactInfos component

export interface ContactSocialLink {
    name: string;
    icon: string;
    url: string;
}

export interface ContactInfosProps {
    title?: string;
    subtitle?: string;
    addressTitle?: string;
    emailTitle?: string;
    phoneTitle?: string;
    socialTitle?: string;
    address?: string;
    email?: string;
    phone?: string;
    socialLinks?: ContactSocialLink[];
}
