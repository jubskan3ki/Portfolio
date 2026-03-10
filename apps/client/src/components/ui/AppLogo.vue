<template>
    <component
        :is="linkTo ? resolveComponent('NuxtLink') : 'div'"
        v-bind="linkTo ? { 'to': linkTo, 'aria-label': 'Accueil' } : {}"
        class="app-logo"
        :class="[`app-logo--${size}`, { 'app-logo--dark': dark }]"
    >
        <NuxtImg
            :src="src"
            :alt="alt"
            :width="dimensions.width"
            :height="dimensions.height"
            class="app-logo__image"
            loading="eager"
            decoding="async"
            :fetchpriority="priority ? 'high' : 'auto'"
        />
    </component>
</template>

<script setup lang="ts">
    import { computed, resolveComponent } from 'vue';

    import type { AppLogoProps } from '@/types/components/ui';

    type Props = AppLogoProps;

    const props = withDefaults(defineProps<Props>(), {
        src: '/logo.svg',
        alt: 'Logo Juba Ait-Adda',
        size: 'md',
        dark: false,
        linkTo: '',
        priority: false,
    });

    // Dimensions selon la taille
    const sizeMap = {
        xs: { width: 24, height: 24 },
        sm: { width: 32, height: 32 },
        md: { width: 48, height: 48 },
        lg: { width: 60, height: 60 },
        xl: { width: 80, height: 80 },
    } as const;

    const dimensions = computed(() => sizeMap[props.size]);
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;

    .app-logo {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        text-decoration: none;
        flex-shrink: 0;

        &__image {
            display: block;
            object-fit: contain;
        }

        // Tailles
        &--xs .app-logo__image {
            width: 24px;
            height: 24px;
        }

        &--sm .app-logo__image {
            width: 32px;
            height: 32px;
        }

        &--md .app-logo__image {
            width: 48px;
            height: 48px;
        }

        &--lg .app-logo__image {
            width: 60px;
            height: 60px;
        }

        &--xl .app-logo__image {
            width: 80px;
            height: 80px;
        }

        // Variante sombre
        &--dark {
            filter: brightness(0) invert(1);
        }

        // Transition au hover si c'est un lien
        &[href] {
            transition: opacity vars.$transition-fast;

            &:hover {
                opacity: 0.8;
            }

            &:focus-visible {
                outline: 2px solid vars.$primary-color;
                outline-offset: 4px;
                border-radius: vars.$border-radius-sm;
            }
        }
    }
</style>
