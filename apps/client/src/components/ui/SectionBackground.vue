<template>
    <div class="section-bg" :class="[`section-bg--${variant}`]" aria-hidden="true">
        <span class="section-bg__dots"></span>
        <span class="section-bg__gradient"></span>
        <ClientOnly>
            <div v-if="showBubbles" class="section-bg__bubbles">
                <span class="section-bg__bubble section-bg__bubble--1"></span>
                <span class="section-bg__bubble section-bg__bubble--2"></span>
                <span class="section-bg__bubble section-bg__bubble--3"></span>
                <span class="section-bg__bubble section-bg__bubble--4"></span>
                <span class="section-bg__bubble section-bg__bubble--5"></span>
            </div>
        </ClientOnly>
    </div>
</template>

<script setup lang="ts">
    import { computed, onMounted, ref } from 'vue';

    type SectionBackgroundVariant = 'light' | 'dark' | 'primary' | 'secondary';

    const props = withDefaults(
        defineProps<{
            variant?: SectionBackgroundVariant;
        }>(),
        { variant: 'primary' },
    );

    const hasBubbleVariant = computed(() => props.variant === 'primary' || props.variant === 'secondary');
    const bubblesReady = ref(false);
    const showBubbles = computed(() => hasBubbleVariant.value && bubblesReady.value);

    onMounted(() => {
        if (!hasBubbleVariant.value) {
            return;
        }
        if ('requestIdleCallback' in window) {
            requestIdleCallback(() => {
                bubblesReady.value = true;
            });
        } else {
            setTimeout(() => {
                bubblesReady.value = true;
            }, 200);
        }
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/functions' as fn;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/variables' as vars;

    .section-bg {
        position: absolute;
        inset: 0;
        pointer-events: none;

        // Dots
        &__dots {
            position: absolute;
            inset: 0;
            opacity: 0.4;
        }

        // Gradient
        &__gradient {
            position: absolute;
            inset: 0;
        }

        // Bubbles container
        &__bubbles {
            position: absolute;
            inset: 0;
            overflow: hidden;
        }

        // Individual bubbles
        &__bubble {
            position: absolute;
            border-radius: 50%;
            pointer-events: none;

            @media (prefers-reduced-motion: reduce) {
                animation: none !important;
            }

            &--1 {
                width: 55px;
                height: 55px;
                top: -10px;
                right: 12%;
                animation: float-bubble 8s ease-in-out infinite;
            }

            &--2 {
                width: 32px;
                height: 32px;
                bottom: 18%;
                left: 12%;
                animation: float-bubble 6s ease-in-out infinite reverse;
            }

            &--3 {
                width: 22px;
                height: 22px;
                top: 40%;
                left: 22%;
                animation: float-bubble 7s ease-in-out infinite 1s;

                @include mix.responsive(mobile) {
                    display: none;
                }
            }

            &--4 {
                width: 42px;
                height: 42px;
                bottom: 20%;
                right: 22%;
                animation: float-bubble 9s ease-in-out infinite 0.5s;

                @include mix.responsive(mobile) {
                    width: 28px;
                    height: 28px;
                }
            }

            &--5 {
                width: 16px;
                height: 16px;
                top: 18%;
                left: 7%;
                animation: float-bubble 5s ease-in-out infinite 2s reverse;
            }
        }

        // ─── Light variant ───
        &--light {
            .section-bg__dots {
                @include mix.dots-pattern(fn.color-alpha(vars.$gray, 0.4), 1.5px, 28px);
            }

            .section-bg__gradient {
                background: radial-gradient(
                    ellipse 80% 50% at 50% -20%,
                    fn.color-alpha(vars.$primary-color, 0.08),
                    transparent
                );
            }
        }

        // ─── Dark variant ───
        &--dark {
            .section-bg__dots {
                @include mix.dots-pattern(fn.color-alpha(vars.$primary-color, 0.65), 1.5px, 28px);
            }

            .section-bg__gradient {
                background: radial-gradient(
                    ellipse 80% 50% at 50% -20%,
                    fn.color-alpha(vars.$primary-dark, 0.4),
                    transparent
                );
            }
        }

        // ─── Primary variant ───
        &--primary {
            .section-bg__dots {
                display: none;
            }

            .section-bg__gradient {
                background: radial-gradient(
                    ellipse 80% 50% at 50% -20%,
                    fn.color-alpha(vars.$primary-color, 0.15),
                    transparent
                );
            }

            .section-bg__bubble {
                background: fn.color-alpha(vars.$white, 0.15);
                box-shadow: 0 4px 16px fn.color-alpha(vars.$white, 0.1);

                &--1 {
                    background: fn.color-alpha(vars.$white, 0.22);
                }

                &--2 {
                    background: fn.color-alpha(vars.$white, 0.14);
                }

                &--3 {
                    background: fn.color-alpha(vars.$white, 0.18);
                }

                &--4 {
                    background: fn.color-alpha(vars.$white, 0.16);
                }

                &--5 {
                    background: fn.color-alpha(vars.$white, 0.12);
                }
            }
        }

        // ─── Secondary variant ───
        &--secondary {
            .section-bg__dots {
                display: none;
            }

            .section-bg__gradient {
                background: radial-gradient(
                    ellipse 80% 50% at 50% -20%,
                    fn.color-alpha(vars.$primary-color, 0.25),
                    transparent
                );
            }

            .section-bg__bubble {
                background: fn.color-alpha(vars.$white, 0.12);
                box-shadow: 0 4px 24px fn.color-alpha(vars.$primary-color, 0.4);

                &--1 {
                    background: fn.color-alpha(vars.$white, 0.18);
                }

                &--2 {
                    background: fn.color-alpha(vars.$white, 0.14);
                }

                &--3 {
                    background: fn.color-alpha(vars.$white, 0.16);
                }

                &--4 {
                    background: fn.color-alpha(vars.$white, 0.12);
                }

                &--5 {
                    background: fn.color-alpha(vars.$white, 0.1);
                }
            }
        }
    }

    // Bubble floating animation
    @keyframes float-bubble {
        0%,
        100% {
            transform: translate(0, 0) rotate(0deg);
        }

        25% {
            transform: translate(-5px, -10px) rotate(5deg);
        }

        50% {
            transform: translate(5px, -5px) rotate(-3deg);
        }

        75% {
            transform: translate(-3px, -12px) rotate(2deg);
        }
    }
</style>
