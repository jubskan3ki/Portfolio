const MUTATION_METHODS = new Set(['POST', 'PUT', 'PATCH', 'DELETE']);

// Mutations à fort volume qui ne modifient pas le contenu public rendu : compteurs de vues,
// télémétrie web-vitals (jusqu'à 180/min/IP) et soumission du formulaire de contact.
// Les purger déclencherait un cache SWR froid global à chaque vue de page ou beacon.
// La cohérence éventuelle des compteurs est assurée par le TTL SWR (300-600 s).
const PURGE_SKIP_PATTERNS = [
    /\/view\/?$/, // articles/projects recordView
    /^\/api\/stats\//, // web-vitals & métriques
    /^\/api\/contacts\/?$/, // soumission du formulaire de contact (pas les sous-routes faqs/infos)
];

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
    const shouldPurge = !PURGE_SKIP_PATTERNS.some((re) => re.test(originalPath));
    if (shouldPurge && MUTATION_METHODS.has(method) && status >= 200 && status < 300) {
        void purgeNitroSWRCache();
    }

    return response;
});

async function purgeNitroSWRCache(): Promise<void> {
    try {
        const storage = useStorage('cache');
        const keys = await storage.getKeys('nitro:handlers');
        await Promise.all(keys.map((key) => storage.removeItem(key)));
    } catch (err) {
        console.warn('[proxy] Échec de la purge du cache SWR Nitro:', err);
    }
}
