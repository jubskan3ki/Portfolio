import { defineConfig, devices } from '@playwright/test';

// Backend mocked at Nitro proxy level (tests/e2e/fixtures/api-mock.ts) | no Django/Postgres needed.
const BASE_URL = process.env.E2E_BASE_URL ?? 'http://127.0.0.1:4173';
const REUSE_SERVER = !process.env.CI;

export default defineConfig({
    testDir: './tests/e2e',
    fullyParallel: true,
    forbidOnly: !!process.env.CI,
    retries: process.env.CI ? 2 : 2,
    workers: process.env.CI ? 2 : undefined,
    reporter: process.env.CI ? [['github'], ['html', { open: 'never' }]] : 'list',

    use: {
        baseURL: BASE_URL,
        trace: 'on-first-retry',
        screenshot: 'only-on-failure',
        video: 'retain-on-failure',
    },

    projects: [
        {
            name: 'chromium',
            use: { ...devices['Desktop Chrome'] },
        },
    ],

    webServer: process.env.E2E_SKIP_WEBSERVER
        ? undefined
        : {
              command: 'pnpm preview:lhci',
              url: BASE_URL,
              reuseExistingServer: REUSE_SERVER,
              timeout: 120_000,
              stdout: 'ignore',
              stderr: 'pipe',
              env: {
                  NUXT_PUBLIC_API_BASE: process.env.NUXT_PUBLIC_API_BASE ?? BASE_URL,
                  NUXT_PUBLIC_WEB_VITALS_SAMPLE_RATE: '0',
              },
          },
});
