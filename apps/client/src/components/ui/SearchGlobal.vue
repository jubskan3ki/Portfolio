<template>
    <div ref="containerRef" class="search-global" :class="{ 'search-global--compact': compact }">
        <GlobalSearchInput
            ref="searchInputRef"
            v-model="searchQuery"
            :placeholder="placeholder"
            :compact="compact"
            :loading="isLoading"
            :is-expanded="isOpen"
            @focus="onFocus"
            @clear="clearSearch"
            @keydown="handleKeydown"
        />

        <!-- Screen reader announcement (result count + empty state) -->
        <span class="sr-only" role="status" aria-live="polite">{{ announcement }}</span>

        <Transition name="fade-slide">
            <div v-if="isOpen" class="search-global__dropdown">
                <!-- Empty-query palette: recents + actions -->
                <template v-if="isEmptyQuery">
                    <section
                        v-if="recentQueries.length || recentItems.length"
                        class="search-global__section"
                        aria-label="Récents"
                    >
                        <div class="search-global__section-head">
                            <span class="search-global__section-title">Récents</span>
                            <button type="button" class="search-global__section-action" @click="clearHistory">
                                Effacer
                            </button>
                        </div>
                        <ul class="search-global__results" role="listbox">
                            <li
                                v-for="q in recentQueries"
                                :key="`recent-q-${q}`"
                                class="search-global__quickitem"
                                tabindex="-1"
                                role="option"
                                @click="applyQuery(q)"
                                @keydown.enter.prevent="applyQuery(q)"
                            >
                                <BaseIcon name="search" :size="16" />
                                <span>{{ q }}</span>
                            </li>
                            <SearchResultItem
                                v-for="item in recentItems"
                                :key="`recent-item-${item.type}-${item.id}`"
                                :link="item.link"
                                :icon="item.icon"
                                :title="item.title"
                                :subtitle="item.subtitle"
                                :type="item.type"
                                badge-label="Récent"
                                :is-selected="false"
                                @select="() => recordItemFromHistory(item)"
                            />
                        </ul>
                    </section>

                    <section class="search-global__section" aria-label="Actions rapides">
                        <div class="search-global__section-head">
                            <span class="search-global__section-title">Actions</span>
                        </div>
                        <ul class="search-global__results" role="listbox">
                            <li
                                v-for="action in actions"
                                :key="action.id"
                                class="search-global__quickitem"
                                tabindex="-1"
                                role="option"
                                @click="runAction(action)"
                                @keydown.enter.prevent="runAction(action)"
                            >
                                <BaseIcon :name="action.icon" :size="16" />
                                <span class="search-global__quickitem-title">{{ action.title }}</span>
                                <small v-if="action.subtitle" class="search-global__quickitem-sub">
                                    {{ action.subtitle }}
                                </small>
                            </li>
                        </ul>
                    </section>
                </template>

                <!-- Active query: filtered results -->
                <template v-else-if="searchQuery.length >= 2">
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
                                <span
                                    class="search-global__group-icon"
                                    :class="`search-global__group-icon--${group.type}`"
                                >
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
                                @select="onResultSelect(item)"
                            />
                        </template>
                    </ul>

                    <SearchEmptyState v-else-if="!isLoading" :query="searchQuery" />

                    <SearchFooter v-if="hasResults" class="search-global__footer" />
                </template>
            </div>
        </Transition>
    </div>
</template>

