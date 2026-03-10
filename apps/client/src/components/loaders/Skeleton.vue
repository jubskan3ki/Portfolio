<template>
    <div :class="classes" :style="style" aria-hidden="true"></div>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import type { SkeletonType, SkeletonAnimation } from '@/types/components/loaders';

    interface Props {
        type?: SkeletonType;
        width?: string | number;
        height?: string | number;
        radius?: string | number;
        animate?: boolean;
        animation?: SkeletonAnimation;
    }

    const props = withDefaults(defineProps<Props>(), {
        type: 'block',
        width: undefined,
        height: undefined,
        radius: undefined,
        animate: true,
        animation: 'wave',
    });

    // Convert number to px
    const toPx = (size: string | number | undefined) => {
        if (size === undefined) {
            return undefined;
        }
        return typeof size === 'number' ? `${size}px` : size;
    };

    // Default dimensions by type
    const DEFAULTS: Record<SkeletonType, { width: string; height: string; radius: string }> = {
        block: { width: '100%', height: '20px', radius: '4px' },
        circle: { width: '48px', height: '48px', radius: '50%' },
        text: { width: '100%', height: '16px', radius: '2px' },
        image: { width: '100%', height: '200px', radius: '8px' },
        button: { width: '120px', height: '40px', radius: '6px' },
        avatar: { width: '48px', height: '48px', radius: '50%' },
    };

    const style = computed(() => ({
        width: toPx(props.width) ?? DEFAULTS[props.type].width,
        height: toPx(props.height) ?? DEFAULTS[props.type].height,
        borderRadius: toPx(props.radius) ?? DEFAULTS[props.type].radius,
    }));

    const classes = computed(() => [
        'skeleton',
        `skeleton--${props.type}`,
        props.animate && `skeleton--${props.animation}`,
    ]);
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as v;
    @use '@/styles/abstracts/functions' as fn;

    .skeleton {
        display: block;
        background: fn.color-alpha(v.$gray-light, 0.5);
        position: relative;
        overflow: hidden;

        // Wave animation (shimmer)
        &--wave::after {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(90deg, transparent 0%, fn.color-alpha(v.$white, 0.5) 50%, transparent 100%);
            transform: translateX(-100%);
            animation: wave 1.5s ease-in-out infinite;
        }

        // Pulse animation
        &--pulse {
            animation: pulse 1.5s ease-in-out infinite;
        }

        // Type-specific
        &--text {
            & + & {
                margin-top: v.$spacing-xxs;
            }
            &:last-of-type:not(:first-of-type) {
                max-width: 70%;
            }
        }

        &--avatar,
        &--button {
            flex-shrink: 0;
        }
    }

    // Animations
    @keyframes wave {
        to {
            transform: translateX(100%);
        }
    }

    @keyframes pulse {
        0%,
        100% {
            opacity: 0.6;
        }
        50% {
            opacity: 0.3;
        }
    }
</style>
