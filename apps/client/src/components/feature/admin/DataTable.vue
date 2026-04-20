<template>
    <div class="data-table-wrapper">
        <DataTableToolbar
            v-if="showToolbar"
            :search-placeholder="searchPlaceholder"
            :selected-count="selectedItems.length"
            :filters="filters"
            :active-filters="activeFilters"
            @search="handleSearch"
            @filter="handleFilter"
            @bulk-delete="handleBulkDelete"
        >
            <template #actions>
                <slot name="toolbar-actions"></slot>
            </template>
        </DataTableToolbar>

        <div class="data-table-container">
            <table class="data-table" :class="{ 'data-table--loading': loading }">
                <thead>
                    <tr>
                        <th v-if="selectable" class="data-table__th data-table__th--checkbox">
                            <BaseCheckbox
                                :model-value="isAllSelected"
                                :indeterminate="isIndeterminate"
                                aria-label="Sélectionner tout"
                                @update:model-value="toggleSelectAll"
                            />
                        </th>
                        <th
                            v-for="column in columns"
                            :key="column.key"
                            class="data-table__th"
                            :class="{
                                'data-table__th--sortable': column.sortable,
                                'data-table__th--sorted': sortBy === column.key,
                            }"
                            :style="{ width: column.width }"
                            :role="column.sortable ? 'button' : undefined"
                            :tabindex="column.sortable ? 0 : undefined"
                            :aria-sort="column.sortable ? getAriaSort(column.key) : undefined"
                            @click="column.sortable && handleSort(column.key)"
                            @keydown.enter="column.sortable && handleSort(column.key)"
                            @keydown.space.prevent="column.sortable && handleSort(column.key)"
                        >
                            <div class="data-table__th-content">
                                <small>{{ column.label }}</small>
                                <BaseIcon
                                    v-if="column.sortable"
                                    :name="getSortIcon(column.key)"
                                    :size="14"
                                    class="data-table__sort-icon"
                                />
                            </div>
                        </th>
                        <th v-if="$slots.actions" class="data-table__th data-table__th--actions">
                            <small>Actions</small>
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <template v-if="loading">
                        <tr v-for="i in skeletonRows" :key="i" class="data-table__row data-table__row--skeleton">
                            <td v-if="selectable" class="data-table__td">
                                <div class="skeleton skeleton--checkbox"></div>
                            </td>
                            <td v-for="column in columns" :key="column.key" class="data-table__td">
                                <div class="skeleton" :style="{ width: column.skeletonWidth || '80%' }"></div>
                            </td>
                            <td v-if="$slots.actions" class="data-table__td">
                                <div class="skeleton skeleton--actions"></div>
                            </td>
                        </tr>
                    </template>

                    <tr v-else-if="!data.length">
                        <td :colspan="totalColumns" class="data-table__empty">
                            <slot name="empty">
                                <EmptyState :title="emptyMessage" icon="inbox" />
                            </slot>
                        </td>
                    </tr>

                    <template v-else>
                        <tr
                            v-for="(item, index) in data"
                            :key="getItemKey(item, index)"
                            class="data-table__row"
                            :class="{ 'data-table__row--selected': isSelected(item) }"
                            @click="$emit('rowClick', item)"
                        >
                            <td v-if="selectable" class="data-table__td data-table__td--checkbox">
                                <BaseCheckbox
                                    :model-value="isSelected(item)"
                                    :aria-label="`Sélectionner l'élément ${getItemKey(item, index)}`"
                                    @click.stop
                                    @update:model-value="toggleSelect(item)"
                                />
                            </td>
                            <td
                                v-for="column in columns"
                                :key="column.key"
                                class="data-table__td"
                                :class="column.class"
                            >
                                <slot
                                    :name="`cell-${column.key}`"
                                    :item="item"
                                    :value="getNestedValue(item, column.key)"
                                >
                                    {{ formatValue(getNestedValue(item, column.key), column) }}
                                </slot>
                            </td>
                            <td v-if="$slots.actions" class="data-table__td data-table__td--actions">
                                <slot name="actions" :item="item"></slot>
                            </td>
                        </tr>
                    </template>
                </tbody>
            </table>
        </div>

        <DataTablePagination
            v-if="showPagination && totalItems > 0"
            :current-page="currentPage"
            :total-pages="totalPages"
            :total-items="totalItems"
            :per-page="perPage"
            :per-page-options="perPageOptions"
            @page-change="handlePageChange"
            @per-page-change="handlePerPageChange"
        />
    </div>
