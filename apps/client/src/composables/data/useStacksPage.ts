import { computed } from 'vue';

import { STACK_CATEGORY_ICONS, STACK_CATEGORY_LABELS } from '@/config/stacks';

import type { Stack, StackCategory, UseStacksPageOptions } from '@/types/feature/stacks';

function extractCategories(data: unknown): StackCategory[] {
    if (!data) {
        return [];
    }
    if (Array.isArray(data)) {
        return data;
    }
    if (typeof data === 'object' && data !== null) {
        if ('data' in data && Array.isArray((data as { data: unknown }).data)) {
            return (data as { data: StackCategory[] }).data;
        }
        if ('categories' in data && Array.isArray((data as { categories: unknown }).categories)) {
            return (data as { categories: StackCategory[] }).categories;
        }
    }
    return [];
}

export function useStacksPage(options: UseStacksPageOptions) {
    const {
        stacksData,
        categoriesData,
        statsData,
        stacksLoading,
        categoriesLoading,
        stacksError,
        categoriesError,
        activeCategory,
        searchQuery,
        isSearchMode,
    } = options;

    const isLoading = computed(() => stacksLoading.value || categoriesLoading.value);
    const hasError = computed(() => stacksError.value || categoriesError.value);

    const allStacks = computed<Stack[]>(() => {
        const stacks = stacksData.value?.data ?? [];
        return [...stacks].sort((a, b) => (Number(b.level) || 0) - (Number(a.level) || 0));
    });

    const categorizedStacks = computed(() => {
        const cats = extractCategories(categoriesData.value);
        const keyByName = new Map<string, string>();
        const keyById = new Map<string, string>();
        for (const cat of cats) {
            const key = cat.name.toLowerCase();
            keyByName.set(cat.name, key);
            keyById.set(String(cat.id), key);
        }

        const byKey = new Map<string, Stack[]>();
        for (const stack of allStacks.value) {
            const raw = stack.category ?? '';
            const key = keyByName.get(raw) ?? keyById.get(String(raw));
            if (!key) {
                continue;
            }
            const list = byKey.get(key);
            if (list) {
                list.push(stack);
            } else {
                byKey.set(key, [stack]);
            }
        }

        return { cats, byKey };
    });

    const availableTabs = computed(() => {
        if (allStacks.value.length === 0 && !stacksLoading.value) {
            return [];
        }

        const { cats, byKey } = categorizedStacks.value;

        const tabs = [
            {
                key: 'all',
                label: `Toutes (${allStacks.value.length})`,
                icon: STACK_CATEGORY_ICONS.all || 'layers',
            },
        ];

        for (const cat of cats) {
            const key = cat.name.toLowerCase();
            const list = byKey.get(key);
            if (list && list.length > 0) {
                const label = STACK_CATEGORY_LABELS[key] || cat.name.charAt(0).toUpperCase() + cat.name.slice(1);
                tabs.push({
                    key,
                    label: `${label} (${list.length})`,
                    icon: STACK_CATEGORY_ICONS[key] || 'code',
                });
            }
        }

        return tabs;
    });

    const filteredStacks = computed(() => {
        if (isSearchMode.value && searchQuery.value.trim()) {
            const query = searchQuery.value.toLowerCase().trim();
            return allStacks.value.filter(
                (s) =>
                    s.name.toLowerCase().includes(query) ||
                    s.description?.toLowerCase().includes(query) ||
                    s.tags?.some((t) => t.toLowerCase().includes(query)) ||
                    s.category?.toLowerCase().includes(query),
            );
        }

        if (activeCategory.value !== 'all') {
            return categorizedStacks.value.byKey.get(activeCategory.value) ?? [];
        }

        return allStacks.value;
    });

    const showSections = computed(() => activeCategory.value === 'all' && !isSearchMode.value && !searchQuery.value);

    const activeCategoryLabel = computed(() => {
        const tab = availableTabs.value.find((t) => t.key === activeCategory.value);
        if (!tab) {
            return STACK_CATEGORY_LABELS[activeCategory.value] || activeCategory.value;
        }
        return tab.label.replace(/\s*\(\d+\)$/, '');
    });

    const activeCategoryIcon = computed(() => {
        return STACK_CATEGORY_ICONS[activeCategory.value] || 'code';
    });

    const stackSections = computed(() => {
        if (!showSections.value) {
            return [];
        }

        const { cats, byKey } = categorizedStacks.value;
        const sections: Array<{ key: string; label: string; icon: string; stacks: Stack[] }> = [];

        for (const cat of cats) {
            const key = cat.name.toLowerCase();
            const list = byKey.get(key);
            if (list && list.length > 0) {
                sections.push({
                    key,
                    label: STACK_CATEGORY_LABELS[key] || cat.name,
                    icon: STACK_CATEGORY_ICONS[key] || 'code',
                    stacks: list,
                });
            }
        }

        return sections;
    });

    const hasAnyData = computed(() => filteredStacks.value.length > 0 || stackSections.value.length > 0);

    const emptyStateTitle = computed(() => (isSearchMode.value ? 'Aucun résultat' : 'Aucun stack disponible'));

    const emptyStateDescription = computed(() =>
        isSearchMode.value
            ? `Aucun stack ne correspond à "${searchQuery.value}"`
            : 'Les stacks seront ajoutés prochainement.',
    );

    const contentKey = computed(() => (isSearchMode.value ? `search-${searchQuery.value}` : activeCategory.value));

    const heroStats = computed(() => {
        const data = statsData.value;
        return [
            { value: data?.totalStacks ?? allStacks.value.length, label: 'Stacks', icon: 'code' },
            { value: availableTabs.value.length - 1, label: 'Catégories', icon: 'layers' },
            { value: `${data?.averageProficiency ?? 85}%`, label: 'Maîtrise', icon: 'trending-up' },
        ];
    });

    return {
        isLoading,
        hasError,
        allStacks,
        availableTabs,
        filteredStacks,
        showSections,
        activeCategoryLabel,
        activeCategoryIcon,
        stackSections,
        hasAnyData,
        emptyStateTitle,
        emptyStateDescription,
        contentKey,
        heroStats,
    };
}
