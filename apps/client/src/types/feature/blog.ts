import type { ArticleBase, CategoryBase, TagBase } from './admin';
import type { PaginationData } from '@/types/api/common';

export type ContentBlockType = 'paragraph' | 'heading' | 'blockquote' | 'image' | 'code' | 'list' | 'table';

export interface ParagraphBlock {
    type: 'paragraph';
    content: string;
}

export interface HeadingBlock {
    type: 'heading';
    content: string;
    level: 2 | 3 | 4;
}

export interface BlockquoteBlock {
    type: 'blockquote';
    content: string;
    cite?: string;
}

export interface ImageBlock {
    type: 'image';
    src: string;
    alt: string;
    caption?: string;
}

export interface CodeBlock {
    type: 'code';
    content: string;
    language?: string;
}

export interface ListBlock {
    type: 'list';
    items: string[];
    ordered: boolean;
}

export interface TableBlock {
    type: 'table';
    headers: string[];
    rows: string[][];
}

export type ContentBlock
    = | ParagraphBlock
        | HeadingBlock
        | BlockquoteBlock
        | ImageBlock
        | CodeBlock
        | ListBlock
        | TableBlock;

export type InlineNode
    = | { type: 'text'; content: string }
        | { type: 'strong'; children: InlineNode[] }
        | { type: 'em'; children: InlineNode[] }
        | { type: 'code'; content: string }
        | { type: 'link'; url: string; children: InlineNode[] };

export interface ArticlesResponse {
    data: Article[];
    pagination: PaginationData;
}

export interface ArticleCreateData {
    title: string;
    content: ContentBlock[] | string[];
    excerpt: string;
    image?: string;
    category: string | number;
    tags?: string[];
    published?: boolean;
}

export interface ArticleUpdateData extends Partial<ArticleCreateData> {
    slug?: string;
}

export interface CategoryCreateData {
    name: string;
    slug?: string;
    description?: string;
}

export type CategoryUpdateData = Partial<CategoryCreateData>;

export interface TagCreateData {
    name: string;
}

export type TagUpdateData = Partial<TagCreateData>;

export interface Article extends ArticleBase {
    excerpt: string;
    image: string;
    category: string;
    tags: string[];
    date: string;
    updatedAt?: string;
    readTime: number;
    views: number;
}

export interface ArticleDetail extends Article {
    content: ContentBlock[];
    isPublished?: boolean;
    seoTitle?: string;
    metaDescription?: string;
}

export interface Category extends CategoryBase {
    count: number;
}

export interface Tag extends TagBase {
    count: number;
    view_count?: number;
}

export interface ArticleCardProps {
    article: Article;
    hoverable?: boolean;
    flat?: boolean;
    excerptLength?: number;
    customClass?: string;
    showTags?: boolean;
    maxTags?: number;
    eager?: boolean;
}

export interface ArticleCarouselProps {
    articles: Article[] | readonly Article[];
    title?: string;
    subtitle?: string;
    limit?: number;
    showFooter?: boolean;
    showStats?: boolean;
    showDots?: boolean;
    autoplay?: boolean;
    autoplaySpeed?: number;
    excerptLength?: number;
    isLoading?: boolean;
    error?: string | null;
    category?: string;
}

export interface ArticleListProps {
    articles?: Article[];
    title?: string;
    description?: string;
    layout?: 'grid' | 'list' | 'compact';
    loading?: boolean;
    error?: string;
    retryable?: boolean;
    retryText?: string;
    loadingText?: string;
    emptyTitle?: string;
    emptyDescription?: string;
    currentPage?: number;
    totalPages?: number;
    showPagination?: boolean;
    cardHoverable?: boolean;
    cardFlat?: boolean;
    cardBordered?: boolean;
    excerptLength?: number;
    showFooter?: boolean;
    showStats?: boolean;
    readMoreText?: string;
    customClass?: string;
    prefersReducedMotion?: boolean;
}

export interface ArticleCategoryItem {
    id: string | number;
    name: string;
    count?: number;
    slug?: string;
}

export interface ArticleCategoriesProps {
    title?: string;
    categories?: ArticleCategoryItem[];
    modelValue?: string | number | ArticleCategoryItem | null;
    maxVisible?: number;
}

export interface ArticleTagsProps {
    title?: string;
    tags?: string[] | Tag[];
    modelValue?: Array<string | number>;
    display?: 'cloud' | 'simple';
    multiSelect?: boolean;
    maxVisible?: number;
}

// ArticleActiveFilters

export interface ArticleActiveFiltersProps {
    title?: string;
    activeCategory?: string | number | Category | null;
    activeTags?: Array<string | number>;
    categories?: Category[];
    tags?: Tag[];
    clearButtonText?: string;
}

// ArticlePopular

export interface PopularArticle {
    id: string | number;
    slug: string;
    title: string;
    image?: string;
    date: string;
    readTime?: number;
    views?: number;
}

export interface ArticlePopularProps {
    articles?: PopularArticle[];
    title?: string;
    showTitle?: boolean;
}
