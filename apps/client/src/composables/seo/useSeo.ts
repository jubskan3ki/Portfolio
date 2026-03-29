import type { SeoOptions, SiteConfig } from '@/types/composables/seo';
import type { ArticleDetail } from '@/types/feature/blog';
import type { ProjectDetail } from '@/types/feature/project';
import type { StackDetail } from '@/types/feature/stacks';

// Configuration SEO centralisee
export const SITE_CONFIG: SiteConfig = {
    name: 'Juba Ait-Adda',
    title: 'Juba Ait-Adda | Développeur Full-Stack & DevOps',
    url: 'https://juba-aitadda.dev',
    defaultImage: '/og-image.png',
    locale: 'fr_FR',
    twitterHandle: '@juba_aitadda',
    author: {
        name: 'Juba Ait-Adda',
        givenName: 'Juba',
        familyName: 'Ait-Adda',
        jobTitle: 'Développeur Full-Stack',
        email: 'contact@aitaddajuba.fr',
        telephone: '+33695217197',
        description:
            'Développeur full-stack et DevOps basé à Paris, spécialisé en Vue.js, React, Python/Django et infrastructure cloud.',
        image: 'https://juba-aitadda.dev/images/profile.jpg',
        address: {
            addressLocality: 'Paris',
            addressCountry: 'FR',
        },
    },
};

// Identifiant stable pour la reconciliation d'entite Person sur toutes les pages
export const PERSON_ID = `${SITE_CONFIG.url}/#person`;

// Reference auteur partagee — relie articles/projets a l'entite principale
export const AUTHOR_REF = {
    '@type': 'Person' as const,
    '@id': PERSON_ID,
    name: SITE_CONFIG.author.name,
    url: SITE_CONFIG.url,
};

// Extrait le nombre de mots depuis les blocs de contenu JSON
function extractWordCount(content: unknown): number {
    if (!content || !Array.isArray(content)) {
        return 0;
    }
    return content.reduce((count: number, block: Record<string, unknown>) => {
        const text = typeof block.content === 'string' ? block.content : '';
        const items = Array.isArray(block.items) ? block.items.join(' ') : '';
        return count + (`${text} ${items}`).split(/\s+/).filter(Boolean).length;
    }, 0);
}

// Composable SEO principal - utilise les auto-imports Nuxt
export function useSeo(options: SeoOptions) {
    const fullTitle = options.title.includes('|') ? options.title : `${options.title} | ${SITE_CONFIG.name}`;

    const imageUrl = options.image?.startsWith('http')
        ? options.image
        : `${SITE_CONFIG.url}${options.image || SITE_CONFIG.defaultImage}`;

    const pageUrl = options.url?.startsWith('http') ? options.url : `${SITE_CONFIG.url}${options.url || ''}`;

    // useSeoMeta auto-importe par Nuxt
    useSeoMeta({
        title: fullTitle,
        description: options.description,
        ogTitle: fullTitle,
        ogDescription: options.description,
        ogImage: imageUrl,
        ogImageWidth: 1200,
        ogImageHeight: 630,
        ogUrl: pageUrl,
        ogType: options.type || 'website',
        ogSiteName: SITE_CONFIG.name,
        ogLocale: SITE_CONFIG.locale,
        twitterCard: 'summary_large_image',
        twitterTitle: fullTitle,
        twitterDescription: options.description,
        twitterImage: imageUrl,
        twitterCreator: SITE_CONFIG.twitterHandle,
        ...(options.publishedTime && { articlePublishedTime: options.publishedTime }),
        ...(options.modifiedTime && { articleModifiedTime: options.modifiedTime }),
        ...(options.noindex && { robots: 'noindex, nofollow' }),
    });

    // useHead auto-importe par Nuxt
    useHead({
        title: fullTitle,
        meta: [
            ...(options.keywords?.length ? [{ name: 'keywords', content: options.keywords.join(', ') }] : []),
            { name: 'author', content: options.author || SITE_CONFIG.author.name },
        ],
        link: [{ rel: 'canonical', href: pageUrl, key: 'canonical' }],
    });
}

