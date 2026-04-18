import { beforeEach, describe, expect, it } from 'vitest';
import { defineComponent, h } from 'vue';

import { mount } from '@vue/test-utils';

import { useSearchHistory, type HistoryItem } from '@/composables/data/useSearchHistory';

// useLocalStorage (VueUse) needs a Vue effect scope to work correctly in tests.
// We mount a tiny host component, pull the composable off `vm.$options` and
// assert on the reactive state + methods.
function mountHistory() {
    const Host = defineComponent({
        setup() {
            return useSearchHistory();
        },
        render() {
            return h('div');
        },
    });
    const wrapper = mount(Host);
    return wrapper.vm as ReturnType<typeof useSearchHistory>;
}

describe('useSearchHistory', () => {
    beforeEach(() => {
        localStorage.clear();
    });

    it('records a new query at the top and caps to 5', () => {
        const h = mountHistory();
        ['one', 'two', 'three', 'four', 'five', 'six'].forEach((q) => h.recordQuery(q));
        expect(h.queries).toHaveLength(5);
        expect(h.queries[0]).toBe('six');
        expect(h.queries).not.toContain('one');
    });

    it('de-duplicates queries case-insensitively and bumps to the top', () => {
        const h = mountHistory();
        h.recordQuery('Vue');
        h.recordQuery('react');
        h.recordQuery('vue');
        expect(h.queries).toEqual(['vue', 'react']);
    });

    it('ignores queries shorter than 2 characters', () => {
        const h = mountHistory();
        h.recordQuery(' ');
        h.recordQuery('a');
        h.recordQuery('ok');
        expect(h.queries).toEqual(['ok']);
    });

    it('records items, de-duplicates by (type, id), and caps to 5', () => {
        const h = mountHistory();
        const mkItem = (id: number, title = `Item ${id}`): HistoryItem => ({
            id,
            type: 'article',
            title,
            icon: 'file-text',
            link: `/blog/a-${id}`,
        });
        for (let i = 1; i <= 7; i++) {
            h.recordItem(mkItem(i));
        }
        expect(h.items).toHaveLength(5);
        expect(h.items[0]?.id).toBe(7);

        h.recordItem(mkItem(3, 'Item 3 updated'));
        const ids = h.items.map((i) => i.id);
        expect(ids[0]).toBe(3);
        expect(ids.filter((id) => id === 3)).toHaveLength(1);
    });

    it('clearHistory empties both queries and items', () => {
        const h = mountHistory();
        h.recordQuery('hello');
        h.recordItem({
            id: 1,
            type: 'project',
            title: 'x',
            icon: 'folder',
            link: '/projects/x',
        });
        expect(h.hasHistory).toBe(true);
        h.clearHistory();
        expect(h.queries).toEqual([]);
        expect(h.items).toEqual([]);
        expect(h.hasHistory).toBe(false);
    });
});
