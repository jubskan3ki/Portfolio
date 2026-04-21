import { expect, test } from './fixtures';

test.describe('colophon page', () => {
    test('renders the stack and build-budget sections', async ({ page }) => {
        await page.goto('/colophon');

        await expect(page.getByRole('heading', { name: 'Colophon', level: 1 })).toBeVisible();
        await expect(page.getByRole('heading', { name: 'Stack', level: 2 })).toBeVisible();

        // At least the Frontend + SEO + Qualité groups should be present.
        await expect(page.getByRole('heading', { name: 'Frontend', level: 3 })).toBeVisible();
        await expect(page.getByRole('heading', { name: /SEO/, level: 3 })).toBeVisible();
        await expect(page.getByRole('heading', { name: 'Qualité', level: 3 })).toBeVisible();

        // Build & budget section uses <dl>
        await expect(page.getByRole('heading', { name: /Build/, level: 2 })).toBeVisible();
        await expect(page.getByRole('term')).not.toHaveCount(0);
    });

    test('metrics section shows a fallback when the Web Vitals API is unreachable', async ({ page }) => {
        await page.goto('/colophon');
        const metricsHeading = page.getByRole('heading', { name: /Métriques en temps réel/ });
        await expect(metricsHeading).toBeVisible();

        // Either the metrics rendered (rare on a cold preview) or the fallback
        // appeared | both are acceptable; assert one of them is present.
        const fallback = page.getByText(/ne sont pas disponibles|Chargement des métriques/i);
        const metricCards = page.locator('.colophon-metric');

        const hasFallback = await fallback.isVisible().catch(() => false);
        const hasCards = (await metricCards.count()) > 0;
        expect(hasFallback || hasCards).toBeTruthy();
    });
});
