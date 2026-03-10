// Cache time constants for TanStack Query (in milliseconds)
export const CACHE_TIMES = {
    // Static data (categories, tags, types)
    STATIC: 30 * 60 * 1000, // 30 min

    // List data (articles, projects)
    LIST: 2 * 60 * 1000, // 2 min

    // Detail data (single item)
    DETAIL: 5 * 60 * 1000, // 5 min

    // Real-time data (stats, sessions)
    REALTIME: 30 * 1000, // 30 sec
} as const;
