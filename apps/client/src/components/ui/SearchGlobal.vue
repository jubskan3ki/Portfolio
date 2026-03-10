<template>
    <div ref="containerRef" class="search-global" :class="{ 'search-global--compact': compact }">
        <GlobalSearchInput
            ref="searchInputRef"
            v-model="searchQuery"
            :placeholder="placeholder"
            :compact="compact"
            :loading="isLoading"
            :is-expanded="isOpen"
            @focus="open"
            @clear="clearSearch"
            @keydown="handleKeydown"
        />

        <Transition name="fade-slide">
            <div v-if="isOpen && searchQuery.length >= 2" class="search-global__dropdown">
                <SearchFilters
                    v-if="hasResults"
                    :groups="filterGroups"
                    :active-filter="activeFilter"
                    class="search-global__filters"
                    @toggle="toggleFilter"
                />

                <ul v-if="hasResults" class="search-global__results" role="listbox">
                    <template v-for="group in filteredGroups" :key="group.type">
                        <li v-if="activeFilter === null" class="search-global__group-label">
                            <span class="search-global__group-icon" :class="`search-global__group-icon--${group.type}`">
                                <BaseIcon :name="group.icon" :size="12" />
                            </span>
                            {{ group.label }}
                        </li>

                        <SearchResultItem
                            v-for="item in group.results"
                            :key="`${item.type}-${item.id}`"
                            :link="item.link"
                            :icon="item.icon"
                            :title="item.title"
                            :subtitle="item.subtitle"
                            :type="group.type"
                            :badge-label="group.label"
                            :is-selected="isResultSelected(item)"
                            @hover="setSelectedByResult(item)"
                            @select="close"
                        />
                    </template>
                </ul>

                <SearchEmptyState v-else-if="!isLoading" :query="searchQuery" />

                <SearchFooter v-if="hasResults" class="search-global__footer" />
            </div>
        </Transition>
    </div>
</template>

