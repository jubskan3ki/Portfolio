import { expect, test } from './fixtures';

const EXPECTED_TOKEN = process.env.NUXT_PUBLIC_GOOGLE_SITE_VERIFICATION ?? '';

const ROUTES = ['/', '/blog', '/projects', '/stacks', '/this-route-does-not-exist-404'];

test.describe('google search console verification meta', () => {
    test.skip(!EXPECTED_TOKEN, 'NUXT_PUBLIC_GOOGLE_SITE_VERIFICATION not set — verification meta is opt-in');

    for (const route of ROUTES) {
        test(`is present on ${route}`, async ({ page }) => {
            await page.goto(route, { waitUntil: 'domcontentloaded' });
            const content = await page.locator('meta[name="google-site-verification"]').first().getAttribute('content');
            expect(content).toBe(EXPECTED_TOKEN);
        });
    }
});
