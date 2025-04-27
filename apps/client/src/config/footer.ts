// src/config/footer.ts
import { ROUTES } from '@/config/routes';
import type { CtaLinks, FooterConfig, LegalLink, SocialLink, StatItem } from '@/types/config/footer';

// Données pour les réseaux sociaux
const socialLinks: SocialLink[] = [
	{
		name: 'GitHub',
		icon: 'github',
		url: 'https://github.com/jubskan3ki',
	},
	{
		name: 'LinkedIn',
		icon: 'linkedin',
		url: 'https://www.linkedin.com/in/juba-aitadda/',
	},
];

// Données pour les liens légaux
const legalLinks: LegalLink[] = [
	{
		label: 'Mentions légales',
		url: ROUTES.LEGAL,
	},
	{
		label: 'Politique de confidentialité',
		url: ROUTES.PRIVACY,
	},
	{
		label: "Conditions d'utilisation",
		url: ROUTES.TERMS,
	},
];

// Données pour les statistiques
const stats: StatItem[] = [
	{
		value: 9,
		label: 'Projets réalisés',
	},
	{
		value: 4,
		label: "Années d'expérience",
	},
	{
		value: 38,
		label: 'Technologies maîtrisées',
	},
];

// Données pour les appels à l'action
const ctaLinks: CtaLinks = {
	primary: {
		label: 'Discutons de votre projet',
		url: ROUTES.CONTACT,
	},
	secondary: {
		label: 'Voir mes réalisations',
		url: ROUTES.PROJECTS,
	},
};

// Configuration complète du footer
export const footerConfig: FooterConfig = {
	// Informations de contact
	contactTitle: 'Contactez-moi',
	email: 'contact@aitaitaddajuba.fr',
	phone: '+33 6 95 21 71 97',
	address: 'Paris, France',

	// Informations de l'entreprise
	companyName: 'Jubs_kan3ki',
	copyrightText: 'Tous droits réservés.',

	// Disponibilité et statut
	isAvailable: true,

	// Statistiques
	projectsCount: 42,
	yearsExperience: 4,
	techCount: 27,

	// Réseaux sociaux et liens légaux
	socialLinks,
	legalLinks,

	// Appels à l'action et statistiques
	ctaLinks,
	stats,
};

// Exports pour utilisation dans le reste de l'application
export { ctaLinks, legalLinks, socialLinks, stats };
export type { CtaLinks, LegalLink, SocialLink, StatItem };
