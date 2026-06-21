<template>
    <div>
        <TransitionGroup name="fade">
            <div
                v-for="loader in fullscreenLoaders"
                :key="loader.id"
                class="loader loader--fullscreen"
                :class="{ 'loader--overlay': loader.hasOverlay }"
                role="status"
                aria-live="polite"
            >
                <div class="loader__content">
                    <Spinner :type="loader.type" :size="loader.size" :label="loader.label" show-label />
                    <button v-if="loader.cancelable" type="button" class="loader__cancel" @click="cancel(loader.id)">
                        Annuler
                    </button>
                </div>
            </div>
        </TransitionGroup>

        <Teleport v-if="containerLoaders.length" to="body">
            <div
                v-for="loader in containerLoaders"
                :key="loader.id"
                class="loader loader--container"
                :class="{ 'loader--overlay': loader.hasOverlay }"
                :style="getStyle(loader)"
                role="status"
                aria-live="polite"
            >
                <div class="loader__content">
                    <Spinner :type="loader.type" :size="loader.size" :label="loader.label" show-label />
                    <button v-if="loader.cancelable" type="button" class="loader__cancel" @click="cancel(loader.id)">
                        Annuler
                    </button>
                </div>
            </div>
        </Teleport>
    </div>
</template>

<script setup lang="ts">
    import { storeToRefs } from 'pinia';

    import { useLoaderStore } from '@/stores/loader';

    import Spinner from './Spinner.vue';

    import type { LoaderItem } from '@/types/stores/loader';

    const store = useLoaderStore();
    const { fullscreenLoaders, containerLoaders } = storeToRefs(store);

    const cancel = (id: string) => store.stop(id);

    const getStyle = (loader: LoaderItem): Record<string, string> => {
        if (!import.meta.client || !loader.targetSelector) {
            return {};
        }

        const el = document.querySelector(loader.targetSelector);
        if (!el) {
            return {};
        }

        const rect = el.getBoundingClientRect();

        return {
            position: 'absolute',
            top: `${rect.top + window.scrollY}px`,
            left: `${rect.left + window.scrollX}px`,
            width: `${rect.width}px`,
            height: `${rect.height}px`,
        };
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as v;
    @use '@/styles/abstracts/functions' as fn;

    .loader {
        position: fixed;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: v.$z-index-toast;

        &--fullscreen {
            inset: 0;
        }

        &--container {
            border-radius: v.$border-radius-md;
            overflow: hidden;
        }

        &--overlay::before {
            content: '';
            position: absolute;
            inset: 0;
            background: fn.color-alpha(v.$white, 0.9);
            backdrop-filter: blur(4px);
        }

        &__content {
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: v.$spacing-md;
            padding: v.$spacing-xl;
            background: v.$white;
            border-radius: v.$border-radius-lg;
            box-shadow: v.$box-shadow-medium;
        }

        &__cancel {
            padding: v.$spacing-xs v.$spacing-md;
            border-radius: v.$border-radius-md;
            background: v.$bg-secondary;
            color: v.$text-primary;
            border: 1px solid v.$border-color;
            font-size: v.$font-size-sm;
            font-weight: v.$font-weight-medium;
            cursor: pointer;
            transition: all v.$transition-fast;

            &:hover {
                background: v.$white;
                border-color: v.$primary-color;
                color: v.$primary-color;
            }

            &:focus-visible {
                outline: 2px solid v.$primary-color;
                outline-offset: 2px;
            }
        }
    }

    .fade-enter-active,
    .fade-leave-active {
        transition: opacity 0.25s ease;
    }

    .fade-enter-from,
    .fade-leave-to {
        opacity: 0;
    }
</style>
