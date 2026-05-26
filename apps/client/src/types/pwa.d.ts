import type { ModuleOptions } from '@vite-pwa/nuxt';

declare module 'nuxt/schema' {
    interface NuxtConfig {
        pwa?: ModuleOptions;
    }
    interface NuxtOptions {
        pwa?: ModuleOptions;
    }
}
