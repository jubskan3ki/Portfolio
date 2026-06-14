# syntax=docker/dockerfile:1.4

ARG BUN_VERSION=1.3
ARG NODE_VERSION=24

FROM oven/bun:${BUN_VERSION}-alpine AS deps

WORKDIR /app

RUN apk upgrade --no-cache --available && \
    apk add --no-cache ca-certificates && \
    rm -rf /var/cache/apk/*

COPY package.json bun.lock ./

RUN bun install --frozen-lockfile

FROM oven/bun:${BUN_VERSION}-alpine AS dev

WORKDIR /app

RUN apk upgrade --no-cache --available && \
    apk add --no-cache curl ca-certificates && \
    rm -rf /var/cache/apk/*

# dev.yml mounts ./apps/client:/app on top; these deps are only a fallback when node_modules volume is fresh.
COPY --from=deps /app/node_modules ./node_modules
COPY package.json bun.lock ./

# Do NOT set PORT here: listhen/Nitro reads PORT and conflicts with `--port` CLI, yielding "http://0.0.0.0:/".
ENV NODE_ENV=development \
    HOST=0.0.0.0 \
    NUXT_TELEMETRY_DISABLED=1

EXPOSE 80
CMD ["bun", "run", "dev", "--host", "0.0.0.0", "--port", "80"]

FROM oven/bun:${BUN_VERSION}-alpine AS builder

ARG NUXT_API_BASE_SERVER=http://backend:8000
ARG NUXT_PUBLIC_API_BASE=http://localhost:8000
ARG NODE_MAX_OLD_SPACE_SIZE=4096

WORKDIR /app

RUN apk upgrade --no-cache --available && \
    rm -rf /var/cache/apk/*

COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app/package.json /app/bun.lock ./

COPY nuxt.config.ts tsconfig.json ./
COPY app.vue error.vue ./
COPY src ./src
COPY public ./public
COPY server ./server

ENV NODE_ENV=production \
    NITRO_PRESET=node-server \
    NUXT_TELEMETRY_DISABLED=1 \
    NUXT_API_BASE_SERVER=${NUXT_API_BASE_SERVER} \
    NUXT_PUBLIC_API_BASE=${NUXT_PUBLIC_API_BASE} \
    NODE_OPTIONS="--max-old-space-size=${NODE_MAX_OLD_SPACE_SIZE}"

# NB : on ne met PAS /app/.nuxt en cache mount. C'est le dossier de build généré
# (modules virtuels inclus, dont le @font-face de @nuxt/fonts). Le cacher entre builds
# fige des artefacts générés : un changement de nuxt.config (ex. font-display) n'était
# pas répercuté (l'ancien @font-face swap restait). On garde uniquement le cache Vite.
RUN --mount=type=cache,target=/app/node_modules/.cache \
    bunx nuxt prepare && bun run build

FROM debian:12-slim AS ssl-patch
RUN apt-get update \
    && apt-get install -y --no-install-recommends libssl3 \
    && dpkg-query -s libssl3 > /libssl3.status \
    && cp /var/lib/dpkg/info/libssl3:amd64.md5sums /libssl3.md5sums

FROM gcr.io/distroless/nodejs${NODE_VERSION}-debian12:nonroot AS runner

COPY --from=ssl-patch /usr/lib/x86_64-linux-gnu/libssl.so.3 /usr/lib/x86_64-linux-gnu/libcrypto.so.3 /usr/lib/x86_64-linux-gnu/
COPY --from=ssl-patch /usr/lib/x86_64-linux-gnu/engines-3/ /usr/lib/x86_64-linux-gnu/engines-3/
COPY --from=ssl-patch /usr/lib/x86_64-linux-gnu/ossl-modules/ /usr/lib/x86_64-linux-gnu/ossl-modules/
COPY --from=ssl-patch /libssl3.status /var/lib/dpkg/status.d/libssl3
COPY --from=ssl-patch /libssl3.md5sums /var/lib/dpkg/status.d/libssl3.md5sums

ARG VCS_REF=unknown
ARG BUILD_DATE=unknown
LABEL org.opencontainers.image.title="portfolio-frontend" \
      org.opencontainers.image.source="https://github.com/jubskan3ki/portfolio" \
      org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.licenses="MIT"

WORKDIR /app

COPY --from=builder --chown=nonroot:nonroot /app/.output ./

ENV NODE_ENV=production \
    PORT=80 \
    HOST=0.0.0.0 \
    NUXT_API_BASE_SERVER=http://backend:8000 \
    NUXT_PUBLIC_API_BASE=http://localhost:8000

EXPOSE 80

USER nonroot

HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
    CMD ["/nodejs/bin/node", "-e", "require('http').get('http://localhost:80/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1)).on('error', () => process.exit(1))"]

CMD ["server/index.mjs"]
