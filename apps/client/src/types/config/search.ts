// Types pour la configuration de recherche

export type SearchResultType = 'article' | 'project' | 'stack' | 'experience';
export type SearchMode = 'public' | 'admin';

export interface SearchTypeConfig {
    label: string;
    icon: string;
    color: string;
}

export interface SearchResult {
    id: number | string;
    type: SearchResultType;
    title: string;
    subtitle?: string;
    slug?: string;
    icon: string;
    link: string;
}

export interface SearchResultGroup {
    type: SearchResultType;
    label: string;
    icon: string;
    color: string;
    results: SearchResult[];
}

// Global search result types from API responses
export interface ArticleSearchResult {
    id: number;
    title: string;
    slug: string;
    category?: { name: string } | string;
}

export interface ProjectSearchResult {
    id: number;
    title: string;
    slug: string;
    category?: { name: string } | string;
}

export interface StackSearchResult {
    id: number;
    name: string;
    slug: string;
    category?: { name: string } | string;
}

export interface ExperienceSearchResult {
    id: number;
    title: string;
    company: string;
    experience_type?: { name: string } | string;
}

export interface UseGlobalSearchOptions {
    mode?: SearchMode;
}

export interface SearchSourceConfig {
    key: string;
    type: SearchResultType;
    endpoint: string;
    mapItem: (item: Record<string, unknown>) => {
        title: string;
        subtitle?: string;
        slug?: string;
    };
}
