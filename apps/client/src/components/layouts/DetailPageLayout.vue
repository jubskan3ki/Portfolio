<template>
    <div class="detail-layout" :style="layoutStyle">
        <div class="detail-layout__main">
            <slot name="main"></slot>
        </div>
        <aside class="detail-layout__sidebar">
            <slot name="sidebar"></slot>
        </aside>
    </div>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import type { DetailPageLayoutProps } from '@/types/components/layouts';

    const props = withDefaults(defineProps<DetailPageLayoutProps>(), {
        sidebarWidth: '340px',
    });

    const layoutStyle = computed(() => ({
        '--sidebar-width': props.sidebarWidth,
    }));
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;

    .detail-layout {
        display: grid;
        grid-template-columns: 1fr var(--sidebar-width, 340px);
        gap: vars.$spacing-xl;

        @include mix.responsive(tablet) {
            grid-template-columns: 1fr;
        }

        &__main {
            display: flex;
            flex-direction: column;
            gap: vars.$spacing-lg;
            contain: layout;
        }

        &__sidebar {
            display: flex;
            flex-direction: column;
            gap: vars.$spacing-lg;
            height: fit-content;
            position: sticky;
            top: calc(vars.$header-height + vars.$spacing-lg);
            align-self: start;
            min-height: 320px;
            contain: layout;

            @include mix.responsive(tablet) {
                position: static;
                order: -1;
                min-height: 0;
            }
        }
    }
</style>
