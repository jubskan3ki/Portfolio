<template>
    <div :class="alertClasses" role="alert" @mouseenter="handleMouseEnter" @mouseleave="handleMouseLeave">
        <div class="alert-item__icon">
            <BaseIcon :name="iconName" :size="20" />
        </div>

        <div class="alert-item__content">
            <h6 v-if="alert.title" class="alert-item__title">{{ alert.title }}</h6>
            <p class="alert-item__message">{{ alert.message }}</p>
        </div>

        <button
            v-if="alert.dismissible !== false"
            type="button"
            class="alert-item__close"
            aria-label="Fermer"
            @click="close"
        >
            <BaseIcon name="x" :size="16" />
        </button>
    </div>
</template>

<script setup lang="ts">
    import { computed, onBeforeUnmount, ref } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import { useProgressTimer } from '@/composables/ui/useProgressTimer';

    import type { AlertItemProps, FeedbackType } from '@/types/components/feedback';

    type Props = AlertItemProps;

    const props = defineProps<Props>();

    const emit = defineEmits<{
        close: [id: string];
    }>();

    const isClosing = ref(false);

    const ICON_MAP: Record<FeedbackType, string> = {
        success: 'check-circle',
        error: 'x-circle',
        warning: 'alert-triangle',
        info: 'info',
    };

    const iconName = computed(() => ICON_MAP[props.alert.type] || 'info');

    const alertClasses = computed(() => [
        'alert-item',
        `alert-item--${props.alert.type}`,
        { 'alert-item--closing': isClosing.value },
    ]);

    const handleMouseEnter = () => {
        if (props.alert.autoClose !== false) {
            timer.pause();
        }
    };

    const handleMouseLeave = () => {
        if (props.alert.autoClose !== false) {
            timer.resume();
        }
    };

    let closeTimer: ReturnType<typeof setTimeout> | null = null;

    const close = () => {
        timer.stop();
        isClosing.value = true;
        closeTimer = setTimeout(() => emit('close', props.alert.id), 300);
    };

    const timer = useProgressTimer({
        duration: props.alert.timeout || 5000,
        autoStart: props.alert.autoClose !== false,
        onComplete: close,
    });

    onBeforeUnmount(() => {
        if (closeTimer) {
            clearTimeout(closeTimer);
        }
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as func;

    .alert-item {
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
        animation: alert-enter 0.4s cubic-bezier(0.23, 1, 0.32, 1);

        &--closing {
            animation: alert-leave 0.3s ease-out forwards;
        }

        &__icon {
            flex-shrink: 0;
            width: 36px;
            height: 36px;
            border-radius: vars.$border-radius-md;
            display: flex;
            align-items: center;
            justify-content: center;
        }

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

        &--success {
            .alert-item__icon {
                background-color: func.color-alpha(vars.$success-color, 0.1);
                color: vars.$success-color;
            }

            .alert-item__title {
                color: vars.$success-dark;
            }
        }

        &--error {
            .alert-item__icon {
                background-color: func.color-alpha(vars.$danger-color, 0.1);
                color: vars.$danger-color;
            }

            .alert-item__title {
                color: vars.$danger-dark;
            }
        }

        &--warning {
            .alert-item__icon {
                background-color: func.color-alpha(vars.$warning-color, 0.15);
                color: vars.$warning-dark;
            }

            .alert-item__title {
                color: vars.$warning-dark;
            }
        }

        &--info {
            .alert-item__icon {
                background-color: func.color-alpha(vars.$info-color, 0.1);
                color: vars.$info-color;
            }

            .alert-item__title {
                color: vars.$info-dark;
            }
        }
    }

    @keyframes alert-enter {
        from {
            opacity: 0;
            transform: translateX(100px);
        }

        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes alert-leave {
        to {
            opacity: 0;
            transform: translateX(100px);
        }
    }
</style>
