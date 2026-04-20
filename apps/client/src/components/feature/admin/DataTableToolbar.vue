<template>
    <div class="data-table-toolbar">
        <div class="data-table-toolbar__left">
            <SearchInput
                v-model="searchQuery"
                :placeholder="searchPlaceholder"
                class="data-table-toolbar__search"
                @search="handleSearch"
                @clear="clearSearch"
            />

            <div v-if="filters.length" class="data-table-toolbar__filters">
                <div v-for="filter in filters" :key="filter.key" class="data-table-toolbar__filter">
                    <BaseSelect
                        v-model="activeFilters[filter.key]"
                        :options="[{ value: '', label: filter.label }, ...filter.options]"
                        :aria-label="filter.label"
                        size="sm"
                        @update:model-value="handleFilterChange"
                    />
                </div>
            </div>

            <Transition name="slide-fade">
                <div v-if="selectedCount > 0" class="data-table-toolbar__bulk">
                    <small class="data-table-toolbar__bulk-count">
                        {{ selectedCount }} sélectionné{{ selectedCount > 1 ? 's' : '' }}
                    </small>
                    <BaseButton variant="danger" size="sm" @click="$emit('bulkDelete')">
                        <template #icon-left>
                            <BaseIcon name="trash-2" :size="14" />
                        </template>
                        Supprimer
                    </BaseButton>
                </div>
            </Transition>
        </div>

        <div class="data-table-toolbar__right">
            <slot name="actions"></slot>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref, reactive, watch } from 'vue';

    import BaseButton from '@/components/base/BaseButton.vue';
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import BaseSelect from '@/components/base/BaseSelect.vue';
    import SearchInput from '@/components/ui/search/SearchInput.vue';

    import type { DataTableFilter } from '@/types/components/admin';

    const props = withDefaults(
        defineProps<{
            searchPlaceholder?: string;
            selectedCount?: number;
            filters?: DataTableFilter[];
            activeFilters?: Record<string, string>;
        }>(),
        {
            searchPlaceholder: 'Rechercher...',
            selectedCount: 0,
            filters: () => [],
            activeFilters: () => ({}),
        },
    );

    const emit = defineEmits<{
        search: [query: string];
        filter: [filters: Record<string, string>];
        bulkDelete: [];
    }>();

    const searchQuery = ref('');
    const activeFilters = reactive<Record<string, string>>({ ...props.activeFilters });

    const handleSearch = (query: string) => {
        emit('search', query);
    };

    const clearSearch = () => {
        emit('search', '');
    };

    const handleFilterChange = () => {
        emit('filter', { ...activeFilters });
    };

    // Sync with parent activeFilters
    watch(
        () => props.activeFilters,
        (newFilters) => {
            if (newFilters) {
                Object.assign(activeFilters, newFilters);
            }
        },
        { deep: true },
    );
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;

    .data-table-toolbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: vars.$spacing-md;
        padding: vars.$spacing-xs vars.$spacing-sm;
        background: vars.$bg-secondary;
        border-bottom: 1px solid rgba(vars.$admin-border, 0.6);
        flex-wrap: wrap;

        &__left {
            display: flex;
            align-items: center;
            gap: vars.$spacing-md;
            flex-wrap: wrap;
            flex: 1;
        }

        &__right {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;
        }

        /* Search */
        &__search {
            min-width: 220px;
            max-width: 320px;
        }

        /* Filters */
        &__filters {
            display: flex;
            gap: vars.$spacing-xs;
        }

        /* Bulk actions */
        &__bulk {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;
            padding: vars.$spacing-xxs vars.$spacing-xs;
            background: rgba(vars.$primary-color, 0.08);
            border: 1px solid rgba(vars.$primary-color, 0.15);
            border-radius: vars.$border-radius-md;
        }

        &__bulk-count {
            color: vars.$primary-color;
            font-weight: vars.$font-weight-semibold;
        }
    }

    /* Transition */
    .slide-fade-enter-active,
    .slide-fade-leave-active {
        transition: all 0.25s cubic-bezier(0.23, 1, 0.32, 1);
    }

    .slide-fade-enter-from,
    .slide-fade-leave-to {
        opacity: 0;
        transform: translateX(-12px);
    }
</style>
