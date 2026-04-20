<template>
    <div :class="classes" role="status" aria-live="polite">
        <Spinner :size="spinnerSize" :label="message" show-label />
    </div>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import Spinner from './Spinner.vue';

    import type { LoadingStateProps } from '@/types/components/loaders';

    const props = withDefaults(defineProps<LoadingStateProps>(), {
        message: 'Chargement...',
        size: 'md',
        spinnerSize: 'lg',
    });

    const classes = computed(() => ['loading-state', `loading-state--${props.size}`]);
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as v;

    .loading-state {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        padding: v.$spacing-xl 0;

        &--sm {
            min-height: 150px;
        }

        &--md {
            min-height: 300px;
        }

        &--lg {
            min-height: 400px;
        }
    }
</style>
