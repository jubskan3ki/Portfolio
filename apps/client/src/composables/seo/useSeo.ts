import { useBreadcrumbSeo } from '@/composables/seo/useBreadcrumbSeo';

import type { SeoOptions, SiteConfig } from '@/types/composables/seo';
import type { ArticleDetail } from '@/types/feature/blog';
import type { ProjectDetail } from '@/types/feature/project';
import type { StackDetail } from '@/types/feature/stacks';

export const SITE_CONFIG: SiteConfig = {
    name: 'Juba Ait-Adda',
    title: 'Juba Ait-Adda | Dev Fullstack | CDI & Freelance',
    url: 'https://juba-aitadda.dev',
    defaultImage: '/og-image.png',
    locale: 'fr_FR',
    author: {
        name: 'Juba Ait-Adda',
        givenName: 'Juba',
        familyName: 'Ait-Adda',
        jobTitle: 'Développeur Fullstack & DevOps',
        email: 'contact@aitaddajuba.fr',
        telephone: '+33695217197',
        description:
            'Développeur fullstack et DevOps basé à Paris, spécialisé en Nuxt 3, Vue 3, TypeScript, Django/Python et infrastructure cloud.',
        image: 'https://juba-aitadda.dev/images/profile.jpg',
        address: {
            addressLocality: 'Paris',
            addressCountry: 'FR',
        },
    },
};

const KNOWS_ABOUT = [
    'Nuxt 3',
    'Vue 3',
    'TypeScript',
    'JavaScript',
    'Django',
    'Python',
    'Node.js',
    'Go',
    'Docker',
    'Docker Compose',
    'Kubernetes',
    'PostgreSQL',
    'Redis',
    'CI/CD',
    'GitHub Actions',
    'Ansible',
    'Grafana',
    'Prometheus',
    'Loki',
    'DevOps',
];

const SAME_AS = ['https://github.com/jubskan3ki', 'https://www.linkedin.com/in/juba-aitadda/'];

// ISO date YYYY-MM-DD, évaluée au rendu SSR pour garder JobPosting / seeks frais.
function today(): string {
    return new Date().toISOString().substring(0, 10);
}

function inSixMonths(): string {
    return new Date(Date.now() + 6 * 30 * 24 * 3600 * 1000).toISOString().substring(0, 10);
}

// Stable @id shared across pages so Schema.org graph reconciles Person references.
export const PERSON_ID = `${SITE_CONFIG.url}/#person`;

export const AUTHOR_REF = {
    '@type': 'Person' as const,
    '@id': PERSON_ID,
    name: SITE_CONFIG.author.name,
    url: SITE_CONFIG.url,
};

// Satori (nuxt-og-image) fetches images server-side; relative paths fail to resolve across envs.
function absoluteImage(url?: string | null): string | undefined {
    if (!url) {
        return undefined;
    }
    if (url.startsWith('http://') || url.startsWith('https://')) {
        return url;
    }
    return undefined;
}

function extractWordCount(content: unknown): number {
    if (!content || !Array.isArray(content)) {
        return 0;
    }
    return content.reduce((count: number, block: Record<string, unknown>) => {
        const text = typeof block.content === 'string' ? block.content : '';
        const items = Array.isArray(block.items) ? block.items.join(' ') : '';
        return count + `${text} ${items}`.split(/\s+/).filter(Boolean).length;
    }, 0);
}

export function useSeo(options: SeoOptions) {
    const fullTitle = options.title.includes('|') ? options.title : `${options.title} | ${SITE_CONFIG.name}`;

    const imageUrl = options.image?.startsWith('http')
        ? options.image
        : `${SITE_CONFIG.url}${options.image || SITE_CONFIG.defaultImage}`;

    const pageUrl = options.url?.startsWith('http') ? options.url : `${SITE_CONFIG.url}${options.url || ''}`;

    const imageAlt = options.imageAlt || `${options.title} | ${SITE_CONFIG.name}`;

    useSeoMeta({
        title: fullTitle,
        description: options.description,
        ogTitle: fullTitle,
        ogDescription: options.description,
        ogImage: imageUrl,
        ogImageAlt: imageAlt,
        ogImageType: 'image/png',
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
        twitterImageAlt: imageAlt,
        ...(options.publishedTime && { articlePublishedTime: options.publishedTime }),
        ...(options.modifiedTime && { articleModifiedTime: options.modifiedTime }),
        ...(options.author && { articleAuthor: [options.author] }),
        ...(options.section && { articleSection: options.section }),
        ...(options.tags?.length && { articleTag: options.tags }),
        ...(options.noindex && { robots: 'noindex, nofollow' }),
    });

    useHead({
        title: fullTitle,
        meta: [
            ...(options.keywords?.length ? [{ name: 'keywords', content: options.keywords.join(', ') }] : []),
            { name: 'author', content: options.author || SITE_CONFIG.author.name },
        ],
        link: [{ rel: 'canonical', href: pageUrl, key: 'canonical' }],
    });
}

