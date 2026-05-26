import { mount } from '@vue/test-utils';
import { beforeEach, describe, expect, it } from 'vitest';
import { defineComponent, h } from 'vue';
import type { HistoryItem } from '@/composables/data/useSearchHistory';
import { useSearchHistory } from '@/composables/data/useSearchHistory';

function mountHistory() {
    let api!: ReturnType<typeof useSearchHistory>;
    const Host = defineComponent({
        setup() {
            api = useSearchHistory();
            return () => h('div');
        },
    });
    mount(Host);
    return api;
}

describe('useSearchHistory', () => {
    beforeEach(() => {
        localStorage.clear();
    });

    it('records a new query at the top and caps to 5', () => {
        const api = mountHistory();
        for (const q of ['one', 'two', 'three', 'four', 'five', 'six']) {
            api.recordQuery(q);
        }
        expect(api.queries.value).toHaveLength(5);
        expect(api.queries.value[0]).toBe('six');
        expect(api.queries.value).not.toContain('one');
    });

    it('de-duplicates queries case-insensitively and bumps to the top', () => {
        const api = mountHistory();
        api.recordQuery('Vue');
        api.recordQuery('react');
        api.recordQuery('vue');
        expect(api.queries.value).toEqual(['vue', 'react']);
    });

    it('ignores queries shorter than 2 characters', () => {
        const api = mountHistory();
        api.recordQuery(' ');
        api.recordQuery('a');
        api.recordQuery('ok');
        expect(api.queries.value).toEqual(['ok']);
    });

    it('records items, de-duplicates by (type, id), and caps to 5', () => {
        const api = mountHistory();
        const mkItem = (id: number, title = `Item ${id}`): HistoryItem => ({
            id,
            type: 'article',
            title,
            icon: 'file-text',
            link: `/blog/a-${id}`,
        });
        for (let i = 1; i <= 7; i++) {
            api.recordItem(mkItem(i));
        }
        expect(api.items.value).toHaveLength(5);
        expect(api.items.value[0]?.id).toBe(7);

        api.recordItem(mkItem(3, 'Item 3 updated'));
        const ids = api.items.value.map((i) => i.id);
        expect(ids[0]).toBe(3);
        expect(ids.filter((id) => id === 3)).toHaveLength(1);
    });

    it('clearHistory empties both queries and items', () => {
        const api = mountHistory();
        api.recordQuery('hello');
        api.recordItem({
            id: 1,
            type: 'project',
            title: 'x',
            icon: 'folder',
            link: '/projects/x',
        });
        expect(api.hasHistory.value).toBe(true);
        api.clearHistory();
        expect(api.queries.value).toEqual([]);
        expect(api.items.value).toEqual([]);
        expect(api.hasHistory.value).toBe(false);
    });
});
