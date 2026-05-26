import type { KnipConfig } from 'knip';

const config: KnipConfig = {
    entry: [
        'nuxt.config.ts',
        'stylelint.config.mjs',
        'playwright.config.ts',
        'vitest.config.ts',
        'app/**/*.ts',
        'server/**/*.{ts,js}',
        'src/pages/**/*.vue',
        'src/layouts/**/*.vue',
        'src/components/**/*.vue',
        'src/composables/**/*.ts',
        'src/stores/**/*.ts',
        'src/config/**/*.ts',
        'src/services/plugins/*.ts',
        'src/middleware/*.ts',
        'tests/**/*.{ts,js}',
    ],
    project: ['src/**/*.{ts,vue}', 'server/**/*.ts', 'tests/**/*.ts'],
};

export default config;
