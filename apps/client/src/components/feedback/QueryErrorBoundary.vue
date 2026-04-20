<template>
    <slot v-if="!isError"></slot>
    <div v-else class="query-error" :class="errorClasses">
        <div class="query-error__content">
            <div class="query-error__icon-wrapper">
                <div class="query-error__icon-bg"></div>
                <BaseIcon :name="errorConfig.icon" :size="40" class="query-error__icon" />
            </div>

            <h4 class="query-error__title">{{ errorConfig.title }}</h4>
            <p class="query-error__message">{{ errorConfig.message }}</p>

            <div v-if="showRetry" class="query-error__actions">
                <BaseButton variant="outline" size="sm" @click="handleRetry">
                    <template #icon-left>
                        <BaseIcon name="refresh-cw" :size="14" />
                    </template>
                    Réessayer
                </BaseButton>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import BaseButton from '@/components/base/BaseButton.vue';
    import BaseIcon from '@/components/base/BaseIcon.vue';

    import type {
        QueryErrorBoundaryErrorConfig,
        QueryErrorBoundaryErrorType,
        QueryErrorBoundaryProps,
    } from '@/types/components/feedback';

    type Props = QueryErrorBoundaryProps;

    const props = withDefaults(defineProps<Props>(), {
        error: null,
        showRetry: true,
    });

    const emit = defineEmits<{
        retry: [];
    }>();

    // Configuration par type d'erreur
    const ERROR_CONFIG: Record<QueryErrorBoundaryErrorType, Omit<QueryErrorBoundaryErrorConfig, 'message'> & { message: string }> = {
        'not-found': {
            icon: 'search-x',
            title: 'Contenu introuvable',
            message: 'Le contenu demandé n\'existe pas ou a été supprimé.',
        },
        forbidden: {
            icon: 'lock',
            title: 'Accès refusé',
            message: 'Vous n\'avez pas les droits pour accéder à ce contenu.',
        },
        unauthorized: {
            icon: 'user-x',
            title: 'Authentification requise',
            message: 'Veuillez vous connecter pour accéder à ce contenu.',
        },
        server: {
            icon: 'server-off',
            title: 'Erreur serveur',
            message: 'Une erreur serveur est survenue. Veuillez réessayer plus tard.',
        },
        client: {
            icon: 'alert-circle',
            title: 'Erreur de requête',
            message: 'La requête a échoué. Veuillez vérifier les données.',
        },
        network: {
            icon: 'wifi-off',
            title: 'Erreur de chargement',
            message: 'Une erreur est survenue lors du chargement des données.',
        },
    };

    // Status HTTP depuis l'erreur
    const httpStatus = computed(() => {
        const err = props.error as { status?: number; statusCode?: number } | null;
        return err?.status ?? err?.statusCode;
    });

    // Type d'erreur basé sur le status HTTP
    const errorType = computed<QueryErrorBoundaryErrorType>(() => {
        const status = httpStatus.value;
        if (status === 404) {
            return 'not-found';
        }
        if (status === 403) {
            return 'forbidden';
        }
        if (status === 401) {
            return 'unauthorized';
        }
        if (status === 500) {
            return 'server';
        }
        if (status !== undefined && status >= 400 && status < 500) {
            return 'client';
        }
        return 'network';
    });

    // Configuration de l'erreur actuelle
    const errorConfig = computed<QueryErrorBoundaryErrorConfig>(() => {
        const config = ERROR_CONFIG[errorType.value];
        return {
            ...config,
            // Utiliser le message de l'erreur si disponible pour network
            message: errorType.value === 'network' && props.error?.message ? props.error.message : config.message,
        };
    });

    const errorClasses = computed(() => [`query-error--${errorType.value}`]);

    const handleRetry = () => {
        props.refetch?.();
        emit('retry');
    };

    defineExpose({
        errorType,
        httpStatus,
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as func;

    .query-error {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: vars.$spacing-xl;
        min-height: 250px;

        &__content {
            text-align: center;
            max-width: 400px;
        }

        // Icon
        &__icon-wrapper {
            position: relative;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-bottom: vars.$spacing-lg;
        }

        &__icon-bg {
            position: absolute;
            width: 80px;
            height: 80px;
            border-radius: vars.$border-radius-full;
            background: func.color-alpha(vars.$warning-color, 0.1);
        }

        &__icon {
            position: relative;
            z-index: 1;
            color: vars.$warning-color;
        }

        // Text
        &__title {
            margin: 0 0 vars.$spacing-xxs;
            font-weight: vars.$font-weight-bold;
            color: vars.$text-primary;
            line-height: vars.$line-height-tight;
        }

        &__message {
            margin: 0 0 vars.$spacing-lg;
            color: vars.$text-secondary;
            line-height: vars.$line-height-relaxed;
        }

        // Actions
        &__actions {
            display: flex;
            justify-content: center;
            gap: vars.$spacing-xs;
        }

        // Variants basées sur le type d'erreur
        &--not-found {
            .query-error__icon-bg {
                background: func.color-alpha(vars.$info-color, 0.1);
            }

            .query-error__icon {
                color: vars.$info-color;
            }
        }

        &--forbidden,
        &--unauthorized {
            .query-error__icon-bg {
                background: func.color-alpha(vars.$danger-color, 0.1);
            }

            .query-error__icon {
                color: vars.$danger-color;
            }
        }

        &--server {
            .query-error__icon-bg {
                background: func.color-alpha(vars.$danger-color, 0.12);
            }

            .query-error__icon {
                color: vars.$danger-color;
            }
        }

        &--client {
            .query-error__icon-bg {
                background: func.color-alpha(vars.$warning-color, 0.12);
            }

            .query-error__icon {
                color: vars.$warning-dark;
            }
        }

        &--network {
            .query-error__icon-bg {
                background: func.color-alpha(vars.$gray, 0.12);
            }

            .query-error__icon {
                color: vars.$gray-dark;
            }
        }
    }
</style>
