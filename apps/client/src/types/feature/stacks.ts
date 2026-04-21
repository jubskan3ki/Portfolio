import type { PaginatedResponse } from '@/types/api/common';
import type { Ref } from 'vue';

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

export interface StackDetail extends Stack {
    description: string;
    isFeatured?: boolean;
    seoTitle?: string;
    metaDescription?: string;
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

export interface StackCategory {
    id: number;
    name: string;
    description: string;
    icon?: string;
    count: number;
}

export interface StackResource {
    id: number;
    title: string;
    description: string;
    url: string;
    type: StackResourceType;
    isFeatured: boolean;
}

export type StackResourceType = 'documentation' | 'tutorial' | 'article' | 'video' | 'other';

export interface RelatedStack {
    name: string;
    logo: string;
    slug: string;
    category: string;
    relationship: StackRelationship;
}

export type StackRelationship = 'alternative' | 'complementary' | 'dependency' | 'similarTo';

export interface StackStats {
    totalStacks: number;
    stacksByCategory: Array<{ category: string; count: number }>;
    averageProficiency: number;
    topStacks: Array<{ name: string; level: number }>;
    yearsOfExperience: Array<{ name: string; years: number }>;
}

export type StacksResponse = PaginatedResponse<Stack>;

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

export interface StackCardProps {
    stack: Stack;
    hoverable?: boolean;
    flat?: boolean;
    compact?: boolean;
    descriptionLength?: number;
    customClass?: string;
}

interface StackFilterOption {
    label: string;
    value: string;
}

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

export interface StackCarouselProps {
    limit?: number;
    autoplay?: boolean;
}

// Light entry for StackBadge | minimal fields the caller is expected to pass.
export interface StackBadgeStack {
    id: string | number;
    name: string;
    logo?: string;
    icon?: string;
    color?: string;
    level?: number;
    category?: string;
}

export interface StackBadgeProps {
    stack: StackBadgeStack;
    size?: 'small' | 'medium' | 'large';
    showName?: boolean;
    showLevel?: boolean;
    clickable?: boolean;
    customClass?: string;
}

// Light entry for StackRelated | the sidebar accepts entries without the canonical `relationship`.
export interface StackRelatedEntry {
    name: string;
    logo: string;
    slug: string;
    category: string;
}

export interface StackRelatedProps {
    stacks?: StackRelatedEntry[];
}

// Light resource entry for the StackResources sidebar.
export interface StackResourceEntry {
    title: string;
    description: string;
    url: string;
}

export interface StackResourcesProps {
    resources?: StackResourceEntry[];
}

export interface StackTagsProps {
    tags?: string[];
}

export interface StackCategorySliderProps {
    label: string;
    icon: string;
    stacks: Stack[];
}

export interface UseStacksPageOptions {
    stacksData: Ref<{ data: Stack[] } | undefined>;
    categoriesData: Ref<unknown>;
    statsData: Ref<{ totalStacks?: number; averageProficiency?: number } | undefined>;
    stacksLoading: Ref<boolean>;
    categoriesLoading: Ref<boolean>;
    stacksError: Ref<boolean>;
    categoriesError: Ref<boolean>;
    activeCategory: Ref<string>;
    searchQuery: Ref<string>;
    isSearchMode: Ref<boolean>;
}
