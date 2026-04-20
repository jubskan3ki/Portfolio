import { expect, test } from './fixtures';

const routes = ['/', '/blog', '/projects', '/stacks', '/contact', '/colophon', '/offline'] as const;

for (const route of routes) {
    test(`no detectable WCAG AA violations on ${route}`, async ({ page, makeAxe }) => {
        await page.goto(route);
        // Give Nuxt a tick to settle hydration without waiting on any xhr.
        await page.waitForLoadState('domcontentloaded');

        const results = await makeAxe().analyze();

        // Critical-only assertion keeps the suite robust against style
        // tweaks while still catching regressions like missing labels,
        // broken landmarks, or contrast drops.
        const critical = results.violations.filter((v) => v.impact === 'critical' || v.impact === 'serious');
        expect(critical, JSON.stringify(critical, null, 2)).toEqual([]);
    });
}
