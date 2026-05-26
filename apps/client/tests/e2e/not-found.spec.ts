import { expect, test } from './fixtures';

const SKIP_BACKEND = !process.env.E2E_RUN_BACKEND_TESTS;

test.describe('404 routing', () => {
    test('unknown route returns 404 and renders error.vue', async ({ page }) => {
        const res = await page.goto('/this-route-does-not-exist');
        expect(res?.status()).toBe(404);

        // error.vue uses an h1 (a11y: unique top-level heading per page).
        const h1 = page.locator('h1.error-page__title');
        await expect(h1).toBeVisible();
        await expect(h1).toHaveText(/Page introuvable/i);

        // 404 code prominently shown.
        await expect(page.locator('.error-page__code')).toHaveText('404');
    });

    test('error.vue exposes a skip-to-content link and a main landmark', async ({ page }) => {
        const res = await page.goto('/another-missing-route');
        expect(res?.status()).toBe(404);

        const skip = page.locator('a.skip-link');
        await expect(skip).toHaveAttribute('href', '#error-main');

        const main = page.locator('main#error-main');
        await expect(main).toBeVisible();
    });

    test('error.vue offers a way back to the home page', async ({ page }) => {
        await page.goto('/foo');

        const homeLink = page.locator('.error-page__actions a[href="/"]');
        await expect(homeLink).toBeVisible();
        await expect(homeLink).toContainText(/Accueil/i);
    });

    test('error.vue is marked noindex,nofollow to keep error URLs out of SERPs', async ({ page }) => {
        await page.goto('/this-page-does-not-exist');
        const robots = await page.locator('meta[name="robots"]').getAttribute('content');
        expect(robots).toMatch(/noindex/i);
        expect(robots).toMatch(/nofollow/i);
    });
});

test.describe(SKIP_BACKEND ? 'dynamic slug 404 (skipped | set E2E_RUN_BACKEND_TESTS=1)' : 'dynamic slug 404', () => {
    test.skip(SKIP_BACKEND, 'Requires a running backend at NUXT_PUBLIC_API_BASE that returns 404 for unknown slugs');

    for (const path of ['/projects/inexistant-test-slug', '/stacks/inexistant-test-slug', '/blog/inexistant-test-slug']) {
        test(`${path} surfaces a 4xx/5xx (never 200) and renders error.vue`, async ({ page }) => {
            const res = await page.goto(path);
            expect(res?.status()).not.toBe(200);
            expect(res?.status()).toBeGreaterThanOrEqual(400);
            await expect(page.locator('h1.error-page__title')).toBeVisible();
        });
    }
});
