// src/config/stacks.ts
// Configuration des catégories de stacks (icônes et labels)

export const STACK_CATEGORY_ICONS: Record<string, string> = {
    all: 'layers',
    frontend: 'layout',
    backend: 'server',
    database: 'database',
    devops: 'git-branch',
    mobile: 'smartphone',
    tools: 'tool',
    testing: 'check-circle',
    cloud: 'cloud',
    design: 'palette',
} as const;

export const STACK_CATEGORY_LABELS: Record<string, string> = {
    all: 'Toutes',
    frontend: 'Frontend',
    backend: 'Backend',
    database: 'Database',
    devops: 'DevOps',
    mobile: 'Mobile',
    tools: 'Outils',
    testing: 'Testing',
    cloud: 'Cloud',
    design: 'Design',
} as const;
