// types/feature/contact.ts

/**
 * Types pour les fonctionnalités de contact
 */

// Type pour une question fréquemment posée
export interface FAQ {
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
	recaptchaToken?: string;
}

// Type pour les champs du formulaire de contact
export interface ContactFormField {
	name: string;
	label: string;
	type: 'text' | 'email' | 'tel' | 'textarea' | 'select';
	placeholder?: string;
	required?: boolean;
	options?: { value: string; label: string }[];
	validation?: {
		pattern?: RegExp;
		minLength?: number;
		maxLength?: number;
		message?: string;
	};
}

// Type pour les informations de contact
export interface ContactInfo {
	email: string;
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
		status: 'available' | 'limited' | 'unavailable';
		message?: string;
	};
}

// Type pour la réponse de soumission du formulaire
export interface ContactSubmissionResponse {
	success: boolean;
	message: string;
	errors?: Record<string, string>;
	referenceId?: string;
}

// Type pour les statistiques de contact
export interface ContactStats {
	totalMessages: number;
	responseRate: number;
	averageResponseTime: string;
	popularSubjects: { subject: string; count: number }[];
}