// SEO pour les articles avec Schema.org BlogPosting
export function useArticleSeo(article: ArticleDetail) {
    const seoTitle = article.seoTitle || article.title;
    const seoDescription = article.metaDescription || article.excerpt?.substring(0, 155);

    useSeo({
        title: seoTitle,
        description: seoDescription,
        image: article.image,
        type: 'article',
        publishedTime: article.date,
        modifiedTime: article.updatedAt || article.date,
        keywords: article.tags,
        author: SITE_CONFIG.author.name,
        url: `/blog/${article.slug}`,
    });

    defineOgImage({
        component: 'OgImageDefault',
        title: article.title,
        description: article.excerpt,
        category: article.category,
        readTime: article.readTime,
    } as Record<string, unknown>);

    const articleUrl = `${SITE_CONFIG.url}/blog/${article.slug}`;

    // Schema.org BlogPosting - auto-importe par @nuxtjs/seo
    useSchemaOrg([
        defineArticle({
            '@type': 'BlogPosting',
            '@id': `${articleUrl}/#article`,
            headline: article.title,
            description: article.excerpt,
            ...(article.image && {
                image: {
                    '@type': 'ImageObject',
                    url: article.image,
                    width: 1200,
                    height: 630,
                },
            }),
            datePublished: article.date,
            dateModified: article.updatedAt || article.date,
            author: AUTHOR_REF,
            publisher: AUTHOR_REF,
            mainEntityOfPage: {
                '@type': 'WebPage',
                '@id': articleUrl,
            },
            wordCount: extractWordCount(article.content),
            timeRequired: `PT${article.readTime}M`,
            articleSection: [article.category],
            inLanguage: 'fr-FR',
        }),
    ]);
}

// SEO pour les projets avec Schema.org SoftwareApplication
export function useProjectSeo(project: ProjectDetail) {
    const seoTitle = project.seoTitle || project.title;
    const seoDescription = project.metaDescription || project.description?.substring(0, 155);

    useSeo({
        title: seoTitle,
        description: seoDescription,
        image: project.image,
        type: 'website',
        keywords: project.technologies,
        url: `/projects/${project.slug}`,
    });

    defineOgImage({
        component: 'OgImageDefault',
        title: project.title,
        description: project.description,
        category: project.category,
    } as Record<string, unknown>);

    useSchemaOrg([
        defineSoftwareApp({
            '@id': `${SITE_CONFIG.url}/projects/${project.slug}/#software`,
            name: project.title,
            description: project.description,
            ...(project.image && {
                image: {
                    '@type': 'ImageObject',
                    url: project.image,
                    width: 1200,
                    height: 630,
                },
            }),
            applicationCategory: 'DeveloperApplication',
            operatingSystem: 'Web',
            author: { ...AUTHOR_REF, url: SITE_CONFIG.url },
            inLanguage: 'fr-FR',
        }),
    ]);
}

// SEO pour les pages de technologies avec Schema.org TechArticle
export function useStackSeo(stack: StackDetail) {
    const seoTitle = stack.seoTitle || `${stack.name} - Compétences`;
    const seoDescription = stack.metaDescription || stack.description?.substring(0, 155);

    useSeo({
        title: seoTitle,
        description: seoDescription,
        image: stack.logo,
        type: 'website',
        keywords: stack.tags,
        url: `/stacks/${stack.slug}`,
    });

    defineOgImage({
        component: 'OgImageDefault',
        title: stack.name,
        description: stack.description,
    } as Record<string, unknown>);

    // Mapper le niveau numerique vers un libelle de competence
    const proficiencyMap: Record<string, string> = {
        1: 'Beginner', 1.5: 'Beginner', 2: 'Beginner',
        2.5: 'Intermediate', 3: 'Intermediate',
        3.5: 'Advanced', 4: 'Advanced',
        4.5: 'Expert', 5: 'Expert',
    };
    const proficiency = proficiencyMap[String(stack.level)] || 'Intermediate';

    useSchemaOrg([
        defineArticle({
            '@type': 'TechArticle',
            '@id': `${SITE_CONFIG.url}/stacks/${stack.slug}/#techarticle`,
            headline: `${stack.name} - Compétences techniques`,
            description: stack.description,
            ...(stack.logo && { image: stack.logo }),
            author: AUTHOR_REF,
            proficiencyLevel: proficiency,
            ...(stack.updatedAt && { dateModified: stack.updatedAt }),
            ...(stack.website && {
                about: {
                    '@type': 'SoftwareApplication' as const,
                    name: stack.name,
                    url: stack.website,
                } as unknown as string,
            }),
        }),
    ]);
}

