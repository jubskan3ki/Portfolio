// src/config/footer.ts
import { ROUTES } from '@/config/routes';

import type { CtaLinks, FooterConfig, LegalLink, SocialLink } from '@/types/config/footer';

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

// Données pour les liens légaux (chemins directs pour éviter les problèmes de résolution)
const legalLinks: LegalLink[] = [
    {
        label: 'Mentions légales',
        url: '/legal',
    },
    {
        label: 'Politique de confidentialité',
        url: '/privacy',
    },
    {
        label: 'Conditions d\'utilisation',
        url: '/terms',
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

    // Appels à l'action
    ctaLinks,
};

// Exports pour utilisation dans le reste de l'application
export type { CtaLinks };
