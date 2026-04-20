import { expect, test } from './fixtures';

test.describe('home page', () => {
    test('renders title, nav and main landmark', async ({ page }) => {
        await page.goto('/');

        await expect(page).toHaveTitle(/Juba Ait-Adda/);
        await expect(page.locator('main#main-content')).toBeVisible();
        await expect(page.locator('a.skip-link')).toHaveAttribute('href', '#main-content');
    });

    test('skip link becomes focused on first Tab press', async ({ page }) => {
        await page.goto('/');
        await page.keyboard.press('Tab');
        const skip = page.locator('a.skip-link');
        await expect(skip).toBeFocused();
    });

    test('exposes dynamic OG image URL on article meta (when any)', async ({ page }) => {
        await page.goto('/');
        const ogImage = await page.locator('meta[property="og:image"]').first().getAttribute('content');
        expect(ogImage, 'og:image meta should be present').toBeTruthy();
    });
});
