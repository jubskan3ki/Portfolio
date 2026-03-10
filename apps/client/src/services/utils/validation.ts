// Validation utilities for route parameters and user input

const SLUG_PATTERN = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const MAX_SLUG_LENGTH = 100;

export function isValidSlug(slug: unknown): slug is string {
    if (typeof slug !== 'string') {
        return false;
    }
    if (!slug || slug.length === 0) {
        return false;
    }
    if (slug.length > MAX_SLUG_LENGTH) {
        return false;
    }
    return SLUG_PATTERN.test(slug);
}
