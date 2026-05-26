import type { StatCardVariant } from '@/types/components/ui';
import type { Stack } from './stacks';

export type HomeVariant = 'light' | 'dark' | 'secondary' | 'primary';

export type HeroStack = Pick<Stack, 'id' | 'name' | 'logo' | 'level'>;

export interface HeroSectionProps {
    featuredStacks?: HeroStack[];
    bio?: string;
}

export interface ExpertiseCardProps {
    title: string;
    description: string;
    icon: string;
    color?: string;
    variant?: HomeVariant;
    animateOnScroll?: boolean;
    to?: string;
    prefetch?: boolean;
}

export interface StatCardProps {
    value: number | string;
    label: string;
    icon: string;
    variant?: StatCardVariant;
    suffix?: string;
    duration?: number;
}
