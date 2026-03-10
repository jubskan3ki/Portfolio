<template>
    <div :class="classes" role="status" :aria-label="label">
        <!-- Spinner visual -->
        <svg v-if="type === 'circle'" class="spinner__circle" viewBox="0 0 24 24">
            <circle
                class="spinner__track"
                cx="12"
                cy="12"
                r="10"
                fill="none"
                stroke-width="2.5"
            />
            <circle
                class="spinner__path"
                cx="12"
                cy="12"
                r="10"
                fill="none"
                stroke-width="2.5"
            />
        </svg>

        <div v-else class="spinner__dots">
            <span v-for="i in 3" :key="i" class="spinner__dot"></span>
        </div>

        <!-- Label -->
        <span v-if="showLabel && label" class="spinner__label">{{ label }}</span>

        <!-- Screen reader -->
        <span class="sr-only">{{ label }}</span>
    </div>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import type { SpinnerSize } from '@/types/components/loaders';

    interface Props {
        type?: 'circle' | 'dots';
        size?: SpinnerSize;
        label?: string;
        showLabel?: boolean;
    }

    const props = withDefaults(defineProps<Props>(), {
        type: 'circle',
        size: 'md',
        label: 'Chargement...',
        showLabel: false,
    });

    const classes = computed(() => ['spinner', `spinner--${props.type}`, `spinner--${props.size}`]);
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as v;

    .spinner {
        display: inline-flex;
        flex-direction: column;
        align-items: center;
        gap: v.$spacing-xs;
        color: v.$primary-color;

        &__label {
            font-size: v.$font-size-sm;
            color: v.$text-secondary;
            font-weight: v.$font-weight-medium;
        }

        // Circle
        &__circle {
            animation: rotate 1s linear infinite;
        }

        &__track {
            stroke: currentcolor;
            opacity: 0.15;
        }

        &__path {
            stroke: currentcolor;
            stroke-linecap: round;
            stroke-dasharray: 62.83;
            stroke-dashoffset: 47.12;
        }

        // Dots
        &__dots {
            display: flex;
            align-items: center;
            gap: 4px;
        }

        &__dot {
            border-radius: v.$border-radius-full;
            background: currentcolor;
            animation: bounce 1.4s ease-in-out infinite both;

            @for $i from 1 through 3 {
                &:nth-child(#{$i}) {
                    animation-delay: #{($i - 1) * 0.16}s;
                }
            }
        }

        // Sizes
        &--xs {
            .spinner__circle {
                width: 16px;
                height: 16px;
            }
            .spinner__dot {
                width: 4px;
                height: 4px;
            }
        }

        &--sm {
            .spinner__circle {
                width: 20px;
                height: 20px;
            }
            .spinner__dot {
                width: 5px;
                height: 5px;
            }
        }

        &--md {
            .spinner__circle {
                width: 24px;
                height: 24px;
            }
            .spinner__dot {
                width: 6px;
                height: 6px;
            }
        }

        &--lg {
            .spinner__circle {
                width: 32px;
                height: 32px;
            }
            .spinner__dot {
                width: 8px;
                height: 8px;
            }
        }

        &--xl {
            .spinner__circle {
                width: 48px;
                height: 48px;
            }
            .spinner__dot {
                width: 10px;
                height: 10px;
            }
        }
    }

    // Animations
    @keyframes rotate {
        to {
            transform: rotate(360deg);
        }
    }

    @keyframes bounce {
        0%,
        80%,
        100% {
            transform: scale(0.6);
            opacity: 0.5;
        }
        40% {
            transform: scale(1);
            opacity: 1;
        }
    }

    // Screen reader only
    .sr-only {
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border: 0;
    }
</style>
