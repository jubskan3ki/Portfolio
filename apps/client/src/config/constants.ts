export const TIMEOUTS = {
    ALERT_DEFAULT: 5000,
    MODAL_CLOSE_ANIMATION: 300,
    SEARCH_DEBOUNCE: 300,
    LOADER_DELAY: 200,
    CAROUSEL_AUTOPLAY: 5000,
    TOKEN_REFRESH: 4 * 60 * 1000,
    SCROLL_THROTTLE: 16,
} as const;

export const BREAKPOINTS = {
    XS: 320,
    SM: 640,
    MD: 768,
    LG: 1024,
    XL: 1280,
    XXL: 1536,
    MOBILE: 767,
    TABLET: 768,
    TABLET_MAX: 1023,
    DESKTOP: 1024,
    DESKTOP_MAX: 1279,
    WIDE: 1280,
} as const;

export const SCROLL_THRESHOLDS = {
    SHOW_SCROLL_TOP: 400,
    IS_SCROLLED: 50,
    HIDE_HEADER: 200,
} as const;

export const TEXT_LIMITS = {
    ARTICLE_EXCERPT: 150,
    PROJECT_DESCRIPTION: 200,
    STACK_DESCRIPTION: 100,
    CARD_TITLE: 50,
} as const;

export const STORAGE_KEYS = {
    SIDEBAR_COLLAPSED: 'sidebar_collapsed',
    ADMIN_SIDEBAR_COLLAPSED: 'admin_sidebar_collapsed',
    THEME: 'theme',
    LANGUAGE: 'language',
} as const;

export const API_RETRY = {
    MAX_RETRIES: 3,
    INITIAL_DELAY: 1000,
    BACKOFF_MULTIPLIER: 2,
    MAX_DELAY: 30000,
} as const;

export const PAGINATION = {
    DEFAULT_PAGE_SIZE: 10,
} as const;

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
    { value: 'today', label: "Aujourd'hui" },
    { value: 'week', label: 'Cette semaine' },
    { value: 'month', label: 'Ce mois' },
] as const;

export type Breakpoint = keyof typeof BREAKPOINTS;
export type StorageKey = keyof typeof STORAGE_KEYS;
