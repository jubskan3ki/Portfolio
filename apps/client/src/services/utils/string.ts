/**
 * Converts text to a URL-friendly slug.
 * Handles diacritics (é→e, ñ→n), replaces non-alphanumeric chars with hyphens.
 */
export function slugify(text: string): string {
    return text
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/(^-|-$)/g, '');
}
