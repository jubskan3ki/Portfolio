/**
 * Nitro render hooks for CSS optimization:
 *
 * 1. Inline entry CSS directly into the HTML to eliminate a render-blocking request.
 *    Under slow networks (Lighthouse mobile simulation), this saves ~560ms by avoiding
 *    a separate round trip for the entry stylesheet.
 *
 * 2. Defer non-critical component CSS files to async loading.
 *    Since Nuxt inlines component styles via `features.inlineStyles`,
 *    the external CSS files are only needed for client-side navigation.
 */
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join, resolve } from 'node:path';

const NON_ENTRY_CSS_RE = /<link\s+rel="stylesheet"\s+href="(\/_nuxt\/(?!entry\.)[^"]+\.css)"\s*([^>]*)>/g;
const ENTRY_CSS_LINK_RE = /<link\s+rel="stylesheet"\s+href="(\/_nuxt\/entry\.[^"]+\.css)"\s*[^>]*>/;

let entryCssCache: string | false | null = null;

function findEntryCss(): string | false {
    const searchDirs = [
        resolve(process.cwd(), '.output', 'public', '_nuxt'),
        resolve(process.cwd(), 'dist', '_nuxt'),
        resolve(process.cwd(), '_nuxt'),
    ];

    for (const dir of searchDirs) {
        if (!existsSync(dir)) continue;
        try {
            const files = readdirSync(dir);
            const entryFile = files.find((f) => f.startsWith('entry.') && f.endsWith('.css'));
            if (entryFile) {
                return readFileSync(join(dir, entryFile), 'utf-8');
            }
        }
        catch { /* skip */ }
    }

    return false;
}

export default defineNitroPlugin((nitroApp) => {
    nitroApp.hooks.hook('render:response', (response) => {
        if (typeof response.body !== 'string') return;

        // 1. Inline entry CSS (lazy-load from disk on first request, then cached)
        if (entryCssCache === null) {
            entryCssCache = findEntryCss();
        }

        if (typeof entryCssCache === 'string') {
            response.body = response.body.replace(
                ENTRY_CSS_LINK_RE,
                `<style>${entryCssCache}</style>`,
            );
        }

        // 2. Defer non-critical CSS to async preload
        response.body = response.body.replace(
            NON_ENTRY_CSS_RE,
            '<link rel="preload" href="$1" as="style" $2 onload="this.rel=\'stylesheet\'">'
            + '<noscript><link rel="stylesheet" href="$1" $2></noscript>',
        );
    });
});
