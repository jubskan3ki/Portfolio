// Configuration pour les opérations de transfert (import/export)

import type { ModuleInfo } from '@/types/composables/data';

// Query keys pour Vue Query
export const TRANSFER_QUERY_KEYS = {
    jobs: ['transfer', 'jobs'] as const,
    stats: ['transfer', 'stats'] as const,
};

// Configuration initiale des modules disponibles
export const TRANSFER_MODULES: ModuleInfo[] = [
    { key: 'articles', name: 'Articles', icon: 'file-text', count: 0 },
    { key: 'projects', name: 'Projets', icon: 'folder', count: 0 },
    { key: 'stacks', name: 'Stacks', icon: 'layers', count: 0 },
    { key: 'experiences', name: 'Expériences', icon: 'briefcase', count: 0 },
];
