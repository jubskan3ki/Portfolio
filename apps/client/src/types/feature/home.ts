// Home Types

import type { Stack } from './stacks';

export type HomeVariant = 'light' | 'dark' | 'secondary' | 'primary';

// Props pour HeroSection
export interface HeroSectionProps {
    featuredStacks?: Stack[];
    bio?: string;
}

// Props pour ExpertiseCard
export interface ExpertiseCardProps {
    title: string;
    description: string;
    icon: string;
    color?: string;
    variant?: HomeVariant;
    animateOnScroll?: boolean;
}
