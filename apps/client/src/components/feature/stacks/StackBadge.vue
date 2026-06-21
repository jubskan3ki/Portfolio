<template>
    <div
        class="stack-badge"
        :class="[`stack-badge--${size}`, { 'stack-badge--clickable': clickable }, customClass]"
        :role="clickable ? 'button' : undefined"
        :tabindex="clickable ? 0 : undefined"
        @click="handleClick"
        @keydown.enter="clickable && handleClick()"
        @keydown.space.prevent="clickable && handleClick()"
    >
        <StackLogo :stack="stack" :size="logoSize" class="stack-badge__icon" />

        <div v-if="showName" class="stack-badge__name">
            {{ stack.name }}
        </div>

        <div v-if="showLevel && stack.level" class="stack-badge__level" :style="levelStyle">
            <div class="stack-badge__level-bar" :style="levelBarStyle"></div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import StackLogo from '@/components/feature/stacks/StackLogo.vue';

    import type { StackBadgeProps } from '@/types/feature/stacks';

    const props = withDefaults(defineProps<StackBadgeProps>(), {
        size: 'medium',
        showName: true,
        showLevel: false,
        clickable: false,
        customClass: '',
    });

    const emit = defineEmits(['click']);

    const handleClick = () => {
        if (props.clickable) {
            emit('click', props.stack);
        }
    };

    // Mapping des tailles StackBadge → StackLogo.
    const LOGO_SIZE_MAP = {
        small: 'sm',
        medium: 'md',
        large: 'lg',
    } as const;

    const logoSize = computed(() => LOGO_SIZE_MAP[props.size] ?? 'md');

    const levelStyle = computed(() => ({
        backgroundColor: props.stack.color ? `${props.stack.color}33` : 'var(--gray-light)',
    }));

    const levelBarStyle = computed(() => {
        const level = props.stack.level || 0;
        const width = Math.min(Math.max(level, 0), 5) * 20;
        return {
            width: `${width}%`,
            backgroundColor: props.stack.color || 'var(--primary-color)',
        };
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .stack-badge {
        display: inline-flex;
        flex-direction: column;
        align-items: center;
        transition:
            transform vars.$transition-base,
            box-shadow vars.$transition-base;
        user-select: none;
        gap: vars.$spacing-xxs;

        &--clickable {
            cursor: pointer;

            &:hover {
                transform: translateY(-2px);
                box-shadow: vars.$box-shadow-medium;
            }
        }

        /* Dimensions icon = StackLogo size. Le reste (name, level) s'adapte. */
        &--small {
            .stack-badge__name {
                background: func.color-alpha(vars.$white, 0.95);
                color: vars.$primary-color;
                border: 1px solid func.color-alpha(vars.$primary-color, 0.15);
                border-radius: vars.$border-radius-md;
                padding: 4px 10px;
                font-size: 11px;
                font-weight: vars.$font-weight-semibold;
                letter-spacing: 0.02em;
                box-shadow: 0 2px 6px func.color-alpha(vars.$black, 0.06);
            }

            .stack-badge__level {
                height: 3px;
            }
        }

        &--medium {
            .stack-badge__name {
                margin-top: vars.$spacing-xxs;
            }

            .stack-badge__level {
                height: 4px;
                margin-top: vars.$spacing-xxs;
            }
        }

        &--large {
            .stack-badge__name {
                margin-top: vars.$spacing-xs;
            }

            .stack-badge__level {
                height: 5px;
                margin-top: vars.$spacing-xs;
            }
        }

        &__name {
            text-align: center;
            font-weight: 500;
            color: vars.$black-light;
            white-space: nowrap;
            max-width: 100px;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        &__level {
            width: 100%;
            border-radius: vars.$border-radius-full;
            overflow: hidden;
        }

        &__level-bar {
            height: 100%;
            border-radius: vars.$border-radius-full;
        }
    }
</style>
