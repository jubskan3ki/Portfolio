// src/config/constants.ts
// Constantes globales de l'application

/**
 * Délais et timeouts (en ms)
 */
export const TIMEOUTS = {
    /** Délai par défaut des alertes auto-close */
    ALERT_DEFAULT: 5000,
    /** Délai animation fermeture modal */
    MODAL_CLOSE_ANIMATION: 300,
    /** Délai debounce recherche */
    SEARCH_DEBOUNCE: 300,
    /** Délai avant affichage loader */
    LOADER_DELAY: 200,
    /** Délai autoplay carousel */
    CAROUSEL_AUTOPLAY: 5000,
    /** Délai refresh token */
    TOKEN_REFRESH: 4 * 60 * 1000, // 4 minutes
    /** Throttle pour le scroll (~60fps) */
    SCROLL_THROTTLE: 16,
} as const;

/**
 * Breakpoints responsive (en px)
 * Aligned with SCSS _spacing.scss for consistency
 *
 * Device ranges:
 * - Mobile: 0 - 767px
 * - Tablet: 768px - 1023px
 * - Desktop: 1024px - 1279px
 * - Wide: 1280px+
 */
export const BREAKPOINTS = {
    // Tailwind-like generic sizes
    XS: 320,
    SM: 640,
    MD: 768,
    LG: 1024,
    XL: 1280,
    XXL: 1536,
    // Semantic breakpoints (min-width values for JS usage)
    // Use these with: windowWidth >= BREAKPOINTS.TABLET
    MOBILE: 767, // Use: width <= MOBILE for mobile
    TABLET: 768, // Use: width >= TABLET for tablet+
    TABLET_MAX: 1023, // Use: width <= TABLET_MAX for tablet
    DESKTOP: 1024, // Use: width >= DESKTOP for desktop+
    DESKTOP_MAX: 1279, // Use: width <= DESKTOP_MAX for desktop
    WIDE: 1280, // Use: width >= WIDE for wide screens
} as const;

/**
 * Seuils de scroll (en px)
 */
export const SCROLL_THRESHOLDS = {
    /** Seuil pour afficher le bouton "retour en haut" */
    SHOW_SCROLL_TOP: 400,
    /** Seuil pour considérer la page comme scrollée */
    IS_SCROLLED: 50,
    /** Seuil pour cacher/afficher le header au scroll */
    HIDE_HEADER: 200,
} as const;

/**
 * Limites de texte
 */
export const TEXT_LIMITS = {
    /** Longueur max excerpt article */
    ARTICLE_EXCERPT: 150,
    /** Longueur max description projet */
    PROJECT_DESCRIPTION: 200,
    /** Longueur max description stack */
    STACK_DESCRIPTION: 100,
    /** Longueur max titre card */
    CARD_TITLE: 50,
} as const;

/**
 * Clés de localStorage
 */
export const STORAGE_KEYS = {
    SIDEBAR_COLLAPSED: 'sidebar_collapsed',
    ADMIN_SIDEBAR_COLLAPSED: 'admin_sidebar_collapsed',
    THEME: 'theme',
    LANGUAGE: 'language',
} as const;

/**
 * API retry configuration
 */
export const API_RETRY = {
    /** Nombre de tentatives */
    MAX_RETRIES: 3,
    /** Délai initial entre les tentatives (ms) */
    INITIAL_DELAY: 1000,
    /** Multiplicateur pour backoff exponentiel */
    BACKOFF_MULTIPLIER: 2,
    /** Délai maximum entre tentatives (ms) */
    MAX_DELAY: 30000,
} as const;

/**
 * Pagination
 */
export const PAGINATION = {
    DEFAULT_PAGE_SIZE: 10,
} as const;

/**
 * Types d'activités admin (icônes et labels)
 */
export const ACTIVITY_TYPE_ICONS: Record<string, string> = {
    message: 'mail',
    article: 'file-text',
    project: 'folder',
    stack: 'layers',
    experience: 'briefcase',
};

export const ACTIVITY_TYPE_LABELS: Record<string, string> = {
    message: 'Message',
    article: 'Article',
    project: 'Projet',
    stack: 'Stack',
    experience: 'Experience',
};

export const ACTIVITY_TYPE_OPTIONS = [
    { value: 'message', label: 'Messages' },
    { value: 'article', label: 'Articles' },
    { value: 'project', label: 'Projets' },
    { value: 'stack', label: 'Stacks' },
    { value: 'experience', label: 'Expériences' },
] as const;

export const ACTIVITY_PERIOD_OPTIONS = [
    { value: 'all', label: 'Tout' },
    { value: 'today', label: 'Aujourd\'hui' },
    { value: 'week', label: 'Cette semaine' },
    { value: 'month', label: 'Ce mois' },
] as const;

// Types exports
export type Breakpoint = keyof typeof BREAKPOINTS;
export type StorageKey = keyof typeof STORAGE_KEYS;
