import type { Route } from '@playwright/test';

import { expect, test } from './fixtures';

interface CapturedRequest {
    url: string;
    method: string;
    fields: Map<string, string[]>;
    hadFile: boolean;
}

async function captureMultipart(route: Route): Promise<CapturedRequest> {
    const req = route.request();
    const buffer = req.postDataBuffer();
    const headers = req.headers();
    const contentType = headers['content-type'] || '';
    const fields = new Map<string, string[]>();
    let hadFile = false;

    if (contentType.includes('multipart/form-data') && buffer) {
        const body = buffer.toString('latin1');
        const boundaryMatch = contentType.match(/boundary=([^;]+)/);
        if (boundaryMatch) {
            const boundary = `--${boundaryMatch[1]}`;
            const parts = body.split(boundary).slice(1, -1);
            for (const part of parts) {
                const headerEnd = part.indexOf('\r\n\r\n');
                if (headerEnd === -1) continue;
                const header = part.slice(0, headerEnd);
                const value = part.slice(headerEnd + 4, part.length - 2);
                const nameMatch = header.match(/name="([^"]+)"/);
                if (!nameMatch) continue;
                const name = nameMatch[1] as string;
                if (header.includes('filename=')) {
                    hadFile = true;
                    const existing = fields.get(name) || [];
                    existing.push(`<file:${value.length}b>`);
                    fields.set(name, existing);
                } else {
                    const existing = fields.get(name) || [];
                    existing.push(value);
                    fields.set(name, existing);
                }
            }
        }
    }

    return {
        url: req.url(),
        method: req.method(),
        fields,
        hadFile,
    };
}

function paginated<T>(items: T[]) {
    return {
        data: items,
        pagination: { total: items.length, page: 1, limit: 100, totalPages: 1 },
    };
}

async function pickOption(page: import('@playwright/test').Page, comboLabel: RegExp, optionLabel: string): Promise<void> {
    const combobox = page.getByRole('combobox', { name: comboLabel });
    await combobox.click();
    await page.getByRole('option', { name: optionLabel }).dispatchEvent('click');
}

async function mockAdminContext(page: import('@playwright/test').Page): Promise<void> {
    await page.addInitScript(() => {
        localStorage.setItem('portfolio.session.hint', '1');
    });

    // Mock auth: refresh token (POST) puis lecture du profil staff.
    await page.route('**/api/users/auth/refresh/', async (route) => {
        await route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify({ ok: true }),
        });
    });
    await page.route('**/api/users/profile/', async (route) => {
        await route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify({
                id: 1,
                email: 'admin@test.local',
                username: 'admin',
                isStaff: true,
                is_staff: true,
                isSuperuser: true,
                is_superuser: true,
            }),
        });
    });

    // Catalogues necessaires aux selects.
    await page.route('**/api/projects/categories/**', async (route) => {
        await route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify(paginated([{ id: 42, name: 'Web', slug: 'web' }])),
        });
    });
    await page.route('**/api/projects/statuses/**', async (route) => {
        await route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify(paginated([{ id: 1, name: 'Termine' }])),
        });
    });
    await page.route('**/api/stacks/?**', async (route) => {
        await route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify(paginated([{ id: 7, name: 'Vue', slug: 'vue', logo: '/media/vue.svg' }])),
        });
    });
    await page.route('**/api/stacks/categories/**', async (route) => {
        await route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify(paginated([{ id: 1, name: 'Framework' }])),
        });
    });
    await page.route('**/api/articles/categories/**', async (route) => {
        await route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify(paginated([{ id: 3, name: 'Tutoriel', slug: 'tutoriel' }])),
        });
    });
    await page.route('**/api/articles/tags/**', async (route) => {
        await route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify(paginated([{ id: 5, name: 'vue' }])),
        });
    });
    await page.route('**/api/experiences/types/**', async (route) => {
        await route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify(paginated([{ id: 2, name: 'Experience pro' }])),
        });
    });
}

