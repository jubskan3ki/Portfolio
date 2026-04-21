<template>
    <div class="session-list">
        <div class="session-list__header">
            <div>
                <h3 class="session-list__title">Sessions actives</h3>
            </div>
            <BaseButton
                v-if="otherSessionsCount > 0"
                variant="outline"
                size="sm"
                :loading="isRevokingAll"
                @click="handleRevokeAll"
            >
                <template #icon-left>
                    <BaseIcon name="x-circle" :size="14" />
                </template>
                Revoquer les autres ({{ otherSessionsCount }})
            </BaseButton>
        </div>

        <div v-if="isLoading" class="session-list__loading">
            <Spinner size="sm" />
            <span>Chargement des sessions...</span>
        </div>

        <EmptyState v-else-if="sessions.length === 0" icon="monitor" title="Aucune session active" size="sm" />

        <div v-else class="session-list__items">
            <SessionItem
                v-for="session in sessions"
                :key="session.id"
                :session="session"
                :is-revoking="revokingSessionId === session.id"
                @revoke="handleRevokeSession"
            />
        </div>
    </div>
</template>

<script setup lang="ts">
    import { computed, ref } from 'vue';

    import BaseButton from '@/components/base/BaseButton.vue';
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import SessionItem from '@/components/feature/admin/SessionItem.vue';
    import EmptyState from '@/components/feedback/EmptyState.vue';
    import Spinner from '@/components/loaders/Spinner.vue';
    import { useAlert } from '@/composables/ui/useAlert';
    import { useSessions, useRevokeSession, useRevokeAllSessions } from '@/services/api/modules/auth';

    const { data: sessionsData, isLoading, refetch } = useSessions();
    const { mutateAsync: revokeSession } = useRevokeSession();
    const { mutateAsync: revokeAll, isPending: isRevokingAll } = useRevokeAllSessions();
    const { success: showSuccess, error: showError } = useAlert();

    const sessions = computed(() => sessionsData.value?.sessions ?? []);
    const otherSessionsCount = computed(() => sessions.value.filter((s) => !s.isCurrent).length);
    const revokingSessionId = ref<string | null>(null);

    const handleRevokeSession = async (sessionId: string) => {
        const session = sessions.value.find((s) => s.id === sessionId);
        if (session?.isCurrent) {
            showError('Utilisez "Se deconnecter" pour terminer la session actuelle.');
            return;
        }

        revokingSessionId.value = sessionId;
        try {
            await revokeSession(sessionId);
            showSuccess('Session revoquee.');
            await refetch();
        } catch {
            showError('Impossible de revoquer la session.');
        } finally {
            revokingSessionId.value = null;
        }
    };

    const handleRevokeAll = async () => {
        try {
            await revokeAll();
            showSuccess('Toutes les autres sessions ont ete revoquees.');
            await refetch();
        } catch {
            showError('Echec de la revocation des sessions.');
        }
    };

    defineExpose({
        refresh: refetch,
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;

    .session-list {
        &__header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: vars.$spacing-sm;
            margin-bottom: vars.$spacing-md;
        }

        &__title {
            font-weight: vars.$font-weight-semibold;
        }

        &__hint {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            font-size: 12px;
            color: vars.$text-muted;
            margin-top: 2px;
        }

        &__loading {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: vars.$spacing-xs;
            padding: vars.$spacing-xl;
            color: vars.$text-muted;
            text-align: center;
        }

        &__items {
            display: flex;
            flex-direction: column;
            gap: vars.$spacing-xs;
        }
    }
</style>
