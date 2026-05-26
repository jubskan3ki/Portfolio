<template>
    <slot v-if="!error"></slot>
    <div
        v-else
        class="error-boundary"
        :class="boundaryClasses"
        role="alert"
        aria-live="assertive"
    >
        <div class="error-boundary__content">
            <div v-if="variant !== 'inline'" class="error-boundary__icon-wrapper">
                <div class="error-boundary__icon-bg"></div>
                <BaseIcon :name="errorIcon" :size="iconSize" class="error-boundary__icon" />
            </div>

            <BaseIcon v-else :name="errorIcon" :size="16" class="error-boundary__inline-icon" />

            <div class="error-boundary__text">
                <h3 v-if="variant !== 'inline'" class="error-boundary__title">{{ title }}</h3>
                <p class="error-boundary__message">{{ displayMessage }}</p>
            </div>

            <div v-if="showActions" class="error-boundary__actions">
                <BaseButton
                    v-if="showRetry"
                    :variant="variant === 'inline' ? 'ghost' : 'primary'"
                    :size="actionSize"
                    @click="handleRetry"
                >
                    <template #icon-left>
                        <BaseIcon name="refresh-cw" :size="actionIconSize" />
                    </template>
                    <span v-if="variant !== 'inline'">Reessayer</span>
                </BaseButton>
                <BaseButton
                    v-if="showHomeButton && variant !== 'inline'"
                    variant="outline"
                    :size="actionSize"
                    :to="ROUTES.HOME"
                >
                    <template #icon-left>
                        <BaseIcon name="home" :size="actionIconSize" />
                    </template>
                    Retour a l'accueil
                </BaseButton>
            </div>

            <!-- Technical details (dev only) -->
            <details v-if="showDetails && error && variant !== 'inline'" class="error-boundary__details">
                <summary>
                    <BaseIcon name="code" :size="14" />
                    Details techniques
                </summary>
                <div class="error-boundary__details-content">
                    <p v-if="errorType !== 'unknown'" class="error-boundary__error-type">Type: {{ errorType }}</p>
                    <pre>{{ error.stack || error.message }}</pre>
                </div>
            </details>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref, onErrorCaptured, computed } from 'vue';

    import BaseButton from '@/components/base/BaseButton.vue';
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import { ROUTES } from '@/config/routes';

    import type {
        ErrorBoundaryErrorType,
        ErrorBoundaryProps,
        ErrorBoundarySize,
    } from '@/types/components/feedback';

    type Props = ErrorBoundaryProps;

    const props = withDefaults(defineProps<Props>(), {
        title: 'Une erreur est survenue',
        fallbackMessage: 'Une erreur inattendue s\'est produite. Veuillez reessayer.',
        showHomeButton: true,
        showDetails: false,
        showRetry: true,
        variant: 'default',
        size: 'md',
    });

    const emit = defineEmits<{
        retry: [];
        error: [error: Error];
    }>();

    const error = ref<Error | null>(null);

    const errorType = computed<ErrorBoundaryErrorType>(() => {
        if (!error.value) {
            return 'unknown';
        }
        const name = error.value.name?.toLowerCase() || '';
        const message = error.value.message?.toLowerCase() || '';

        if (name.includes('type') || message.includes('is not a')) {
            return 'type';
        }
        if (name.includes('reference') || message.includes('is not defined')) {
            return 'reference';
        }
        if (name.includes('syntax')) {
            return 'syntax';
        }
        if (message.includes('network') || message.includes('fetch')) {
            return 'network';
        }
        if (message.includes('timeout')) {
            return 'timeout';
        }
        return 'unknown';
    });

    const errorIcon = computed(() => {
        const icons: Record<ErrorBoundaryErrorType, string> = {
            type: 'alert-triangle',
            reference: 'file-question',
            syntax: 'code',
            network: 'wifi-off',
            timeout: 'clock',
            unknown: 'alert-circle',
        };
        return icons[errorType.value];
    });

    const displayMessage = computed(() => {
        if (props.fallbackMessage) {
            return props.fallbackMessage;
        }
        if (error.value?.message) {
            return error.value.message;
        }
        return 'Une erreur inattendue s\'est produite.';
    });

    // Size-based computeds
    const iconSize = computed(() => {
        const sizes: Record<ErrorBoundarySize, number> = { sm: 32, md: 48, lg: 64 };
        return sizes[props.size];
    });

    const actionSize = computed(() => {
        const sizes: Record<ErrorBoundarySize, 'sm' | 'md' | 'lg'> = { sm: 'sm', md: 'sm', lg: 'md' };
        return sizes[props.size];
    });

    const actionIconSize = computed(() => {
        const sizes: Record<ErrorBoundarySize, number> = { sm: 14, md: 16, lg: 18 };
        return sizes[props.size];
    });

    const boundaryClasses = computed(() => [`error-boundary--${props.variant}`, `error-boundary--${props.size}`]);

    const showActions = computed(() => props.showRetry || (props.showHomeButton && props.variant !== 'inline'));

    onErrorCaptured((err: Error) => {
        // Let Nuxt fatal errors (createError) bubble up to error.vue.
        const nuxtError = err as Error & {
            statusCode?: number;
            fatal?: boolean;
            cause?: { statusCode?: number; fatal?: boolean };
        };
        if (
            nuxtError.fatal
            || typeof nuxtError.statusCode === 'number'
            || nuxtError.cause?.fatal
            || typeof nuxtError.cause?.statusCode === 'number'
        ) {
            return undefined;
        }

        error.value = err;
        props.onError?.(err);
        emit('error', err);

        if (import.meta.dev) {
            console.error('[ErrorBoundary]', err);
        }

        return false;
    });

    const handleRetry = () => {
        error.value = null;
        emit('retry');
    };

    defineExpose({
        reset: () => {
            error.value = null;
        },
        hasError: computed(() => !!error.value),
        errorType,
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as func;

    .error-boundary {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: vars.$spacing-xl;

        &--default {
            min-height: 400px;
        }

        &--compact {
            min-height: 200px;
            padding: vars.$spacing-lg;
        }

        &--inline {
            min-height: auto;
            padding: vars.$spacing-sm vars.$spacing-md;
            background-color: func.color-alpha(vars.$danger-color, 0.08);
            border-radius: vars.$border-radius-md;
            border: 1px solid func.color-alpha(vars.$danger-color, 0.2);
        }

        // Size variants
        &--sm {
            .error-boundary__title {
                font-size: vars.$font-size-md;
            }

            .error-boundary__message {
                font-size: vars.$font-size-sm;
            }

            .error-boundary__icon-bg {
                width: 64px;
                height: 64px;
            }
        }

        &--lg {
            .error-boundary__title {
                font-size: vars.$font-size-xl;
            }

            .error-boundary__icon-bg {
                width: 128px;
                height: 128px;
            }
        }

        &__content {
            text-align: center;
            max-width: 500px;
        }

        &--inline &__content {
            display: flex;
            align-items: center;
            gap: vars.$spacing-sm;
            text-align: left;
            max-width: none;
            width: 100%;
        }

        // Icon
        &__icon-wrapper {
            position: relative;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-bottom: vars.$spacing-lg;
        }

        &--compact &__icon-wrapper {
            margin-bottom: vars.$spacing-md;
        }

        &__icon-bg {
            position: absolute;
            width: 96px;
            height: 96px;
            border-radius: vars.$border-radius-full;
            background: func.color-alpha(vars.$danger-color, 0.1);
        }

        &__icon {
            position: relative;
            z-index: 1;
            color: vars.$danger-color;
        }

        &__inline-icon {
            color: vars.$danger-color;
            flex-shrink: 0;
        }

        // Text
        &__text {
            flex: 1;
            min-width: 0;
        }

        &__title {
            margin: 0 0 vars.$spacing-xs;
            font-weight: vars.$font-weight-bold;
            color: vars.$text-primary;
        }

        &__message {
            margin: 0;
            color: vars.$text-secondary;
            line-height: vars.$line-height-relaxed;
        }

        &--default &__message,
        &--compact &__message {
            margin-bottom: vars.$spacing-lg;
        }

        &--inline &__message {
            color: vars.$danger-color;
            font-size: vars.$font-size-sm;
        }

        // Actions
        &__actions {
            display: flex;
            gap: vars.$spacing-xs;
            justify-content: center;
            flex-wrap: wrap;
        }

        &--inline &__actions {
            flex-shrink: 0;
        }

        // Details
        &__details {
            margin-top: vars.$spacing-xl;
            text-align: left;
            background-color: vars.$bg-secondary;
            border-radius: vars.$border-radius-lg;
            overflow: hidden;

            summary {
                display: flex;
                align-items: center;
                gap: vars.$spacing-xxs;
                padding: vars.$spacing-xs vars.$spacing-md;
                cursor: pointer;
                color: vars.$text-secondary;
                font-weight: vars.$font-weight-medium;
                transition: all vars.$transition-fast;
                list-style: none;

                &::-webkit-details-marker {
                    display: none;
                }

                &:hover {
                    color: vars.$primary-color;
                    background-color: func.color-alpha(vars.$primary-color, 0.05);
                }
            }

            &-content {
                padding: vars.$spacing-md;
                border-top: 1px solid func.color-alpha(vars.$gray-light, 0.5);
                background-color: vars.$bg-tertiary;
            }
        }

        &__error-type {
            margin: 0 0 vars.$spacing-xs;
            font-size: vars.$font-size-sm;
            color: vars.$text-muted;
            font-family: 'Fira Code', monospace;
        }

        &__details pre {
            margin: 0;
            font-family: 'Fira Code', monospace;
            font-size: vars.$font-size-xs;
            line-height: vars.$line-height-relaxed;
            overflow-x: auto;
            max-height: 200px;
            color: vars.$danger-color;
            white-space: pre-wrap;
            word-break: break-word;
        }
    }
</style>
