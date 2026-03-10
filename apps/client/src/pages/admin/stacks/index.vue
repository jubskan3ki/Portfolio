<template>
    <AdminListPage
        ref="listPage"
        title="Stacks"
        subtitle="Gérez vos technologies et compétences"
        :create-route="ADMIN_ROUTES.STACKS.CREATE.path"
        create-label="Nouvelle stack"
        seo-title="Gestion des Technologies"
        seo-description="Administration des stacks et technologies"
        :columns="columns"
        :query-key="['admin', 'stacks']"
        :query-fn="queryFn"
        :delete-fn="deleteFn"
        default-sort="name"
        default-sort-order="asc"
        :show-view="false"
        :edit-route="(item) => ADMIN_ROUTES.STACKS.EDIT(item.id).path"
        :type-guard="asAdminStack"
        resource-name="Stack"
        delete-title="Supprimer la stack ?"
        :delete-message="
            (item) => `Cette action est irréversible. La stack &quot;${item.name}&quot; sera définitivement supprimée.`
        "
        bulk-delete-title="Supprimer les stacks sélectionnées ?"
        :bulk-delete-message="
            (count) => `Cette action est irréversible. ${count} stack(s) seront définitivement supprimées.`
        "
    >
        <template #cell-name="{ item }">
            <div class="cell-title">
                <BaseImage
                    v-if="typed(item).logo"
                    :src="String(typed(item).logo)"
                    :alt="String(typed(item).name || '')"
                    :show-placeholder="false"
                    class="cell-title__image"
                />
                <span class="cell-title__text">{{ typed(item).name }}</span>
            </div>
        </template>

        <template #cell-level="{ item }">
            <div class="progress-bar">
                <div class="progress-bar__fill" :style="{ width: `${(Number(typed(item).level) || 0) * 20}%` }"></div>
                <span class="progress-bar__text">{{ typed(item).level || 0 }}/5</span>
            </div>
        </template>
    </AdminListPage>
</template>

<script setup lang="ts">
    import AdminListPage from '@/components/feature/admin/AdminListPage.vue';
    import { ADMIN_ROUTES } from '@/config/routes';
    import { stacksApi } from '@/services/api/modules/stacks';
    import { asAdminStack } from '@/services/utils/guards/admin';

    import type { ListParams } from '@/types/composables';
    import type { AdminStack, DataItem, PaginatedResponse } from '@/types/feature/admin';

    const typed = (item: DataItem) => asAdminStack(item);

    definePageMeta({ layout: 'admin', title: 'Stacks' });

    const columns = [
        { key: 'name', label: 'Nom', sortable: true, width: '30%' },
        { key: 'category', label: 'Catégorie', sortable: false },
        { key: 'level', label: 'Niveau', sortable: true, width: '200px' },
        { key: 'experience', label: 'Expérience', sortable: false },
    ];

    const queryFn = (params: ListParams) => {
        const queryParams: Record<string, unknown> = {
            page: params.page,
            page_size: params.pageSize,
            ordering: params.ordering,
        };
        if (params.search) {
            queryParams.search = params.search;
        }
        return stacksApi.getAdminList<PaginatedResponse<AdminStack>>(queryParams);
    };

    const deleteFn = async (item: AdminStack) => {
        await stacksApi.delete(String(item.id));
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;

    .cell-title {
        @include mix.cell-title-row;

        &__image {
            @include mix.cell-title-image(24px);

            border: none;
            object-fit: contain;
        }

        &__text {
            @include mix.cell-title-text;
        }
    }

    .progress-bar {
        position: relative;
        height: 8px;
        background-color: vars.$bg-tertiary;
        border-radius: vars.$border-radius-full;
        overflow: hidden;
        min-width: 100px;

        &__fill {
            height: 100%;
            background-color: vars.$primary-color;
            border-radius: vars.$border-radius-full;
        }

        &__text {
            position: absolute;
            right: -40px;
            top: 50%;
            transform: translateY(-50%);
            color: vars.$text-secondary;
        }
    }
</style>
