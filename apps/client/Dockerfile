# Étape 1 : Construction de l'application
FROM node:22-alpine AS builder

# Définir le répertoire de travail
WORKDIR /app

# Installer PNPM via corepack
RUN corepack enable && corepack prepare pnpm@latest --activate

# Copier les fichiers package.json et pnpm-lock.yaml
COPY package.json pnpm-lock.yaml ./

# Installer les dépendances
RUN pnpm install --frozen-lockfile

# Copier le reste du code source
COPY . .

# Construire l'application Nuxt.js
RUN pnpm run build

# Étape 2 : Préparer l'image pour l'exécution
FROM node:22-alpine AS runner

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers construits depuis l'étape de construction
COPY --from=builder /app/.output ./

# Définir les variables d'environnement
ENV PORT=80
ENV HOST=0.0.0.0

# Exposer le port sur lequel l'application s'exécute
EXPOSE 80

# Démarrer l'application Nuxt.js
CMD ["node", "server/index.mjs"]
