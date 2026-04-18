<template>
    <Transition name="offline-fade">
        <div v-if="!isOnline" class="offline-badge" role="status" aria-live="polite">
            <BaseIcon name="wifi-off" :size="14" />
            <span>Mode hors ligne</span>
        </div>
    </Transition>
</template>

<script setup lang="ts">
    import { useOnline } from '@vueuse/core';

    import BaseIcon from '@/components/base/BaseIcon.vue';

    const isOnline = useOnline();
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as fn;

    .offline-badge {
        position: fixed;
        bottom: vars.$spacing-md;
        left: 50%;
        transform: translateX(-50%);
        z-index: vars.$z-index-fixed;
        display: inline-flex;
        align-items: center;
        gap: vars.$spacing-xs;
        padding: vars.$spacing-xs vars.$spacing-md;
        font-size: vars.$font-size-sm;
        font-weight: vars.$font-weight-semibold;
        color: vars.$white;
        background: vars.$warning-color;
        border-radius: vars.$border-radius-full;
        box-shadow: 0 4px 18px fn.color-alpha(vars.$black, 0.18);
        pointer-events: none;
    }

    .offline-fade-enter-active,
    .offline-fade-leave-active {
        transition: opacity 180ms ease, transform 180ms ease;
    }

    .offline-fade-enter-from,
    .offline-fade-leave-to {
        opacity: 0;
        transform: translate(-50%, 8px);
    }

    @media (prefers-reduced-motion: reduce) {
        .offline-fade-enter-active,
        .offline-fade-leave-active {
            transition: none;
        }
    }
</style>
