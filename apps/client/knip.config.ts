import type { KnipConfig } from 'knip';

const config: KnipConfig = {
    entry: [
        'src/pages/**/*.vue',
        'src/layouts/**/*.vue',
        'src/components/**/*.vue',
        'src/composables/**/*.ts',
        'src/stores/**/*.ts',
        'src/config/**/*.ts',
        'src/services/plugins/*.ts',
        'src/middleware/*.ts',
    ],
    project: ['src/**/*.{ts,vue}'],
    ignoreDependencies: ['sass', 'eslint-plugin-vuejs-accessibility'],
    ignoreBinaries: ['eslint'],
};

export default config;
