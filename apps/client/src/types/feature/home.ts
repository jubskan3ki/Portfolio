// Home Types

import type { Stack } from './stacks';

export type HomeVariant = 'light' | 'dark' | 'secondary' | 'primary';

/** Minimal stack fields needed by the hero badges */
export type HeroStack = Pick<Stack, 'id' | 'name' | 'logo' | 'level'>;

// Props pour HeroSection
export interface HeroSectionProps {
    featuredStacks?: HeroStack[];
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
    to?: string;
}
