import { computed } from 'vue';

import { createPath } from '@/config/routes';

import type { UseLinkResolverOptions, UseLinkResolverReturn } from '@/types/composables/ui';

const EXTERNAL_PREFIXES = ['http://', 'https://', '//', 'tel:', 'mailto:'] as const;
const SAFE_SCHEMES = new Set(['http:', 'https:', 'mailto:', 'tel:']);

// Bloque les schémas dangereux (javascript:, data:, vbscript:, ...) qui pourraient
// se déguiser en « lien interne » et être passés tels quels à NuxtLink :to.
function hasUnsafeScheme(value: string): boolean {
    const scheme = /^\s*([a-z][a-z0-9+.-]*):/i.exec(value)?.[1];
    if (!scheme) {
        return false; // chemin relatif/absolu sans schéma => sûr
    }
    return !SAFE_SCHEMES.has(`${scheme.toLowerCase()}:`);
}

export function useLinkResolver(options: () => UseLinkResolverOptions): UseLinkResolverReturn {
    const resolvedPath = computed(() => {
        const { to, params = {} } = options();
        if (!to) {
            return '';
        }
        if (typeof to === 'object' && 'path' in to) {
            return createPath(to, params);
        }
        return to as string;
    });

    const isExternalLink = computed(() => {
        const { to } = options();
        if (!to || typeof to !== 'string') {
            return false;
        }
        return EXTERNAL_PREFIXES.some((prefix) => to.startsWith(prefix));
    });

    const isInternalLink = computed(() => {
        const { to } = options();
        return !!to && !isExternalLink.value;
    });

    const linkProps = computed(() => {
        const { target } = options();
        const effectiveTarget = target || undefined;

        if (isInternalLink.value) {
            // Un « chemin interne » avec un schéma non autorisé (javascript:, data:)
            // est neutralisé vers l'accueil plutôt que passé à NuxtLink.
            const to = hasUnsafeScheme(resolvedPath.value) ? '/' : resolvedPath.value;
            return {
                to,
                target: effectiveTarget,
            };
        }
        if (isExternalLink.value) {
            return {
                href: resolvedPath.value,
                target: effectiveTarget,
                rel: target === '_blank' ? 'noopener noreferrer' : undefined,
            };
        }
        return {};
    });

    return {
        isExternalLink,
        isInternalLink,
        linkProps,
        resolvedPath,
    };
}
