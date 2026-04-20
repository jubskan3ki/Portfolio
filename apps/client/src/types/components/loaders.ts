// Types for Loader components

// Spinner
export type SpinnerSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl';

export type SpinnerType = 'circle' | 'dots';

export interface SpinnerProps {
    type?: SpinnerType;
    size?: SpinnerSize;
    label?: string;
    showLabel?: boolean;
}

// LoadingState
export type LoadingStateSize = 'sm' | 'md' | 'lg';

export interface LoadingStateProps {
    message?: string;
    size?: LoadingStateSize;
    spinnerSize?: SpinnerSize;
}

// Skeleton
export type SkeletonType = 'block' | 'circle' | 'text' | 'image' | 'button' | 'avatar';
export type SkeletonAnimation = 'pulse' | 'wave' | 'none';

export interface SkeletonProps {
    type?: SkeletonType;
    width?: string | number;
    height?: string | number;
    radius?: string | number;
    animate?: boolean;
    animation?: SkeletonAnimation;
}

// SkeletonCard
export type SkeletonCardVariant = 'article' | 'project' | 'stack' | 'experience' | 'default';

export interface SkeletonCardProps {
    variant?: SkeletonCardVariant;
    showImage?: boolean;
    showAvatar?: boolean;
    showDescription?: boolean;
    showTags?: boolean;
    showFooter?: boolean;
    imageHeight?: string;
    titleHeight?: string;
    descriptionLines?: number;
}

// SkeletonList
export type SkeletonListLayout = 'grid' | 'list';

export interface SkeletonListProps {
    count?: number;
    layout?: SkeletonListLayout;
    columns?: number;
    variant?: SkeletonCardVariant;
    showImage?: boolean;
    showAvatar?: boolean;
    showDescription?: boolean;
    showTags?: boolean;
    showFooter?: boolean;
}
