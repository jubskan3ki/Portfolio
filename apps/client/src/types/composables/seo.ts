// Types for SEO composables

import type { ComputedRef, Ref } from 'vue';

export type SeoType = 'website' | 'article' | 'profile';

export interface SeoOptions {
    title: string;
    description: string;
    image?: string;
    imageAlt?: string;
    url?: string;
    type?: SeoType;
    publishedTime?: string;
    modifiedTime?: string;
    author?: string;
    keywords?: string[];
    section?: string;
    tags?: string[];
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
        givenName: string;
        familyName: string;
        jobTitle: string;
        email: string;
        telephone: string;
        description: string;
        image: string;
        address: {
            addressLocality: string;
            addressCountry: string;
        };
    };
}

export interface PaginationSeoOptions {
    basePath: string;
    currentPage: Ref<number> | ComputedRef<number>;
    totalPages: Ref<number> | ComputedRef<number>;
}

// Breadcrumb SEO types

export interface BreadcrumbSeoItem {
    label: string;
    to: string;
    icon?: string;
}

export interface BreadcrumbSeoMeta {
    title?: string;
    category?: string;
    categoryPath?: string;
}

export interface BreadcrumbSeoOptions {
    meta?: BreadcrumbSeoMeta;
}

export interface BreadcrumbSeoReturn {
    items: ComputedRef<BreadcrumbSeoItem[]>;
}

// useItemListSeo

export interface ItemListItem {
    name: string;
    url: string;
    image?: string;
}

export interface ItemListSeoOptions {
    items: Ref<ItemListItem[]> | ComputedRef<ItemListItem[]>;
}
