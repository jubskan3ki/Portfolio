import { ROUTES } from '@/config/routes';

import type { CtaLinks, FooterConfig, LegalLink, SocialLink } from '@/types/config/footer';

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

export const footerConfig: FooterConfig = {
    contactTitle: 'Contactez-moi',
    email: 'contact@aitaitaddajuba.fr',
    phone: '+33 6 95 21 71 97',
    address: 'Paris, France',

    companyName: 'Jubs_kan3ki',
    copyrightText: 'Tous droits réservés.',

    isAvailable: true,

    projectsCount: 42,
    yearsExperience: 4,
    techCount: 27,

    socialLinks,
    legalLinks,

    ctaLinks,
};

export type { CtaLinks };
