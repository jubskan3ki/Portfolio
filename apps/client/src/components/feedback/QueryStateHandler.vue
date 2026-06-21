<template>
    <div class="query-state-handler">
        <div v-if="loading" class="query-state-handler__state">
            <slot name="loading">
                <Spinner :size="loadingSize" :label="loadingMessage" />
            </slot>
        </div>

        <div v-else-if="error" class="query-state-handler__state query-state-handler__state--error">
            <slot name="error" :error="error">
                <ErrorMessage :message="typeof error === 'string' ? error : error.message" />
                <BaseButton
                    v-if="retryable"
                    variant="primary"
                    size="sm"
                    class="query-state-handler__retry"
                    @click="$emit('retry')"
                >
                    {{ retryText }}
                </BaseButton>
            </slot>
        </div>

        <!--
            État vide : le slot `empty` (override total) a TOUJOURS priorité sur les props
            `emptyTitle`/`emptyDescription`/`emptyIcon`, qui ne servent qu'au rendu par défaut.
        -->
        <div v-else-if="empty" class="query-state-handler__state">
            <slot name="empty">
                <EmptyState :title="emptyTitle" :description="emptyDescription" :icon="emptyIcon" :icon-size="48">
                    <template v-if="$slots['empty-action']" #action>
                        <slot name="empty-action"></slot>
                    </template>
                </EmptyState>
            </slot>
        </div>

        <slot v-else></slot>
    </div>
</template>

<script setup lang="ts">
    import BaseButton from '@/components/base/BaseButton.vue';
    import EmptyState from '@/components/feedback/EmptyState.vue';
    import ErrorMessage from '@/components/feedback/ErrorMessage.vue';
    import Spinner from '@/components/loaders/Spinner.vue';

    import type { QueryStateHandlerProps } from '@/types/components/feedback';

    withDefaults(defineProps<QueryStateHandlerProps>(), {
        loading: false,
        error: null,
        empty: false,
        loadingMessage: 'Chargement...',
        loadingSize: 'lg',
        emptyTitle: 'Aucun résultat',
        emptyDescription: '',
        emptyIcon: 'folder',
        retryable: true,
        retryText: 'Réessayer',
    });

    defineEmits<{
        retry: [];
    }>();
</script>

<style lang="scss" scoped>
    .query-state-handler {
        width: 100%;

        &__state {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 2rem 1rem;
            min-height: 200px;
        }

        &__retry {
            margin-top: 1rem;
        }
    }
</style>
