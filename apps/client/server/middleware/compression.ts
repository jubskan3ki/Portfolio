import { brotliCompressSync, constants, gzipSync } from 'node:zlib';

const MIN_COMPRESS_SIZE = 1024;

// Strip Nuxt dev error overlay (bridge <script> + <nuxt-error-overlay> + shadow-DOM <script>).
function stripDevOverlay(html: string): string {
    const tag = '<nuxt-error-overlay>';
    const idx = html.indexOf(tag);
    if (idx === -1) return html;

    const scriptBefore = html.lastIndexOf('<script>', idx);
    if (scriptBefore === -1) return html;

    const closeTag = '</nuxt-error-overlay>';
    const afterOverlay = html.indexOf(closeTag, idx);
    if (afterOverlay === -1) return html;
    const lastScriptEnd = html.indexOf('</script>', afterOverlay);
    if (lastScriptEnd === -1) return html;

    return html.substring(0, scriptBefore) + html.substring(lastScriptEnd + '</script>'.length);
}

type WritableChunk = string | Buffer | Uint8Array | null | undefined;

function toBuffer(chunk: WritableChunk): Buffer | null {
    if (chunk === null || chunk === undefined) return null;
    if (Buffer.isBuffer(chunk)) return chunk;
    if (chunk instanceof Uint8Array) return Buffer.from(chunk);
    return Buffer.from(String(chunk));
}

export default defineEventHandler((event) => {
    const acceptEncoding = event.node.req.headers['accept-encoding'];
    if (!acceptEncoding) return;

    const encoding =
        typeof acceptEncoding === 'string'
            ? acceptEncoding.includes('br')
                ? 'br'
                : acceptEncoding.includes('gzip')
                  ? 'gzip'
                  : ''
            : '';

    if (!encoding) return;

    const url = event.node.req.url ?? '';
    if (url.startsWith('/api/') || url.startsWith('/__nuxt_error')) return;

    // Assets statiques : non-HTML, déjà compressés (compressPublicAssets) et servis par nginx en prod.
    // On court-circuite avant d'intercepter res.write/end pour ne pas bufferiser des bundles en mémoire.
    if (
        url.startsWith('/_nuxt/')
        || url.startsWith('/_ipx/')
        || url.startsWith('/_fonts/')
        || url.startsWith('/fonts/')
        || url.startsWith('/images/')
        || url.endsWith('.svg')
    ) {
        return;
    }

    const res = event.node.res;
    const originalWrite = res.write;
    const originalEnd = res.end;
    const chunks: Buffer[] = [];

    res.write = ((chunk: WritableChunk): boolean => {
        const buf = toBuffer(chunk);
        if (buf) chunks.push(buf);
        return true;
    }) as typeof res.write;

    res.end = ((chunk?: WritableChunk): typeof res => {
        if (chunk && typeof chunk !== 'function') {
            const buf = toBuffer(chunk);
            if (buf) chunks.push(buf);
        }

        res.write = originalWrite;
        res.end = originalEnd;

        const contentType = res.getHeader('content-type');
        const isHtml = typeof contentType === 'string' && contentType.includes('text/html');
        const isError = res.statusCode >= 400;
        const body = Buffer.concat(chunks);

        // Error pages: strip dev overlay so error.vue renders cleanly, skip compression.
        if (isError && isHtml) {
            const html = stripDevOverlay(body.toString('utf-8'));
            const cleaned = Buffer.from(html, 'utf-8');
            res.setHeader('content-length', cleaned.length);
            return res.end(cleaned);
        }

        if (!isHtml || body.length < MIN_COMPRESS_SIZE) {
            res.setHeader('content-length', body.length);
            return res.end(body);
        }

        try {
            const compressed =
                encoding === 'br'
                    ? brotliCompressSync(body, { params: { [constants.BROTLI_PARAM_QUALITY]: 4 } })
                    : gzipSync(body, { level: 6 });

            if (compressed.length < body.length) {
                res.setHeader('content-encoding', encoding);
                res.setHeader('vary', 'Accept-Encoding');
                res.setHeader('content-length', compressed.length);
                return res.end(compressed);
            }
        } catch {
            /* fall through to uncompressed */
        }

        res.setHeader('content-length', body.length);
        return res.end(body);
    }) as typeof res.end;
});
