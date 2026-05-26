import type { FaqItem } from '@/types/feature/contact';

export const FAQ_ITEMS: FaqItem[] = [
    {
        question: 'Quels types de missions acceptez-vous ?',
        answer:
            'Freelance et CDI, front-end Vue/React, back-end Python/Django ou Node, et DevOps ' +
            "(Docker, CI/CD). Je travaille en remote depuis Paris, et j'accepte les déplacements " +
            'ponctuels en Île-de-France.',
    },
    {
        question: 'Quelle est votre disponibilité ?',
        answer:
            'Je suis ouvert aux missions à temps plein à partir du mois suivant notre premier échange. ' +
            'Pour les projets courts (audit, POC, review), je peux me libérer sous 1 à 2 semaines.',
    },
    {
        question: 'Travaillez-vous sous NDA ?',
        answer:
            'Oui. Je signe volontiers un accord de confidentialité avant tout échange technique ' +
            "approfondi. Pour les portfolios privés, n'hésitez pas à me transmettre le NDA de votre choix.",
    },
    {
        question: 'Comment se déroule un premier échange ?',
        answer:
            "Un appel de 30 minutes pour cadrer les besoins, l'équipe, la stack et les contraintes. " +
            'Je reviens ensuite avec une proposition (chiffrée si pertinent) sous 48 heures ouvrées.',
    },
    {
        question: 'Quels sont vos tarifs ?',
        answer:
            "Le TJM dépend du scope, de la durée et de l'engagement. Je communique une fourchette " +
            'dès le premier échange pour éviter les pertes de temps. Pas de paiement en amont ; ' +
            'facturation mensuelle, à 30 jours.',
    },
    {
        question: 'Où suivre vos publications ?',
        answer:
            'Sur ce site via le blog et le flux Atom (/feed.xml), sur GitHub ' +
            '(github.com/jubskan3ki) pour le code public, et sur LinkedIn pour les posts longs.',
    },
];

// Subset optimisé pour l'intention recruteur sur la home (types de missions, dispo, process).
const HOME_FAQ_KEYS = new Set([
    'Quels types de missions acceptez-vous ?',
    'Quelle est votre disponibilité ?',
    'Comment se déroule un premier échange ?',
]);
export const HOME_FAQ_ITEMS: FaqItem[] = FAQ_ITEMS.filter((i) => HOME_FAQ_KEYS.has(i.question));

// Helper réutilisable : émet un nœud FAQPage JSON-LD pour n'importe quelle page.
export function useFaqPageSchema(pageUrl: string, items: FaqItem[], anchor = 'faq') {
    useSchemaOrg([
        defineWebPage({
            '@type': 'FAQPage',
            '@id': `${pageUrl}/#${anchor}`,
            name: 'FAQ - Juba Ait-Adda',
            url: pageUrl,
            mainEntity: items.map((item) => ({
                '@type': 'Question' as const,
                name: item.question,
                acceptedAnswer: {
                    '@type': 'Answer' as const,
                    text: item.answer,
                },
            })),
        }),
    ]);
}
