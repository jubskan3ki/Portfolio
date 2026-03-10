<template>
    <div :class="emptyStateClasses" role="status">
        <!-- Icon -->
        <div class="empty-state__icon-wrapper">
            <div class="empty-state__icon-bg"></div>
            <BaseIcon :name="icon" :size="iconSize" class="empty-state__icon" />
        </div>

        <!-- Content -->
        <div class="empty-state__content">
            <component :is="titleTag" class="empty-state__title">{{ title }}</component>
            <p v-if="description" class="empty-state__description">
                {{ description }}
            </p>
        </div>

        <!-- Action -->
        <div v-if="actionText || $slots.action" class="empty-state__action">
            <slot name="action">
                <BaseButton v-if="actionText" :variant="actionVariant" :text="actionText" @click="emit('action')">
                    <template v-if="actionIcon" #icon-left>
                        <BaseIcon :name="actionIcon" :size="18" />
                    </template>
                </BaseButton>
            </slot>
        </div>

        <!-- Extra slot -->
        <small v-if="$slots.extra" class="empty-state__extra">
            <slot name="extra"></slot>
        </small>
    </div>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import BaseButton from '@/components/base/BaseButton.vue';
    import BaseIcon from '@/components/base/BaseIcon.vue';

    import type { EmptyStateProps, EmptyStateSize } from '@/types/components/feedback';

    type Props = EmptyStateProps;

    const props = withDefaults(defineProps<Props>(), {
        icon: 'inbox',
        description: '',
        actionText: '',
        actionIcon: '',
        actionVariant: 'primary',
        size: 'md',
        centered: true,
        customClass: '',
    });

    const emit = defineEmits<{
        action: [];
    }>();

    const ICON_SIZE_MAP: Record<EmptyStateSize, number> = {
        sm: 32,
        md: 48,
        lg: 64,
    };

    const TITLE_TAG_MAP: Record<EmptyStateSize, string> = {
        sm: 'h6',
        md: 'h5',
        lg: 'h4',
    };

    const iconSize = computed(() => ICON_SIZE_MAP[props.size]);
    const titleTag = computed(() => TITLE_TAG_MAP[props.size]);

    const emptyStateClasses = computed(() => [
        'empty-state',
        `empty-state--${props.size}`,
        {
            'empty-state--centered': props.centered,
        },
        props.customClass,
    ]);
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as func;

    .empty-state {
        display: flex;
        flex-direction: column;
        gap: vars.$spacing-md;
        padding: vars.$spacing-xl;

        &--centered {
            align-items: center;
            text-align: center;
        }

        /* Icon wrapper */
        &__icon-wrapper {
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        &__icon-bg {
            position: absolute;
            border-radius: vars.$border-radius-full;
            background: func.color-alpha(vars.$primary-color, 0.08);
        }

        &__icon {
            position: relative;
            color: vars.$text-secondary;
            z-index: 1;
        }

        /* Sizes */
        &--sm {
            padding: vars.$spacing-lg;
            gap: vars.$spacing-xs;

            .empty-state__icon-bg {
                width: 56px;
                height: 56px;
            }
        }

        &--md {
            .empty-state__icon-bg {
                width: 80px;
                height: 80px;
            }
        }

        &--lg {
            padding: vars.$spacing-xxl;
            gap: vars.$spacing-lg;

            .empty-state__icon-bg {
                width: 112px;
                height: 112px;
            }
        }

        /* Content */
        &__content {
            display: flex;
            flex-direction: column;
            gap: vars.$spacing-xxs;
        }

        &__title {
            margin: 0;
            font-weight: vars.$font-weight-semibold;
            color: vars.$text-primary;
            line-height: vars.$line-height-tight;
        }

        &__description {
            margin: 0;
            color: vars.$text-secondary;
            line-height: vars.$line-height-relaxed;
            max-width: 400px;
        }

        /* Action */
        &__action {
            margin-top: vars.$spacing-xs;
        }

        /* Extra */
        &__extra {
            display: block;
            margin-top: vars.$spacing-md;
            color: vars.$text-secondary;
        }
    }
</style>
