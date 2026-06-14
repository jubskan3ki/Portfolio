import { mount } from '@vue/test-utils';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { computed, defineComponent, h, nextTick, ref } from 'vue';

import { useTabIndicator } from '@/composables/ui/useTabIndicator';

type TabKey = 'a' | 'b';

interface IndicatorApi {
    indicatorLeft: number;
    indicatorWidth: number;
    indicatorReady: boolean;
    setActive: (key: TabKey) => void;
}

function mountHost(opts: { listenResize?: boolean } = {}) {
    let api!: IndicatorApi;

    const Host = defineComponent({
        setup() {
            const trackRef = ref<HTMLElement | null>(null);
            const tabRefs = ref<Array<HTMLElement | null>>([]);
            const active = ref<TabKey>('a');
            const tabs = [
                { key: 'a' as const, label: 'A' },
                { key: 'b' as const, label: 'B' },
            ];

            const indicator = useTabIndicator({
                trackRef,
                tabRefs,
                activeIndex: computed(() => tabs.findIndex((t) => t.key === active.value)),
                tabs: () => tabs,
                mode: 'css-vars',
                listenResize: opts.listenResize ?? false,
            });

            api = {
                get indicatorLeft() {
                    return Number(indicator.indicatorStyle.value.transform.match(/-?\d+/)?.[0] ?? 0);
                },
                get indicatorWidth() {
                    return parseInt(indicator.indicatorStyle.value.width, 10) || 0;
                },
                get indicatorReady() {
                    return indicator.indicatorReady.value;
                },
                setActive(key) {
                    active.value = key;
                },
            };

            return () =>
                h('div', { ref: trackRef as never }, [
                    h(
                        'button',
                        {
                            ref: (el: unknown) => {
                                indicator.setTabRef(0, (el as HTMLElement) || null);
                            },
                        },
                        'A',
                    ),
                    h(
                        'button',
                        {
                            ref: (el: unknown) => {
                                indicator.setTabRef(1, (el as HTMLElement) || null);
                            },
                        },
                        'B',
                    ),
                ]);
        },
    });

    mount(Host, { attachTo: document.body });
    return api;
}

describe('useTabIndicator', () => {
    let rafQueue: FrameRequestCallback[];

    beforeEach(() => {
        rafQueue = [];
        // Synchronous rAF lets us run a single flush after each Vue update tick.
        vi.stubGlobal('requestAnimationFrame', ((cb: FrameRequestCallback) => {
            rafQueue.push(cb);
            return rafQueue.length;
        }) as typeof requestAnimationFrame);
        vi.stubGlobal('cancelAnimationFrame', vi.fn() as typeof cancelAnimationFrame);
    });

    afterEach(() => {
        vi.unstubAllGlobals();
    });

    function flushRaf() {
        const q = rafQueue;
        rafQueue = [];
        for (const cb of q) {
            cb(performance.now());
        }
    }

    it('does not coalesce multiple synchronous updates into more than one rAF', async () => {
        const api = mountHost();
        await nextTick();

        // Initial mount schedules one frame.
        expect(rafQueue.length).toBeGreaterThanOrEqual(1);

        const before = rafQueue.length;
        api.setActive('b');
        api.setActive('a');
        api.setActive('b');
        await nextTick();

        // Despite three changes, watchers should batch into at most one new pending frame.
        expect(rafQueue.length - before).toBeLessThanOrEqual(1);

        flushRaf();
        // happy-dom returns 0 for offsetWidth; the composable defers, so indicator never marks ready -
        // that's fine, we only assert the rAF coalescing contract here.
        expect(api.indicatorReady).toBe(false);
    });
});
