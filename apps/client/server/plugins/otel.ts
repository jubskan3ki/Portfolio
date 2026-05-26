// Nitro-side OTel (SSR + server routes); browser stays uninstrumented by design.
// Traces: Traefik -> Nuxt SSR -> Django via W3C traceparent (http instrumentation).
// Enable via OTEL_ENABLED=true + OTEL_EXPORTER_OTLP_ENDPOINT; no-op if SDK missing.
export default defineNitroPlugin(async () => {
    if (process.env.OTEL_ENABLED === 'false') {
        return;
    }
    const endpoint = process.env.OTEL_EXPORTER_OTLP_ENDPOINT;
    if (!endpoint) {
        return;
    }

    try {
        const { NodeSDK } = await import('@opentelemetry/sdk-node');
        const { getNodeAutoInstrumentations } = await import('@opentelemetry/auto-instrumentations-node');
        const { OTLPTraceExporter } = await import('@opentelemetry/exporter-trace-otlp-http');
        // Cross-version shim between @opentelemetry/resources v1 (Resource ctor)
        // and v2 (resourceFromAttributes fn); the constant export names in
        // semantic-conventions also moved. `any` is the honest escape hatch for
        // a runtime feature-detection bridge between API generations.
        // biome-ignore lint/suspicious/noExplicitAny: cross-version OTel shim, runtime-detected
        const resourcesMod: any = await import('@opentelemetry/resources');
        // biome-ignore lint/suspicious/noExplicitAny: cross-version OTel shim, runtime-detected
        const semconv: any = await import('@opentelemetry/semantic-conventions');

        const attributes = {
            [semconv.ATTR_SERVICE_NAME ?? 'service.name']: process.env.OTEL_SERVICE_NAME || 'portfolio-frontend',
            [semconv.ATTR_SERVICE_VERSION ?? 'service.version']: process.env.DEPLOYMENT_IMAGE_TAG || 'dev',
            'deployment.environment': process.env.DJANGO_ENV || 'dev',
        };
        // Shim: resourceFromAttributes (v2.x) vs new Resource (v1.x).
        const resource =
            typeof resourcesMod.resourceFromAttributes === 'function'
                ? resourcesMod.resourceFromAttributes(attributes)
                : new resourcesMod.Resource(attributes);

        const sdk = new NodeSDK({
            resource,
            traceExporter: new OTLPTraceExporter({
                url: `${endpoint.replace(/\/$/, '')}/v1/traces`,
            }),
            instrumentations: [
                getNodeAutoInstrumentations({
                    '@opentelemetry/instrumentation-fs': { enabled: false },
                    '@opentelemetry/instrumentation-dns': { enabled: false },
                }),
            ],
        });

        sdk.start();
        // eslint-disable-next-line no-console
        console.info(`[otel] Nitro instrumentation started -> ${endpoint}`);

        const shutdown = async () => {
            try {
                await sdk.shutdown();
            } catch (err) {
                // eslint-disable-next-line no-console
                console.warn('[otel] shutdown error', err);
            }
        };
        process.on('SIGTERM', shutdown);
        process.on('SIGINT', shutdown);
    } catch (err) {
        // eslint-disable-next-line no-console
        console.warn('[otel] SDK not available | running uninstrumented.', err);
    }
});