// SEO pour la page d'accueil avec Schema.org Person + ProfilePage + WebSite
export function useHomeSeo() {
    useSeo({
        title: SITE_CONFIG.title,
        description:
            'Portfolio de Juba Ait-Adda, développeur full-stack passionné spécialisé en Vue.js, React, Node.js, Python et DevOps.',
        keywords: ['développeur', 'full-stack', 'devops', 'vue.js', 'react', 'python', 'portfolio'],
        url: '/',
    });

    const { author } = SITE_CONFIG;

    useSchemaOrg([
        defineWebPage({
            '@type': 'ProfilePage',
            '@id': `${SITE_CONFIG.url}/#profilepage`,
            name: `${author.name} - Portfolio`,
            description:
                'Portfolio de Juba Ait-Adda, développeur full-stack et DevOps',
            mainEntity: { '@id': PERSON_ID },
        }),
        definePerson({
            '@id': PERSON_ID,
            name: author.name,
            givenName: author.givenName,
            familyName: author.familyName,
            url: SITE_CONFIG.url,
            jobTitle: author.jobTitle,
            description: author.description,
            email: author.email,
            telephone: author.telephone,
            image: {
                '@type': 'ImageObject',
                '@id': `${SITE_CONFIG.url}/#personimage`,
                url: author.image,
                contentUrl: author.image,
                caption: `${author.name} - ${author.jobTitle}`,
            },
            address: {
                '@type': 'PostalAddress',
                addressLocality: author.address.addressLocality,
                addressCountry: author.address.addressCountry,
            },
            nationality: { '@type': 'Country', name: 'France' },
            sameAs: [
                'https://github.com/jubskan3ki',
                'https://www.linkedin.com/in/juba-aitadda/',
                'https://x.com/juba_aitadda',
            ],
            knowsAbout: [
                'Vue.js', 'React', 'TypeScript', 'Python', 'Django',
                'Node.js', 'DevOps', 'Docker', 'Kubernetes', 'Go',
            ],
            knowsLanguage: ['fr', 'en'],
            hasOccupation: {
                '@type': 'Occupation',
                name: 'Développeur Full-Stack',
                occupationLocation: { '@type': 'City', name: 'Paris' },
                skills: 'Vue.js, React, TypeScript, Python, Django, Node.js, Docker, Kubernetes',
            },
        }),
        defineWebSite({
            '@id': `${SITE_CONFIG.url}/#website`,
            name: SITE_CONFIG.name,
            url: SITE_CONFIG.url,
            description: 'Portfolio de Juba Ait-Adda, développeur full-stack et DevOps',
            publisher: { '@id': PERSON_ID },
            potentialAction: {
                '@type': 'SearchAction',
                target: [{
                    '@type': 'EntryPoint',
                    urlTemplate: `${SITE_CONFIG.url}/blog?search={search_term_string}`,
                }],
                'query-input': 'required name=search_term_string',
            },
        }),
    ]);
}

// SEO pour la page contact + about fusionnee avec Schema.org ContactPage + AboutPage + Person
export function useContactSeo() {
    useSeo({
        title: 'À propos & Contact',
        description:
            'Découvrez le parcours de Juba Ait-Adda, développeur full-stack et DevOps à Paris. Contactez-le pour vos projets web.',
        type: 'profile',
        keywords: ['contact', 'à propos', 'freelance', 'développeur', 'full-stack', 'devops', 'paris', 'portfolio'],
        url: '/contact',
    });

    const { author } = SITE_CONFIG;

    useSchemaOrg([
        defineWebPage({
            '@type': ['ContactPage', 'AboutPage'],
            '@id': `${SITE_CONFIG.url}/contact/#page`,
            name: 'À propos & Contact - Juba Ait-Adda',
            description: 'Découvrez le parcours de Juba Ait-Adda et contactez-le pour vos projets web.',
            mainEntity: { '@id': PERSON_ID },
        }),
        definePerson({
            '@id': PERSON_ID,
            name: author.name,
            givenName: author.givenName,
            familyName: author.familyName,
            url: SITE_CONFIG.url,
            jobTitle: author.jobTitle,
            description: author.description,
            email: author.email,
            telephone: author.telephone,
            image: author.image,
            address: {
                '@type': 'PostalAddress',
                addressLocality: author.address.addressLocality,
                addressCountry: author.address.addressCountry,
            },
            sameAs: [
                'https://github.com/jubskan3ki',
                'https://www.linkedin.com/in/juba-aitadda/',
                'https://x.com/juba_aitadda',
            ],
            knowsAbout: [
                'Vue.js', 'React', 'TypeScript', 'Python', 'Django',
                'Node.js', 'DevOps', 'Docker', 'Kubernetes', 'Go',
            ],
            knowsLanguage: ['fr', 'en'],
        }),
    ]);
}

