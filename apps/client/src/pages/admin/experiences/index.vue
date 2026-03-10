<template>
    <AdminListPage
        ref="listPage"
        title="Expériences"
        subtitle="Gérez vos expériences professionnelles et formations"
        :create-route="ADMIN_ROUTES.EXPERIENCES.CREATE.path"
        create-label="Nouvelle expérience"
        seo-title="Gestion des Expériences"
        seo-description="Administration des expériences professionnelles et formations"
        :columns="columns"
        :query-key="['admin', 'experiences']"
        :query-fn="queryFn"
        :delete-fn="deleteFn"
        default-sort="start_date"
        default-sort-order="desc"
        :show-view="false"
        :edit-route="(item) => ADMIN_ROUTES.EXPERIENCES.EDIT(item.id).path"
        :type-guard="asAdminExperience"
        resource-name="Expérience"
        delete-title="Supprimer l'expérience ?"
        :delete-message="
            (item) =>
                `Cette action est irréversible. L'expérience &quot;${item.title}&quot; sera définitivement supprimée.`
        "
        bulk-delete-title="Supprimer les expériences sélectionnées ?"
        :bulk-delete-message="
            (count) => `Cette action est irréversible. ${count} expérience(s) seront définitivement supprimées.`
        "
    >
        <template #cell-title="{ item }">
            <div class="cell-title">
                <span class="cell-title__text">{{ typed(item).title }}</span>
                <small class="cell-title__company">{{ typed(item).company || typed(item).institution }}</small>
            </div>
        </template>

        <template #cell-type="{ item }">
            <Badge variant="secondary">
                {{ typed(item).type || 'Non défini' }}
            </Badge>
        </template>

        <template #cell-period="{ item }">
            <span class="cell-period">
                {{ getField(item, 'period') || formatPeriod(item) }}
            </span>
        </template>

        <template #cell-isCurrent="{ item }">
            <BaseIcon
                :name="typed(item).isCurrent ? 'check-circle' : 'circle'"
                :size="16"
                :class="typed(item).isCurrent ? 'text-success' : 'text-muted'"
            />
        </template>
    </AdminListPage>
</template>

<script setup lang="ts">
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import AdminListPage from '@/components/feature/admin/AdminListPage.vue';
    import Badge from '@/components/ui/Badge.vue';
    import { ADMIN_ROUTES } from '@/config/routes';
    import { experiencesApi } from '@/services/api/modules/experiences';
    import { formatDateRange } from '@/services/utils/date';
    import { asAdminExperience } from '@/services/utils/guards/admin';

    import type { ListParams } from '@/types/composables';
    import type { AdminExperience, DataItem, PaginatedResponse } from '@/types/feature/admin';

    const typed = (item: DataItem) => asAdminExperience(item);

    const getField = (item: DataItem, key: string): unknown => (item as Record<string, unknown>)[key];

    definePageMeta({ layout: 'admin', title: 'Expériences' });

    const columns = [
        { key: 'title', label: 'Poste / Diplôme', sortable: true, width: '35%' },
        { key: 'type', label: 'Type', sortable: true },
        { key: 'period', label: 'Période', sortable: false },
        { key: 'isCurrent', label: 'Actuel', sortable: true },
    ];

    const formatPeriod = (item: DataItem): string => {
        const exp = asAdminExperience(item);
        return formatDateRange(exp.startDate, exp.endDate);
    };

    const queryFn = (params: ListParams) => {
        const queryParams: Record<string, unknown> = {
            page: params.page,
            page_size: params.pageSize,
            ordering: params.ordering,
        };
        if (params.search) {
            queryParams.search = params.search;
        }
        return experiencesApi.getAdminList<PaginatedResponse<AdminExperience>>(queryParams);
    };

    const deleteFn = async (item: AdminExperience) => {
        await experiencesApi.delete(String(item.id));
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;

    .cell-title {
        display: flex;
        flex-direction: column;

        &__text {
            @include mix.cell-title-text;
        }

        &__company {
            color: vars.$text-muted;
        }
    }

    .cell-period {
        color: vars.$text-secondary;
    }

    .text-success {
        color: vars.$success-color;
    }

    .text-muted {
        color: vars.$text-muted;
    }
</style>
