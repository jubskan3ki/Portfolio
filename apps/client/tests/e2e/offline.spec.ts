import { expect, test } from './fixtures';

test.describe('offline fallback page', () => {
    test('renders the offline heading and actions', async ({ page }) => {
        await page.goto('/offline');

        await expect(page.getByRole('heading', { name: 'Hors ligne', level: 1 })).toBeVisible();
        await expect(page.getByRole('button', { name: /Réessayer/i })).toBeVisible();
        await expect(page.getByRole('link', { name: /Articles en cache/i })).toHaveAttribute('href', '/blog');
    });

    test('the retry button navigates back to the current URL', async ({ page }) => {
        await page.goto('/offline');

        const button = page.getByRole('button', { name: /Réessayer/i });
        await Promise.all([page.waitForURL('**/offline'), button.click()]);
        await expect(page.getByRole('heading', { name: 'Hors ligne', level: 1 })).toBeVisible();
    });
});
