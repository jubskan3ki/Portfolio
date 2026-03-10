const ENTITY_RE = /&(?:#x[0-9a-fA-F]+|#\d+|[a-zA-Z]+);/;

function decodeStr(s: string): string {
    if (!ENTITY_RE.test(s)) return s;
    return s
        .replace(/&amp;/g, '&')
        .replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>')
        .replace(/&quot;/g, '"')
        .replace(/&#0?39;/g, "'")
        .replace(/&#x27;/g, "'")
        .replace(/&#(\d+);/g, (_m, code) => String.fromCharCode(Number(code)))
        .replace(/&#x([0-9a-fA-F]+);/g, (_m, hex) => String.fromCharCode(parseInt(hex, 16)));
}

/**
 * Recursively decode HTML entities in all string values of an object/array.
 * Useful to clean API responses that contain double-encoded entities.
 */
export function decodeHtmlEntities<T>(obj: T): T {
    if (obj == null) return obj;
    if (typeof obj === 'string') return decodeStr(obj) as T;
    if (Array.isArray(obj)) return obj.map((item) => decodeHtmlEntities(item)) as T;
    if (typeof obj === 'object') {
        const result = { ...obj } as Record<string, unknown>;
        for (const key of Object.keys(result)) {
            const val = result[key];
            if (typeof val === 'string') {
                result[key] = decodeStr(val);
            } else if (typeof val === 'object' && val !== null) {
                result[key] = decodeHtmlEntities(val);
            }
        }
        return result as T;
    }
    return obj;
}

export function resolveMediaUrl(path: string | null | undefined): string {
    if (!path) {
        return '';
    }

    // Already a full URL — normalize Docker-internal hostname to public base
    if (path.startsWith('http')) {
        const runtimeConfig = useRuntimeConfig();
        const publicBase = (runtimeConfig.public?.apiBase as string) || 'http://localhost:8000';
        const serverBase = (runtimeConfig.apiBaseServer as string) || '';
        if (serverBase && serverBase !== publicBase && path.startsWith(serverBase)) {
            return path.replace(serverBase, publicBase);
        }
        return path;
    }

    // Already starts with /media/ — good
    if (path.startsWith('/media/')) {
        return path;
    }

    // Relative path (e.g. "stacks/git/git.svg" or "deviprop") — prepend /media/
    return `/media/${path}`;
}

export function truncateText(text: string, maxLength = 100): string {
    if (!text || text.length <= maxLength) {
        return text;
    }
    return `${text.slice(0, maxLength)}...`;
}

type BadgeVariant = 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'info' | 'outline';

const PROJECT_STATUS_MAP: Record<string, BadgeVariant> = {
    completed: 'success',
    in_progress: 'warning',
    planned: 'info',
    archived: 'secondary',
};

export function getProjectStatusVariant(status: string): BadgeVariant {
    return PROJECT_STATUS_MAP[status] || 'secondary';
}

export function formatViews(views: number): string {
    if (views >= 1000) {
        return `${(views / 1000).toFixed(1)}k`;
    }
    return views.toString();
}

export function sliceTags(tags: string[] | undefined, maxTags: number): { displayed: string[]; remaining: number } {
    const all = tags ?? [];
    return {
        displayed: all.slice(0, maxTags),
        remaining: Math.max(0, all.length - maxTags),
    };
}
