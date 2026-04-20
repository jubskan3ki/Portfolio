<template>
    <Teleport to="body">
        <Transition name="confirm">
            <div
                v-if="modelValue"
                class="confirm-dialog"
                role="alertdialog"
                aria-modal="true"
                :aria-labelledby="titleId"
                :aria-describedby="messageId"
            >
                <div class="confirm-dialog__overlay" aria-hidden="true" @click="handleCancel"></div>

                <div ref="containerRef" :class="dialogClasses">
                    <div class="confirm-dialog__icon-wrapper">
                        <div :class="iconBgClasses"></div>
                        <BaseIcon :name="iconName" :size="28" :class="iconClasses" />
                    </div>

                    <div class="confirm-dialog__content">
                        <h5 :id="titleId" class="confirm-dialog__title">{{ title }}</h5>
                        <p :id="messageId" class="confirm-dialog__message">{{ message }}</p>
                    </div>

                    <div class="confirm-dialog__actions">
                        <BaseButton variant="ghost" :text="cancelText" :disabled="loading" @click="handleCancel" />
                        <BaseButton
                            :variant="confirmButtonVariant"
                            :text="confirmText"
                            :loading="loading"
                            @click="handleConfirm"
                        />
                    </div>
                </div>
            </div>
        </Transition>
    </Teleport>
</template>

<script setup lang="ts">
    import { computed, useId, ref, watch, nextTick } from 'vue';

    import BaseButton from '@/components/base/BaseButton.vue';
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import { useEscapeKey } from '@/composables/accessibility/useEscapeKey';
    import { useFocusTrap } from '@/composables/accessibility/useFocusTrap';

    import type { ConfirmDialogProps, ConfirmDialogVariant, ButtonVariant } from '@/types/components/feedback';

    type Props = ConfirmDialogProps;

    const props = withDefaults(defineProps<Props>(), {
        title: 'Confirmer',
        variant: 'warning',
        icon: '',
        confirmText: 'Confirmer',
        cancelText: 'Annuler',
        loading: false,
        customClass: '',
    });

    const emit = defineEmits<{
        'update:modelValue': [value: boolean];
        confirm: [];
        cancel: [];
    }>();

    const titleId = useId();
    const messageId = useId();

    const ICON_MAP: Record<ConfirmDialogVariant, string> = {
        info: 'info',
        warning: 'alert-triangle',
        danger: 'trash-2',
    };

    const BUTTON_VARIANT_MAP: Record<ConfirmDialogVariant, ButtonVariant> = {
        info: 'primary',
        warning: 'primary',
        danger: 'danger',
    };

    const iconName = computed(() => props.icon || ICON_MAP[props.variant]);
    const confirmButtonVariant = computed(() => BUTTON_VARIANT_MAP[props.variant]);

    const dialogClasses = computed(() => [
        'confirm-dialog__container',
        `confirm-dialog__container--${props.variant}`,
        props.customClass,
    ]);

    const iconBgClasses = computed(() => ['confirm-dialog__icon-bg', `confirm-dialog__icon-bg--${props.variant}`]);

    const iconClasses = computed(() => ['confirm-dialog__icon', `confirm-dialog__icon--${props.variant}`]);

    const handleConfirm = () => {
        if (props.loading) {
            return;
        }
        emit('confirm');
    };

    const handleCancel = () => {
        if (props.loading) {
            return;
        }
        emit('update:modelValue', false);
        emit('cancel');
    };

    const containerRef = ref<HTMLElement | null>(null);
    const { activate: activateFocusTrap, deactivate: deactivateFocusTrap } = useFocusTrap(containerRef);

    useEscapeKey(() => {
        if (props.modelValue && !props.loading) {
            handleCancel();
        }
    });

    watch(
        () => props.modelValue,
        async (isOpen) => {
            if (isOpen) {
                await nextTick();
                activateFocusTrap();
            } else {
                deactivateFocusTrap();
            }
        },
    );
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as func;
    @use '@/styles/abstracts/mixins' as mix;

    .confirm-dialog {
        position: fixed;
        inset: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: vars.$z-index-modal + 10;
        padding: vars.$spacing-md;

        &__overlay {
            position: absolute;
            inset: 0;
            background-color: func.color-alpha(vars.$black, 0.6);
            backdrop-filter: blur(4px);
        }

        &__container {
            position: relative;
            background-color: vars.$white;
            border-radius: vars.$border-radius-xl;
            box-shadow: vars.$box-shadow-large;
            padding: vars.$spacing-xl;
            max-width: 400px;
            width: 100%;
            text-align: center;
        }

        &__icon-wrapper {
            position: relative;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-bottom: vars.$spacing-lg;
        }

        &__icon-bg {
            position: absolute;
            width: 64px;
            height: 64px;
            border-radius: vars.$border-radius-full;

            &--info {
                background-color: func.color-alpha(vars.$info-color, 0.1);
            }

            &--warning {
                background-color: func.color-alpha(vars.$warning-color, 0.1);
            }

            &--danger {
                background-color: func.color-alpha(vars.$danger-color, 0.1);
            }
        }

        &__icon {
            position: relative;
            z-index: 1;

            &--info {
                color: vars.$info-color;
            }

            &--warning {
                color: vars.$warning-color;
            }

            &--danger {
                color: vars.$danger-color;
            }
        }

        &__content {
            margin-bottom: vars.$spacing-lg;
        }

        &__title {
            margin: 0 0 vars.$spacing-xs;
            font-weight: vars.$font-weight-semibold;
            color: vars.$text-primary;
        }

        &__message {
            margin: 0;
            color: vars.$text-secondary;
            line-height: vars.$line-height-relaxed;
        }

        &__actions {
            display: flex;
            gap: vars.$spacing-xs;
            justify-content: center;
        }
    }

    .confirm-enter-active {
        transition: opacity 0.2s ease-out;

        .confirm-dialog__container {
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        }
    }

    .confirm-leave-active {
        transition: opacity 0.15s ease-in;

        .confirm-dialog__container {
            transition: all 0.15s ease-in;
        }
    }

    .confirm-enter-from,
    .confirm-leave-to {
        opacity: 0;

        .confirm-dialog__container {
            transform: scale(0.9);
            opacity: 0;
        }
    }
</style>
