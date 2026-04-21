import { expect, test } from '@playwright/test';

const SKIP = !process.env.E2E_RUN_BACKEND_TESTS;

test.describe(SKIP ? 'feeds (skipped | set E2E_RUN_BACKEND_TESTS=1)' : 'feeds', () => {
    test.skip(SKIP, 'Requires a running backend at NUXT_PUBLIC_API_BASE');

    test('/feed.xml returns an Atom feed', async ({ page }) => {
        const res = await page.request.get('/feed.xml');
        expect(res.status()).toBe(200);
        expect(res.headers()['content-type']).toMatch(/atom\+xml/);
        const body = await res.text();
        expect(body).toContain('<feed');
    });

    test('/feed.json returns a JSON Feed 1.1 document', async ({ page }) => {
        const res = await page.request.get('/feed.json');
        expect(res.status()).toBe(200);
        expect(res.headers()['content-type']).toMatch(/feed\+json/);
        const body = await res.json();
        expect(body.version).toMatch(/jsonfeed\.org\/version\/1\.1/);
    });
});