// SEO pour la page experiences avec Schema.org ProfilePage
export function useExperienceSeo() {
    useSeo({
        title: 'Mon Parcours',
        description: 'Parcours professionnel et académique de Juba Ait-Adda, développeur full-stack.',
        keywords: ['expérience', 'parcours', 'CV', 'formation', 'emploi', 'expériences professionnelles', 'expériences académiques', 'expériences d\'association'],
        url: '/experience',
    });

    useSchemaOrg([
        defineWebPage({
            '@type': 'ProfilePage',
            '@id': `${SITE_CONFIG.url}/experience/#profilepage`,
            name: 'Parcours - Juba Ait-Adda',
            mainEntity: { '@id': PERSON_ID },
        }),
    ]);
}

// SEO pour la page blog (liste) avec Schema.org CollectionPage
export function useBlogSeo() {
    useSeo({
        title: 'Blog',
        description: 'Articles techniques sur le développement web, DevOps et bonnes pratiques.',
        keywords: ['blog', 'articles', 'développement', 'tutoriels', 'conseils', 'web'],
        url: '/blog',
    });

    useSchemaOrg([
        defineWebPage({
            '@type': 'CollectionPage',
            '@id': `${SITE_CONFIG.url}/blog/#collectionpage`,
            name: 'Blog - Juba Ait-Adda',
            description: 'Articles techniques sur le développement web, DevOps et bonnes pratiques.',
        }),
    ]);
}

// SEO pour la page projets (liste) avec Schema.org CollectionPage
export function useProjectsSeo() {
    useSeo({
        title: 'Projets',
        description: 'Mes réalisations et projets web : applications, sites, APIs.',
        keywords: ['projets', 'portfolio', 'réalisations', 'applications', 'sites'],
        url: '/projects',
    });

    useSchemaOrg([
        defineWebPage({
            '@type': 'CollectionPage',
            '@id': `${SITE_CONFIG.url}/projects/#collectionpage`,
            name: 'Projets - Juba Ait-Adda',
            description: 'Mes réalisations et projets web : applications, sites, APIs.',
        }),
    ]);
}

// SEO pour la page technologies (liste) avec Schema.org CollectionPage
export function useStacksSeo() {
    useSeo({
        title: 'Stacks',
        description: 'Mes compétences techniques : frameworks, langages, outils DevOps.',
        keywords: ['Stacks', 'compétences', 'stack', 'frameworks', 'langages', 'outils', 'technologies'],
        url: '/stacks',
    });

    useSchemaOrg([
        defineWebPage({
            '@type': 'CollectionPage',
            '@id': `${SITE_CONFIG.url}/stacks/#collectionpage`,
            name: 'Stacks - Juba Ait-Adda',
            description: 'Mes compétences techniques : frameworks, langages, outils DevOps.',
        }),
    ]);
}

// SEO pour la page a propos avec Schema.org AboutPage
export function useAboutSeo() {
    useSeo({
        title: 'À propos de Juba Ait-Adda',
        description:
            'Développeur full-stack et DevOps basé à Paris. Découvrez mon parcours, mes compétences et ma vision du développement web.',
        type: 'profile',
        keywords: ['juba ait-adda', 'développeur', 'full-stack', 'devops', 'paris', 'portfolio', 'à propos'],
        url: '/about',
    });

    const { author } = SITE_CONFIG;

    useSchemaOrg([
        defineWebPage({
            '@type': 'AboutPage',
            '@id': `${SITE_CONFIG.url}/about/#aboutpage`,
            name: 'À propos de Juba Ait-Adda',
            description:
                'Développeur full-stack et DevOps basé à Paris. Découvrez mon parcours, mes compétences et ma vision du développement web.',
            mainEntity: { '@id': PERSON_ID },
        }),
        definePerson({
            '@id': PERSON_ID,
            name: author.name,
            givenName: author.givenName,
            familyName: author.familyName,
            url: SITE_CONFIG.url,
            jobTitle: author.jobTitle,
            description: author.description,
            email: author.email,
            telephone: author.telephone,
            image: author.image,
            address: {
                '@type': 'PostalAddress',
                addressLocality: author.address.addressLocality,
                addressCountry: author.address.addressCountry,
            },
            sameAs: [
                'https://github.com/jubskan3ki',
                'https://www.linkedin.com/in/juba-aitadda/',
                'https://x.com/juba_aitadda',
            ],
            knowsAbout: [
                'Vue.js', 'React', 'TypeScript', 'Python', 'Django',
                'Node.js', 'DevOps', 'Docker', 'Kubernetes', 'Go',
            ],
            knowsLanguage: ['fr', 'en'],
        }),
    ]);
}
