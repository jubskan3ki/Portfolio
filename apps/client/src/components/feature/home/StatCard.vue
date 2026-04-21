<template>
    <div ref="cardRef" class="stat-card" :class="[`stat-card--${variant}`]" @mouseenter="startCount">
        <div class="stat-card__icon">
            <BaseIcon :name="icon" :size="22" />
        </div>
        <div class="stat-card__info">
            <p class="stat-card__value">
                {{ displayValue }}<span v-if="suffix" class="stat-card__suffix">{{ suffix }}</span>
            </p>
            <small class="stat-card__label">{{ label }}</small>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { computed, onMounted, ref } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import { useReducedMotion } from '@/composables/accessibility/useReducedMotion';

    import type { StatCardProps } from '@/types/feature/home';

    const props = withDefaults(defineProps<StatCardProps>(), {
        variant: 'light',
        suffix: '',
        duration: 2000,
    });

    const { prefersReducedMotion } = useReducedMotion();
    const currentValue = ref(0);
    const counted = ref(false);

    const displayValue = computed(() => {
        if (typeof props.value === 'string' && props.value.endsWith('+')) {
            const numPart = parseInt(props.value.replace('+', ''));
            return Math.min(numPart, currentValue.value);
        }
        return currentValue.value;
    });

    const targetValue = computed(() => {
        if (typeof props.value === 'string') {
            if (props.value.endsWith('+')) {
                return parseInt(props.value.replace('+', ''));
            }
            return parseInt(props.value);
        }
        return props.value;
    });

    const startCount = () => {
        if (counted.value) {
            return;
        }
        counted.value = true;

        if (prefersReducedMotion.value) {
            currentValue.value = targetValue.value;
            return;
        }

        const startTime = Date.now();
        const endTime = startTime + props.duration;

        const updateCounter = () => {
            const now = Date.now();
            const remaining = Math.max(0, endTime - now);
            const progress = 1 - remaining / props.duration;

            currentValue.value = Math.floor(progress * targetValue.value);

            if (remaining > 0) {
                requestAnimationFrame(updateCounter);
            } else {
                currentValue.value = targetValue.value;
            }
        };

        updateCounter();
    };

    const cardRef = ref<HTMLElement | null>(null);

    onMounted(() => {
        startCount();
    });

    defineExpose({ cardRef });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as fn;

    .stat-card {
        display: flex;
        align-items: center;
        gap: vars.$spacing-xs;
        padding: vars.$spacing-sm vars.$spacing-md;
        min-width: 180px;
        border-radius: vars.$border-radius-lg;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        transition:
            transform 0.3s ease,
            box-shadow 0.3s ease;

        @media (prefers-reduced-motion: reduce) {
            transition: none;
        }

        &:hover {
            transform: translateY(-3px);
        }

        // Icon
        &__icon {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 44px;
            height: 44px;
            border-radius: vars.$border-radius-md;
            flex-shrink: 0;
        }

        // Info
        &__info {
            display: flex;
            flex-direction: column;
            gap: vars.$spacing-xxs;
            flex: 1;
            text-align: right;
        }

        // Value
        &__value {
            font-weight: vars.$font-weight-bold;
            line-height: 1;
            letter-spacing: -0.02em;
        }

        &__suffix {
            font-weight: vars.$font-weight-semibold;
            margin-left: 1px;
        }

        // Label
        &__label {
            font-weight: vars.$font-weight-medium;
            line-height: 1.2;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        // Light variant
        &--light {
            background: fn.color-alpha(vars.$white, 0.9);
            border: 1px solid fn.color-alpha(vars.$white, 0.8);
            box-shadow: 0 4px 20px fn.color-alpha(vars.$black, 0.06);

            &:hover {
                box-shadow: 0 8px 32px fn.color-alpha(vars.$black, 0.1);
            }

            .stat-card__icon {
                background: fn.color-alpha(vars.$primary-color, 0.1);
                color: vars.$primary-color;
            }

            .stat-card__value {
                color: vars.$primary-color;
            }

            .stat-card__suffix {
                color: vars.$primary-color;
            }

            .stat-card__label {
                color: vars.$text-secondary;
            }
        }

        // Dark variant
        &--dark {
            background: fn.color-alpha(vars.$black-light, 0.95);
            border: 1px solid fn.color-alpha(vars.$primary-color, 0.25);
            box-shadow: 0 4px 24px fn.color-alpha(vars.$black, 0.4);

            &:hover {
                border-color: fn.color-alpha(vars.$primary-color, 0.4);
                box-shadow: 0 8px 32px fn.color-alpha(vars.$black, 0.5);
            }

            .stat-card__icon {
                background: fn.color-alpha(vars.$primary-color, 0.2);
                border: 1px solid fn.color-alpha(vars.$primary-color, 0.3);
                color: vars.$secondary-light;
            }

            .stat-card__value {
                color: vars.$white;
            }

            .stat-card__suffix {
                color: vars.$secondary-light;
            }

            .stat-card__label {
                color: fn.color-alpha(vars.$white, 0.55);
            }
        }

        // Primary variant
        &--primary {
            background: fn.color-alpha(vars.$white, 0.12);
            border: 1px solid fn.color-alpha(vars.$white, 0.2);
            box-shadow: 0 4px 20px fn.color-alpha(vars.$black, 0.15);

            &:hover {
                background: fn.color-alpha(vars.$white, 0.18);
                box-shadow: 0 8px 32px fn.color-alpha(vars.$black, 0.2);
            }

            .stat-card__icon {
                background: fn.color-alpha(vars.$white, 0.15);
                border: 1px solid fn.color-alpha(vars.$white, 0.2);
                color: vars.$white;
            }

            .stat-card__value {
                color: vars.$white;
            }

            .stat-card__suffix {
                color: fn.color-alpha(vars.$white, 0.85);
            }

            .stat-card__label {
                color: fn.color-alpha(vars.$white, 0.65);
            }
        }

        // Secondary variant
        &--secondary {
            background: fn.color-alpha(vars.$black, 0.6);
            border: 1px solid fn.color-alpha(vars.$primary-color, 0.45);
            box-shadow:
                0 4px 24px fn.color-alpha(vars.$black, 0.4),
                0 0 30px fn.color-alpha(vars.$primary-color, 0.15);

            &:hover {
                border-color: fn.color-alpha(vars.$primary-color, 0.6);
                box-shadow:
                    0 8px 32px fn.color-alpha(vars.$black, 0.5),
                    0 0 40px fn.color-alpha(vars.$primary-color, 0.2);
            }

            .stat-card__icon {
                background: fn.color-alpha(vars.$primary-color, 0.35);
                border: 1px solid fn.color-alpha(vars.$primary-color, 0.5);
                color: vars.$white;
            }

            .stat-card__value {
                color: vars.$white;
            }

            .stat-card__suffix {
                color: fn.color-alpha(vars.$white, 0.85);
            }

            .stat-card__label {
                color: fn.color-alpha(vars.$white, 0.6);
            }
        }
    }
</style>
