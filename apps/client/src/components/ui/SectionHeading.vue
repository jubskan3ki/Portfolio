<template>
    <header class="section-heading" :class="[`section-heading--${size}`, customClass]">
        <component :is="computedTitleTag" class="section-heading__title">
            <slot name="icon">
                <BaseIcon
                    v-if="icon"
                    :name="icon"
                    :size="iconSize"
                    class="section-heading__icon"
                    aria-hidden="true"
                />
            </slot>
            {{ title }}
        </component>
        <div v-if="!noSeparator" class="section-heading__separator"></div>
        <div v-if="$slots.actions" class="section-heading__actions">
            <slot name="actions"></slot>
        </div>
    </header>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';

    import type { HeadingSize, SectionHeadingProps, TitleTag } from '@/types/components/ui';

    type Props = SectionHeadingProps;

    const props = withDefaults(defineProps<Props>(), {
        titleTag: 'h3',
        size: 'md',
        icon: '',
        noSeparator: false,
        customClass: '',
    });

    const ICON_SIZES: Record<HeadingSize, number> = {
        sm: 16,
        md: 20,
        lg: 24,
    };

    const TAG_MAP: Record<HeadingSize, TitleTag> = {
        sm: 'h5',
        md: 'h4',
        lg: 'h3',
    };

    const iconSize = computed(() => ICON_SIZES[props.size]);
    const computedTitleTag = computed(() => props.titleTag || TAG_MAP[props.size]);
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as func;

    .section-heading {
        display: flex;
        align-items: center;
        gap: vars.$spacing-md;
        margin-bottom: vars.$spacing-md;

        &--sm {
            margin-bottom: vars.$spacing-xs;
        }

        &--md {
            margin-bottom: vars.$spacing-md;
        }

        &--lg {
            margin-bottom: vars.$spacing-lg;
        }

        &__title {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;
            margin: 0;
            font-weight: vars.$font-weight-semibold;
            color: vars.$text-primary;
            white-space: nowrap;
        }

        &__icon {
            color: vars.$primary-color;
        }

        &__separator {
            flex: 1;
            height: 1px;
            background: func.color-alpha(vars.$gray-light, 0.4);
        }

        &__actions {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xxs;
            flex-shrink: 0;
        }
    }
</style>
