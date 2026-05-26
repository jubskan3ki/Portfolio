import { fileURLToPath } from 'node:url';
import { defineNuxtConfig } from 'nuxt/config';
import { visualizer } from 'rollup-plugin-visualizer';

const SITE_URL = process.env.NUXT_PUBLIC_SITE_URL || 'https://juba-aitadda.dev';
const API_BASE = process.env.NUXT_PUBLIC_API_BASE || '';
const LOOPBACK_HOSTS = new Set(['localhost', '127.0.0.1', '::1', '0.0.0.0']);
const apiPreconnectHref = (() => {
    if (!/^https?:\/\//i.test(API_BASE)) return null;
    try {
        const apiUrl = new URL(API_BASE);
        if (new URL(SITE_URL).origin === apiUrl.origin) return null;
        if (LOOPBACK_HOSTS.has(apiUrl.hostname.replace(/^\[|]$/g, ''))) return null;
        return apiUrl.origin;
    } catch {
        return null;
    }
})();

export default defineNuxtConfig({
    modules: [
        '@pinia/nuxt',
        '@nuxt/image',
        '@nuxt/fonts',
        '@nuxtjs/seo',
        'nuxt-delay-hydration',
        'nuxt-security',
        ...(process.env.NODE_ENV !== 'development' ? ['@vite-pwa/nuxt' as const] : []),
    ],

    plugins: [
        '~/src/services/plugins/vue-query.ts',
        '~/src/services/plugins/auth.ts',
        '~/src/services/plugins/web-vitals.client.ts',
        '~/src/services/plugins/easter-egg.client.ts',
        ...(process.env.NODE_ENV === 'development' ? ['~/src/services/plugins/sw-cleanup.client.ts'] : []),
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
            title: 'Juba Ait-Adda | Dev Fullstack | CDI & Freelance',
            htmlAttrs: {
                lang: 'fr',
            },
            meta: [
                { name: 'viewport', content: 'width=device-width, initial-scale=1, viewport-fit=cover' },
                { charset: 'utf-8' },
                {
                    name: 'description',
                    content: 'Portfolio de Juba Ait-Adda, développeur fullstack & DevOps ouvert CDI et freelance.',
                },
                { name: 'author', content: 'Juba Ait-Adda' },
                { name: 'publisher', content: 'Juba Ait-Adda' },
                { name: 'theme-color', content: '#1a1a2e' },
                { name: 'color-scheme', content: 'light dark' },
                { name: 'format-detection', content: 'telephone=no' },
                { name: 'referrer', content: 'strict-origin-when-cross-origin' },
                { name: 'geo.region', content: 'FR-IDF' },
                { name: 'geo.placename', content: 'Paris' },
                { name: 'geo.position', content: '48.8566;2.3522' },
                { name: 'ICBM', content: '48.8566, 2.3522' },
                // PWA / Apple / Microsoft tiles
                { name: 'application-name', content: 'Juba Ait-Adda' },
                { name: 'apple-mobile-web-app-title', content: 'Juba A.' },
                { name: 'apple-mobile-web-app-capable', content: 'yes' },
                { name: 'apple-mobile-web-app-status-bar-style', content: 'black-translucent' },
                { name: 'mobile-web-app-capable', content: 'yes' },
                { name: 'msapplication-TileColor', content: '#1a1a2e' },
                { name: 'msapplication-config', content: 'none' },
            ],
            link: [
                { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' },
                { rel: 'mask-icon', href: '/favicon.svg', color: '#1a1a2e' },
                { rel: 'apple-touch-icon', href: '/logo.png' },
                ...(apiPreconnectHref
                    ? [{ rel: 'preconnect', href: apiPreconnectHref, crossorigin: 'anonymous' } as const]
                    : []),
                // Explicit Lato preloads with fetchpriority="high" — @nuxt/fonts auto-preload
                // (preload: true) is disabled below to avoid emitting duplicate <link rel="preload">
                // tags without fetchpriority. Hashes are content-derived by @nuxt/fonts; stable
                // across builds unless the upstream Google Font file changes.
                // - Lato 400: body copy + smaller LCP elements
                // - Lato 700: H1 (LCP element on most pages)
                {
                    rel: 'preload',
                    as: 'font',
                    type: 'font/woff2',
                    href: '/_fonts/E9gAUejIpWiYG4NXk_H7-EI7uoXiYOJAJOsfxkChFnY-DEQ80D3nJs2q1ZN9RCtfuxGZLKpX_1xw0AirgnJ4lt0.woff2',
                    crossorigin: 'anonymous',
                    fetchpriority: 'high',
                },
                {
                    rel: 'preload',
                    as: 'font',
                    type: 'font/woff2',
                    href: '/_fonts/q_QnoPBQzztBGYstej5dRS1mKx_g6hjNfQWiBzRGy7o-oH6p1vIGT7djDjOJBVh4kw9aYpVbtRZ2bYAi2c6WN9I.woff2',
                    crossorigin: 'anonymous',
                    fetchpriority: 'high',
                },
                { rel: 'alternate', type: 'application/atom+xml', title: 'Blog | Atom', href: '/feed.xml' },
                { rel: 'alternate', type: 'application/feed+json', title: 'Blog | JSON Feed', href: '/feed.json' },
                { rel: 'me', href: 'https://github.com/jubskan3ki' },
                { rel: 'me', href: 'https://www.linkedin.com/in/juba-aitadda/' },
                { rel: 'author', href: '/humans.txt', type: 'text/plain' },
            ],
        },
        pageTransition: { name: 'page', mode: 'out-in' },
        layoutTransition: { name: 'layout', mode: 'out-in' },
        rootId: 'app',
    },

    // main.scss is imported via app.vue's <style> block so it lands in the inlined SSR
    // styles (features.inlineStyles below). Declaring it again here would also emit an
    // external entry.css link — that's the render-blocking stylesheet flagged by Lighthouse.

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
            googleSiteVerification: process.env.NUXT_PUBLIC_GOOGLE_SITE_VERIFICATION || '',
            webVitalsSampleRate:
                process.env.NUXT_PUBLIC_WEB_VITALS_SAMPLE_RATE
                || (process.env.NODE_ENV === 'development' ? '0' : '0.2'),
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
        '/': { swr: 600 },
        '/blog': { swr: 300 },
        '/blog/**': { swr: 600 },
        '/projects': { swr: 300 },
        '/projects/**': { swr: 600 },
        '/stacks': { swr: 300 },
        '/stacks/**': { swr: 600 },
        '/experience': { swr: 600 },
        '/contact': { prerender: true },
        '/legal': { prerender: true },
        '/privacy': { prerender: true },
        '/terms': { prerender: true },
        '/offline': { prerender: true },
        '/status': { headers: { 'X-Robots-Tag': 'noindex, nofollow' } },
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
    hooks: {
        close: (nuxt) => {
            if (!nuxt.options.dev) {
                setTimeout(() => process.exit(0), 100);
            }
        },
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
        // true respects prefers-reduced-motion; 'always' would override it.
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
        // API proxy handled by server/routes/api/[...path].ts.
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
            '/_fonts/**': {
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

        server: process.env.NODE_ENV === 'development' ? { allowedHosts: true } : undefined,

        plugins: (() => {
            if (process.env.ANALYZE !== 'true') return [];
            // rollup-plugin-visualizer returns a Rollup Plugin; Vite/Nuxt expects
            // Vite's PluginOption. The two type trees share the same shape but
            // Rolldown vs upstream Vite diverge on hook contexts. Runtime is fine.
            // biome-ignore lint/suspicious/noExplicitAny: cross-package Plugin type mismatch
            const analyzerPlugin: any = visualizer({
                open: true,
                filename: '.nuxt/bundle-stats.html',
                gzipSize: true,
                brotliSize: true,
                template: 'treemap',
            });
            return [analyzerPlugin];
        })(),
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
                    manualChunks: (id) => {
                        if (!id.includes('node_modules')) return;

                        // Admin-only / heavy lazy deps — keep isolated so the home doesn't pull them.
                        if (id.includes('chart.js')) return 'chartjs';
                        if (id.includes('/dayjs/') && !id.includes('/dayjs/plugin/')) return 'vendor-dayjs';
                        if (id.includes('/@tanstack/')) return 'vendor-query';

                        // Deferred via dynamic import in plugins — let Rollup split by entry.
                        if (id.includes('web-vitals')) return;
                        if (id.includes('workbox-') || id.includes('@vite-pwa/')) return;

                        // Per-icon code splitting handled by defineAsyncComponent in BaseIcon.
                        if (id.includes('lucide-vue-next')) return;

                        if (
                            id.includes('/vue/')
                            || id.includes('/@vue/')
                            || id.includes('/vue-router/')
                            || id.includes('/pinia/')
                        ) {
                            return 'vendor-core';
                        }

                        if (id.includes('/@vueuse/')) return 'vendor-vueuse';

                        return 'vendor-lib';
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

    fonts: {
        families: [
            {
                name: 'Lato',
                provider: 'google',
                weights: [400, 700],
                display: 'swap',
                subsets: ['latin'],
                // Disabled to avoid duplicate preload tags — both weights are explicitly
                // preloaded with fetchpriority="high" in app.head.link above.
                preload: false,
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
        // En prod, /media/ est servi par nginx-static (Django ne sert pas les
        // fichiers media quand DEBUG=false). En dev, Django les sert directement.
        alias: {
            '/media': `${process.env.NUXT_IMAGE_MEDIA_BASE || process.env.NUXT_API_BASE_SERVER || 'http://localhost:8000'}/media`,
        },
        domains: ['localhost', 'backend', 'nginx-static', 'aitaddajuba.fr'],
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
            name: 'Juba Ait-Adda | Portfolio',
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

    security: {
        headers: {
            contentSecurityPolicy:
                process.env.NODE_ENV === 'development'
                    ? false
                    : {
                            'base-uri': ['\'self\''],
                            'default-src': ['\'self\''],
                            'script-src': ['\'self\'', '\'unsafe-inline\''],
                            'script-src-attr': ['\'none\''],
                            'style-src': ['\'self\'', '\'unsafe-inline\'', 'https://fonts.googleapis.com'],
                            'img-src': ['\'self\'', 'data:', 'blob:', 'https:'],
                            'font-src': ['\'self\'', 'data:', 'https://fonts.gstatic.com'],
                            'connect-src': ['\'self\'', 'https:'],
                            'frame-src': ['\'self\''],
                            'frame-ancestors': ['\'none\''],
                            'object-src': ['\'none\''],
                            'form-action': ['\'self\''],
                            'worker-src': ['\'self\'', 'blob:'],
                            'manifest-src': ['\'self\''],
                            'upgrade-insecure-requests': true,
                        },
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
        exclude: ['/admin/**', '/login', '/status', '/offline'],
        cacheMaxAgeSeconds: 3600,
    },
});
