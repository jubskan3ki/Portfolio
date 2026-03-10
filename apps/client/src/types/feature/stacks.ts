import type { PaginatedResponse } from '@/types/api/common';

// Stack Types

// Type pour une stack technique (liste)
export interface Stack {
    id: number;
    name: string;
    slug: string;
    logo: string;
    category: string;
    description?: string;
    tags: string[];
    experience: number;
    startedDate?: string;
    level: number;
}

// Type pour une stack technique (detail)
export interface StackDetail extends Stack {
    description: string;
    isFeatured?: boolean;
    website?: string;
    websiteLabel?: string;
    github?: string;
    githubLabel?: string;
    firstRelease?: string;
    license?: string;
    content?: string;
    resources: StackResource[];
    relatedStacks: RelatedStack[];
    createdAt: string;
    updatedAt: string;
}

// Type pour une categorie de stack technique
export interface StackCategory {
    id: number;
    name: string;
    description: string;
    icon?: string;
    count: number;
}

// Type pour une ressource de stack
export interface StackResource {
    id: number;
    title: string;
    description: string;
    url: string;
    type: StackResourceType;
    isFeatured: boolean;
}

export type StackResourceType = 'documentation' | 'tutorial' | 'article' | 'video' | 'other';

// Type pour une stack associee
export interface RelatedStack {
    name: string;
    logo: string;
    slug: string;
    category: string;
    relationship: StackRelationship;
}

export type StackRelationship = 'alternative' | 'complementary' | 'dependency' | 'similarTo';

// Type pour les statistiques de stacks
export interface StackStats {
    totalStacks: number;
    stacksByCategory: Array<{ category: string; count: number }>;
    averageProficiency: number;
    topStacks: Array<{ name: string; level: number }>;
    yearsOfExperience: Array<{ name: string; years: number }>;
}

// API Response Types

export type StacksResponse = PaginatedResponse<Stack>;

// API Request Types (Create/Update)

export interface StackCreateData {
    name: string;
    slug?: string;
    logo?: string;
    category: string | number;
    description?: string;
    tags?: string[];
    startedDate?: string;
    level?: number;
    website?: string;
    github?: string;
    firstRelease?: string;
    license?: string;
    content?: string;
}

export type StackUpdateData = Partial<StackCreateData>;

export interface StackCategoryCreateData {
    name: string;
    description?: string;
    icon?: string;
}

export type StackCategoryUpdateData = Partial<StackCategoryCreateData>;

export interface StackResourceCreateData {
    title: string;
    description?: string;
    url: string;
    type: StackResourceType;
    stack: number | string;
    isFeatured?: boolean;
}

export type StackResourceUpdateData = Partial<StackResourceCreateData>;

export interface StackResourceFilters {
    stack_id?: number;
    stack_slug?: string;
    type?: string;
}

// Props pour StackCard
export interface StackCardProps {
    stack: Stack;
    hoverable?: boolean;
    flat?: boolean;
    compact?: boolean;
    descriptionLength?: number;
    customClass?: string;
}

// Filter option pour StackList
interface StackFilterOption {
    label: string;
    value: string;
}

// Props pour StackList
export interface StackListProps {
    stacks?: Stack[];
    title?: string;
    description?: string;
    displayMode?: 'grid' | 'list' | 'badges';
    showFilters?: boolean;
    categoryFilters?: StackFilterOption[];
    filterLabel?: string;
    allFilterLabel?: string;
    loading?: boolean;
    error?: string;
    retryable?: boolean;
    retryText?: string;
    loadingText?: string;
    emptyTitle?: string;
    emptyDescription?: string;
    badgeSize?: 'small' | 'medium' | 'large';
    showStackName?: boolean;
    showStackLevel?: boolean;
    clickableItems?: boolean;
    cardHoverable?: boolean;
    cardFlat?: boolean;
    cardBordered?: boolean;
    descriptionLength?: number;
    customClass?: string;
}

// Props pour StackCarousel
export interface StackCarouselProps {
    limit?: number;
    autoplay?: boolean;
}
