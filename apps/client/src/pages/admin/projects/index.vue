<template>
    <AdminListPage
        ref="listPage"
        title="Projets"
        subtitle="Gérez vos projets portfolio"
        :create-route="ADMIN_ROUTES.PROJECTS.CREATE.path"
        create-label="Nouveau projet"
        seo-title="Gestion des Projets"
        seo-description="Administration des projets portfolio"
        :columns="columns"
        :query-key="['admin', 'projects']"
        :query-fn="queryFn"
        :delete-fn="deleteFn"
        :sort-field-map="{ view: 'views' }"
        default-sort="date"
        default-sort-order="desc"
        :edit-route="(item) => ADMIN_ROUTES.PROJECTS.EDIT(item.id).path"
        :view-route="(item) => ROUTES.PROJECTS.DETAIL(item.slug).path"
        :type-guard="asAdminProject"
        resource-name="Projet"
        delete-title="Supprimer le projet ?"
        :delete-message="
            (item) => `Cette action est irréversible. Le projet &quot;${item.title}&quot; sera définitivement supprimé.`
        "
        bulk-delete-title="Supprimer les projets sélectionnés ?"
        :bulk-delete-message="
            (count) => `Cette action est irréversible. ${count} projet(s) seront définitivement supprimés.`
        "
    >
        <template #cell-title="{ item }">
            <div class="cell-title">
                <BaseImage
                    v-if="typed(item).image"
                    :src="String(typed(item).image)"
                    :alt="String(typed(item).title || '')"
                    :show-placeholder="false"
                    class="cell-title__image"
                />
                <div v-else class="cell-title__placeholder">
                    <BaseIcon name="image" :size="20" />
                </div>
                <div class="cell-title__content">
                    <span class="cell-title__text">{{ typed(item).title }}</span>
                    <small class="cell-title__slug">/projects/{{ typed(item).slug }}</small>
                </div>
            </div>
        </template>

        <template #cell-category="{ item }">
            <Badge variant="secondary">{{ typed(item).category || 'Non classé' }}</Badge>
        </template>

        <template #cell-status="{ item }">
            <Badge :variant="getProjectStatusVariant(String(typed(item).status || ''))">
                {{ typed(item).status || 'Non défini' }}
            </Badge>
        </template>

        <template #cell-view="{ item }">
            <span class="cell-stats">
                <BaseIcon name="eye" :size="14" />
                {{ getField(item, 'view') || 0 }}
            </span>
        </template>

        <template #cell-date="{ item }">
            <span class="cell-date">{{ formatDateShort(typed(item).createdAt) }}</span>
        </template>
    </AdminListPage>
</template>

<script setup lang="ts">
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import AdminListPage from '@/components/feature/admin/AdminListPage.vue';
    import Badge from '@/components/ui/Badge.vue';
    import { ADMIN_ROUTES, ROUTES } from '@/config/routes';
    import { projectsApi } from '@/services/api/modules/projects';
    import { formatDateShort } from '@/services/utils/date';
    import { asAdminProject } from '@/services/utils/guards/admin';
    import { getProjectStatusVariant } from '@/services/utils/helpers';

    import type { ListParams } from '@/types/composables';
    import type { AdminProject, DataItem, PaginatedResponse } from '@/types/feature/admin';

    const typed = (item: DataItem) => asAdminProject(item);

    const getField = (item: DataItem, key: string): unknown => (item as Record<string, unknown>)[key];

    definePageMeta({ layout: 'admin', title: 'Projets' });

    const columns = [
        { key: 'title', label: 'Titre', sortable: true, width: '40%' },
        { key: 'category', label: 'Catégorie', sortable: false },
        { key: 'status', label: 'Statut', sortable: false },
        { key: 'view', label: 'Vues', sortable: true },
        { key: 'date', label: 'Date', sortable: true },
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
        return projectsApi.getAdminList<PaginatedResponse<AdminProject>>(queryParams);
    };

    const deleteFn = async (item: AdminProject) => {
        await projectsApi.delete(String(item.id));
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;

    .cell-title {
        @include mix.cell-title-row;

        &__image {
            @include mix.cell-title-image;
        }

        &:hover &__image {
            transform: scale(1.05);
        }

        &__content {
            @include mix.cell-title-content;
        }
        &__text {
            @include mix.cell-title-text;
        }
        &__slug {
            @include mix.cell-title-slug;
        }

        &__placeholder {
            @include mix.cell-title-image;

            @include mix.flex-center;

            background-color: vars.$bg-tertiary;
            color: vars.$text-muted;
        }
    }
</style>
