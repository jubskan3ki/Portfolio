import { mount } from '@vue/test-utils';
import { beforeEach, describe, expect, it } from 'vitest';
import { defineComponent, h, nextTick } from 'vue';

import OfflineBadge from '@/components/ui/OfflineBadge.vue';

// Drive navigator.onLine directly: VueUse's useOnline() subscribes to
// the online/offline window events, so a CustomEvent dispatch flips the
// exposed ref without needing to mock the whole module.
function setOnline(value: boolean) {
    Object.defineProperty(window.navigator, 'onLine', {
        configurable: true,
        get: () => value,
    });
    window.dispatchEvent(new Event(value ? 'online' : 'offline'));
}

const stubs = {
    BaseIcon: defineComponent({
        props: ['name'],
        setup: (p) => () => h('span', { 'aria-hidden': 'true' }, p.name),
    }),
};

describe('OfflineBadge', () => {
    beforeEach(() => {
        setOnline(true);
    });

    it('stays hidden while online', () => {
        const wrapper = mount(OfflineBadge, { global: { stubs } });
        expect(wrapper.find('.offline-badge').exists()).toBe(false);
    });

    it('surfaces the badge once offline, with a polite live region', async () => {
        const wrapper = mount(OfflineBadge, { global: { stubs } });
        setOnline(false);
        await nextTick();

        const badge = wrapper.find('.offline-badge');
        expect(badge.exists()).toBe(true);
        expect(badge.attributes('role')).toBe('status');
        expect(badge.attributes('aria-live')).toBe('polite');
        expect(badge.text()).toContain('Mode hors ligne');
    });
});
