const MUTATION_METHODS = new Set(['POST', 'PUT', 'PATCH', 'DELETE']);

export default defineEventHandler(async (event) => {
    const path = getRouterParam(event, 'path') || '';

    if (path.startsWith('__')) {
        return;
    }

    const config = useRuntimeConfig();
    const apiBase = config.apiBaseServer || config.public.apiBase || 'http://localhost:8000';

    // Preserve trailing slash so Django APPEND_SLASH does not 301 a POST.
    const originalPath = getRequestURL(event).pathname;
    const queryString = getRequestURL(event).search || '';
    const response = await proxyRequest(event, `${apiBase}${originalPath}${queryString}`);

    const method = event.node.req.method || '';
    const status = event.node.res.statusCode;
    if (MUTATION_METHODS.has(method) && status >= 200 && status < 300) {
        purgeNitroSWRCache().catch(() => {});
    }

    return response;
});

async function purgeNitroSWRCache(): Promise<void> {
    const storage = useStorage('cache');
    const keys = await storage.getKeys('nitro:handlers');
    await Promise.all(keys.map((key) => storage.removeItem(key)));
}
