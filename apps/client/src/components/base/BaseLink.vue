<template>
    <NuxtLink v-if="isInternalLink" v-bind="componentProps" :class="linkClasses">
        <slot name="icon-left"></slot>
        <slot>{{ text }}</slot>
        <slot name="icon-right"></slot>
    </NuxtLink>

    <a v-else-if="isExternalLink" v-bind="componentProps" :class="linkClasses">
        <slot name="icon-left"></slot>
        <slot>{{ text }}</slot>
        <slot name="icon-right"></slot>
    </a>

    <button v-else v-bind="componentProps" :class="linkClasses">
        <slot name="icon-left"></slot>
        <slot>{{ text }}</slot>
        <slot name="icon-right"></slot>
    </button>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import { useLinkResolver } from '@/composables/ui/useLinkResolver';

    import type { LinkProps, LinkVariant, LinkTarget } from '@/types/components/base';

    type Props = Omit<LinkProps, 'variant' | 'target'> & {
        variant?: LinkVariant | '';
        target?: LinkTarget | '';
    };

    const props = withDefaults(defineProps<Props>(), {
        params: () => ({}),
        text: '',
        variant: '',
        target: '',
        block: false,
        underline: false,
        ariaLabel: '',
        customClass: '',
    });

    const { isInternalLink, isExternalLink, linkProps } = useLinkResolver(() => ({
        to: props.to,
        params: props.params,
        target: props.target,
    }));

    const componentProps = computed(() => ({
        ...linkProps.value,
        'aria-label': props.ariaLabel || undefined,
    }));

    const linkClasses = computed(() => [
        'link',
        props.variant && `link--${props.variant}`,
        {
            'link--block': props.block,
            'link--underline': props.underline,
        },
        props.customClass,
    ]);
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .link {
        display: inline-flex;
        align-items: center;
        gap: vars.$spacing-xxs;
        color: vars.$primary-color;
        text-decoration: none;
        transition: color vars.$transition-base;

        @include mix.focus-outline;

        &:hover {
            color: vars.$primary-dark;
            text-decoration: underline;
        }

        &--primary {
            color: vars.$primary-color;

            &:hover {
                color: vars.$primary-dark;
            }
        }

        &--secondary {
            color: vars.$secondary-color;

            &:hover {
                color: vars.$secondary-dark;
            }
        }

        &--white {
            color: vars.$white;

            &:hover {
                color: func.adjust-color-brightness(vars.$white, -15%);
            }
        }

        &--subtle {
            color: vars.$gray-dark;

            &:hover {
                color: vars.$black-light;
            }
        }

        &--block {
            display: flex;
        }

        &--underline {
            text-decoration: underline;
        }
    }
</style>
