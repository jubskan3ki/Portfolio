// src/types/config/footer.ts

// Type pour les objets route
export interface RouteObject {
	path: string;
	name?: string;
}

export interface CtaLink {
	label: string;
	url: string | RouteObject;
}

export interface CtaLinks {
	primary: CtaLink;
	secondary: CtaLink;
}

export interface SocialLink {
	name: string;
	icon: string;
	url: string;
}

export interface LegalLink {
	label: string;
	url: string | RouteObject;
}

export interface StatItem {
	value: number;
	label: string;
}

export interface FooterConfig {
	// Informations de contact
	contactTitle: string;
	email: string;
	phone: string;
	address: string;

	// Informations de l'entreprise
	companyName: string;
	copyrightText: string;

	// Disponibilité et statut
	isAvailable: boolean;

	// Statistiques
	projectsCount: number;
	yearsExperience: number;
	techCount: number;

	// Réseaux sociaux et liens légaux
	socialLinks: SocialLink[];
	legalLinks: LegalLink[];

	// Appels à l'action et statistiques
	ctaLinks: CtaLinks;
	stats: StatItem[];
}
