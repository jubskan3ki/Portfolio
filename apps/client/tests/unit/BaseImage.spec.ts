import { mount } from '@vue/test-utils';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { defineComponent, h, nextTick } from 'vue';

import BaseImage from '@/components/base/BaseImage.vue';

const stubs = {
    BaseIcon: defineComponent({
        props: ['name', 'size'],
        setup: (p) => () => h('span', { class: 'stub-icon', 'data-name': p.name }),
    }),
    NuxtImg: defineComponent({
        props: ['src', 'alt'],
        setup: (p) => () => h('img', { src: p.src, alt: p.alt }),
    }),
};

describe('BaseImage', () => {
    beforeEach(() => {
        vi.useFakeTimers();
    });

    afterEach(() => {
        vi.useRealTimers();
    });

    it('renders neither skeleton nor <img> when src is empty', async () => {
        const wrapper = mount(BaseImage, {
            props: { src: '', alt: 'fallback' },
            global: { stubs },
        });
        await nextTick();

        expect(wrapper.find('.base-image__skeleton').exists()).toBe(false);
        expect(wrapper.find('.base-image__placeholder').exists()).toBe(false);
        expect(wrapper.find('img').exists()).toBe(false);
        expect(wrapper.find('.base-image__error').exists()).toBe(true);
    });

    it('falls back to error state after the 5s safety timeout when the image never loads', async () => {
        const wrapper = mount(BaseImage, {
            props: { src: 'https://example.com/never-loads.jpg', alt: 'stalled' },
            global: { stubs },
        });
        await nextTick();

        expect(wrapper.find('.base-image__skeleton').exists()).toBe(true);
        expect(wrapper.find('.base-image__error').exists()).toBe(false);

        vi.advanceTimersByTime(5000);
        await nextTick();

        expect(wrapper.find('.base-image__skeleton').exists()).toBe(false);
        expect(wrapper.find('.base-image__error').exists()).toBe(true);
        expect(wrapper.emitted('error')?.[0]).toEqual(['timeout']);
    });
});
