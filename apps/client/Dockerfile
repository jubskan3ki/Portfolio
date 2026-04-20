# syntax=docker/dockerfile:1.4

ARG NODE_VERSION=24
ARG PNPM_VERSION=10.28.0

FROM node:${NODE_VERSION}-alpine AS deps

ARG PNPM_VERSION

WORKDIR /app

RUN apk upgrade --no-cache --available && \
    apk add --no-cache ca-certificates && \
    rm -rf /var/cache/apk/*

RUN corepack enable && corepack prepare pnpm@${PNPM_VERSION} --activate

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./

RUN pnpm install --frozen-lockfile

FROM node:${NODE_VERSION}-alpine AS dev

ARG PNPM_VERSION

WORKDIR /app

RUN apk upgrade --no-cache --available && \
    apk add --no-cache curl ca-certificates && \
    rm -rf /var/cache/apk/*

RUN corepack enable && corepack prepare pnpm@${PNPM_VERSION} --activate

# dev.yml mounts ./apps/client:/app on top; these deps are only a fallback when node_modules volume is fresh.
COPY --from=deps /app/node_modules ./node_modules
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./

# Do NOT set PORT here: listhen/Nitro reads PORT and conflicts with `--port` CLI, yielding "http://0.0.0.0:/".
ENV NODE_ENV=development \
    HOST=0.0.0.0 \
    NUXT_TELEMETRY_DISABLED=1

EXPOSE 80
CMD ["pnpm", "dev", "--host", "0.0.0.0", "--port", "80"]

FROM node:${NODE_VERSION}-alpine AS builder

ARG PNPM_VERSION
ARG NUXT_API_BASE_SERVER=http://backend:8000
ARG NUXT_PUBLIC_API_BASE=http://localhost:8000
ARG NODE_MAX_OLD_SPACE_SIZE=4096

WORKDIR /app

RUN apk upgrade --no-cache --available && \
    rm -rf /var/cache/apk/*

RUN corepack enable && corepack prepare pnpm@${PNPM_VERSION} --activate

COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app/package.json /app/pnpm-lock.yaml /app/pnpm-workspace.yaml ./

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

RUN --mount=type=cache,target=/app/.nuxt \
    --mount=type=cache,target=/app/node_modules/.cache \
    pnpm nuxt prepare && pnpm run build

FROM gcr.io/distroless/nodejs24-debian12:nonroot AS runner

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
