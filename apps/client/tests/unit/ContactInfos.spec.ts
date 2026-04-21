import { mount } from '@vue/test-utils';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { defineComponent, h, ref } from 'vue';

import ContactInfos from '@/components/feature/contact/ContactInfos.vue';

vi.mock('@/services/api/modules/contact', () => ({
    contactApi: {
        getInfo: vi.fn(),
    },
}));

const stubs = {
    BaseIcon: defineComponent({
        props: ['name', 'size'],
        setup: (p) => () => h('span', { class: 'stub-icon', 'data-name': p.name }),
    }),
    BaseLink: defineComponent({
        props: ['to'],
        setup: (p, { slots }) => () => h('a', { href: p.to }, slots.default?.()),
    }),
};

describe('ContactInfos — rendering driven by site settings (same source as footer)', () => {
    it('renders address, email, phone and social links when settings are populated', () => {
        const wrapper = mount(ContactInfos, {
            props: {
                address: 'Paris, France',
                email: 'juba@example.com',
                phone: '+33 6 95 21 71 97',
                socialLinks: [
                    { name: 'LinkedIn', icon: 'linkedin', url: 'https://www.linkedin.com/in/juba-aitadda/' },
                    { name: 'GitHub', icon: 'github', url: 'https://github.com/jubskan3ki' },
                ],
            },
            global: { stubs },
        });

        expect(wrapper.text()).toContain('Paris, France');
        expect(wrapper.text()).toContain('juba@example.com');
        expect(wrapper.text()).toContain('+33 6 95 21 71 97');
        expect(wrapper.text()).toContain('LinkedIn');
        expect(wrapper.text()).toContain('GitHub');

        const links = wrapper.findAll('.contact-infos__social-btn').map((n) => n.attributes('href'));
        expect(links).toContain('https://www.linkedin.com/in/juba-aitadda/');
        expect(links).toContain('https://github.com/jubskan3ki');
    });

    it('hides each item entirely when its value is empty (no "null" placeholder)', () => {
        const wrapper = mount(ContactInfos, {
            props: { address: '', email: '', phone: '', socialLinks: [] },
            global: { stubs },
        });

        expect(wrapper.findAll('.contact-infos__item')).toHaveLength(0);
        expect(wrapper.find('.contact-infos__social').exists()).toBe(false);
        expect(wrapper.text()).not.toContain('null');
        expect(wrapper.text()).not.toContain('undefined');
    });
});

describe('useSiteSettings — shared source of truth feeding both footer and contact-infos', () => {
    afterEach(() => {
        vi.unstubAllGlobals();
        vi.resetModules();
    });

    it('maps the contact info API response to the shape consumed by footer and contact-infos', async () => {
        vi.stubGlobal(
            'useAsyncData',
            async (_key: string, handler: () => Promise<unknown>, options: { transform?: (v: unknown) => unknown; default?: () => unknown }) => {
                const raw = (await handler()) ?? options?.default?.();
                const value = options?.transform ? options.transform(raw) : raw;
                return {
                    data: ref(value),
                    refresh: vi.fn(),
                    pending: ref(false),
                    error: ref(null),
                };
            },
        );

        const { contactApi } = await import('@/services/api/modules/contact');
        (contactApi.getInfo as ReturnType<typeof vi.fn>).mockResolvedValue({
            id: 1,
            email: 'juba@example.com',
            phone: '+33 6 95 21 71 97',
            bio: 'Dev fullstack',
            address: { city: 'Paris', country: 'France', street: '', zipCode: '' },
            socialMedia: {
                linkedin: 'https://www.linkedin.com/in/juba-aitadda/',
                github: 'https://github.com/jubskan3ki',
                medium: '',
            },
            availability: { status: 'available', message: 'Ouvert aux missions' },
        });

        const { useSiteSettings } = await import('@/composables/data/useSiteSettings');
        const { settings } = await useSiteSettings();

        expect(settings.value.email).toBe('juba@example.com');
        expect(settings.value.phone).toBe('+33 6 95 21 71 97');
        expect(settings.value.addressCity).toBe('Paris');
        expect(settings.value.addressCountry).toBe('France');
        expect(settings.value.socialLinkedin).toBe('https://www.linkedin.com/in/juba-aitadda/');
        expect(settings.value.socialGithub).toBe('https://github.com/jubskan3ki');
        expect(settings.value.isAvailable).toBe(true);
    });

    it('falls back to the hardcoded defaults when the API returns no data (no empty placeholders)', async () => {
        vi.stubGlobal(
            'useAsyncData',
            async (_key: string, _handler: () => Promise<unknown>, options: { transform?: (v: unknown) => unknown }) => ({
                data: ref(options?.transform ? options.transform(null) : null),
                refresh: vi.fn(),
                pending: ref(false),
                error: ref(null),
            }),
        );

        const { useSiteSettings, DEFAULT_SETTINGS } = await import('@/composables/data/useSiteSettings');
        const { settings } = await useSiteSettings();

        expect(settings.value.email).toBe(DEFAULT_SETTINGS.email);
        expect(settings.value.phone).toBe(DEFAULT_SETTINGS.phone);
        expect(settings.value.addressCity).toBe(DEFAULT_SETTINGS.addressCity);
        expect(settings.value.addressCountry).toBe(DEFAULT_SETTINGS.addressCountry);
        expect(settings.value.socialLinkedin).toBe(DEFAULT_SETTINGS.socialLinkedin);
        expect(settings.value.socialGithub).toBe(DEFAULT_SETTINGS.socialGithub);
        expect(settings.value.bio).toBe(DEFAULT_SETTINGS.bio);
    });
});
