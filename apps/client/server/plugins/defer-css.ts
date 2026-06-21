// CSS critique au paint sans FOUC/CLS :
// 1. Inline l'entry CSS (évite une requête render-blocking ~560ms sur Lighthouse mobile).
// 2. Inline aussi le CSS des composants. Nuxt émet un <link rel="stylesheet"> par composant ;
//    laissé tel quel c'est render-blocking (FCP), mis en différé c'est asynchrone (FOUC/CLS sur
//    le hero/header above-the-fold). On le transforme en <style> inline : présent au paint,
//    aucune requête bloquante, zéro layout shift. Équivalent au inlineStyles natif de Nuxt, qui
//    n'est pas buildable ici (rolldown-vite + @nuxt/fonts : double export `default`).
import { existsSync, readFileSync } from 'node:fs';
import { basename, join, resolve } from 'node:path';

const NON_ENTRY_CSS_RE = /<link\s+rel="stylesheet"\s+href="(\/_nuxt\/(?!entry\.)[^"]+\.css)"\s*([^>]*)>/g;
const ENTRY_CSS_LINK_RE = /<link\s+rel="stylesheet"\s+href="(\/_nuxt\/entry\.[^"]+\.css)"\s*[^>]*>/;

let nuxtDirCache: string | false | null = null;
const cssContentCache = new Map<string, string | null>();

function findNuxtDir(): string | false {
    const searchDirs = [
        resolve(process.cwd(), 'public', '_nuxt'),
        resolve(process.cwd(), '.output', 'public', '_nuxt'),
        resolve(process.cwd(), 'dist', '_nuxt'),
        resolve(process.cwd(), '_nuxt'),
    ];
    for (const dir of searchDirs) {
        if (existsSync(dir)) return dir;
    }
    return false;
}

// Lit le contenu d'un /_nuxt/<file>.css depuis le disque (mis en cache : noms hashés = immuables).
function readCss(href: string): string | null {
    if (cssContentCache.has(href)) return cssContentCache.get(href) ?? null;

    if (nuxtDirCache === null) nuxtDirCache = findNuxtDir();

    let content: string | null = null;
    if (typeof nuxtDirCache === 'string') {
        const file = join(nuxtDirCache, basename(href));
        try {
            if (existsSync(file)) content = readFileSync(file, 'utf-8');
        } catch {
            /* skip */
        }
    }
    cssContentCache.set(href, content);
    return content;
}

export default defineNitroPlugin((nitroApp) => {
    nitroApp.hooks.hook('render:response', (response) => {
        if (typeof response.body !== 'string') return;

        // Entry CSS -> <style> inline.
        const entryContent = (() => {
            const m = response.body.match(ENTRY_CSS_LINK_RE);
            if (!m) return null;
            return readCss(m[1]);
        })();
        if (entryContent !== null) {
            response.body = response.body.replace(ENTRY_CSS_LINK_RE, `<style>${entryContent}</style>`);
        }

        // CSS des composants -> <style> inline. Si la lecture échoue, on garde le <link>
        // render-blocking d'origine (jamais de différé : pas de FOUC).
        response.body = response.body.replace(NON_ENTRY_CSS_RE, (match, href: string) => {
            const css = readCss(href);
            return css === null ? match : `<style>${css}</style>`;
        });
    });
});
