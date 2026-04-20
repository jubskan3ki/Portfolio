<template>
    <div class="admin-page">
        <div class="admin-page__header">
            <div>
                <h1 class="admin-page__title">Messages</h1>
                <p class="admin-page__subtitle">Gérez les messages de contact reçus</p>
            </div>
        </div>

        <DataTable
            :data="messages"
            :columns="columns"
            :loading="isLoading"
            :total-items="pagination.totalItems.value"
            :current-page="pagination.currentPage.value"
            :per-page="pagination.perPage.value"
            :filters="filters"
            selectable
            @sort="handleSort"
            @query-change="handleQueryChange"
            @pagination-change="handlePaginationChange"
            @bulk-delete="handleBulkDelete"
        >
            <template #toolbar-actions>
                <BaseButton variant="outline" size="icon" @click="refresh">
                    <BaseIcon name="refresh-cw" :size="16" />
                </BaseButton>
            </template>

            <template #cell-sender="{ item }">
                <div class="cell-sender">
                    <div class="cell-sender__avatar">{{ getInitials(String(typed(item).name || '')) }}</div>
                    <div class="cell-sender__info">
                        <span class="cell-sender__name">{{ typed(item).name }}</span>
                        <small class="cell-sender__email">{{ typed(item).email }}</small>
                    </div>
                </div>
            </template>

            <template #cell-subject="{ item }">
                <div class="cell-subject" :class="{ 'cell-subject--unread': !typed(item).isRead }">
                    <span class="cell-subject__text">{{ typed(item).subject }}</span>
                    <small class="cell-subject__preview">
                        {{ truncateText(String(typed(item).message || ''), 60) }}
                    </small>
                </div>
            </template>

            <template #cell-status="{ item }">
                <Badge :variant="typed(item).isRead ? 'outline' : 'primary'">
                    {{ typed(item).isRead ? 'Lu' : 'Non lu' }}
                </Badge>
            </template>

            <template #cell-created_at="{ value }">
                {{ formatMessageDate(value) }}
            </template>

            <template #actions="{ item }">
                <DataTableActions :show-edit="false" @view="viewMessage(item)" @delete="confirmDelete(item)" />
            </template>
        </DataTable>

        <Teleport to="body">
            <Transition name="fade">
                <div
                    v-if="showViewModal"
                    class="modal-overlay"
                    role="button"
                    tabindex="0"
                    aria-label="Fermer"
                    @click="showViewModal = false"
                    @keydown.enter="showViewModal = false"
                >
                    <div class="modal-content modal-content--lg" @click.stop>
                        <div class="message-detail">
                            <div class="message-detail__header">
                                <h2>{{ selectedMessage?.subject }}</h2>
                                <BaseButton
                                    variant="ghost"
                                    size="icon"
                                    aria-label="Fermer"
                                    @click="showViewModal = false"
                                >
                                    <BaseIcon name="x" :size="20" />
                                </BaseButton>
                            </div>
                            <div class="message-detail__meta">
                                <div class="message-detail__sender">
                                    <div class="cell-sender__avatar">{{ getInitials(selectedMessage?.name) }}</div>
                                    <div>
                                        <strong>{{ selectedMessage?.name }}</strong>
                                        <small>{{ selectedMessage?.email }}</small>
                                    </div>
                                </div>
                                <small class="message-detail__date">{{
                                    formatMessageDate(selectedMessage?.createdAt)
                                }}</small>
                            </div>
                            <div class="message-detail__body">
                                <p>{{ selectedMessage?.message }}</p>
                            </div>
                            <div class="message-detail__actions">
                                <BaseButton
                                    :to="`mailto:${selectedMessage?.email}?subject=Re: ${selectedMessage?.subject}`"
                                    variant="primary"
                                    target="_blank"
                                >
                                    <template #icon-left>
                                        <BaseIcon name="reply" :size="16" />
                                    </template>
                                    Répondre
                                </BaseButton>
                                <BaseButton variant="danger" @click="confirmDeleteFromModal">
                                    <template #icon-left>
                                        <BaseIcon name="trash-2" :size="16" />
                                    </template>
                                    Supprimer
                                </BaseButton>
                            </div>
                        </div>
                    </div>
                </div>
            </Transition>
        </Teleport>

        <ConfirmDialog
            v-model="deletion!.showModal.value"
            variant="danger"
            title="Supprimer le message ?"
            :message="`Cette action est irréversible. Le message de &quot;${deletion?.itemToDelete.value?.name}&quot;
            sera définitivement supprimé.`"
            confirm-text="Supprimer"
            :loading="deletion?.isDeleting.value"
            @confirm="deletion?.execute()"
            @cancel="deletion?.cancel()"
        />

        <ConfirmDialog
            v-model="bulkDeletion!.showModal.value"
            variant="danger"
            title="Supprimer les messages sélectionnés ?"
            :message="`Cette action est irréversible. ${bulkDeletion?.itemsToDelete.value.length} message(s)
            seront définitivement supprimés.`"
            confirm-text="Supprimer tout"
            :loading="bulkDeletion?.isDeleting.value"
            @confirm="bulkDeletion?.execute()"
            @cancel="bulkDeletion?.cancel()"
        />
    </div>
</template>

<script setup lang="ts">
    import { ref } from 'vue';

    import BaseButton from '@/components/base/BaseButton.vue';
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import DataTable from '@/components/feature/admin/DataTable.vue';
    import DataTableActions from '@/components/feature/admin/DataTableActions.vue';
    import ConfirmDialog from '@/components/feedback/ConfirmDialog.vue';
    import Badge from '@/components/ui/Badge.vue';
    import { useEscapeKey } from '@/composables';
    import { useDataList } from '@/composables/data/useDataList';
    import { useSeo } from '@/composables/seo/useSeo';
    import { useAlert } from '@/composables/ui/useAlert';
    import { contactApi } from '@/services/api/modules/contact';
    import { formatDate } from '@/services/utils/date';
    import { asAdminMessage } from '@/services/utils/guards/admin';
    import { truncateText } from '@/services/utils/helpers';

    import type { ListParams, BulkDeleteResult } from '@/types/composables';
    import type { AdminMessage, DataItem, PaginatedResponse } from '@/types/feature/admin';

    /** Type-safe cast for template use */
    const typed = (item: DataItem) => asAdminMessage(item);

    definePageMeta({ layout: 'admin', title: 'Messages' });

    // SEO - noindex for admin pages
    useSeo({
        title: 'Gestion des Messages',
        description: 'Administration des messages de contact',
        noindex: true,
    });

    const { error: showError, success: showSuccess } = useAlert();

    // View modal state (separate from delete modal)
    const showViewModal = ref(false);
    const selectedMessage = ref<AdminMessage | null>(null);

    // Close modal on Escape (auto cleanup)
    useEscapeKey(
        () => {
            showViewModal.value = false;
        },
        { enabled: showViewModal },
    );

    const columns = [
        { key: 'sender', label: 'Expéditeur', width: '25%' },
        { key: 'subject', label: 'Sujet', width: '40%' },
        { key: 'status', label: 'Statut', sortable: true },
        { key: 'created_at', label: 'Date', sortable: true },
    ];

    const filters = [
        {
            key: 'isRead',
            label: 'Statut',
            options: [
                { value: 'false', label: 'Non lu' },
                { value: 'true', label: 'Lu' },
            ],
        },
    ];

    // Utilisation du composable generique useDataList
    const {
        items: messages,
        isLoading,
        pagination,
        sorting,
        search,
        deletion,
        bulkDeletion,
        refresh,
    } = useDataList<AdminMessage>({
        queryKey: ['admin', 'messages'],
        queryFn: (params: ListParams) => {
            const queryParams: Record<string, unknown> = {
                page: params.page,
                page_size: params.pageSize,
                ordering: params.ordering,
            };
            if (params.search) {
                queryParams.search = params.search;
            }
            return contactApi.getAdminMessages<PaginatedResponse<AdminMessage>>(queryParams);
        },
        defaultSort: 'created_at',
        defaultSortOrder: 'desc',
        defaultPerPage: 10,
        deleteFn: async (item: AdminMessage) => {
            await contactApi.deleteMessage(String(item.id));
        },
        onDeleteSuccess: () => {
            showSuccess('Message supprimé avec succès');
        },
        onDeleteError: (error) => {
            showError(error.message || 'Impossible de supprimer le message', 'Erreur');
        },
        onBulkDeleteSuccess: (result: BulkDeleteResult) => {
            if (result.errorCount === 0) {
                showSuccess(`${result.successCount} message(s) supprimé(s) avec succès`);
            } else {
                showSuccess(`${result.successCount} supprimé(s), ${result.errorCount} erreur(s)`);
            }
        },
        onBulkDeleteError: (error) => {
            showError(error.message || 'Impossible de supprimer les messages', 'Erreur');
        },
    });

    const getInitials = (name: string | undefined) => {
        if (!name) {
            return '?';
        }
        return name
            .split(' ')
            .map((n) => n[0])
            .join('')
            .toUpperCase()
            .slice(0, 2);
    };

    // Format date avec heure pour les messages
    const formatMessageDate = (date: unknown) => {
        if (!date) {
            return '';
        }
        return formatDate(String(date), 'D MMM YYYY à HH:mm');
    };

    // Handlers pour le DataTable
    const handleSort = (key: string, order: 'asc' | 'desc') => {
        sorting.setSort(key, order);
    };

    const handleQueryChange = (payload: { search?: string; filters?: Record<string, string> }) => {
        if (payload.search !== undefined) {
            search.setSearch(payload.search);
        }
        if (payload.filters !== undefined) {
            // Filters are handled via URL params or separate state
            refresh();
        }
    };

    const handlePaginationChange = (payload: { page?: number; perPage?: number }) => {
        if (payload.page !== undefined) {
            pagination.setPage(payload.page);
        }
        if (payload.perPage !== undefined) {
            pagination.setPerPage(payload.perPage);
        }
    };

    const handleBulkDelete = (items: DataItem[]) => {
        const messagesToDelete = items.map(asAdminMessage);
        bulkDeletion?.confirm(messagesToDelete);
    };

    const viewMessage = async (item: DataItem) => {
        const message = asAdminMessage(item);

        // IMPORTANT: Marquer comme lu AVANT d'afficher la modale (corrige race condition)
        if (!message.isRead) {
            try {
                await contactApi.markAsRead(String(message.id));
                message.isRead = true;
            } catch {
                // Echec silencieux — le marquage comme lu est non-critique
            }
        }

        // Afficher la modale seulement après avoir marqué comme lu
        selectedMessage.value = message;
        showViewModal.value = true;
    };

    const confirmDelete = (item: DataItem) => {
        deletion?.confirm(asAdminMessage(item));
    };

    const confirmDeleteFromModal = () => {
        if (selectedMessage.value) {
            showViewModal.value = false;
            deletion?.confirm(selectedMessage.value);
        }
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;

    .admin-page {
        &__header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: vars.$spacing-lg;
        }

        &__title {
            margin-bottom: vars.$spacing-xxxs;
        }

        &__subtitle {
            color: vars.$text-secondary;
        }
    }

    .cell-sender {
        display: flex;
        align-items: center;
        gap: vars.$spacing-xs;

        &__avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background-color: vars.$primary-color;
            color: vars.$white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: vars.$font-weight-bold;
        }

        &__info {
            display: flex;
            flex-direction: column;
        }

        &__name {
            font-weight: vars.$font-weight-medium;
        }

        &__email {
            color: vars.$text-muted;
        }
    }

    .cell-subject {
        &--unread {
            .cell-subject__text {
                font-weight: vars.$font-weight-semibold;
            }
        }

        &__text {
            display: block;
            color: vars.$text-primary;
        }

        &__preview {
            display: block;
            color: vars.$text-muted;
            margin-top: 2px;
        }
    }

    .modal-overlay {
        position: fixed;
        inset: 0;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: vars.$spacing-lg;
        z-index: vars.$z-index-modal;
    }

    .modal-content {
        background-color: vars.$white;
        border-radius: vars.$border-radius-xl;
        max-width: 400px;
        width: 100%;

        &--lg {
            max-width: 600px;
        }
    }

    .message-detail {
        padding: vars.$spacing-xl;
        position: relative;

        &__header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: vars.$spacing-lg;

            h2 {
                padding-right: vars.$spacing-xl;
            }
        }

        &__meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: vars.$spacing-md;
            border-bottom: 1px solid vars.$admin-border;
            margin-bottom: vars.$spacing-md;
        }

        &__sender {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;

            strong {
                display: block;
            }

            small {
                color: vars.$text-muted;
            }
        }

        &__date {
            color: vars.$text-muted;
        }

        &__body {
            padding: vars.$spacing-md 0;

            p {
                line-height: 1.6;
                color: vars.$text-primary;
                white-space: pre-wrap;
            }
        }

        &__actions {
            display: flex;
            gap: vars.$spacing-xs;
            padding-top: vars.$spacing-md;
            border-top: 1px solid vars.$admin-border;
        }
    }

    .fade-enter-active,
    .fade-leave-active {
        transition: opacity 0.2s ease;
    }

    .fade-enter-from,
    .fade-leave-to {
        opacity: 0;
    }
</style>
