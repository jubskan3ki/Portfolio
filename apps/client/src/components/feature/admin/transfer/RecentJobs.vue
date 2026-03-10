<template>
    <div v-if="jobs.length" class="admin-card">
        <div class="admin-card__header">
            <h2 class="admin-card__title">Historique récent</h2>
        </div>
        <div class="jobs-list">
            <div v-for="job in jobs" :key="job.id" class="job-item">
                <div class="job-item__icon" :class="`job-item__icon--${job.type}`">
                    <BaseIcon :name="job.type === 'export' ? 'download' : 'upload'" :size="16" />
                </div>
                <div class="job-item__info">
                    <span class="job-item__title">
                        {{ job.type === 'export' ? 'Export' : 'Import' }} {{ job.module }}
                    </span>
                    <small class="job-item__date">{{ formatTransferDate(job.createdAt) }}</small>
                </div>
                <small class="job-item__status" :class="`job-item__status--${job.status}`">
                    {{ getStatusLabel(job.status) }}
                </small>
                <BaseButton
                    v-if="job.downloadUrl && job.status === 'completed'"
                    :to="job.downloadUrl"
                    variant="outline"
                    size="sm"
                    aria-label="Télécharger le fichier"
                >
                    <template #icon-left>
                        <BaseIcon name="download" :size="14" />
                    </template>
                </BaseButton>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import BaseButton from '@/components/base/BaseButton.vue';
    import { formatTransferDate, getStatusLabel } from '@/composables/data/useTransfer';

    import type { JobStatus } from '@/types/api/transfer';

    interface TransferJob {
        id: string | number;
        type: 'export' | 'import';
        module: string;
        status: JobStatus;
        createdAt: string;
        downloadUrl?: string;
    }

    defineProps<{
        jobs: TransferJob[];
    }>();
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as func;

    .admin-card {
        background: vars.$white;
        border-radius: 16px;
        border: 1px solid vars.$admin-border;
        padding: vars.$spacing-lg;
        box-shadow:
            0 1px 3px rgba(0, 0, 0, 0.02),
            0 4px 12px rgba(0, 0, 0, 0.02);

        &__header {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xxxxs;
            margin-bottom: vars.$spacing-lg;
            padding-bottom: vars.$spacing-xxxxs;
            border-bottom: 1px solid vars.$admin-border;
        }

        &__title {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xxxxs;
            font-weight: vars.$font-weight-semibold;
        }
    }

    .jobs-list {
        display: flex;
        flex-direction: column;
        gap: vars.$spacing-xs;
    }

    .job-item {
        display: flex;
        align-items: center;
        gap: vars.$spacing-md;
        padding: vars.$spacing-xs 0;
        border-bottom: 1px solid vars.$admin-border;

        &:last-child {
            border-bottom: none;
        }

        &__icon {
            width: 32px;
            height: 32px;
            border-radius: vars.$border-radius-md;
            display: flex;
            align-items: center;
            justify-content: center;

            &--export {
                background-color: rgba(#3b82f6, 0.1);
                color: #3b82f6;
            }

            &--import {
                background-color: rgba(#10b981, 0.1);
                color: #10b981;
            }
        }

        &__info {
            flex: 1;
        }

        &__title {
            display: block;
            font-weight: vars.$font-weight-medium;
        }

        &__date {
            color: vars.$text-muted;
        }

        &__status {
            padding: 2px 8px;
            border-radius: vars.$border-radius-full;

            &--completed {
                background-color: func.color-alpha(vars.$success-color, 0.1);
                color: vars.$success-color;
            }

            &--partially_completed {
                background-color: func.color-alpha(vars.$warning-color, 0.1);
                color: vars.$warning-color;
            }

            &--processing,
            &--validating {
                background-color: func.color-alpha(vars.$warning-color, 0.1);
                color: vars.$warning-color;
            }

            &--failed {
                background-color: func.color-alpha(vars.$danger-color, 0.1);
                color: vars.$danger-color;
            }

            &--pending {
                background-color: vars.$bg-tertiary;
                color: vars.$text-muted;
            }
        }
    }
</style>
