import { expect, test } from './fixtures';

test.describe.configure({ mode: 'serial' });

test.describe('command palette', () => {
    test('opens on input focus and displays the Actions group', async ({ page }) => {
        await page.goto('/', { waitUntil: 'networkidle' });
        const input = page.locator('.search-global input').first();
        await input.waitFor({ state: 'visible', timeout: 15_000 });
        await input.click();

        const dropdown = page.locator('.search-global__dropdown');
        await expect(dropdown).toBeVisible();

        await expect(dropdown.getByText(/Aller au blog/i)).toBeVisible();
        await expect(dropdown.getByText(/Copier mon email/i)).toBeVisible();
    });

    test('Escape key closes the dropdown', async ({ page }) => {
        await page.goto('/', { waitUntil: 'networkidle' });
        const input = page.locator('.search-global input').first();
        await input.waitFor({ state: 'visible', timeout: 15_000 });
        await input.click();

        const dropdown = page.locator('.search-global__dropdown');
        await expect(dropdown).toBeVisible();

        await page.keyboard.press('Escape');
        await expect(dropdown).not.toBeVisible();
    });

    test('selecting a navigation action routes client-side', async ({ page }) => {
        await page.goto('/', { waitUntil: 'networkidle' });
        const input = page.locator('.search-global input').first();
        await input.waitFor({ state: 'visible', timeout: 15_000 });
        await input.click();

        await page
            .getByRole('region', { name: /Actions rapides/i })
            .getByText(/Aller au blog/i)
            .click();

        await expect(page).toHaveURL(/\/blog\/?$/);
    });
});
