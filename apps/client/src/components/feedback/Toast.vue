<template>
    <Transition name="toast">
        <div
            v-if="isVisible"
            :class="toastClasses"
            role="alert"
            @mouseenter="pauseTimer"
            @mouseleave="resumeTimer"
        >
            <!-- Icon -->
            <div v-if="showIcon" class="toast__icon">
                <BaseIcon :name="iconName" :size="20" />
            </div>

            <!-- Content -->
            <div class="toast__content">
                <h6 v-if="title" class="toast__title">{{ title }}</h6>
                <p class="toast__message">
                    <slot>{{ message }}</slot>
                </p>
            </div>

            <!-- Action slot -->
            <div v-if="$slots.action" class="toast__action">
                <slot name="action"></slot>
            </div>

            <!-- Close button -->
            <button
                v-if="dismissible"
                type="button"
                class="toast__close"
                aria-label="Fermer"
                @click="dismiss"
            >
                <BaseIcon name="x" :size="16" />
            </button>

            <!-- Progress bar -->
            <div v-if="autoClose && progress" class="toast__progress">
                <div class="toast__progress-bar" :style="{ width: `${progressValue}%` }"></div>
            </div>
        </div>
    </Transition>
</template>

<script setup lang="ts">
    import { computed, ref, watch } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import { useProgressTimer } from '@/composables/ui/useProgressTimer';

    import type { FeedbackType, ToastProps } from '@/types/components/feedback';

    type Props = ToastProps;

    const props = withDefaults(defineProps<Props>(), {
        type: 'info',
        title: '',
        message: '',
        autoClose: true,
        duration: 5000,
        dismissible: true,
        showIcon: true,
        progress: true,
        customClass: '',
    });

    const emit = defineEmits<{
        close: [];
    }>();

    const isVisible = ref(true);

    const ICON_MAP: Record<FeedbackType, string> = {
        info: 'info',
        success: 'check-circle',
        warning: 'alert-triangle',
        error: 'x-circle',
    };

    const iconName = computed(() => ICON_MAP[props.type || 'info']);

    const toastClasses = computed(() => [
        'toast',
        `toast--${props.type}`,
        {
            'toast--with-action': true,
        },
        props.customClass,
    ]);

    const dismiss = () => {
        isVisible.value = false;
        timer.stop();
        emit('close');
    };

    // Use composable for timer management
    const timer = useProgressTimer({
        duration: props.duration,
        autoStart: props.autoClose,
        onComplete: dismiss,
    });

    const progressValue = computed(() => timer.progress.value);

    const pauseTimer = () => {
        if (!props.autoClose) {
            return;
        }
        timer.pause();
    };

    const resumeTimer = () => {
        if (!props.autoClose) {
            return;
        }
        timer.resume();
    };

    watch(
        () => props.duration,
        () => {
            timer.reset();
            if (props.autoClose) {
                timer.start();
            }
        },
    );

    defineExpose({
        dismiss,
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as func;

    .toast {
        position: relative;
        display: flex;
        align-items: flex-start;
        gap: vars.$spacing-xs;
        width: 100%;
        max-width: 400px;
        padding: vars.$spacing-md;
        border-radius: vars.$border-radius-lg;
        background-color: vars.$white;
        box-shadow: vars.$box-shadow-medium;
        overflow: hidden;

        // Icon
        &__icon {
            flex-shrink: 0;
            width: 36px;
            height: 36px;
            border-radius: vars.$border-radius-md;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        // Content
        &__content {
            flex: 1;
            min-width: 0;
            padding-top: 2px;
        }

        &__title {
            margin: 0 0 vars.$spacing-xxs;
            font-weight: vars.$font-weight-semibold;
            line-height: vars.$line-height-tight;
        }

        &__message {
            margin: 0;
            color: vars.$text-secondary;
            line-height: vars.$line-height-relaxed;
        }

        // Action
        &__action {
            flex-shrink: 0;
            align-self: center;
        }

        // Close
        &__close {
            flex-shrink: 0;
            width: 28px;
            height: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: none;
            border: none;
            border-radius: vars.$border-radius-md;
            color: vars.$gray;
            cursor: pointer;
            transition: all vars.$transition-fast;

            &:hover {
                background-color: func.color-alpha(vars.$black, 0.05);
                color: vars.$text-primary;
            }
        }

        // Progress
        &__progress {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 3px;
            background-color: func.color-alpha(vars.$black, 0.05);
        }

        &__progress-bar {
            height: 100%;
            transition: width 10ms linear;
        }

        // Variants
        &--info {
            .toast__icon {
                background-color: func.color-alpha(vars.$info-color, 0.1);
                color: vars.$info-color;
            }

            .toast__title {
                color: vars.$info-dark;
            }

            .toast__progress-bar {
                background-color: vars.$info-color;
            }
        }

        &--success {
            .toast__icon {
                background-color: func.color-alpha(vars.$success-color, 0.1);
                color: vars.$success-color;
            }

            .toast__title {
                color: vars.$success-dark;
            }

            .toast__progress-bar {
                background-color: vars.$success-color;
            }
        }

        &--warning {
            .toast__icon {
                background-color: func.color-alpha(vars.$warning-color, 0.15);
                color: vars.$warning-dark;
            }

            .toast__title {
                color: vars.$warning-dark;
            }

            .toast__progress-bar {
                background-color: vars.$warning-color;
            }
        }

        &--error {
            .toast__icon {
                background-color: func.color-alpha(vars.$danger-color, 0.1);
                color: vars.$danger-color;
            }

            .toast__title {
                color: vars.$danger-dark;
            }

            .toast__progress-bar {
                background-color: vars.$danger-color;
            }
        }
    }

    // Transitions
    .toast-enter-active {
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
    }

    .toast-leave-active {
        transition: all 0.3s ease-out;
    }

    .toast-enter-from {
        opacity: 0;
        transform: translateY(-20px) scale(0.95);
    }

    .toast-leave-to {
        opacity: 0;
        transform: translateX(100px);
    }
</style>
