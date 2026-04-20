import AxeBuilder from '@axe-core/playwright';
import { test as base, expect } from '@playwright/test';

interface TestFixtures {
    makeAxe: () => AxeBuilder;
}

export const test = base.extend<TestFixtures>({
    makeAxe: async ({ page }, use) => {
        const factory = () =>
            new AxeBuilder({ page })
                // WCAG 2.1 AA baseline + best practices
                .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'best-practice']);
        await use(factory);
    },

    context: async ({ browser }, use) => {
        const context = await browser.newContext({
            reducedMotion: 'reduce',
            colorScheme: 'light',
        });
        await use(context);
        await context.close();
    },
});

export { expect };
