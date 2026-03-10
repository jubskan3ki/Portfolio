<template>
    <div class="glass-bg" :class="[`glass-bg--${variant}`, { 'glass-bg--animated': animated }]" aria-hidden="true">
        <!-- Dots pattern -->
        <span v-if="showDots" class="glass-bg__dots"></span>

        <!-- Gradient overlay -->
        <span class="glass-bg__gradient"></span>

        <!-- Floating bubbles -->
        <ClientOnly>
            <div v-if="showBubbles" class="glass-bg__bubbles">
                <span v-for="i in bubbleCount" :key="i" :class="`glass-bg__bubble glass-bg__bubble--${i}`"></span>
            </div>
        </ClientOnly>

        <!-- Optional glow effect -->
        <span v-if="showGlow" class="glass-bg__glow"></span>
    </div>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    type Variant = 'primary' | 'secondary' | 'light' | 'dark';

    interface Props {
        variant?: Variant;
        showDots?: boolean;
        showBubbles?: boolean;
        showGlow?: boolean;
        animated?: boolean;
        bubbleCount?: number;
    }

    const props = withDefaults(defineProps<Props>(), {
        variant: 'primary',
        showDots: true,
        showBubbles: true,
        showGlow: false,
        animated: true,
        bubbleCount: 5,
    });

    const showBubbles = computed(
        () => props.showBubbles && (props.variant === 'primary' || props.variant === 'secondary'),
    );
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/functions' as fn;
    @use '@/styles/abstracts/variables' as vars;

    .glass-bg {
        position: absolute;
        inset: 0;
        pointer-events: none;
        overflow: hidden;

        // Dots pattern
        &__dots {
            position: absolute;
            inset: 0;
            background-image: radial-gradient(fn.color-alpha(vars.$black, 0.07) 1px, transparent 1px);
            background-size: 20px 20px;
            opacity: 0.5;
        }

        // Gradient overlay
        &__gradient {
            position: absolute;
            inset: 0;
        }

        // Bubbles container
        &__bubbles {
            position: absolute;
            inset: 0;
        }

        // Individual bubbles
        &__bubble {
            position: absolute;
            border-radius: 50%;
            filter: blur(40px);
            opacity: 0.5;
            will-change: transform; // GPU acceleration
            backface-visibility: hidden; // Prevent flickering

            &--1 {
                width: 200px;
                height: 200px;
                top: 10%;
                left: 5%;
            }

            &--2 {
                width: 150px;
                height: 150px;
                top: 50%;
                right: 10%;
            }

            &--3 {
                width: 180px;
                height: 180px;
                bottom: 20%;
                left: 20%;
            }

            &--4 {
                width: 120px;
                height: 120px;
                top: 30%;
                right: 30%;
            }

            &--5 {
                width: 100px;
                height: 100px;
                bottom: 10%;
                right: 5%;
            }
        }

        // Glow effect
        &__glow {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 60%;
            height: 60%;
            border-radius: 50%;
            filter: blur(80px);
            opacity: 0.3;
        }

        // Variant: Primary
        &--primary {
            .glass-bg__gradient {
                background: linear-gradient(
                    135deg,
                    fn.color-alpha(vars.$primary-color, 0.08) 0%,
                    fn.color-alpha(vars.$secondary-color, 0.04) 50%,
                    transparent 100%
                );
            }

            .glass-bg__bubble {
                background: vars.$primary-color;

                &--2,
                &--4 {
                    background: vars.$secondary-color;
                }
            }

            .glass-bg__glow {
                background: vars.$primary-color;
            }
        }

        // Variant: Secondary
        &--secondary {
            .glass-bg__gradient {
                background: linear-gradient(
                    135deg,
                    fn.color-alpha(vars.$secondary-color, 0.08) 0%,
                    fn.color-alpha(vars.$primary-color, 0.04) 50%,
                    transparent 100%
                );
            }

            .glass-bg__glow {
                background: vars.$secondary-color;
            }
        }

        // Variant: Light
        &--light {
            .glass-bg__gradient {
                background: linear-gradient(135deg, fn.color-alpha(vars.$white, 0.8) 0%, transparent 100%);
            }

            .glass-bg__dots {
                background-image: radial-gradient(fn.color-alpha(vars.$black, 0.04) 1px, transparent 1px);
            }
        }

        // Variant: Dark
        &--dark {
            .glass-bg__gradient {
                background: linear-gradient(
                    135deg,
                    fn.color-alpha(vars.$black, 0.4) 0%,
                    fn.color-alpha(vars.$primary-color, 0.1) 100%
                );
            }

            .glass-bg__dots {
                background-image: radial-gradient(fn.color-alpha(vars.$white, 0.05) 1px, transparent 1px);
            }
        }

        // Animation
        &--animated {
            .glass-bg__bubble {
                animation: float-bubble 20s ease-in-out infinite;

                &--1 {
                    animation-delay: 0s;
                }

                &--2 {
                    animation-delay: -4s;
                    animation-duration: 25s;
                }

                &--3 {
                    animation-delay: -8s;
                    animation-duration: 22s;
                }

                &--4 {
                    animation-delay: -12s;
                    animation-duration: 28s;
                }

                &--5 {
                    animation-delay: -16s;
                    animation-duration: 18s;
                }
            }
        }
    }

    @keyframes float-bubble {
        0%,
        100% {
            transform: translateY(0) translateX(0);
        }

        25% {
            transform: translateY(-20px) translateX(10px);
        }

        50% {
            transform: translateY(-10px) translateX(-10px);
        }

        75% {
            transform: translateY(-25px) translateX(5px);
        }
    }
</style>
