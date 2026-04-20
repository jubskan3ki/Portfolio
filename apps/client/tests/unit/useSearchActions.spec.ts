import { mount } from '@vue/test-utils';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { defineComponent, h } from 'vue';

import { useSearchActions } from '@/composables/data/useSearchActions';

vi.mock('vue-router', () => ({
    useRouter: () => ({
        push: vi.fn(),
    }),
}));

function mountActions() {
    let api!: ReturnType<typeof useSearchActions>;
    const Host = defineComponent({
        setup() {
            api = useSearchActions();
            return () => h('div');
        },
    });
    mount(Host);
    return api;
}

describe('useSearchActions', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('exposes the expected action ids', () => {
        const { actions } = mountActions();
        const ids = actions.value.map((a) => a.id);
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
        const copyEmail = actions.value.find((a) => a.id === 'copy-email');
        expect(copyEmail).toBeDefined();
        if (!copyEmail) {
            return;
        }

        await run(copyEmail);
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
        const github = actions.value.find((a) => a.id === 'ext-github');
        expect(github).toBeDefined();
        if (!github) {
            return;
        }

        await run(github);
        expect(openSpy).toHaveBeenCalledOnce();
        expect(openSpy.mock.calls[0]?.[0]).toContain('github.com');
        expect(openSpy.mock.calls[0]?.[1]).toBe('_blank');
    });
});
