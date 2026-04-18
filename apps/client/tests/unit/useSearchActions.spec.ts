import { beforeEach, describe, expect, it, vi } from 'vitest';
import { defineComponent, h } from 'vue';

import { mount } from '@vue/test-utils';

vi.mock('vue-router', () => ({
    useRouter: () => ({
        push: vi.fn(),
    }),
}));

import { useSearchActions } from '@/composables/data/useSearchActions';

function mountActions() {
    const Host = defineComponent({
        setup() {
            return useSearchActions();
        },
        render() {
            return h('div');
        },
    });
    const wrapper = mount(Host);
    return wrapper.vm as ReturnType<typeof useSearchActions>;
}

describe('useSearchActions', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('exposes the expected action ids', () => {
        const { actions } = mountActions();
        const ids = actions.map((a) => a.id);
        expect(ids).toContain('nav-blog');
        expect(ids).toContain('nav-projects');
        expect(ids).toContain('nav-stacks');
        expect(ids).toContain('nav-contact');
        expect(ids).toContain('copy-email');
        expect(ids).toContain('ext-github');
        expect(ids).toContain('ext-linkedin');
    });

    it('copy-email calls navigator.clipboard.writeText', async () => {
        const writeText = vi.fn().mockResolvedValue(undefined);
        Object.defineProperty(globalThis, 'navigator', {
            configurable: true,
            value: { clipboard: { writeText } },
        });

        const { actions, run } = mountActions();
        const copyEmail = actions.find((a) => a.id === 'copy-email');
        expect(copyEmail).toBeDefined();

        await run(copyEmail!);
        expect(writeText).toHaveBeenCalledOnce();
        expect(writeText.mock.calls[0]?.[0]).toMatch(/@/);
    });

    it('external action opens window without navigating', async () => {
        const openSpy = vi.fn();
        Object.defineProperty(globalThis, 'window', {
            configurable: true,
            value: { open: openSpy },
        });

        const { actions, run } = mountActions();
        const github = actions.find((a) => a.id === 'ext-github');
        await run(github!);

        expect(openSpy).toHaveBeenCalledOnce();
        expect(openSpy.mock.calls[0]?.[0]).toContain('github.com');
        expect(openSpy.mock.calls[0]?.[1]).toBe('_blank');
    });
});