<script setup lang="ts">
    import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
    import { useRouter } from 'vue-router';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import {
        GlobalSearchInput,
        SearchFilters,
        SearchResultItem,
        SearchEmptyState,
        SearchFooter,
    } from '@/components/ui/search';
    import { useGlobalSearch, type SearchResult, type SearchResultType } from '@/composables/data/useGlobalSearch';
    import { useSearchActions, type SearchAction } from '@/composables/data/useSearchActions';
    import { useSearchHistory, type HistoryItem } from '@/composables/data/useSearchHistory';
    import { useClickOutside } from '@/composables/ui/useClickOutside';

    import type { SearchGlobalProps } from '@/types/components/ui';

    const props = withDefaults(defineProps<SearchGlobalProps>(), {
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
        totalResults,
        clear,
        close,
        open,
        navigateUp,
        navigateDown,
        getSelectedResult,
    } = useGlobalSearch({ mode: props.mode });

    const { queries: recentQueries, items: recentItems, recordQuery, recordItem, clearHistory } = useSearchHistory();

    const { actions, run: runActionImperative } = useSearchActions();

    const isEmptyQuery = computed(() => searchQuery.value.trim().length < 2);

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

    const toggleFilter = (type: string) => {
        activeFilter.value = activeFilter.value === type ? null : (type as SearchResultType);
    };

    const clearSearch = () => {
        clear();
        searchInputRef.value?.focus();
    };

    const isResultSelected = (result: SearchResult) => {
        // selectedIndex est piloté par navigateUp/Down et setSelectedByResult sur
        // flatResults (non filtré) ; le surlignage doit utiliser le même espace
        // d'index, sinon il diverge de la sélection quand un filtre est actif.
        const idx = flatResults.value.findIndex((r) => r.id === result.id && r.type === result.type);
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

    // Open whenever the input is focused | the palette shows recents + actions
    // when empty, results when not.
    const onFocus = () => {
        isOpen.value = true;
        open();
    };

    const applyQuery = (query: string) => {
        searchQuery.value = query;
        searchInputRef.value?.focus();
    };

    const onResultSelect = (result: SearchResult) => {
        recordItem(result);
        const query = searchQuery.value.trim();
        if (query.length >= 2) {
            recordQuery(query);
        }
        close();
    };

    const recordItemFromHistory = (item: HistoryItem) => {
        // touching it bumps it to the top of the recents list
        recordItem(item);
        close();
    };

    const runAction = async (action: SearchAction) => {
        await runActionImperative(action);
        close();
    };

    // Live-region announcement: result count once results settle.
    const announcement = ref('');
    watch([isOpen, isLoading, hasResults, totalResults, isEmptyQuery], () => {
        if (!isOpen.value) {
            announcement.value = '';
            return;
        }
        if (isEmptyQuery.value) {
            const parts: string[] = [];
            if (recentQueries.value.length) {
                parts.push(`${recentQueries.value.length} recherche(s) récente(s)`);
            }
            parts.push(`${actions.value.length} actions disponibles`);
            announcement.value = parts.join(', ');
            return;
        }
        if (isLoading.value) {
            announcement.value = 'Recherche en cours';
            return;
        }
        announcement.value = hasResults.value ? `${totalResults.value} résultat(s) trouvé(s)` : 'Aucun résultat';
    });

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

        &__section {
            display: flex;
            flex-direction: column;
            border-bottom: 1px solid v.$border-color;

            &:last-child {
                border-bottom: none;
            }
        }

        &__section-head {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: v.$spacing-xs v.$spacing-sm;
        }

        &__section-title {
            font-size: v.$font-size-xs;
            font-weight: v.$font-weight-semibold;
            text-transform: uppercase;
            letter-spacing: v.$letter-spacing-wide;
            color: v.$text-muted;
        }

        &__section-action {
            background: none;
            border: none;
            color: v.$text-muted;
            cursor: pointer;
            font-size: v.$font-size-xs;
            padding: 2px v.$spacing-xs;
            border-radius: v.$border-radius-sm;
            transition:
                color v.$transition-fast,
                background v.$transition-fast;

            &:hover,
            &:focus-visible {
                color: v.$primary-color;
                background: fn.color-alpha(v.$primary-color, 0.08);
            }
        }

        &__quickitem {
            display: flex;
            align-items: center;
            gap: v.$spacing-sm;
            padding: v.$spacing-xs v.$spacing-sm;
            border-radius: v.$border-radius-md;
            cursor: pointer;
            transition: background v.$transition-fast;

            &:hover,
            &:focus-visible {
                background: fn.color-alpha(v.$primary-color, 0.06);
                outline: none;
            }
        }

        &__quickitem-title {
            flex: 1;
            font-weight: v.$font-weight-medium;
            color: v.$text-primary;
        }

        &__quickitem-sub {
            color: v.$text-muted;
            font-size: v.$font-size-xs;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 180px;
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
