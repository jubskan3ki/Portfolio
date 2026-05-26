// 1. Inline entry CSS to avoid a render-blocking request (~560ms on Lighthouse mobile).
// 2. Defer non-critical component CSS (Nuxt inlines styles via features.inlineStyles).
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join, resolve } from 'node:path';

const NON_ENTRY_CSS_RE = /<link\s+rel="stylesheet"\s+href="(\/_nuxt\/(?!entry\.)[^"]+\.css)"\s*([^>]*)>/g;
const ENTRY_CSS_LINK_RE = /<link\s+rel="stylesheet"\s+href="(\/_nuxt\/entry\.[^"]+\.css)"\s*[^>]*>/;

let entryCssCache: string | false | null = null;

function findEntryCss(): string | false {
    const searchDirs = [
        resolve(process.cwd(), 'public', '_nuxt'),
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
        } catch {
            /* skip */
        }
    }

    return false;
}

const DEFER_CSS_BOOTSTRAP = '<script>document.querySelectorAll(\'link[data-defer-css]\').forEach(function(l){l.rel=\'stylesheet\';});</script>';

export default defineNitroPlugin((nitroApp) => {
    nitroApp.hooks.hook('render:response', (response) => {
        if (typeof response.body !== 'string') return;

        if (entryCssCache === null) {
            entryCssCache = findEntryCss();
        }

        if (typeof entryCssCache === 'string') {
            response.body = response.body.replace(ENTRY_CSS_LINK_RE, `<style>${entryCssCache}</style>`);
        }

        let replaced = false;
        response.body = response.body.replace(NON_ENTRY_CSS_RE, (_match, href: string, attrs: string) => {
            replaced = true;
            return (
                `<link rel="preload" href="${href}" as="style" ${attrs} data-defer-css>`
                + `<noscript><link rel="stylesheet" href="${href}" ${attrs}></noscript>`
            );
        });

        if (replaced) {
            response.body = response.body.replace('</head>', `${DEFER_CSS_BOOTSTRAP}</head>`);
        }
    });
});
