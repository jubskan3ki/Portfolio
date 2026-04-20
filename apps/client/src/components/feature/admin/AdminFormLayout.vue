<template>
    <div class="admin-page">
        <div class="admin-page__header">
            <div>
                <h1 class="admin-page__title">{{ title }}</h1>
                <p v-if="subtitle" class="admin-page__subtitle">{{ subtitle }}</p>
            </div>
            <slot name="header-actions"></slot>
        </div>

        <div v-if="loading" class="admin-loading">
            <Spinner />
            <p>{{ loadingText }}</p>
        </div>

        <div v-else-if="error" class="admin-error">
            <div class="admin-error__icon">
                <BaseIcon :name="errorIcon" :size="48" />
            </div>
            <h3 class="admin-error__title">{{ errorTitle }}</h3>
            <p class="admin-error__message">{{ error }}</p>
            <div class="admin-error__actions">
                <BaseButton v-if="showRetry" variant="primary" @click="$emit('retry')"> Réessayer </BaseButton>
                <BaseButton :to="backUrl" variant="outline">
                    {{ backText }}
                </BaseButton>
            </div>
        </div>

        <div v-else class="admin-form">
            <form @submit.prevent="$emit('submit')">
                <div class="admin-form__body">
                    <slot></slot>
                </div>

                <div class="admin-form__footer">
                    <BaseButton :to="backUrl" variant="outline" :disabled="submitting">
                        {{ cancelText }}
                    </BaseButton>
                    <BaseButton type="submit" variant="primary" :disabled="submitting || submitDisabled">
                        <template v-if="submitting" #icon-left>
                            <span class="spinner"></span>
                        </template>
                        {{ submitting ? submittingText : submitText }}
                    </BaseButton>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
    import BaseButton from '@/components/base/BaseButton.vue';
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import Spinner from '@/components/loaders/Spinner.vue';

    import type { AdminFormLayoutProps } from '@/types/components/admin';

    withDefaults(defineProps<AdminFormLayoutProps>(), {
        subtitle: '',
        loading: false,
        loadingText: 'Chargement...',
        error: '',
        errorTitle: 'Erreur',
        errorIcon: 'alert-triangle',
        showRetry: true,
        backText: 'Retour',
        cancelText: 'Annuler',
        submitText: 'Enregistrer',
        submittingText: 'Enregistrement...',
        submitting: false,
        submitDisabled: false,
    });

    defineEmits<{
        submit: [];
        retry: [];
    }>();
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;

    .admin-page {
        &__header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: vars.$spacing-lg;
            gap: vars.$spacing-md;

            @include mix.responsive(mobile) {
                flex-direction: column;
            }
        }

        &__title {
            margin-bottom: vars.$spacing-xxxs;
        }

        &__subtitle {
            color: vars.$text-secondary;
        }
    }

    .admin-loading {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: vars.$spacing-xxl;
        color: vars.$text-muted;
        gap: vars.$spacing-md;
    }

    .admin-error {
        @include mix.admin-card(vars.$spacing-md);
        text-align: center;
        padding: vars.$spacing-xxl;

        &__icon {
            color: vars.$danger-color;
            margin-bottom: vars.$spacing-md;
        }

        &__title {
            margin-bottom: vars.$spacing-xs;
            color: vars.$text-primary;
        }

        &__message {
            color: vars.$text-secondary;
            margin-bottom: vars.$spacing-lg;
            max-width: 400px;
            margin-left: auto;
            margin-right: auto;
        }

        &__actions {
            display: flex;
            gap: vars.$spacing-xs;
            justify-content: center;
        }
    }

    .admin-form {
        @include mix.admin-card(vars.$spacing-md);

        &__body {
            display: flex;
            flex-direction: column;
            gap: vars.$spacing-md;
        }

        &__footer {
            display: flex;
            justify-content: flex-end;
            gap: vars.$spacing-xs;
            margin-top: vars.$spacing-xl;
            padding-top: vars.$spacing-lg;
            border-top: 1px solid vars.$admin-border;
        }
    }

    .spinner {
        width: 16px;
        height: 16px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-top-color: vars.$white;
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }
</style>
