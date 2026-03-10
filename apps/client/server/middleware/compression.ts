import { brotliCompressSync, gzipSync, constants } from 'node:zlib';

const MIN_COMPRESS_SIZE = 1024;

// Strip Nuxt dev error overlay from HTML so custom error.vue shows cleanly
// The overlay block is: <script>..bridge..</script><nuxt-error-overlay></nuxt-error-overlay><script>..shadow DOM..</script>
function stripDevOverlay(html: string): string {
    const tag = '<nuxt-error-overlay>';
    const idx = html.indexOf(tag);
    if (idx === -1) return html;

    // Find the <script> block before the overlay (parentStorageBridge)
    const scriptBefore = html.lastIndexOf('<script>', idx);
    if (scriptBefore === -1) return html;

    // Find the closing </script> after </nuxt-error-overlay> (webComponent script)
    const closeTag = '</nuxt-error-overlay>';
    const afterOverlay = html.indexOf(closeTag, idx);
    if (afterOverlay === -1) return html;
    const lastScriptEnd = html.indexOf('</script>', afterOverlay);
    if (lastScriptEnd === -1) return html;

    return html.substring(0, scriptBefore) + html.substring(lastScriptEnd + '</script>'.length);
}

export default defineEventHandler((event) => {
    const acceptEncoding = event.node.req.headers['accept-encoding'];
    if (!acceptEncoding) return;

    const encoding = typeof acceptEncoding === 'string'
        ? (acceptEncoding.includes('br') ? 'br' : acceptEncoding.includes('gzip') ? 'gzip' : '')
        : '';

    if (!encoding) return;

    // Skip internal error page renders (Nuxt renders errors at /__nuxt_error with status 200)
    const url = event.node.req.url ?? '';
    if (url.startsWith('/__nuxt_error')) return;

    const res = event.node.res;
    const originalWrite = res.write;
    const originalEnd = res.end;
    const chunks: Buffer[] = [];

    // Buffer all writes instead of sending immediately
    res.write = function (chunk: any, ...args: any[]): boolean {
        if (chunk) {
            chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(String(chunk)));
        }
        return true;
    } as typeof res.write;

    // On end, compress the buffered content and send
    res.end = function (chunk?: any, ...args: any[]): any {
        if (chunk && typeof chunk !== 'function') {
            chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(String(chunk)));
        }

        // Restore original methods before calling them
        res.write = originalWrite;
        res.end = originalEnd;

        const contentType = res.getHeader('content-type');
        const isHtml = typeof contentType === 'string' && contentType.includes('text/html');
        const isError = res.statusCode >= 400;
        let body = Buffer.concat(chunks);

        // For error pages: strip dev overlay so custom error.vue shows cleanly, skip compression
        if (isError && isHtml) {
            const html = stripDevOverlay(body.toString('utf-8'));
            const cleaned = Buffer.from(html, 'utf-8');
            res.setHeader('content-length', cleaned.length);
            return res.end(cleaned);
        }

        // Skip compression for non-HTML or small responses
        if (!isHtml || body.length < MIN_COMPRESS_SIZE) {
            res.setHeader('content-length', body.length);
            return res.end(body);
        }

        try {
            const compressed = encoding === 'br'
                ? brotliCompressSync(body, { params: { [constants.BROTLI_PARAM_QUALITY]: 4 } })
                : gzipSync(body, { level: 6 });

            // Only use compressed version if it's actually smaller
            if (compressed.length < body.length) {
                res.setHeader('content-encoding', encoding);
                res.setHeader('vary', 'Accept-Encoding');
                res.setHeader('content-length', compressed.length);
                return res.end(compressed);
            }
        } catch {
            // Compression failed — send uncompressed
        }

        res.setHeader('content-length', body.length);
        return res.end(body);
    } as typeof res.end;
});
