import { describe, expect, it } from 'vitest';

import { extractErrorStatus } from '@/services/utils/errors';

describe('extractErrorStatus', () => {
    it('returns undefined for nullish input', () => {
        expect(extractErrorStatus(null)).toBeUndefined();
        expect(extractErrorStatus(undefined)).toBeUndefined();
    });

    it('returns undefined for primitives', () => {
        expect(extractErrorStatus('not found')).toBeUndefined();
        expect(extractErrorStatus(404)).toBeUndefined();
    });

    it('reads `status` from a plain ApiError shape', () => {
        const err = { code: 'NOT_FOUND', status: 404, message: 'not found', timestamp: 1 };
        expect(extractErrorStatus(err)).toBe(404);
    });

    it('reads `statusCode` from a Nuxt-style H3Error', () => {
        const err = { statusCode: 404, statusMessage: 'Not found', fatal: true };
        expect(extractErrorStatus(err)).toBe(404);
    });

    it('falls through to `cause` when the top-level error carries no status', () => {
        const inner = { status: 404, code: 'NOT_FOUND' };
        const wrapper = new Error('wrapped');
        (wrapper as Error & { cause?: unknown }).cause = inner;
        expect(extractErrorStatus(wrapper)).toBe(404);
    });

    it('walks several levels of nested causes', () => {
        const inner = { status: 503 };
        const middle = { cause: inner };
        const outer = { cause: middle };
        expect(extractErrorStatus(outer)).toBe(503);
    });

    it('gives up after a finite depth to avoid cycles', () => {
        const a: Record<string, unknown> = {};
        const b: Record<string, unknown> = { cause: a };
        a.cause = b;
        // No status anywhere; the function must terminate.
        expect(extractErrorStatus(a)).toBeUndefined();
    });
});
