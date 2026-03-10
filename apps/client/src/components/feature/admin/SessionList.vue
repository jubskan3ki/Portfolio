<template>
    <div class="session-list">
        <div class="session-list__header">
            <h3 class="session-list__title">Sessions actives</h3>
            <BaseButton
                v-if="sessions.length > 1"
                variant="outline"
                size="sm"
                :loading="isRevokingAll"
                @click="handleRevokeAll"
            >
                <template #icon-left>
                    <BaseIcon name="x-circle" :size="14" />
                </template>
                Tout revoquer
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
    import { useSessions, useRevokeSession, useRevokeAllSessions } from '@/services/api/modules/auth';

    const { data: sessionsData, isLoading, refetch } = useSessions();
    const { mutateAsync: revokeSession } = useRevokeSession();
    const { mutateAsync: revokeAll, isPending: isRevokingAll } = useRevokeAllSessions();

    const sessions = computed(() => sessionsData.value ?? []);
    const revokingSessionId = ref<string | null>(null);

    const handleRevokeSession = async (sessionId: string) => {
        revokingSessionId.value = sessionId;
        try {
            await revokeSession(sessionId);
        } finally {
            revokingSessionId.value = null;
        }
    };

    const handleRevokeAll = async () => {
        await revokeAll();
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
            align-items: center;
            margin-bottom: vars.$spacing-md;
        }

        &__title {
            font-weight: vars.$font-weight-semibold;
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