// PNG 1x1 minimal pour tester l'upload.
const TINY_PNG = Buffer.from(
    '89504e470d0a1a0a0000000d49484452000000010000000108020000009077533de0000000c4944415478da626400000000ff0300000000000000000000000000000000000000004949454e44ae426082',
    'hex',
);

// ─── PROJECTS ─────────────────────────────────────────────────────────────────

test.describe('admin projects/create', () => {
    test.beforeEach(async ({ page }) => {
        await mockAdminContext(page);
    });

    test('POST /api/projects/ envoie title/slug/description/category et links en JSON', async ({ page }) => {
        let captured: CapturedRequest | null = null;
        await page.route('**/api/projects/', async (route) => {
            if (route.request().method() === 'POST') {
                captured = await captureMultipart(route);
                await route.fulfill({
                    status: 201,
                    contentType: 'application/json',
                    body: JSON.stringify({ id: 1, slug: 'demo', title: 'Demo', image: '/media/projets/demo/demo.png' }),
                });
                return;
            }
            await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(paginated([])) });
        });

        await page.goto('/admin/projects/create');
        await page.getByLabel(/^Titre\s*\*?$/).fill('Demo');
        await page.getByLabel(/^Slug\s*\*?$/).fill('demo');
        await page.getByLabel(/^Description courte\s*\*?$/).fill('Une description.');
        await page.getByLabel(/^URL Démo\s*\*?$/).fill('https://demo.example.com');
        await pickOption(page, /Catégorie/, 'Web');

        await page.getByRole('button', { name: /Créer le projet/i }).click();

        await expect.poll(() => captured !== null, { timeout: 5000 }).toBe(true);
        const cap = captured as unknown as CapturedRequest;
        expect(cap.method).toBe('POST');
        expect(cap.fields.get('title')?.[0]).toBe('Demo');
        expect(cap.fields.get('slug')?.[0]).toBe('demo');
        expect(cap.fields.get('description')?.[0]).toBe('Une description.');
        const linksRaw = cap.fields.get('links')?.[0] ?? '';
        const links = linksRaw ? JSON.parse(linksRaw) : {};
        expect(links.demo).toBe('https://demo.example.com');
    });

    test('formulaire bloque sans titre / categorie (validation client)', async ({ page }) => {
        let posted = false;
        await page.route('**/api/projects/', async (route) => {
            if (route.request().method() === 'POST') {
                posted = true;
            }
            await route.fulfill({ status: 201, contentType: 'application/json', body: '{}' });
        });

        await page.goto('/admin/projects/create');
        await page.getByRole('button', { name: /Créer le projet/i }).click();

        await page.waitForTimeout(500);
        expect(posted).toBe(false);
    });
});

// ─── EXPERIENCES ──────────────────────────────────────────────────────────────

test.describe('admin experiences/create', () => {
    test.beforeEach(async ({ page }) => {
        await mockAdminContext(page);
    });

    test('POST envoie start_date/end_date en snake_case (regression principale)', async ({ page }) => {
        let captured: CapturedRequest | null = null;
        await page.route('**/api/experiences/', async (route) => {
            if (route.request().method() === 'POST') {
                captured = await captureMultipart(route);
                await route.fulfill({
                    status: 201,
                    contentType: 'application/json',
                    body: JSON.stringify({ id: 1, title: 'x', startDate: '2024-01-01' }),
                });
                return;
            }
            await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(paginated([])) });
        });

        await page.goto('/admin/experiences/create');
        await page.getByLabel(/Titre du poste/).fill('Dev Full Stack');
        await page.getByLabel(/Entreprise|Établissement/).fill('Anthropic');
        await page.getByLabel(/^Localisation\s*\*?$/).fill('Paris');
        await page.getByLabel(/^Date de début\s*\*?$/).fill('2024-01-15');
        await page.getByLabel(/^Description\s*\*?$/).fill('Mission backend Django + frontend Vue.');
        await pickOption(page, /Type/, 'Experience pro');

        await page.getByRole('button', { name: /Créer l'expérience/i }).click();

        await expect.poll(() => captured !== null, { timeout: 5000 }).toBe(true);
        const cap = captured as unknown as CapturedRequest;
        // PRINCIPAL : le frontend envoie start_date en snake_case.
        expect(cap.fields.get('start_date')?.[0]).toBe('2024-01-15');
        expect(cap.fields.get('title')?.[0]).toBe('Dev Full Stack');
        expect(cap.fields.get('company')?.[0]).toBe('Anthropic');
    });
});