</template>

<script setup lang="ts">
    import { computed, ref, useSlots, watch } from 'vue';

    import BaseCheckbox from '@/components/base/BaseCheckbox.vue';
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import EmptyState from '@/components/feedback/EmptyState.vue';

    import DataTablePagination from './DataTablePagination.vue';
    import DataTableToolbar from './DataTableToolbar.vue';

    import type {
        DataItem,
        DataTableColumn as Column,
        DataTableProps,
        QueryChangePayload,
        PaginationChangePayload,
    } from '@/types/components/admin';

    const props = withDefaults(defineProps<DataTableProps>(), {
        loading: false,
        selectable: false,
        itemKey: 'id',
        sortOrder: 'asc',
        searchPlaceholder: 'Rechercher...',
        emptyMessage: 'Aucune donnée disponible',
        showToolbar: true,
        showPagination: true,
        currentPage: 1,
        totalItems: 0,
        perPage: 10,
        perPageOptions: () => [10, 25, 50, 100],
        filters: () => [],
        skeletonRows: 5,
    });

    const emit = defineEmits<{
        rowClick: [item: DataItem];
        sort: [key: string, order: 'asc' | 'desc'];
        queryChange: [payload: QueryChangePayload];
        paginationChange: [payload: PaginationChangePayload];
        selectionChange: [items: DataItem[]];
        bulkDelete: [items: DataItem[]];
    }>();

    const slots = useSlots();
    const selectedItems = ref<DataItem[]>([]);
    const activeFilters = ref<Record<string, string>>({});
    const internalSortBy = ref(props.sortBy || '');
    const internalSortOrder = ref<'asc' | 'desc'>(props.sortOrder);

    const sortBy = computed(() => props.sortBy ?? internalSortBy.value);

    const totalColumns = computed(() => {
        let count = props.columns.length;
        if (props.selectable) {
            count++;
        }
        if (slots.actions) {
            count++;
        }
        return count;
    });

    const totalPages = computed(() => {
        return Math.ceil(props.totalItems / props.perPage);
    });

    const isAllSelected = computed(() => {
        return props.data.length > 0 && selectedItems.value.length === props.data.length;
    });

    const isIndeterminate = computed(() => {
        return selectedItems.value.length > 0 && selectedItems.value.length < props.data.length;
    });

    const getItemKey = (item: DataItem, index: number): string | number => {
        return ((item as Record<string, unknown>)[props.itemKey] as string | number) ?? index;
    };

    const getNestedValue = (obj: DataItem, path: string): unknown => {
        return path.split('.').reduce<unknown>((acc, part) => {
            if (acc && typeof acc === 'object' && part in acc) {
                return (acc as Record<string, unknown>)[part];
            }
            return undefined;
        }, obj);
    };

    const formatValue = (value: unknown, column: Column): string => {
        if (value === null || value === undefined) {
            return '-';
        }
        if (column.format) {
            return column.format(value);
        }
        if (value instanceof Date) {
            return value.toLocaleDateString('fr-FR');
        }
        return String(value);
    };

    const getSortIcon = (key: string): string => {
        if (sortBy.value !== key) {
            return 'arrow-up-down';
        }
        return internalSortOrder.value === 'asc' ? 'arrow-up' : 'arrow-down';
    };

    const getAriaSort = (key: string): 'ascending' | 'descending' | 'none' => {
        if (sortBy.value !== key) {
            return 'none';
        }
        return internalSortOrder.value === 'asc' ? 'ascending' : 'descending';
    };

    const isSelected = (item: DataItem): boolean => {
        const key = (item as Record<string, unknown>)[props.itemKey];
        return selectedItems.value.some((i) => (i as Record<string, unknown>)[props.itemKey] === key);
    };

    const toggleSelect = (item: DataItem) => {
        const key = (item as Record<string, unknown>)[props.itemKey];
        const index = selectedItems.value.findIndex((i) => (i as Record<string, unknown>)[props.itemKey] === key);

        if (index === -1) {
            selectedItems.value.push(item);
        } else {
            selectedItems.value.splice(index, 1);
        }

        emit('selectionChange', selectedItems.value);
    };

    const toggleSelectAll = () => {
        if (isAllSelected.value) {
            selectedItems.value = [];
        } else {
            selectedItems.value = [...props.data];
        }
        emit('selectionChange', selectedItems.value);
    };

    const handleSort = (key: string) => {
        if (sortBy.value === key) {
            internalSortOrder.value = internalSortOrder.value === 'asc' ? 'desc' : 'asc';
        } else {
            internalSortBy.value = key;
            internalSortOrder.value = 'asc';
        }
        emit('sort', internalSortBy.value, internalSortOrder.value);
    };

    const handleSearch = (query: string) => {
        emit('queryChange', { search: query });
    };

    const handleFilter = (filters: Record<string, string>) => {
        activeFilters.value = filters;
        emit('queryChange', { filters });
    };

    const handlePageChange = (page: number) => {
        emit('paginationChange', { page });
    };

    const handlePerPageChange = (perPage: number) => {
        emit('paginationChange', { perPage });
    };

    const handleBulkDelete = () => {
        emit('bulkDelete', selectedItems.value);
    };

    // Clear selection only when the actual dataset changes (not on sort/reorder)
    watch(
        () => props.data.map((item) => (item as Record<string, unknown>)[props.itemKey]),
        (newIds, oldIds) => {
            if (!oldIds || newIds.length !== oldIds.length || newIds.some((id, i) => id !== oldIds[i])) {
                selectedItems.value = [];
            }
        },
    );
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;

    .data-table-wrapper {
        background: vars.$white;
        border-radius: vars.$border-radius-xl;
        border: 1px solid rgba(vars.$admin-border, 0.6);
        box-shadow: vars.$box-shadow-xs;
        overflow: hidden;
    }

    .data-table-container {
        overflow-x: auto;

        &::-webkit-scrollbar {
            height: 6px;
        }

        &::-webkit-scrollbar-track {
            background: vars.$bg-secondary;
        }

        &::-webkit-scrollbar-thumb {
            background: rgba(0, 0, 0, 0.15);
            border-radius: 3px;
        }
    }

    .data-table {
        width: 100%;
        border-collapse: collapse;

        &--loading {
            pointer-events: none;
        }

        &__th {
            padding: vars.$spacing-xs vars.$spacing-sm;
            text-align: left;
            font-weight: vars.$font-weight-semibold;
            color: vars.$text-secondary;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            background: vars.$bg-secondary;
            border-bottom: 1px solid rgba(vars.$admin-border, 0.6);
            white-space: nowrap;
            position: sticky;
            top: 0;
            z-index: 1;

            small {
                color: inherit;
            }

            &--checkbox {
                width: 50px;
                text-align: center;
            }

            &--sortable {
                cursor: pointer;
                user-select: none;
                transition: all vars.$transition-fast;

                &:hover {
                    color: vars.$text-primary;
                }
            }

            &--sorted {
                color: vars.$primary-color;
            }

            &--actions {
                width: 100px;
                text-align: right;
            }
        }

        &__th-content {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xxs;
        }

        &__sort-icon {
            opacity: 0.4;
            transition: all vars.$transition-fast;

            .data-table__th--sorted & {
                opacity: 1;
                color: vars.$primary-color;
            }

            .data-table__th--sortable:hover & {
                opacity: 0.8;
            }
        }

        &__row {
            transition: all vars.$transition-fast;

            &:hover {
                background-color: rgba(vars.$primary-color, 0.03);

                .data-table__td {
                    color: vars.$text-primary;
                }
            }

            &--selected {
                background-color: rgba(vars.$primary-color, 0.06);

                &:hover {
                    background-color: rgba(vars.$primary-color, 0.08);
                }
            }

            &--skeleton {
                pointer-events: none;
            }

            &:last-child .data-table__td {
                border-bottom: none;
            }
        }

        &__td {
            padding: vars.$spacing-xs vars.$spacing-md;
            color: vars.$text-primary;
            border-bottom: 1px solid rgba(vars.$admin-border, 0.3);
            vertical-align: middle;
            transition: color vars.$transition-fast;

            &--checkbox {
                text-align: center;
            }

            &--actions {
                text-align: right;
                white-space: nowrap;
            }
        }

        &__empty {
            padding: vars.$spacing-xxxl;
        }
    }

    /* Skeleton loading */
    .skeleton {
        height: 14px;
        background: vars.$bg-secondary;
        animation: skeleton-pulse 1.5s ease-in-out infinite;
        border-radius: vars.$border-radius-sm;

        &--checkbox {
            width: 16px;
            height: 16px;
            margin: 0 auto;
            border-radius: vars.$border-radius-sm;
        }

        &--actions {
            width: 60px;
            margin-left: auto;
        }
    }

    @keyframes skeleton-pulse {
        0%,
        100% {
            opacity: 1;
        }

        50% {
            opacity: 0.5;
        }
    }
</style>
