import { computed, type ComputedRef } from 'vue';

import { createPath } from '@/config/routes';

import type { RouteObject, LinkTarget } from '@/types/components/base';

export interface UseLinkResolverOptions {
    to?: string | RouteObject;
    params?: Record<string, string | number>;
    target?: LinkTarget | '';
}

export interface UseLinkResolverReturn {
    /** Whether the link points to an external URL (http, https, //, tel:, mailto:) */
    isExternalLink: ComputedRef<boolean>;
    /** Whether the link points to an internal route */
    isInternalLink: ComputedRef<boolean>;
    /** The resolved props to bind on the component (href/to/rel/target) */
    linkProps: ComputedRef<Record<string, unknown>>;
    /** The resolved URL path */
    resolvedPath: ComputedRef<string>;
}

const EXTERNAL_PREFIXES = ['http://', 'https://', '//', 'tel:', 'mailto:'] as const;

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
            return {
                to: resolvedPath.value,
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
