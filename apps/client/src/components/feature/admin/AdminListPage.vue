<template>
    <div class="admin-page">
        <div class="admin-page__header">
            <div>
                <h1 class="admin-page__title">{{ title }}</h1>
                <p class="admin-page__subtitle">{{ subtitle }}</p>
            </div>
            <BaseButton :to="createRoute" variant="primary">
                <template #icon-left>
                    <BaseIcon name="plus" :size="16" />
                </template>
                <slot name="create-label">{{ createLabel }}</slot>
            </BaseButton>
        </div>

        <DataTable
            :data="items"
            :columns="columns"
            :loading="isLoading"
            :total-items="pagination.totalItems.value"
            :current-page="pagination.currentPage.value"
            :per-page="pagination.perPage.value"
            selectable
            @sort="dataList.handlers.sort"
            @query-change="dataList.handlers.queryChange"
            @pagination-change="dataList.handlers.paginationChange"
            @bulk-delete="onBulkDelete"
        >
            <template #toolbar-actions>
                <BaseButton variant="outline" size="icon" @click="refresh">
                    <BaseIcon name="refresh-cw" :size="16" />
                </BaseButton>
                <slot name="toolbar-extra"></slot>
            </template>

            <!-- Forward all cell-* slots -->
            <template v-for="col in columns" :key="col.key" #[`cell-${col.key}`]="slotProps">
                <slot :name="`cell-${col.key}`" v-bind="slotProps">
                    {{ slotProps.value }}
                </slot>
            </template>

            <template #actions="{ item }">
                <slot name="actions" :item="item">
                    <DataTableActions
                        :show-view="showView"
                        @view="onView(item)"
                        @edit="onEdit(item)"
                        @delete="onConfirmDelete(item)"
                    />
                </slot>
            </template>
        </DataTable>

        <ConfirmDialog
            v-if="deletion"
            v-model="deletion.showModal.value"
            variant="danger"
            :title="deleteTitle"
            :message="deleteItemMessage"
            confirm-text="Supprimer"
            :loading="deletion.isDeleting.value"
            @confirm="deletion.execute()"
            @cancel="deletion.cancel()"
        />

        <ConfirmDialog
            v-if="bulkDeletion"
            v-model="bulkDeletion.showModal.value"
            variant="danger"
            :title="bulkDeleteTitle"
            :message="bulkDeleteItemsMessage"
            confirm-text="Supprimer tout"
            :loading="bulkDeletion.isDeleting.value"
            @confirm="bulkDeletion.execute()"
            @cancel="bulkDeletion.cancel()"
        />
    </div>
</template>

<script setup lang="ts" generic="T extends { id: number | string }">
    import { computed } from 'vue';
    import { useRouter } from 'vue-router';

    import BaseButton from '@/components/base/BaseButton.vue';
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import DataTable from '@/components/feature/admin/DataTable.vue';
    import DataTableActions from '@/components/feature/admin/DataTableActions.vue';
    import ConfirmDialog from '@/components/feedback/ConfirmDialog.vue';
    import { useDataList } from '@/composables/data/useDataList';
    import { useSeo } from '@/composables/seo/useSeo';
    import { useAlert } from '@/composables/ui/useAlert';

    import type { AdminListPageProps } from '@/types/components/admin';
    import type { ListParams, BulkDeleteResult } from '@/types/composables';
    import type { DataItem } from '@/types/feature/admin';

    const props = withDefaults(defineProps<AdminListPageProps<T>>(), {
        createLabel: 'Créer',
        defaultSort: 'created_at',
        defaultSortOrder: 'desc',
        showView: true,
        deleteTitle: 'Supprimer ?',
        bulkDeleteTitle: 'Supprimer la sélection ?',
    });

    // SEO - noindex for admin pages
    useSeo({
        title: props.seoTitle,
        description: props.seoDescription,
        noindex: true,
    });

    const router = useRouter();
    const { error: showError, success: showSuccess } = useAlert();

    const dataList = useDataList<T>({
        queryKey: props.queryKey,
        queryFn: props.queryFn as (params: ListParams) => Promise<never>,
        defaultSort: props.defaultSort,
        defaultSortOrder: props.defaultSortOrder,
        sortFieldMap: props.sortFieldMap,
        defaultPerPage: 10,
        deleteFn: props.deleteFn,
        onDeleteSuccess: () => {
            showSuccess(`${props.resourceName} supprimé(e) avec succès`);
        },
        onDeleteError: (error: Error) => {
            showError(error.message || `Impossible de supprimer`, 'Erreur');
        },
        onBulkDeleteSuccess: (result: BulkDeleteResult) => {
            if (result.errorCount === 0) {
                showSuccess(`${result.successCount} ${props.resourceName.toLowerCase()}(s) supprimé(e)(s)`);
            } else {
                showSuccess(`${result.successCount} supprimé(e)(s), ${result.errorCount} erreur(s)`);
            }
        },
        onBulkDeleteError: (error: Error) => {
            showError(error.message || `Impossible de supprimer`, 'Erreur');
        },
    });

    const { items, isLoading, pagination, deletion, bulkDeletion, refresh } = dataList;

    // Delete confirmation messages
    const deleteItemMessage = computed(() => {
        const item = deletion?.itemToDelete.value;
        if (!item || !props.deleteMessage) {
            return `Cette action est irréversible.`;
        }
        return props.deleteMessage(item);
    });

    const bulkDeleteItemsMessage = computed(() => {
        const count = bulkDeletion?.itemsToDelete.value.length ?? 0;
        if (props.bulkDeleteMessage) {
            return props.bulkDeleteMessage(count);
        }
        return `Cette action est irréversible. ${count} élément(s) seront supprimés.`;
    });

    // Navigation handlers
    const onView = (item: DataItem) => {
        if (props.viewRoute) {
            const typed = props.typeGuard(item);
            window.open(props.viewRoute(typed), '_blank');
        }
    };

    const onEdit = (item: DataItem) => {
        const typed = props.typeGuard(item);
        router.push(props.editRoute(typed));
    };

    const onConfirmDelete = (item: DataItem) => {
        deletion?.confirm(props.typeGuard(item));
    };

    const onBulkDelete = (rawItems: DataItem[]) => {
        const typedItems = rawItems.map(props.typeGuard);
        bulkDeletion?.confirm(typedItems);
    };

    // Expose for parent component access (deletion/bulkDeletion needed when overriding #actions slot)
    defineExpose({ refresh, items, selection: dataList.selection, deletion, bulkDeletion });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/mixins' as mix;

    .admin-page {
        &__header {
            @include mix.admin-page-header;
        }
        &__title {
            @include mix.admin-page-title;
        }
        &__subtitle {
            @include mix.admin-page-subtitle;
        }
    }
</style>