// ─── STACKS ───────────────────────────────────────────────────────────────────

test.describe('admin stacks/create', () => {
    test.beforeEach(async ({ page }) => {
        await mockAdminContext(page);
    });

    test('POST envoie name/category/level + logo (multipart)', async ({ page }) => {
        let captured: CapturedRequest | null = null;
        await page.route('**/api/stacks/', async (route) => {
            if (route.request().method() === 'POST') {
                captured = await captureMultipart(route);
                await route.fulfill({
                    status: 201,
                    contentType: 'application/json',
                    body: JSON.stringify({ id: 99, slug: 'vue-3', name: 'Vue 3', logo: '/media/stacks/vue/vue.png' }),
                });
                return;
            }
            await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(paginated([])) });
        });

        await page.goto('/admin/stacks/create');
        await page.getByLabel(/Nom de la technologie/).fill('Vue 3');
        await page.getByLabel(/Niveau de maîtrise/).fill('85');
        await pickOption(page, /Catégorie/, 'Framework');

        const fileInput = page.locator('input[type="file"]').first();
        await fileInput.setInputFiles({
            name: 'vue.png',
            mimeType: 'image/png',
            buffer: TINY_PNG,
        });

        await page.getByRole('button', { name: /Créer la stack/i }).click();

        await expect.poll(() => captured !== null, { timeout: 5000 }).toBe(true);
        const cap = captured as unknown as CapturedRequest;
        expect(cap.fields.get('name')?.[0]).toBe('Vue 3');
        // proficiency=85 -> level=4.2 (85/20).
        const level = Number(cap.fields.get('level')?.[0] ?? '0');
        expect(level).toBeGreaterThan(4);
        expect(level).toBeLessThanOrEqual(4.3);
        expect(cap.hadFile).toBe(true);
    });
});

// ─── ARTICLES ─────────────────────────────────────────────────────────────────

test.describe('admin articles/create', () => {
    test.beforeEach(async ({ page }) => {
        await mockAdminContext(page);
    });

    test('POST envoie title/slug/excerpt/content + is_published', async ({ page }) => {
        let captured: CapturedRequest | null = null;
        await page.route('**/api/articles/', async (route) => {
            if (route.request().method() === 'POST') {
                captured = await captureMultipart(route);
                await route.fulfill({
                    status: 201,
                    contentType: 'application/json',
                    body: JSON.stringify({ id: 1, slug: 'my-post', title: 'My post', image: '/media/articles/my-post/img.png' }),
                });
                return;
            }
            await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(paginated([])) });
        });

        await page.goto('/admin/articles/create');
        await page.getByLabel(/^Titre\s*\*?$/).fill('My post');
        await page.getByLabel(/^Slug\s*\*?$/).fill('my-post');
        await page.getByLabel(/Contenu/).fill('Un contenu en Markdown.');

        await page.getByRole('button', { name: /Créer l'article/i }).click();

        await expect.poll(() => captured !== null, { timeout: 5000 }).toBe(true);
        const cap = captured as unknown as CapturedRequest;
        expect(cap.fields.get('title')?.[0]).toBe('My post');
        expect(cap.fields.get('slug')?.[0]).toBe('my-post');
        expect(['true', 'false']).toContain(cap.fields.get('is_published')?.[0]);
    });
});
