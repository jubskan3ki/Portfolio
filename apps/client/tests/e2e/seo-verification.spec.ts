import { expect, test } from './fixtures';

const EXPECTED_TOKEN = 'q4wxKu9JSOg0DLhCDJIu-bbPW_Hz_hGXipe2ePrvNEQ';

// 404 path is intentionally tested to guarantee the verification meta is global,
// not scoped to a layout that 404 might bypass.
const ROUTES = ['/', '/blog', '/projects', '/stacks', '/this-route-does-not-exist-404'];

test.describe('google search console verification meta', () => {
    for (const route of ROUTES) {
        test(`is present on ${route}`, async ({ page }) => {
            await page.goto(route, { waitUntil: 'domcontentloaded' });
            const content = await page.locator('meta[name="google-site-verification"]').first().getAttribute('content');
            expect(content).toBe(EXPECTED_TOKEN);
        });
    }
});
