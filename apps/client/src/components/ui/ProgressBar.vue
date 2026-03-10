<template>
    <div
        class="progress"
        :class="[{ 'progress--striped': striped, 'progress--animated': animated }, customClass]"
        role="progressbar"
        :aria-valuenow="percentage"
        :aria-valuemin="0"
        :aria-valuemax="100"
        :aria-label="label || 'Progression'"
    >
        <div v-if="label || $slots.label" class="progress__label">
            <small><slot name="label">{{ label }}</slot></small>
            <small v-if="showPercentage" class="progress__percentage">{{ percentage }}%</small>
        </div>

        <div class="progress__container" :class="`progress__container--${size}`">
            <div class="progress__bar" :class="`progress__bar--${variant}`" :style="{ width: `${percentage}%` }">
                <small v-if="showTextInside && size !== 'sm'" class="progress__text">{{ percentage }}%</small>
            </div>

            <div v-if="steps > 0" class="progress__steps">
                <div
                    v-for="step in steps"
                    :key="step"
                    class="progress__step"
                    :class="{ 'progress__step--active': (step / steps) * 100 <= percentage }"
                ></div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import type { ProgressBarProps } from '@/types/components/ui';

    type Props = ProgressBarProps;

    const props = withDefaults(defineProps<Props>(), {
        value: 0,
        max: 100,
        label: '',
        showPercentage: true,
        showTextInside: false,
        striped: false,
        animated: false,
        variant: 'primary',
        size: 'md',
        steps: 0,
        customClass: '',
    });

    const percentage = computed(() => {
        const value = Math.max(0, Math.min(props.value, props.max));
        return Math.round((value / props.max) * 100);
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as func;

    @keyframes progress-bar-stripes {
        from {
            background-position: 1rem 0;
        }

        to {
            background-position: 0 0;
        }
    }

    .progress {
        margin-bottom: vars.$spacing-md;

        &__label {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: vars.$spacing-xxs;
            color: vars.$text-secondary;
        }

        &__percentage {
            font-weight: vars.$font-weight-medium;
            color: vars.$text-primary;
        }

        &__container {
            position: relative;
            background-color: func.color-alpha(vars.$gray-light, 0.5);
            border-radius: vars.$border-radius-full;
            overflow: hidden;

            &--sm {
                height: 4px;
            }

            &--md {
                height: 8px;
            }

            &--lg {
                height: 12px;
            }
        }

        &__bar {
            height: 100%;
            border-radius: vars.$border-radius-full;
            transition: width 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;

            &--primary {
                background: vars.$primary-color;
            }

            &--secondary {
                background: vars.$secondary-color;
            }

            &--success {
                background: vars.$success-color;
            }

            &--danger {
                background: vars.$danger-color;
            }

            &--warning {
                background: vars.$warning-color;
            }

            &--info {
                background: vars.$info-color;
            }
        }

        &__text {
            color: vars.$white;
            font-weight: vars.$font-weight-semibold;
            white-space: nowrap;
            text-shadow: 0 1px 2px func.color-alpha(vars.$black, 0.2);
        }

        &--striped &__bar {
            background-image: linear-gradient(
                45deg,
                func.color-alpha(vars.$white, 0.15) 25%,
                transparent 25%,
                transparent 50%,
                func.color-alpha(vars.$white, 0.15) 50%,
                func.color-alpha(vars.$white, 0.15) 75%,
                transparent 75%,
                transparent
            );
            background-size: 1rem 1rem;
        }

        &--animated &__bar {
            animation: progress-bar-stripes 1s linear infinite;
        }

        &__steps {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: space-between;
            padding: 0 calc(100% / v-bind(steps) / 2);
            pointer-events: none;
        }

        &__step {
            width: 1px;
            height: 100%;
            background-color: func.color-alpha(vars.$white, 0.3);
            transition: background-color 0.3s ease;

            &--active {
                background-color: func.color-alpha(vars.$white, 0.6);
            }
        }
    }
</style>