export function useArticleSeo(article: ArticleDetail) {
    const seoTitle = article.seoTitle || article.title;
    const seoDescription = article.metaDescription || article.excerpt?.substring(0, 155);

    useSeo({
        title: seoTitle,
        description: seoDescription,
        image: article.image,
        imageAlt: article.title,
        type: 'article',
        publishedTime: article.date,
        modifiedTime: article.updatedAt || article.date,
        keywords: article.tags,
        author: SITE_CONFIG.author.name,
        section: article.category,
        tags: article.tags,
        url: `/blog/${article.slug}`,
    });

    defineOgImage({
        component: 'OgImageArticle',
        title: article.title,
        description: article.excerpt,
        image: absoluteImage(article.image),
        category: article.category,
        readTime: article.readTime,
    } as Record<string, unknown>);

    const articleUrl = `${SITE_CONFIG.url}/blog/${article.slug}`;

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

export function useProjectSeo(project: ProjectDetail) {
    const seoTitle = project.seoTitle || project.title;
    const seoDescription = project.metaDescription || project.description?.substring(0, 155);
    const projectUrl = `${SITE_CONFIG.url}/projects/${project.slug}`;

    useSeo({
        title: seoTitle,
        description: seoDescription,
        image: project.image,
        imageAlt: `${project.title} | projet ${project.category}`,
        type: 'website',
        keywords: project.technologies,
        tags: project.technologies,
        url: `/projects/${project.slug}`,
    });

    defineOgImage({
        component: 'OgImageProject',
        title: project.title,
        description: project.description,
        image: absoluteImage(project.image),
        category: project.category,
        technologies: project.technologies,
    } as Record<string, unknown>);

    useSchemaOrg([
        defineSoftwareApp({
            '@id': `${projectUrl}/#software`,
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
        ...(project.links?.github
            ? [
                  {
                      '@type': 'SoftwareSourceCode' as const,
                      '@id': `${projectUrl}/#code`,
                      name: project.title,
                      codeRepository: project.links.github,
                      programmingLanguage: project.technologies,
                      author: AUTHOR_REF,
                      inLanguage: 'fr-FR',
                  },
              ]
            : []),
        {
            '@type': 'CreativeWork' as const,
            '@id': `${projectUrl}/#creative`,
            name: project.title,
            description: project.description,
            creator: AUTHOR_REF,
            inLanguage: 'fr-FR',
            ...(project.date && { dateCreated: project.date }),
            ...(project.updatedAt && { dateModified: project.updatedAt }),
        },
    ]);
}

export function useStackSeo(stack: StackDetail) {
    const seoTitle = stack.seoTitle || `${stack.name} - Compétences`;
    const seoDescription = stack.metaDescription || stack.description?.substring(0, 155);

    useSeo({
        title: seoTitle,
        description: seoDescription,
        image: stack.logo,
        imageAlt: `${stack.name} | compétence technique`,
        type: 'website',
        keywords: stack.tags,
        url: `/stacks/${stack.slug}`,
    });

    defineOgImage({
        component: 'OgImageStack',
        name: stack.name,
        description: stack.description,
        logo: absoluteImage(stack.logo),
        level: stack.level,
    } as Record<string, unknown>);

    const proficiencyMap: Record<string, string> = {
        1: 'Beginner',
        1.5: 'Beginner',
        2: 'Beginner',
        2.5: 'Intermediate',
        3: 'Intermediate',
        3.5: 'Advanced',
        4: 'Advanced',
        4.5: 'Expert',
        5: 'Expert',
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

export function useHomeSeo() {
    useSeo({
        title: SITE_CONFIG.title,
        description:
            'Développeur fullstack & DevOps à Paris. Nuxt 3, Vue, TypeScript, Django, Docker. Ouvert aux missions CDI et freelance. Échangeons sous 48h.',
        keywords: [
            'développeur fullstack',
            'freelance',
            'CDI',
            'paris',
            'remote',
            'nuxt 3',
            'vue 3',
            'typescript',
            'django',
            'python',
            'docker',
            'devops',
        ],
        url: '/',
    });

    const { author } = SITE_CONFIG;

    useSchemaOrg([
        defineWebPage({
            '@type': 'ProfilePage',
            '@id': `${SITE_CONFIG.url}/#profilepage`,
            name: `${author.name} - Portfolio`,
            description: 'Portfolio de Juba Ait-Adda, développeur fullstack & DevOps ouvert CDI et freelance.',
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
            workLocation: {
                '@type': 'Place',
                name: 'Paris, Île-de-France (remote-first)',
                address: {
                    '@type': 'PostalAddress',
                    addressLocality: 'Paris',
                    addressCountry: 'FR',
                },
            },
            nationality: { '@type': 'Country', name: 'France' },
            sameAs: SAME_AS,
            knowsAbout: KNOWS_ABOUT,
            knowsLanguage: ['fr', 'en'],
            hasOccupation: {
                '@type': 'Occupation',
                name: 'Développeur Fullstack & DevOps',
                occupationLocation: { '@type': 'City', name: 'Paris' },
                skills: 'Nuxt 3, Vue 3, TypeScript, Django, Python, Docker, PostgreSQL, CI/CD, Ansible, Grafana',
            },
            seeks: {
                '@type': 'Demand',
                name: 'CDI ou mission freelance fullstack',
                availability: 'InStock',
                availabilityStarts: today(),
                areaServed: { '@type': 'Country', name: 'France' },
                eligibleRegion: { '@type': 'Place', name: 'Île-de-France / Remote' },
                itemOffered: {
                    '@type': 'Service',
                    name: 'Développement fullstack Nuxt/Django & DevOps',
                    serviceType: ['Développement fullstack', 'Intégration frontend', 'API backend', 'DevOps / Infra'],
                },
            },
        } as Record<string, unknown>),
        defineWebSite({
            '@id': `${SITE_CONFIG.url}/#website`,
            name: SITE_CONFIG.name,
            url: SITE_CONFIG.url,
            description: 'Portfolio de Juba Ait-Adda, développeur fullstack & DevOps ouvert CDI et freelance.',
            inLanguage: 'fr-FR',
            publisher: { '@id': PERSON_ID },
            potentialAction: {
                '@type': 'SearchAction',
                target: [
                    {
                        '@type': 'EntryPoint',
                        urlTemplate: `${SITE_CONFIG.url}/blog?search={search_term_string}`,
                    },
                ],
                'query-input': 'required name=search_term_string',
            },
        }),
    ]);
}

export function useContactSeo() {
    useSeo({
        title: 'Me recruter | Juba Ait-Adda, Dev Fullstack Paris',
        description:
            'Recrutez Juba Ait-Adda, développeur fullstack & DevOps à Paris. Disponible en CDI ou freelance. Réponse sous 48 heures ouvrées.',
        type: 'profile',
        keywords: [
            'recruter',
            'contact',
            'freelance',
            'CDI',
            'développeur fullstack',
            'devops',
            'paris',
            'remote',
            'nuxt',
            'vue',
            'django',
            'python',
            'docker',
        ],
        url: '/contact',
    });

    const { author } = SITE_CONFIG;
    const contactUrl = `${SITE_CONFIG.url}/contact`;

    useSchemaOrg([
        defineWebPage({
            '@type': ['ContactPage', 'AboutPage'],
            '@id': `${contactUrl}/#page`,
            name: 'Me recruter | Juba Ait-Adda',
            description: 'Développeur fullstack & DevOps à Paris, ouvert CDI et freelance. Contact direct.',
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
            sameAs: SAME_AS,
            knowsAbout: KNOWS_ABOUT,
            knowsLanguage: ['fr', 'en'],
        }),
        {
            '@type': 'JobPosting' as const,
            '@id': `${contactUrl}/#jobposting`,
            title: 'Développeur Fullstack Nuxt/Django | ouvert CDI & Freelance',
            description:
                'Juba Ait-Adda, développeur fullstack & DevOps à Paris, est ouvert aux missions freelance et aux opportunités CDI. ' +
                'Stack Nuxt 3, Vue 3, TypeScript, Django, Python, Docker. Remote-first, déplacements Île-de-France.',
            datePosted: today(),
            validThrough: inSixMonths(),
            employmentType: ['FULL_TIME', 'CONTRACTOR', 'PART_TIME'],
            hiringOrganization: { '@id': PERSON_ID },
            jobLocation: {
                '@type': 'Place',
                address: {
                    '@type': 'PostalAddress',
                    addressLocality: 'Paris',
                    addressRegion: 'Île-de-France',
                    addressCountry: 'FR',
                },
            },
            jobLocationType: 'TELECOMMUTE',
            applicantLocationRequirements: { '@type': 'Country', name: 'France' },
            directApply: true,
            url: contactUrl,
            skills: 'Nuxt 3, Vue 3, TypeScript, Django, Python, Node.js, Docker, PostgreSQL, CI/CD, Ansible, Grafana',
        },
    ]);

    useBreadcrumbSeo();
}

export function useExperienceSeo() {
    useSeo({
        title: 'Mon parcours | Dev Fullstack & DevOps à Paris',
        description:
            'Parcours professionnel, formations et projets associatifs de Juba Ait-Adda, développeur fullstack basé à Paris.',
        keywords: ['expérience', 'parcours', 'CV', 'formation', 'emploi', 'développeur fullstack', 'paris'],
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

    useBreadcrumbSeo();
}

export function useBlogSeo() {
    useSeo({
        title: 'Blog | Dev web, DevOps & bonnes pratiques',
        description:
            "Articles techniques sur Nuxt, Vue, Django, Docker, CI/CD et DevOps par Juba Ait-Adda, dev fullstack à Paris. Retours d'expérience terrain.",
        keywords: ['blog', 'articles', 'nuxt', 'vue', 'django', 'docker', 'devops', 'ci/cd'],
        url: '/blog',
    });

    useSchemaOrg([
        defineWebPage({
            '@type': 'CollectionPage',
            '@id': `${SITE_CONFIG.url}/blog/#collectionpage`,
            name: 'Blog - Juba Ait-Adda',
            description: 'Articles techniques sur Nuxt, Vue, Django, Docker, CI/CD et DevOps.',
            inLanguage: 'fr-FR',
            isPartOf: { '@id': `${SITE_CONFIG.url}/#website` },
        }),
    ]);

    useBreadcrumbSeo();
}

export function useProjectsSeo() {
    useSeo({
        title: 'Projets | Portfolio Fullstack Nuxt, Django, Docker',
        description:
            'Sélection de projets fullstack : applications Nuxt 3, APIs Django, plateformes DevOps. Code source public sur GitHub, démos live.',
        keywords: ['projets', 'portfolio', 'réalisations', 'nuxt 3', 'django', 'docker', 'fullstack', 'github'],
        url: '/projects',
    });

    useSchemaOrg([
        defineWebPage({
            '@type': 'CollectionPage',
            '@id': `${SITE_CONFIG.url}/projects/#collectionpage`,
            name: 'Projets - Juba Ait-Adda',
            description: 'Applications Nuxt 3, APIs Django, plateformes DevOps. Code et démos publics.',
            inLanguage: 'fr-FR',
            isPartOf: { '@id': `${SITE_CONFIG.url}/#website` },
        }),
    ]);

    useBreadcrumbSeo();
}

export function useStacksSeo() {
    useSeo({
        title: 'Stacks | Nuxt, Vue, Django, Docker, CI/CD',
        description:
            'Mes compétences techniques détaillées : frontend Nuxt/Vue, backend Django/Python, DevOps Docker/Ansible/Grafana/Prometheus.',
        keywords: [
            'stacks',
            'compétences',
            'technologies',
            'nuxt',
            'vue',
            'django',
            'docker',
            'ansible',
            'grafana',
            'prometheus',
        ],
        url: '/stacks',
    });

    useSchemaOrg([
        defineWebPage({
            '@type': 'CollectionPage',
            '@id': `${SITE_CONFIG.url}/stacks/#collectionpage`,
            name: 'Stacks - Juba Ait-Adda',
            description: 'Frontend Nuxt/Vue, backend Django/Python, DevOps Docker/Ansible/Grafana.',
            inLanguage: 'fr-FR',
            isPartOf: { '@id': `${SITE_CONFIG.url}/#website` },
        }),
    ]);

    useBreadcrumbSeo();
}
