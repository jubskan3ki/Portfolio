import { describe, expect, it, vi } from 'vitest';

import { useContactFaqSeo } from '@/composables/seo/useContactFaqSeo';

// Stub the auto-imported Nuxt helpers so the composable runs outside Nuxt.
const schemaCapture = { calls: [] as unknown[] };

vi.stubGlobal('useSchemaOrg', (input: unknown) => {
    schemaCapture.calls.push(input);
});
vi.stubGlobal('defineWebPage', (input: unknown) => input);

describe('useContactFaqSeo', () => {
    it('returns a non-empty FAQ list', () => {
        const { items } = useContactFaqSeo();
        expect(items.length).toBeGreaterThanOrEqual(5);
        for (const item of items) {
            expect(item.question).toBeTruthy();
            expect(item.answer).toBeTruthy();
        }
    });

    it('emits a FAQPage JSON-LD with matching Question/Answer entries', () => {
        schemaCapture.calls.length = 0;
        const { items } = useContactFaqSeo();
        expect(schemaCapture.calls).toHaveLength(1);
        const schemas = schemaCapture.calls[0] as unknown[];
        expect(Array.isArray(schemas)).toBe(true);
        const page = schemas[0] as { '@type': string; mainEntity: unknown[] };
        expect(page['@type']).toBe('FAQPage');
        expect(Array.isArray(page.mainEntity)).toBe(true);
        expect(page.mainEntity).toHaveLength(items.length);
        const first = page.mainEntity[0] as {
            '@type': string;
            name: string;
            acceptedAnswer: { '@type': string; text: string };
        };
        expect(first['@type']).toBe('Question');
        expect(first.acceptedAnswer['@type']).toBe('Answer');
        expect(first.name).toBe(items[0]?.question);
    });
});
