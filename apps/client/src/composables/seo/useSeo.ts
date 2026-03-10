import type { SeoOptions, SiteConfig } from '@/types/composables/seo';
import type { ArticleDetail } from '@/types/feature/blog';
import type { ProjectDetail } from '@/types/feature/project';
import type { StackDetail } from '@/types/feature/stacks';

// Configuration SEO centralisee
const SITE_CONFIG: SiteConfig = {
    name: 'Juba Ait-Adda',
    title: 'Juba Ait-Adda | Développeur Full-Stack & DevOps',
    url: 'https://juba-aitadda.dev',
    defaultImage: '/og-image.png',
    locale: 'fr_FR',
    twitterHandle: '@juba_aitadda',
    author: {
        name: 'Juba Ait-Adda',
        jobTitle: 'Développeur Full-Stack',
        email: 'contact@aitaddajuba.fr',
    },
};

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
        ogUrl: pageUrl,
        ogType: options.type || 'website',
        ogSiteName: SITE_CONFIG.name,
        ogLocale: SITE_CONFIG.locale,
        twitterCard: 'summary_large_image',
        twitterTitle: fullTitle,
        twitterDescription: options.description,
        twitterImage: imageUrl,
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
        link: [{ rel: 'canonical', href: pageUrl }],
    });
}

// SEO pour les articles avec Schema.org BlogPosting
export function useArticleSeo(article: ArticleDetail) {
    useSeo({
        title: article.title,
        description: article.excerpt,
        image: article.image,
        type: 'article',
        publishedTime: article.date,
        keywords: article.tags,
        author: SITE_CONFIG.author.name,
        url: `/blog/${article.slug}`,
    });

    // Schema.org BlogPosting - auto-importe par @nuxtjs/seo
    useSchemaOrg([
        defineArticle({
            '@type': 'BlogPosting',
            headline: article.title,
            description: article.excerpt,
            image: article.image,
            datePublished: article.date,
            dateModified: article.date,
            author: {
                '@type': 'Person',
                name: SITE_CONFIG.author.name,
                url: SITE_CONFIG.url,
            },
            wordCount: article.content?.join(' ').split(' ').length || 0,
        }),
    ]);
}

// SEO pour les projets avec Schema.org SoftwareApplication
export function useProjectSeo(project: ProjectDetail) {
    useSeo({
        title: project.title,
        description: project.description,
        image: project.image,
        type: 'website',
        keywords: project.technologies,
        url: `/projects/${project.slug}`,
    });

    useSchemaOrg([
        defineSoftwareApp({
            name: project.title,
            description: project.description,
            image: project.image,
            applicationCategory: 'DeveloperApplication',
            operatingSystem: 'Web',
            author: {
                '@type': 'Person',
                name: SITE_CONFIG.author.name,
            },
        }),
    ]);
}

// SEO pour les pages de technologies
export function useStackSeo(stack: StackDetail) {
    useSeo({
        title: `${stack.name} - Compétences`,
        description: stack.description,
        image: stack.logo,
        type: 'website',
        keywords: stack.tags,
        url: `/stacks/${stack.slug}`,
    });
}

// SEO pour la page d'accueil avec Schema.org Person + WebSite
export function useHomeSeo() {
    useSeo({
        title: SITE_CONFIG.title,
        description:
            'Portfolio de Juba Ait-Adda, développeur full-stack passionné spécialisé en Vue.js, React, Node.js, Python et DevOps.',
        keywords: ['développeur', 'full-stack', 'devops', 'vue.js', 'react', 'python', 'portfolio'],
        url: '/',
    });

    useSchemaOrg([
        definePerson({
            name: SITE_CONFIG.author.name,
            url: SITE_CONFIG.url,
            jobTitle: SITE_CONFIG.author.jobTitle,
            email: SITE_CONFIG.author.email,
            sameAs: ['https://github.com/jubskan3ki', 'https://www.linkedin.com/in/juba-aitadda/'],
            knowsAbout: ['Vue.js', 'React', 'TypeScript', 'Python', 'Django', 'Node.js', 'DevOps', 'Docker'],
        }),
        defineWebSite({
            name: SITE_CONFIG.name,
            url: SITE_CONFIG.url,
            description: 'Portfolio de Juba Ait-Adda, développeur full-stack et DevOps',
        }),
    ]);
}

// SEO pour la page contact
export function useContactSeo() {
    useSeo({
        title: 'Contact',
        description:
            'Contactez Juba Ait-Adda pour vos projets web. Développeur full-stack disponible pour missions freelance.',
        keywords: ['contact', 'freelance', 'développeur', 'projet', 'web', 'développement'],
        url: '/contact',
    });
}

// SEO pour la page experiences
export function useExperienceSeo() {
    useSeo({
        title: 'Mon Parcours',
        description: 'Parcours professionnel et académique de Juba Ait-Adda, développeur full-stack.',
        keywords: ['expérience', 'parcours', 'CV', 'formation', 'emploi', 'expériences professionnelles', 'expériences académiques', 'expériences d\'association'],
        url: '/experience',
    });
}

// SEO pour la page blog (liste)
export function useBlogSeo() {
    useSeo({
        title: 'Blog',
        description: 'Articles techniques sur le développement web, DevOps et bonnes pratiques.',
        keywords: ['blog', 'articles', 'développement', 'tutoriels', 'conseils', 'web'],
        url: '/blog',
    });
}

// SEO pour la page projets (liste)
export function useProjectsSeo() {
    useSeo({
        title: 'Projets',
        description: 'Mes réalisations et projets web : applications, sites, APIs.',
        keywords: ['projets', 'portfolio', 'réalisations', 'applications', 'sites'],
        url: '/projects',
    });
}

// SEO pour la page technologies (liste)
export function useStacksSeo() {
    useSeo({
        title: 'Stacks',
        description: 'Mes compétences techniques : frameworks, langages, outils DevOps.',
        keywords: ['Stacks', 'compétences', 'stack', 'frameworks', 'langages', 'outils', 'technologies'],
        url: '/stacks',
    });
}
