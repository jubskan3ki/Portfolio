<template>
    <div class="segmented-tabs">
        <div ref="trackRef" class="segmented-tabs__track">
            <button
                v-for="(tab, index) in tabs"
                :key="tab.key"
                :ref="(el) => setTabRef(index, el as HTMLButtonElement)"
                class="segmented-tabs__btn"
                :class="{ 'segmented-tabs__btn--active': modelValue === tab.key }"
                :aria-selected="modelValue === tab.key"
                role="tab"
                @click="$emit('update:modelValue', tab.key)"
            >
                <BaseIcon v-if="tab.icon" :name="tab.icon" :size="14" />
                <span>{{ tab.label }}</span>
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { computed, ref } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import { useTabIndicator } from '@/composables/ui/useTabIndicator';

    import type { SegmentedTabsProps } from '@/types/components/ui';

    const props = defineProps<SegmentedTabsProps>();

    defineEmits<{
        'update:modelValue': [value: string];
    }>();

    const trackRef = ref<HTMLElement | null>(null);
    const tabRefs = ref<Array<HTMLButtonElement | null>>([]);
    const activeIndex = computed(() => props.tabs.findIndex((t) => t.key === props.modelValue));

    const { setTabRef } = useTabIndicator({
        trackRef,
        tabRefs,
        activeIndex,
        tabs: () => props.tabs,
        mode: 'css-vars',
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as func;

    .segmented-tabs {
        &__track {
            --indicator-left: 0;
            --indicator-width: 0;

            position: relative;
            display: flex;
            background: vars.$bg-secondary;
            border-radius: vars.$border-radius-md;
            padding: vars.$spacing-xxxs;
            gap: vars.$spacing-xxxxs;

            &::before {
                content: '';
                position: absolute;
                top: vars.$spacing-xxxs;
                left: var(--indicator-left);
                width: var(--indicator-width);
                height: calc(100% - vars.$spacing-xxxs * 2);
                background: vars.$white;
                border-radius: vars.$border-radius-md;
                box-shadow:
                    0 1px 3px func.color-alpha(vars.$black, 0.1),
                    0 1px 2px func.color-alpha(vars.$black, 0.06);
                transition:
                    left 0.25s cubic-bezier(0.4, 0, 0.2, 1),
                    width 0.25s cubic-bezier(0.4, 0, 0.2, 1);
                z-index: 0;
            }
        }

        &__btn {
            flex: 1;
            position: relative;
            z-index: 1;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: vars.$spacing-xxxs;
            padding: vars.$spacing-xxs vars.$spacing-xs;
            background: transparent;
            border: none;
            border-radius: vars.$border-radius-md;
            color: vars.$text-muted;
            font-weight: vars.$font-weight-medium;
            cursor: pointer;
            transition: color 0.2s ease;
            white-space: nowrap;

            &:hover {
                color: vars.$text-inverted;
            }

            &--active {
                color: vars.$text-primary;
            }
        }
    }
</style>
