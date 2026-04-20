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

    const getCategoryCount = (categoryKey: string): number => {
        if (categoryKey === 'all') {
            return allStacks.value.length;
        }
        const cats = extractCategories(categoriesData.value);
        const cat = cats.find((c) => c.name.toLowerCase() === categoryKey);
        if (!cat) {
            return 0;
        }
        return allStacks.value.filter((s) => s.category === cat.name || s.category === String(cat.id)).length;
    };

    const availableTabs = computed(() => {
        if (allStacks.value.length === 0 && !stacksLoading.value) {
            return [];
        }

        const cats = extractCategories(categoriesData.value);
        const categoriesWithData = new Set<string>();

        allStacks.value.forEach((stack) => {
            const cat = cats.find((c) => c.name === stack.category || String(c.id) === stack.category);
            if (cat) {
                categoriesWithData.add(cat.name.toLowerCase());
            }
        });

        const tabs = [
            {
                key: 'all',
                label: `Toutes (${allStacks.value.length})`,
                icon: STACK_CATEGORY_ICONS['all'] || 'layers',
            },
        ];

        cats.forEach((cat) => {
            const key = cat.name.toLowerCase();
            if (categoriesWithData.has(key)) {
                const count = getCategoryCount(key);
                const label = STACK_CATEGORY_LABELS[key] || cat.name.charAt(0).toUpperCase() + cat.name.slice(1);
                tabs.push({
                    key,
                    label: `${label} (${count})`,
                    icon: STACK_CATEGORY_ICONS[key] || 'code',
                });
            }
        });

        return tabs;
    });

    const filteredStacks = computed(() => {
        let stacks = allStacks.value;

        if (isSearchMode.value && searchQuery.value.trim()) {
            const query = searchQuery.value.toLowerCase().trim();
            stacks = stacks.filter(
                (s) =>
                    s.name.toLowerCase().includes(query)
                    || s.description?.toLowerCase().includes(query)
                    || s.tags?.some((t) => t.toLowerCase().includes(query))
                    || s.category?.toLowerCase().includes(query),
            );
        } else if (activeCategory.value !== 'all') {
            const cats = extractCategories(categoriesData.value);
            const cat = cats.find((c) => c.name.toLowerCase() === activeCategory.value);
            if (cat) {
                stacks = stacks.filter((s) => s.category === cat.name || s.category === String(cat.id));
            }
        }

        return stacks;
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

        const cats = extractCategories(categoriesData.value);
        const sections: Array<{ key: string; label: string; icon: string; stacks: Stack[] }> = [];

        cats.forEach((cat) => {
            const key = cat.name.toLowerCase();
            const categoryStacks = allStacks.value.filter(
                (s) => s.category === cat.name || s.category === String(cat.id),
            );

            if (categoryStacks.length > 0) {
                sections.push({
                    key,
                    label: STACK_CATEGORY_LABELS[key] || cat.name,
                    icon: STACK_CATEGORY_ICONS[key] || 'code',
                    stacks: categoryStacks,
                });
            }
        });

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
