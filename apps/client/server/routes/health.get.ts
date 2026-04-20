// Used by Docker HEALTHCHECK and Traefik loadbalancer healthcheck.
export default defineEventHandler(async (event) => {
    const config = useRuntimeConfig();
    const apiBase = config.apiBaseServer || config.public.apiBase;

    const checks: Record<string, { ok: boolean; message: string }> = {
        nitro: { ok: true, message: 'ready' },
    };

    try {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 2000);
        const response = await $fetch.raw(`${apiBase}/health`, {
            signal: controller.signal,
            retry: 0,
        });
        clearTimeout(timeout);
        checks.upstream = {
            ok: response.status === 200,
            message: `status=${response.status}`,
        };
    } catch (err) {
        checks.upstream = {
            ok: false,
            message: err instanceof Error ? err.message : String(err),
        };
    }

    const allOk = Object.values(checks).every((c) => c.ok);
    if (!allOk) {
        setResponseStatus(event, 503);
    }
    return { status: allOk ? 'ok' : 'degraded', checks };
});
