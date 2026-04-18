import { useLocalStorage } from '@vueuse/core';
import { computed } from 'vue';

import type { SearchResult } from '@/types/config/search';

const QUERY_KEY = 'portfolio.search.history.queries';
const ITEM_KEY = 'portfolio.search.history.items';
const MAX_QUERIES = 5;
const MAX_ITEMS = 5;

// Minimal shape stored for history items — keeps localStorage footprint low
// and decouples persistence from API schema drift.
export interface HistoryItem {
    id: number | string;
    type: string;
    title: string;
    subtitle?: string;
    icon: string;
    link: string;
}

export function useSearchHistory() {
    const queries = useLocalStorage<string[]>(QUERY_KEY, []);
    const items = useLocalStorage<HistoryItem[]>(ITEM_KEY, []);

    function recordQuery(query: string) {
        const trimmed = query.trim();
        if (trimmed.length < 2) {
            return;
        }
        const existing = queries.value.filter((q) => q.toLowerCase() !== trimmed.toLowerCase());
        queries.value = [trimmed, ...existing].slice(0, MAX_QUERIES);
    }

    function recordItem(result: SearchResult) {
        const historyItem: HistoryItem = {
            id: result.id,
            type: result.type,
            title: result.title,
            subtitle: result.subtitle,
            icon: result.icon,
            link: result.link,
        };
        const existing = items.value.filter((i) => !(i.id === historyItem.id && i.type === historyItem.type));
        items.value = [historyItem, ...existing].slice(0, MAX_ITEMS);
    }

    function clearHistory() {
        queries.value = [];
        items.value = [];
    }

    const hasHistory = computed(() => queries.value.length > 0 || items.value.length > 0);

    return {
        queries,
        items,
        hasHistory,
        recordQuery,
        recordItem,
        clearHistory,
    };
}
