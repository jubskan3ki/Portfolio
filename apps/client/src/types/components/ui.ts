// Types for UI components

import type { ColorVariant, RouteObject } from './base';
import type { StatItem } from '../config/footer';

// Tooltip
type TooltipPosition = 'top' | 'bottom' | 'left' | 'right';

type TooltipTrigger = 'hover' | 'click' | 'focus';

type TooltipVariant = 'dark' | 'light' | 'primary';

export interface TooltipProps {
    content?: string;
    position?: TooltipPosition;
    trigger?: TooltipTrigger;
    delay?: number;
    variant?: TooltipVariant;
    offset?: number;
    customClass?: string;
}

// ProgressBar
export type ProgressSize = 'sm' | 'md' | 'lg';

export interface ProgressBarProps {
    value?: number;
    max?: number;
    label?: string;
    showPercentage?: boolean;
    showTextInside?: boolean;
    striped?: boolean;
    animated?: boolean;
    variant?: ColorVariant;
    size?: ProgressSize;
    steps?: number;
    customClass?: string;
}

// SectionHeading
export type HeadingSize = 'sm' | 'md' | 'lg';

export type TitleTag = 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6';

export interface SectionHeadingProps {
    title: string;
    titleTag?: TitleTag;
    size?: HeadingSize;
    icon?: string;
    noSeparator?: boolean;
    customClass?: string;
}

// Swiper
export interface SwiperProps {
    slides: number;
    slidesToShow?: number;
    slidesToScroll?: number;
    showControls?: boolean;
    showDots?: boolean;
    autoplay?: boolean;
    autoplayInterval?: number;
    infinite?: boolean;
    fullwidth?: boolean;
    height?: string | number;
    gap?: number;
}

// Hero
export type HeroVariant = 'light' | 'dark' | 'primary' | 'secondary';

export type HeroSize = 'compact' | 'default' | 'large';

export interface HeroProps {
    title: string;
    description?: string;
    variant?: HeroVariant;
    showTitleUnderline?: boolean;
    logo?: string;
    logoAlt?: string;
    hasMeta?: boolean;
    badge?: string;
    centered?: boolean;
    size?: HeroSize;
    showDots?: boolean;
    showOrbs?: boolean;
    showBottomFade?: boolean;
    animateDots?: boolean;
    parallaxIntensity?: number;
}

// StatCard
export type StatCardVariant = 'light' | 'dark' | 'primary' | 'secondary';

// CTA
export type CTAVariant = 'primary' | 'light' | 'dark' | 'secondary';

export interface CTAButtonConfig {
    show?: boolean;
    label?: string;
    to?: string;
    icon?: string;
}

// AppLogo
export type AppLogoSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl';

export interface AppLogoProps {
    src?: string;
    alt?: string;
    size?: AppLogoSize;
    dark?: boolean;
    linkTo?: string;
    priority?: boolean;
}

// PortfolioSummary
interface PortfolioCtaLink {
    label: string;
    url: string | RouteObject;
}

export interface PortfolioCtaLinks {
    primary: PortfolioCtaLink;
    secondary: PortfolioCtaLink;
}

export interface PortfolioSummaryProps {
    title?: string;
    description?: string;
    ctaLinks?: PortfolioCtaLinks;
    stats?: StatItem[];
}

// RatingStars
export interface RatingStarsProps {
    modelValue?: number;
    max?: number;
    size?: number;
    readonly?: boolean;
    precision?: number;
    showValue?: boolean;
    label?: string;
    starIcon?: string;
    customClass?: string;
}

// ContentCarousel
export interface CarouselItem {
    id: number | string;
}

export interface ContentCarouselProps {
    items: CarouselItem[];
    isLoading?: boolean;
    isError?: boolean;
    loadingLabel?: string;
    errorMessage?: string;
    emptyTitle?: string;
    emptyDescription?: string;
    slidesDesktop?: number;
    slidesTablet?: number;
    slidesMobile?: number;
    autoplay?: boolean;
    autoplayInterval?: number;
    gap?: number;
    showDots?: boolean;
}

// DateRangeSelector
export interface DateRange {
    startDate: string;
    endDate: string;
}

export interface DateRangeSelectorProps {
    availableDates?: string[];
    minDays?: number;
    maxDays?: number;
    disabled?: boolean;
}

export interface CalendarDay {
    day: number;
    date: string;
    isCurrentMonth: boolean;
    isAvailable: boolean;
    isDisabled: boolean;
    isSelected: boolean;
    isInRange: boolean;
    isRangeStart: boolean;
    isRangeEnd: boolean;
    isToday: boolean;
}

export interface DateRangeInputProps {
    displayValue: string;
    isOpen: boolean;
    disabled: boolean;
}

export interface DateRangeCalendarProps {
    currentMonthYear: string;
    weekDays: string[];
    calendarDays: CalendarDay[];
    isValidSelection: boolean;
}
