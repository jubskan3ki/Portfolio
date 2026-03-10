<template>
    <Teleport to="body">
        <Transition name="modal">
            <div
                v-if="visible"
                ref="modalRef"
                class="modal"
                role="dialog"
                aria-modal="true"
                :aria-labelledby="options.title ? titleId : undefined"
                :aria-describedby="options.subtitle ? descriptionId : undefined"
            >
                <!-- Overlay -->
                <div class="modal__overlay" aria-hidden="true" @click="handleOverlayClick"></div>

                <!-- Container -->
                <div :class="containerClasses">
                    <!-- Header -->
                    <div v-if="options.title || !options.hideCloseButton" class="modal__header">
                        <div class="modal__header-content">
                            <h4 v-if="options.title" :id="titleId" class="modal__title">
                                {{ options.title }}
                            </h4>
                            <small v-if="options.subtitle" :id="descriptionId" class="modal__subtitle">
                                {{ options.subtitle }}
                            </small>
                        </div>

                        <button
                            v-if="!options.hideCloseButton"
                            type="button"
                            class="modal__close"
                            aria-label="Fermer"
                            @click="closeModal"
                        >
                            <BaseIcon name="x" :size="18" />
                        </button>
                    </div>

                    <!-- Body -->
                    <div class="modal__body">
                        <p v-if="options.content">{{ options.content }}</p>
                        <component
                            :is="options.component"
                            v-else-if="options.component"
                            v-bind="options.componentProps"
                            @close="closeModal"
                        />
                        <slot v-else></slot>
                    </div>

                    <!-- Footer -->
                    <div v-if="$slots.footer || options.showFooter" class="modal__footer">
                        <slot name="footer"></slot>
                    </div>
                </div>
            </div>
        </Transition>
    </Teleport>
</template>

<script setup lang="ts">
    import { computed, ref, watch, nextTick, onUnmounted, useId } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import { useEscapeKey } from '@/composables/accessibility/useEscapeKey';
    import { useFocusTrap } from '@/composables/accessibility/useFocusTrap';
    import { lockBodyOverflow, unlockBodyOverflow } from '@/services/utils/dom';
    import { useModalStore } from '@/stores/modal';

    import type { ModalProps, ModalOptions } from '@/types/components/feedback';

    type Props = ModalProps;

    const props = withDefaults(defineProps<Props>(), {
        modelValue: undefined,
        title: '',
        subtitle: '',
        size: 'md',
        closable: true,
        closeOnClickOutside: true,
        persistent: false,
        hideCloseButton: false,
        showFooter: false,
        customClass: '',
    });

    const emit = defineEmits<{
        'update:modelValue': [value: boolean];
        close: [];
    }>();

    const modalStore = useModalStore();
    const modalRef = ref<HTMLElement | null>(null);
    const titleId = useId();
    const descriptionId = useId();

    // Determine if using store or v-model
    const isUsingStore = computed(() => props.modelValue === undefined);

    const visible = computed(() => {
        if (isUsingStore.value) {
            return modalStore.visible;
        }
        return props.modelValue;
    });

    const options = computed<ModalOptions>(() => {
        if (isUsingStore.value) {
            return modalStore.options;
        }
        return {
            title: props.title,
            subtitle: props.subtitle,
            size: props.size,
            closable: props.closable,
            closeOnClickOutside: props.closeOnClickOutside,
            persistent: props.persistent,
            hideCloseButton: props.hideCloseButton,
            showFooter: props.showFooter,
        };
    });

    const containerClasses = computed(() => [
        'modal__container',
        `modal__container--${options.value.size || props.size}`,
        props.customClass,
    ]);

    const closeModal = () => {
        if (options.value.closable === false) {
            return;
        }

        if (isUsingStore.value) {
            modalStore.close();
        } else {
            emit('update:modelValue', false);
        }
        emit('close');
    };

    const handleOverlayClick = () => {
        if (options.value.closeOnClickOutside && !options.value.persistent) {
            closeModal();
        }
    };

    // Focus trap — reuse existing composable (consistent with ConfirmDialog.vue)
    const { activate: activateFocusTrap, deactivate: deactivateFocusTrap } = useFocusTrap(modalRef);

    // Escape key — reuse existing composable (consistent with ConfirmDialog.vue)
    useEscapeKey(
        () => {
            if (!options.value.persistent) {
                closeModal();
            }
        },
        { enabled: computed(() => !!visible.value) },
    );

    // Manage focus trap and body overflow on visibility change
    watch(visible, (isVisible) => {
        if (isVisible) {
            // Store mode: overflow already locked by modalStore.open()
            if (!isUsingStore.value) {
                lockBodyOverflow();
            }
            nextTick(() => activateFocusTrap());
        } else {
            deactivateFocusTrap();
            if (!isUsingStore.value) {
                unlockBodyOverflow();
            }
        }
    });

    onUnmounted(() => {
        // Release overflow lock for v-model mode if still visible
        if (!isUsingStore.value && visible.value) {
            unlockBodyOverflow();
        }
        // Clean up store timeouts and state
        if (isUsingStore.value) {
            modalStore.cleanup();
        }
    });

    defineExpose({
        close: closeModal,
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .modal {
        position: fixed;
        inset: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: vars.$z-index-modal;
        padding: vars.$spacing-md;

        &__overlay {
            position: absolute;
            inset: 0;
            background-color: func.color-alpha(vars.$black, 0.5);
            backdrop-filter: blur(4px);
        }

        &__container {
            position: relative;
            background-color: vars.$white;
            border-radius: vars.$border-radius-xl;
            box-shadow: vars.$box-shadow-large;
            max-height: 90vh;
            max-width: 90vw;
            width: 100%;
            display: flex;
            flex-direction: column;
            overflow: hidden;

            // Sizes
            &--sm {
                max-width: 400px;
            }

            &--md {
                max-width: 560px;
            }

            &--lg {
                max-width: 720px;
            }

            &--xl {
                max-width: 960px;
            }

            &--full {
                max-width: 100%;
                max-height: 100%;
                height: 100%;
                border-radius: 0;
            }
        }

        &__header {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: vars.$spacing-md;
            padding: vars.$spacing-lg vars.$spacing-lg vars.$spacing-md;
            border-bottom: 1px solid func.color-alpha(vars.$gray-light, 0.5);
        }

        &__header-content {
            flex: 1;
            min-width: 0;
        }

        &__title {
            margin: 0;
            font-weight: vars.$font-weight-semibold;
            color: vars.$text-primary;
            line-height: vars.$line-height-tight;
        }

        &__subtitle {
            display: block;
            margin: vars.$spacing-xxs 0 0;
            color: vars.$text-secondary;
        }

        &__close {
            flex-shrink: 0;
            width: 36px;
            height: 36px;
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

            @include mix.focus-outline;
        }

        &__body {
            flex: 1;
            padding: vars.$spacing-lg;
            overflow-y: auto;
        }

        &__footer {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: vars.$spacing-xs;
            padding: vars.$spacing-md vars.$spacing-lg vars.$spacing-lg;
            border-top: 1px solid func.color-alpha(vars.$gray-light, 0.5);
        }
    }

    // Animations
    .modal-enter-active {
        transition: opacity 0.3s cubic-bezier(0.23, 1, 0.32, 1);

        .modal__container {
            transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
        }
    }

    .modal-leave-active {
        transition: opacity 0.2s ease-out;

        .modal__container {
            transition: all 0.2s ease-out;
        }
    }

    .modal-enter-from,
    .modal-leave-to {
        opacity: 0;

        .modal__container {
            transform: scale(0.95) translateY(10px);
            opacity: 0;
        }
    }
</style>
