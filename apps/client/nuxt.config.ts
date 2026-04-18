import { fileURLToPath } from 'url';

import { defineNuxtConfig } from 'nuxt/config';
import { visualizer } from 'rollup-plugin-visualizer';

export default defineNuxtConfig({
    modules: [
        '@nuxt/eslint',
        '@pinia/nuxt',
        '@nuxt/image',
        '@nuxt/fonts',
        '@nuxtjs/seo',
        'nuxt-delay-hydration',
        'nuxt-security',
        '@vite-pwa/nuxt',
    ],

    plugins: [
        '~/src/services/plugins/vue-query.ts',
        '~/src/services/plugins/auth.ts',
        '~/src/services/plugins/web-vitals.client.ts',
    ],

    ssr: true,

    components: {
        dirs: [
            'src/components/base',
            { path: 'src/components/feature', pathPrefix: false },
            'src/components/feedback',
            'src/components/layouts',
            'src/components/loaders',
            'src/components/navigation',
            'src/components/ui',
        ],
    },

    imports: {
        autoImport: true,
    },

    devtools: {
        enabled: process.env.NODE_ENV === 'development',
    },

    app: {
        head: {
            title: 'Juba Ait-Adda | Développeur Full-Stack',
            htmlAttrs: {
                lang: 'fr',
            },
            meta: [
                { name: 'viewport', content: 'width=device-width, initial-scale=1' },
                { charset: 'utf-8' },
                { name: 'description', content: 'Portfolio de Juba Ait-Adda, développeur full-stack et DevOps' },
                { name: 'theme-color', content: '#1a1a2e' },
            ],
            link: [
                { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' },
                { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
                { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
                { rel: 'preconnect', href: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000' },
                { rel: 'alternate', type: 'application/atom+xml', title: 'Blog — Atom', href: '/feed.xml' },
                { rel: 'alternate', type: 'application/feed+json', title: 'Blog — JSON Feed', href: '/feed.json' },
            ],
        },
        pageTransition: { name: 'page', mode: 'out-in' },
        layoutTransition: { name: 'layout', mode: 'out-in' },
        rootId: 'app',
    },

    css: ['~/src/styles/main.scss'],

    router: {
        options: {
            strict: false,
        },
    },

    site: {
        url: process.env.NUXT_PUBLIC_SITE_URL || 'https://juba-aitadda.dev',
        name: 'Juba Ait-Adda',
        description: 'Portfolio de Juba Ait-Adda, développeur full-stack et DevOps',
        defaultLocale: 'fr',
    },

    runtimeConfig: {
        apiBaseServer: process.env.NUXT_API_BASE_SERVER || process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000',
        public: {
            apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000',
            webVitalsSampleRate:
                process.env.NUXT_PUBLIC_WEB_VITALS_SAMPLE_RATE ||
                (process.env.NODE_ENV === 'development' ? '0' : '0.2'),
        },
    },

    dir: {
        pages: 'src/pages',
        layouts: 'src/layouts',
        middleware: 'src/middleware',
        public: 'public',
        plugins: 'src/plugins',
    },

    srcDir: './',

    serverDir: 'server',

    build: {
        transpile: ['@tanstack/vue-query'],
    },

    routeRules: {
        // headers gérés par nuxt-security (cf. bloc security ci-dessous)
        '/': { swr: 600 },
        '/blog': { swr: 300 },
        '/blog/**': { swr: 600 },
        '/projects': { swr: 300 },
        '/projects/**': { swr: 600 },
        '/stacks': { swr: 300 },
        '/stacks/**': { swr: 600 },
        '/about': { redirect: { to: '/contact', statusCode: 301 } },
        '/experience': { swr: 600 },
        '/contact': { swr: 3600 },
        '/legal': { swr: 86400 },
        '/privacy': { swr: 86400 },
        '/terms': { swr: 86400 },
        '/admin/**': {
            ssr: true,
            headers: {
                'Cache-Control': 'private, no-cache, no-store, must-revalidate',
            },
        },
        '/admin/login': {
            experimentalNoScripts: false,
        },
    },

    sourcemap: {
        server: process.env.NODE_ENV === 'development',
        client: process.env.NODE_ENV === 'development',
    },

    devServer: {
        host: 'localhost',
    },

    watch: ['./src/styles/**/*.scss'],

    future: {
        compatibilityVersion: 4,
    },

    features: {
        inlineStyles: true,
    },

    experimental: {
        payloadExtraction: true,
        inlineRouteRules: true,
        renderJsonPayloads: true,
        // true respects prefers-reduced-motion; 'always' would force it on.
        viewTransition: true,
    },

    compatibilityDate: '2025-12-30',

    nitro: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url)),
        },
        preset: 'node-server',
        compressPublicAssets: {
            brotli: true,
            gzip: true,
        },
        // API proxy handled by server/routes/api/[...path].ts (works in dev + production)
        routeRules: {
            '/_nuxt/**': {
                headers: { 'Cache-Control': 'public, max-age=31536000, immutable' },
            },
            '/_ipx/**': {
                headers: { 'Cache-Control': 'public, max-age=2592000, immutable' },
            },
            '/fonts/**': {
                headers: { 'Cache-Control': 'public, max-age=31536000, immutable' },
            },
            '/images/**': {
                headers: { 'Cache-Control': 'public, max-age=31536000, immutable' },
            },
            '/*.svg': {
                headers: { 'Cache-Control': 'public, max-age=31536000, immutable' },
            },
            '/logo.svg': {
                headers: { 'Cache-Control': 'public, max-age=31536000, immutable' },
            },
            '/favicon.ico': {
                headers: { 'Cache-Control': 'public, max-age=31536000, immutable' },
            },
        },
        minify: true,
    },

    vite: {
        cacheDir: 'node_modules/.cache/vite',

        plugins:
            process.env.ANALYZE === 'true'
                ? [
                      visualizer({
                          open: true,
                          filename: '.nuxt/bundle-stats.html',
                          gzipSize: true,
                          brotliSize: true,
                          template: 'treemap',
                      }) as any,
                  ]
                : [],
        css: {
            preprocessorOptions: {
                scss: {
                    additionalData: '',
                },
            },
            devSourcemap: true,
        },
        resolve: {
            alias: {
                '@': fileURLToPath(new URL('./src', import.meta.url)),
                '~': fileURLToPath(new URL('./', import.meta.url)),
            },
        },
        build: {
            cssMinify: 'esbuild',
            cssCodeSplit: true,
            minify: 'esbuild',
            reportCompressedSize: false,
            rollupOptions: {
                output: {
                    experimentalMinChunkSize: 30_000,
                    manualChunks: (id) => {
                        if (id.includes('node_modules')) {
                            if (id.includes('chart.js')) return 'chartjs';
                            if (
                                id.includes('/vue/') ||
                                id.includes('/@vue/') ||
                                id.includes('/vue-router/') ||
                                id.includes('/pinia/')
                            ) {
                                return 'vendor-core';
                            }
                            return 'vendor-lib';
                        }
                    },
                },
            },
            chunkSizeWarningLimit: 1000,
        },
        optimizeDeps: {
            include: ['vue', 'vue-router', 'pinia', '@tanstack/vue-query'],
            exclude: ['chart.js'],
        },
    },

    typescript: {
        strict: true,
        typeCheck: false,
    },

    delayHydration: {
        mode: process.env.NODE_ENV === 'development' ? false : 'mount',
        debug: false,
        exclude: ['/admin/**'],
    },

    eslint: {
        config: {
            stylistic: {
                indent: 4,
                semi: true,
                quotes: 'single',
                commaDangle: 'always-multiline',
                braceStyle: '1tbs',
                arrowParens: true,
                quoteProps: 'as-needed',
                blockSpacing: true,
            },
        },
    },

    fonts: {
        families: [
            {
                name: 'Lato',
                provider: 'google',
                weights: [400, 700],
                display: 'swap',
                subsets: ['latin'],
            },
            {
                name: 'Fira Code',
                provider: 'google',
                weights: [400],
                display: 'optional',
                subsets: ['latin'],
            },
        ],
        defaults: {
            weights: [400, 700],
            styles: ['normal'],
        },
    },

    image: {
        provider: 'ipx',
        quality: 80,
        format: ['avif', 'webp', 'png', 'jpg'],
        alias: {
            '/media': `${process.env.NUXT_API_BASE_SERVER || process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000'}/media`,
        },
        domains: ['localhost', 'backend'],
        screens: {
            xs: 320,
            sm: 640,
            md: 768,
            lg: 1024,
            xl: 1280,
            '2xl': 1536,
        },
        densities: [1, 2],
        presets: {
            avatar: {
                modifiers: { format: 'webp', width: 80, height: 80, fit: 'cover', quality: 85 },
            },
            thumbnail: {
                modifiers: { format: 'webp', width: 400, height: 300, fit: 'cover', quality: 80 },
            },
            card: {
                modifiers: { format: 'webp', width: 600, height: 400, fit: 'cover', quality: 80 },
            },
            hero: {
                modifiers: { format: 'webp', width: 1920, height: 600, fit: 'cover', quality: 75 },
            },
            'card-mobile': {
                modifiers: { format: 'webp', width: 400, height: 267, fit: 'cover', quality: 80 },
            },
        },
    },

    ogImage: {
        enabled: true,
        defaults: {
            width: 1200,
            height: 630,
            component: 'OgImageDefault',
        },
        fonts: [
            { name: 'Lato', weight: 400 },
            { name: 'Lato', weight: 700 },
        ],
    },

    pwa: {
        registerType: 'autoUpdate',
        injectRegister: 'auto',
        strategies: 'generateSW',
        manifest: {
            name: 'Juba Ait-Adda — Portfolio',
            short_name: 'Juba A.',
            description: 'Portfolio de Juba Ait-Adda, développeur full-stack et DevOps',
            theme_color: '#1a1a2e',
            background_color: '#ffffff',
            display: 'standalone',
            start_url: '/',
            scope: '/',
            lang: 'fr',
            icons: [{ src: '/favicon.svg', sizes: 'any', type: 'image/svg+xml', purpose: 'any' }],
        },
        workbox: {
            globPatterns: [],
            navigateFallback: '/offline',
            navigateFallbackDenylist: [/^\/admin/, /^\/api/, /^\/feed\./, /^\/_ipx/, /^\/_nuxt/],
            runtimeCaching: [
                {
                    urlPattern: ({ url }: { url: URL }) => url.pathname.startsWith('/api/articles/'),
                    handler: 'StaleWhileRevalidate',
                    options: {
                        cacheName: 'articles-api',
                        expiration: { maxEntries: 40, maxAgeSeconds: 24 * 3600 },
                        cacheableResponse: { statuses: [0, 200] },
                    },
                },
                {
                    urlPattern: ({ url }: { url: URL }) => url.pathname.startsWith('/media/'),
                    handler: 'StaleWhileRevalidate',
                    options: {
                        cacheName: 'media-assets',
                        expiration: { maxEntries: 80, maxAgeSeconds: 30 * 24 * 3600 },
                        cacheableResponse: { statuses: [0, 200] },
                    },
                },
            ],
        },
        devOptions: {
            enabled: false,
        },
        client: {
            installPrompt: false,
        },
    },

    robots: {
        enabled: true,
        groups: [
            {
                userAgent: '*',
                disallow: ['/admin', '/admin/**'],
                allow: '/',
            },
        ],
    },

    schemaOrg: {
        identity: {
            type: 'Person',
            name: 'Juba Ait-Adda',
            url: 'https://juba-aitadda.dev',
            image: 'https://juba-aitadda.dev/images/profile.jpg',
            logo: '/logo.svg',
            sameAs: [
                'https://github.com/jubskan3ki',
                'https://www.linkedin.com/in/juba-aitadda/',
                'https://x.com/juba_aitadda',
            ],
        },
    },

    // ── Security headers (remplace les headers manuels dans routeRules) ───────
    security: {
        headers: {
            contentSecurityPolicy: false,
            crossOriginEmbedderPolicy: false,
            crossOriginOpenerPolicy: process.env.NODE_ENV === 'development' ? false : 'same-origin',
            crossOriginResourcePolicy: 'same-origin',
            strictTransportSecurity: {
                maxAge: 31536000,
                includeSubdomains: true,
                preload: true,
            },
            xFrameOptions: 'DENY',
            xContentTypeOptions: 'nosniff',
            referrerPolicy: 'strict-origin-when-cross-origin',
            permissionsPolicy: {
                camera: [],
                microphone: [],
                geolocation: [],
            },
        },
        requestSizeLimiter: {
            maxRequestSizeInBytes: 5_000_000,
            maxUploadFileRequestInBytes: 5_000_000,
        },
        rateLimiter: false,
        corsHandler: false,
        allowedMethodsRestricter: false,
        hidePoweredBy: true,
        basicAuth: false,
        csrf: false,
        nonce: false,
        ssg: false,
        sri: false,
    },

    sitemap: {
        sources: ['/api/__sitemap__/urls'],
        exclude: ['/admin/**', '/login'],
        cacheMaxAgeSeconds: 3600,
    },
});
