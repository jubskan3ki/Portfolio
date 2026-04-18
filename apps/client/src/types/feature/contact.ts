// Contact Types

// Type pour une question frequemment posee
export interface FAQ {
    id: number;
    question: string;
    answer: string;
    isPublished: boolean;
    order: number;
}

// Lightweight static FAQ item (front-only, emitted in FAQPage JSON-LD)
export interface FaqItem {
    question: string;
    answer: string;
}

// Type pour le formulaire de contact
export interface ContactForm {
    name: string;
    email: string;
    subject: string;
    message: string;
    phone?: string;
    company?: string;
}

// Type pour la reponse de soumission de contact
export interface ContactResponse {
    success: boolean;
    message: string;
    referenceId: string;
}

// Type pour les informations de contact
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
        twitter: string;
        medium: string;
    };
    availability: {
        status: ContactAvailabilityStatus;
        message: string;
    };
}

export type ContactAvailabilityStatus = 'available' | 'limited' | 'unavailable';

// Type pour les statistiques de contact
export interface ContactStats {
    totalMessages: number;
    responseRate: number;
    averageResponseTime: string;
    popularSubjects: Array<{ subject: string; count: number }>;
}

// Admin Types

// Contact message type (admin)
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

// API Request Types (Create/Update)

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
    address?: {
        street?: string;
        city?: string;
        zipCode?: string;
        country?: string;
    };
    socialMedia?: {
        linkedin?: string;
        github?: string;
        twitter?: string;
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

// Props pour ContactForm (component)
export interface ContactFormProps {
    title?: string;
    subtitle?: string;
    customClass?: string;
    formId?: string;
}
