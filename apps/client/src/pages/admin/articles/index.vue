<template>
    <AdminListPage
        ref="listPage"
        title="Articles"
        subtitle="Gérez vos articles de blog"
        :create-route="ADMIN_ROUTES.ARTICLES.CREATE.path"
        create-label="Nouvel article"
        seo-title="Gestion des Articles"
        seo-description="Administration des articles de blog"
        :columns="columns"
        :query-key="['admin', 'articles']"
        :query-fn="queryFn"
        :delete-fn="deleteFn"
        :sort-field-map="sortFieldMap"
        default-sort="created_at"
        default-sort-order="desc"
        :edit-route="(item) => ADMIN_ROUTES.ARTICLES.EDIT(item.id).path"
        :view-route="(item) => ROUTES.BLOG.DETAIL(item.slug).path"
        :type-guard="asAdminArticle"
        resource-name="Article"
        delete-title="Supprimer l'article ?"
        :delete-message="
            (item) => `Cette action est irréversible. L'article &quot;${item.title}&quot; sera définitivement supprimé.`
        "
        bulk-delete-title="Supprimer les articles sélectionnés ?"
        :bulk-delete-message="
            (count) => `Cette action est irréversible. ${count} article(s) seront définitivement supprimés.`
        "
    >
        <template #cell-title="{ item }">
            <div class="cell-title">
                <BaseImage
                    v-if="typed(item).coverImage"
                    :src="String(typed(item).coverImage)"
                    :alt="String(typed(item).title || '')"
                    :width="24"
                    :height="24"
                    :show-placeholder="false"
                    class="cell-title__image"
                />
                <div class="cell-title__content">
                    <span class="cell-title__text">{{ typed(item).title }}</span>
                    <small class="cell-title__slug">{{ typed(item).slug }}</small>
                </div>
            </div>
        </template>

        <template #cell-status="{ item }">
            <Badge :variant="typed(item).isPublished ? 'success' : 'warning'">
                {{ typed(item).isPublished ? 'Publié' : 'Brouillon' }}
            </Badge>
        </template>

        <template #cell-date="{ value }">
            {{ formatDateShort(value as string) }}
        </template>

        <template #actions="{ item }">
            <DataTableActions @view="viewArticle(item)" @edit="editArticle(item)" @delete="confirmDelete(item)">
                <BaseButton
                    v-if="typed(item).isPublished"
                    variant="ghost"
                    size="icon"
                    class="action-btn--disabled"
                    title="Deja publie"
                    disabled
                >
                    <template #icon-left>
                        <BaseIcon name="check-circle" :size="16" />
                    </template>
                </BaseButton>
                <BaseButton
                    v-else
                    variant="ghost"
                    size="icon"
                    class="action-btn--publish"
                    title="Publier"
                    :loading="publishingId === typed(item).id"
                    @click="togglePublish(item)"
                >
                    <template #icon-left>
                        <BaseIcon name="send" :size="16" />
                    </template>
                </BaseButton>
            </DataTableActions>
        </template>
    </AdminListPage>
</template>

<script setup lang="ts">
    import { ref } from 'vue';
    import { useRouter } from 'vue-router';

    import BaseButton from '@/components/base/BaseButton.vue';
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import AdminListPage from '@/components/feature/admin/AdminListPage.vue';
    import DataTableActions from '@/components/feature/admin/DataTableActions.vue';
    import Badge from '@/components/ui/Badge.vue';
    import { useAlert } from '@/composables/ui/useAlert';
    import { ADMIN_ROUTES, ROUTES } from '@/config/routes';
    import { articlesApi, useToggleArticlePublish } from '@/services/api/modules/articles';
    import { formatDateShort } from '@/services/utils/date';
    import { asAdminArticle } from '@/services/utils/guards/admin';

    import type { ListParams } from '@/types/composables';
    import type { AdminArticle, DataItem, PaginatedResponse } from '@/types/feature/admin';

    const typed = (item: DataItem) => asAdminArticle(item);

    definePageMeta({ layout: 'admin', title: 'Articles' });

    const router = useRouter();
    const { error: showError, success: showSuccess } = useAlert();
    const listPage = ref<{ deletion?: { confirm: (item: AdminArticle) => void } | null } | null>(null);

    const columns = [
        { key: 'title', label: 'Titre', sortable: true, width: '40%' },
        { key: 'category', label: 'Catégorie', sortable: true },
        { key: 'status', label: 'Statut', sortable: true },
        { key: 'views', label: 'Vues', sortable: true },
        { key: 'date', label: 'Date', sortable: true },
    ];

    const sortFieldMap = {
        views: 'view_count',
        date: 'published_date',
        status: 'isPublished',
        category: 'category__name',
    };

    const queryFn = (params: ListParams) => {
        const queryParams: Record<string, unknown> = {
            page: params.page,
            page_size: params.pageSize,
            ordering: params.ordering,
            all: 'true',
        };
        if (params.search) {
            queryParams.search = params.search;
        }
        return articlesApi.getAdminList<PaginatedResponse<AdminArticle>>(queryParams);
    };

    const deleteFn = async (item: AdminArticle) => {
        await articlesApi.delete(String(item.id));
    };

    // Article-specific: navigation handlers needed for custom actions slot
    const viewArticle = (item: DataItem) => {
        window.open(ROUTES.BLOG.DETAIL(asAdminArticle(item).slug).path, '_blank');
    };

    const editArticle = (item: DataItem) => {
        router.push(ADMIN_ROUTES.ARTICLES.EDIT(asAdminArticle(item).id).path);
    };

    const confirmDelete = (item: DataItem) => {
        listPage.value?.deletion?.confirm(asAdminArticle(item));
    };

    // Article-specific: toggle publication status
    const togglePublishMutation = useToggleArticlePublish();
    const publishingId = ref<number | null>(null);

    const togglePublish = (item: DataItem) => {
        const article = asAdminArticle(item);
        publishingId.value = article.id;

        togglePublishMutation.mutate(
            { slug: article.slug, isPublished: !article.isPublished },
            {
                onSuccess: () => {
                    showSuccess(article.isPublished ? 'Article depublie' : 'Article publie');
                },
                onError: () => {
                    showError('Impossible de modifier le statut', 'Erreur');
                },
                onSettled: () => {
                    publishingId.value = null;
                },
            },
        );
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
            @include mix.truncate;
        }

        &__slug {
            @include mix.cell-title-slug;
        }
    }

    .action-btn--publish {
        &:hover {
            background-color: rgba(vars.$success-color, 0.1);
            color: vars.$success-color;
        }
    }

    .action-btn--disabled {
        color: vars.$text-muted;
        opacity: 0.5;
        cursor: not-allowed;
    }
</style>
