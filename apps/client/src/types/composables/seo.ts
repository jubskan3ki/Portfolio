// Types for SEO composables

export type SeoType = 'website' | 'article' | 'profile';

export interface SeoOptions {
    title: string;
    description: string;
    image?: string;
    url?: string;
    type?: SeoType;
    publishedTime?: string;
    modifiedTime?: string;
    author?: string;
    keywords?: string[];
    noindex?: boolean;
}

export interface SiteConfig {
    name: string;
    title: string;
    url: string;
    defaultImage: string;
    locale: string;
    twitterHandle: string;
    author: {
        name: string;
        jobTitle: string;
        email: string;
    };
}
