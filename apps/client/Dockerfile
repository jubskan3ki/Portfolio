# syntax=docker/dockerfile:1.4

# ──────────────────────────────────────────────
# Build arguments (overridable from docker-compose)
# ──────────────────────────────────────────────
ARG NODE_VERSION=24
ARG PNPM_VERSION=10.28.0

# Stage 1: Dependencies
FROM node:${NODE_VERSION}-alpine AS deps

ARG PNPM_VERSION

WORKDIR /app

# Update Alpine packages
RUN apk upgrade --no-cache --available && \
    apk add --no-cache ca-certificates && \
    rm -rf /var/cache/apk/*

# Install pnpm
RUN corepack enable && corepack prepare pnpm@${PNPM_VERSION} --activate

# Copy dependency files for optimal caching
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Stage 2: Builder
FROM node:${NODE_VERSION}-alpine AS builder

ARG PNPM_VERSION
ARG NUXT_API_BASE_SERVER=http://backend:8000
ARG NUXT_PUBLIC_API_BASE=http://localhost:8000
ARG NODE_MAX_OLD_SPACE_SIZE=4096

WORKDIR /app

# Update Alpine packages
RUN apk upgrade --no-cache --available && \
    rm -rf /var/cache/apk/*

# Install pnpm
RUN corepack enable && corepack prepare pnpm@${PNPM_VERSION} --activate

# Copy dependencies from deps stage
COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app/package.json /app/pnpm-lock.yaml /app/pnpm-workspace.yaml ./

# Copy source files
COPY nuxt.config.ts tsconfig.json ./
COPY app.vue error.vue ./
COPY src ./src
COPY public ./public
COPY server ./server

# Build with cache mounts and optimizations
ENV NODE_ENV=production \
    NITRO_PRESET=node-server \
    NUXT_TELEMETRY_DISABLED=1 \
    NUXT_API_BASE_SERVER=${NUXT_API_BASE_SERVER} \
    NUXT_PUBLIC_API_BASE=${NUXT_PUBLIC_API_BASE} \
    NODE_OPTIONS="--max-old-space-size=${NODE_MAX_OLD_SPACE_SIZE}"

RUN --mount=type=cache,target=/app/.nuxt \
    --mount=type=cache,target=/app/node_modules/.cache \
    pnpm nuxt prepare && pnpm run build

# Stage 3: Runner (Production)
FROM node:${NODE_VERSION}-alpine AS runner

WORKDIR /app

# Update Alpine packages and install curl
RUN apk upgrade --no-cache --available && \
    apk add --no-cache curl ca-certificates && \
    rm -rf /var/cache/apk/*

# Copy built application
COPY --from=builder /app/.output ./

# Create non-root user for security
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nuxtjs && \
    chown -R nuxtjs:nodejs /app

USER nuxtjs

# Runtime environment variables (overridable at container start)
ENV NODE_ENV=production \
    PORT=80 \
    HOST=0.0.0.0 \
    NUXT_API_BASE_SERVER=http://backend:8000 \
    NUXT_PUBLIC_API_BASE=http://localhost:8000

EXPOSE 80

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:80/ || exit 1

CMD ["node", "server/index.mjs"]
