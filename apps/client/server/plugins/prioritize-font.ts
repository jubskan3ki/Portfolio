const FONT_PRELOAD_RE = /<link\s+rel="preload"\s+as="font"\s+([^>]*?)href="([^"]+\.woff2)"([^>]*)>/g;

export default defineNitroPlugin((nitroApp) => {
    nitroApp.hooks.hook('render:response', (response) => {
        if (typeof response.body !== 'string') return;

        response.body = response.body.replace(FONT_PRELOAD_RE, (_, pre, href, post) => {
            const attrs = `${pre} ${post}`;
            const hasType = /\btype=/.test(attrs);
            const hasPriority = /\bfetchpriority=/.test(attrs);
            const extra = [
                hasType ? '' : 'type="font/woff2"',
                hasPriority ? '' : 'fetchpriority="high"',
            ]
                .filter(Boolean)
                .join(' ');
            return `<link rel="preload" as="font" ${pre}href="${href}" ${extra}${post}>`;
        });
    });
});