<script setup lang="ts">
    import { ref, computed, onMounted, onUnmounted } from 'vue';
    import { useRouter } from 'vue-router';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import {
        GlobalSearchInput,
        SearchFilters,
        SearchResultItem,
        SearchEmptyState,
        SearchFooter,
    } from '@/components/ui/search';
    import {
        useGlobalSearch,
        type SearchResult,
        type SearchResultType,
        type SearchMode,
    } from '@/composables/data/useGlobalSearch';
    import { useClickOutside } from '@/composables/ui/useClickOutside';

    interface Props {
        placeholder?: string;
        mode?: SearchMode;
        compact?: boolean;
    }

    const props = withDefaults(defineProps<Props>(), {
        placeholder: 'Rechercher...',
        mode: 'public',
        compact: false,
    });

    const router = useRouter();
    const containerRef = ref<HTMLElement | null>(null);
    const searchInputRef = ref<InstanceType<typeof GlobalSearchInput> | null>(null);
    const activeFilter = ref<SearchResultType | null>(null);

    const {
        searchQuery,
        isOpen,
        isLoading,
        selectedIndex,
        groupedResults,
        flatResults,
        hasResults,
        clear,
        close,
        open,
        navigateUp,
        navigateDown,
        getSelectedResult,
    } = useGlobalSearch({ mode: props.mode });

    // Computed
    const filterGroups = computed(() =>
        groupedResults.value.map((g) => ({
            type: g.type,
            label: g.label,
            icon: g.icon,
            count: g.results.length,
        })),
    );

    const filteredGroups = computed(() => {
        if (activeFilter.value === null) {
            return groupedResults.value;
        }
        return groupedResults.value.filter((g) => g.type === activeFilter.value);
    });

    const filteredFlatResults = computed(() => filteredGroups.value.flatMap((g) => g.results));

    // Methods
    const toggleFilter = (type: string) => {
        activeFilter.value = activeFilter.value === type ? null : (type as SearchResultType);
    };

    const clearSearch = () => {
        clear();
        searchInputRef.value?.focus();
    };

    const isResultSelected = (result: SearchResult) => {
        const idx = filteredFlatResults.value.findIndex((r) => r.id === result.id && r.type === result.type);
        return idx === selectedIndex.value;
    };

    const setSelectedByResult = (result: SearchResult) => {
        const idx = flatResults.value.findIndex((r) => r.id === result.id && r.type === result.type);
        if (idx !== -1) {
            selectedIndex.value = idx;
        }
    };

    const cycleFilter = (direction: number) => {
        const types = groupedResults.value.map((g) => g.type);
        if (types.length === 0) {
            return;
        }

        if (activeFilter.value === null) {
            activeFilter.value = (direction > 0 ? types[0] : types[types.length - 1]) ?? null;
        } else {
            const currentIndex = types.indexOf(activeFilter.value);
            const nextIndex = currentIndex + direction;
            if (nextIndex < 0 || nextIndex >= types.length) {
                activeFilter.value = null;
            } else {
                activeFilter.value = types[nextIndex] ?? null;
            }
        }
    };

    const handleKeydown = (e: KeyboardEvent) => {
        const actions: Record<string, () => void> = {
            ArrowDown: () => {
                e.preventDefault();
                navigateDown();
            },
            ArrowUp: () => {
                e.preventDefault();
                navigateUp();
            },
            Enter: () => {
                e.preventDefault();
                const selected = getSelectedResult();
                if (selected) {
                    router.push(selected.link);
                    close();
                }
            },
            Escape: () => {
                e.preventDefault();
                close();
                searchInputRef.value?.blur();
            },
            Tab: () => {
                if (hasResults.value && isOpen.value) {
                    e.preventDefault();
                    cycleFilter(e.shiftKey ? -1 : 1);
                }
            },
        };
        actions[e.key]?.();
    };

    const handleShortcut = (e: KeyboardEvent) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            searchInputRef.value?.focus();
        }
    };

    useClickOutside(containerRef, close);

    onMounted(() => document.addEventListener('keydown', handleShortcut));
    onUnmounted(() => document.removeEventListener('keydown', handleShortcut));
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as v;
    @use '@/styles/abstracts/mixins' as m;
    @use '@/styles/abstracts/functions' as fn;

    $type-colors: (
        article: v.$info-color,
        project: v.$success-color,
        stack: v.$secondary-color,
        experience: v.$warning-color,
    );

    .search-global {
        position: relative;
        width: 100%;
        max-width: 320px;
        border-radius: v.$border-radius-md;
        border: 1px solid v.$border-color;

        &--compact {
            max-width: 160px;
        }

        &__dropdown {
            position: absolute;
            top: calc(100% + v.$spacing-xs);
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            flex-direction: column;
            width: 480px;
            max-height: 480px;
            background: v.$white;
            border: 1px solid v.$border-color;
            border-radius: v.$border-radius-lg;
            box-shadow: v.$box-shadow-large;
            z-index: v.$z-index-dropdown;
            overflow: hidden;

            @include m.responsive(tablet) {
                width: 420px;
            }

            @include m.responsive(mobile) {
                position: fixed;
                top: v.$navbar-height-mobile + v.$spacing-xs;
                left: v.$spacing-md;
                right: v.$spacing-md;
                width: auto;
                transform: none;
                max-height: calc(100vh - v.$navbar-height-mobile - v.$spacing-xl);
            }
        }

        &__filters {
            flex-shrink: 0;
            padding: v.$spacing-sm;
            background: v.$bg-secondary;
            border-bottom: 1px solid v.$border-color;
        }

        &__results {
            flex: 1;
            margin: 0;
            padding: v.$spacing-xxs;
            list-style: none;
            overflow-y: auto;

            &::-webkit-scrollbar {
                width: 4px;
            }

            &::-webkit-scrollbar-thumb {
                background: fn.color-alpha(v.$black, 0.1);
                border-radius: 2px;
            }
        }

        &__group-label {
            display: flex;
            align-items: center;
            gap: v.$spacing-xxs;
            padding: v.$spacing-xs v.$spacing-sm;
            margin-top: v.$spacing-xxs;
            color: v.$text-muted;
            font-weight: v.$font-weight-semibold;
            text-transform: uppercase;
            letter-spacing: v.$letter-spacing-wide;

            &:first-child {
                margin-top: 0;
            }
        }

        &__group-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 18px;
            height: 18px;
            border-radius: v.$border-radius-sm;

            @each $type, $color in $type-colors {
                &--#{$type} {
                    background: fn.color-alpha($color, 0.12);
                    color: $color;
                }
            }
        }

        &__footer {
            flex-shrink: 0;
            border-top: 1px solid v.$border-color;
            background: v.$bg-secondary;
        }
    }

    .fade-slide-enter-active,
    .fade-slide-leave-active {
        transition:
            opacity 0.2s ease,
            transform 0.2s ease;
    }

    .fade-slide-enter-from,
    .fade-slide-leave-to {
        opacity: 0;
        transform: translateX(-50%) translateY(-8px);

        @include m.responsive(mobile) {
            transform: translateY(-8px);
        }
    }
</style>
