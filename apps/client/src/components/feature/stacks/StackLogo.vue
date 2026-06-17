<template>
    <div
        class="stack-logo"
        :class="[`stack-logo--${size}`, `stack-logo--${rounded}`]"
        :style="logoStyle"
    >
        <BaseImage
            v-if="stack.logo"
            :src="stack.logo"
            :alt="`${stack.name} logo`"
            :width="iconPx"
            :height="iconPx"
            :show-placeholder="false"
            class="stack-logo__img"
        />
        <span v-else class="stack-logo__letter">
            {{ firstLetter }}
        </span>
    </div>
</template>

<script setup lang="ts">
    import { computed, type CSSProperties } from 'vue';

    import BaseImage from '@/components/base/BaseImage.vue';

    type Size = 'xs' | 'sm' | 'md' | 'lg' | 'xl';
    type Rounded = 'md' | 'lg';

    interface StackLike {
        name: string;
        logo?: string;
        color?: string;
    }

    const props = withDefaults(
        defineProps<{
            stack: StackLike;
            size?: Size;
            rounded?: Rounded;
            transitionName?: string;
        }>(),
        {
            size: 'md',
            rounded: 'lg',
            transitionName: undefined,
        },
    );

    // `md` est calé sur le design référence `stack-card__logo` (48px).
    const SIZE_MAP: Record<Size, { box: number; img: number; font: string }> = {
        xs: { box: 24, img: 18, font: '0.75rem' },
        sm: { box: 40, img: 28, font: '1.1rem' },
        md: { box: 48, img: 32, font: '1.25rem' },
        lg: { box: 64, img: 44, font: '1.6rem' },
        xl: { box: 96, img: 64, font: '2.25rem' },
    };

    const iconPx = computed(() => SIZE_MAP[props.size].img);

    const firstLetter = computed(() => (props.stack.name?.charAt(0) ?? '?').toUpperCase());

    // Couleur du stack en bg alpha + lettre saturée ; fallback sur la couleur primary si absente.
    const logoStyle = computed<CSSProperties>(() => {
        const style: CSSProperties = {
            width: `${SIZE_MAP[props.size].box}px`,
            height: `${SIZE_MAP[props.size].box}px`,
            fontSize: SIZE_MAP[props.size].font,
        };

        if (props.stack.color) {
            style.backgroundColor = `${props.stack.color}1F`; // ~12% alpha
            style.color = props.stack.color;
        }

        if (props.transitionName) {
            (style as Record<string, unknown>)['viewTransitionName'] = props.transitionName;
        }

        return style;
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as fn;

    .stack-logo {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        background: fn.color-alpha(vars.$primary-color, 0.1);
        color: vars.$primary-color;
        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;

        // Carrés arrondis (jamais ronds), cohérent avec StackCard.
        &--md {
            border-radius: vars.$border-radius-lg;
        }

        &--lg {
            border-radius: vars.$border-radius-lg;
        }

        &__img {
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;

            :deep(img) {
                width: 68%;
                height: 68%;
                object-fit: contain;
            }
        }

        &__letter {
            font-weight: vars.$font-weight-bold;
            line-height: 1;
            letter-spacing: -0.02em;
        }

        @media (prefers-reduced-motion: reduce) {
            transition: none;
        }
    }
</style>
