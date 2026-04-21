// Unified search API types | FTS PostgreSQL multi-entity

export interface UnifiedSearchItem {
    type: 'article' | 'project' | 'stack' | 'experience';
    id: number;
    slug: string;
    title: string;
    url: string;
    rank: number;
    snippet: string;
    metadata: Record<string, unknown>;
}

export interface UnifiedSearchResponse {
    data: UnifiedSearchItem[];
    pagination: {
        total?: number;
        page?: number;
        limit?: number;
        totalPages?: number;
        next?: string | null;
        previous?: string | null;
    };
}

export type UnifiedSearchType = 'all' | 'articles' | 'projects' | 'stacks' | 'experiences';

export interface UnifiedSearchParams {
    q: string;
    type?: UnifiedSearchType;
    page?: number;
    limit?: number;
}
