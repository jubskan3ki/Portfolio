<template>
    <div class="footer-contact-item">
        <BaseIcon :name="icon" :size="18" aria-hidden="true" />

        <a v-if="isLink" :href="linkHref" class="footer-contact-item__link">
            {{ text }}
        </a>
        <span v-else class="footer-contact-item__text">{{ text }}</span>
    </div>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';

    import type { FooterContactItemProps, ContactItemLinkType } from '@/types/components/layouts';

    const props = withDefaults(defineProps<FooterContactItemProps>(), {
        isLink: false,
        linkType: 'none',
    });

    // Link href mapping
    const LINK_PREFIXES: Record<ContactItemLinkType, string> = {
        email: 'mailto:',
        phone: 'tel:',
        url: '',
        none: '',
    };

    const linkHref = computed(() => {
        const prefix = LINK_PREFIXES[props.linkType];
        return `${prefix}${props.text}`;
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;

    .footer-contact-item {
        display: flex;
        align-items: center;
        gap: vars.$spacing-xs;
        color: vars.$gray-dark;
        transition: transform vars.$transition-fast;

        &:hover {
            transform: translateX(5px);
        }

        &__link {
            color: inherit;
            text-decoration: none;
            transition: color vars.$transition-fast;

            &:hover {
                color: vars.$primary-color;
            }

            &:focus-visible {
                outline: 2px solid vars.$primary-color;
                outline-offset: 2px;
            }
        }

        &__text {
            color: inherit;
        }
    }
</style>
