<template>
    <button
        v-if="isTab"
        :id="`tab-${tabsId}-${id}`"
        :class="tabClasses"
        :disabled="disabled"
        :aria-controls="`panel-${tabsId}-${id}`"
        :aria-selected="isActive"
        role="tab"
        :tabindex="isActive ? 0 : -1"
        @click="emit('select')"
    >
        <span v-if="icon" class="tabs-item__icon" aria-hidden="true">
            <BaseIcon :name="icon" :size="16" />
        </span>
        <span class="tabs-item__label">{{ label }}</span>
        <span v-if="badge" class="tabs-item__badge">
            <Badge :text="String(badge.text)" :variant="(badge.type as BadgeVariant) || 'primary'" size="sm" rounded />
        </span>
    </button>

    <div
        v-else
        :id="`panel-${tabsId}-${id}`"
        :class="panelClasses"
        :aria-labelledby="`tab-${tabsId}-${id}`"
        :hidden="!isActive"
        role="tabpanel"
        tabindex="0"
    >
        <slot></slot>
    </div>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import Badge from '@/components/ui/Badge.vue';

    import type { BadgeVariant } from '@/types/components/base';

    interface TabBadge {
        text: string | number;
        type?: string;
        variant?: string;
    }

    interface Props {
        id: string;
        tabsId: string;
        isActive?: boolean;
        isTab?: boolean;
        label?: string;
        icon?: string;
        disabled?: boolean;
        badge?: TabBadge | null;
    }

    const props = withDefaults(defineProps<Props>(), {
        isActive: false,
        isTab: false,
        label: '',
        icon: '',
        disabled: false,
        badge: null,
    });

    const emit = defineEmits<{
        select: [];
    }>();

    const tabClasses = computed(() => [
        'tabs-item__tab',
        {
            'tabs-item__tab--active': props.isActive,
            'tabs-item__tab--disabled': props.disabled,
            'tabs-item__tab--with-icon': props.icon,
            'tabs-item__tab--with-badge': props.badge,
        },
    ]);

    const panelClasses = computed(() => ['tabs-item__panel', { 'tabs-item__panel--active': props.isActive }]);
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .tabs-item__tab {
        position: relative;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: vars.$spacing-xxs;
        padding: vars.$spacing-xs vars.$spacing-md;
        border: none;
        background: transparent;
        font-weight: 500;
        color: vars.$text-secondary;
        white-space: nowrap;
        cursor: pointer;
        border-radius: vars.$border-radius-md;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);

        &::before {
            content: '';
            position: absolute;
            inset: 0;
            background: transparent;
            border-radius: inherit;
            transition: background 0.3s ease;
            z-index: -1;
        }

        &:hover:not(:disabled, &--active) {
            color: vars.$text-primary;

            &::before {
                background: func.color-alpha(vars.$gray-light, 0.5);
            }

            .tabs-item__icon {
                transform: scale(1.1);
            }
        }

        &:focus-visible {
            outline: 2px solid vars.$primary-color;
            outline-offset: 2px;
        }

        &--active {
            color: vars.$primary-color;

            .tabs-item__icon {
                color: vars.$primary-color;
            }
        }

        &--disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
    }

    .tabs-item__icon {
        display: flex;
        align-items: center;
        justify-content: center;
        transition: transform 0.3s ease;
    }

    .tabs-item__label {
        line-height: 1;
    }

    .tabs-item__badge {
        margin-left: vars.$spacing-xxxs;
    }

    .tabs-item__panel {
        outline: none;

        &:focus-visible {
            outline: 2px solid vars.$primary-color;
            outline-offset: 4px;
            border-radius: vars.$border-radius-md;
        }
    }
</style>
