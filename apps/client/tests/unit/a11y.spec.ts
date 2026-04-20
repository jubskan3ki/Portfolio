import { mount } from '@vue/test-utils';
import { describe, expect, it } from 'vitest';
import { axe } from 'vitest-axe';
import { defineComponent, h } from 'vue';

import ContactFAQ from '@/components/feature/contact/ContactFAQ.vue';

describe('a11y: ContactFAQ', () => {
    it('has no detectable WCAG AA violations', async () => {
        const wrapper = mount(ContactFAQ, {
            props: {
                items: [
                    { question: 'Première question ?', answer: 'Première réponse complète.' },
                    { question: 'Deuxième question ?', answer: 'Deuxième réponse complète.' },
                ],
            },
            global: {
                stubs: {
                    BaseIcon: defineComponent({
                        props: ['name'],
                        setup(p) {
                            return () => h('span', { 'aria-hidden': 'true' }, p.name);
                        },
                    }),
                },
            },
        });

        const results = await axe(wrapper.element as Element, {
            rules: {
                // color-contrast requires a real layout engine; skip under happy-dom.
                'color-contrast': { enabled: false },
            },
        });
        expect(results.violations).toHaveLength(0);
    });
});
