<template>
    <div class="sidebar-card">
        <h3 class="sidebar-card__heading">
            <BaseIcon name="Share2" :size="16" class="sidebar-card__heading-icon" />
            Partager
        </h3>
        <div class="share-actions">
            <button class="share-actions__btn" title="Partager sur Twitter" @click="shareOn('twitter')">
                <BaseIcon name="twitter" :size="16" />
                <span>Twitter</span>
            </button>
            <button class="share-actions__btn" title="Partager sur LinkedIn" @click="shareOn('linkedin')">
                <BaseIcon name="linkedin" :size="16" />
                <span>LinkedIn</span>
            </button>
            <button class="share-actions__btn" title="Copier le lien" @click="copyLink">
                <BaseIcon :name="linkCopied ? 'check' : 'link'" :size="16" />
                <span>{{ linkCopied ? 'Copié !' : 'Copier le lien' }}</span>
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import { useShare } from '@/composables/ui/useShare';

    import type { MaybeRef } from 'vue';

    const props = defineProps<{
        title: MaybeRef<string>;
    }>();

    const { linkCopied, shareOn, copyLink } = useShare(props.title);
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as fn;

    .sidebar-card {
        background: fn.color-alpha(vars.$white, 0.95);
        border: 1px solid fn.color-alpha(vars.$border-color, 0.1);
        border-radius: vars.$border-radius-xl;
        padding: vars.$spacing-lg;
        box-shadow: 0 4px 24px fn.color-alpha(vars.$black, 0.06);

        &__heading {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;
            margin: 0 0 vars.$spacing-md;
            font-weight: vars.$font-weight-semibold;
            color: vars.$text-primary;
            letter-spacing: vars.$letter-spacing-tight;
        }

        &__heading-icon {
            color: vars.$secondary-color;
            flex-shrink: 0;
        }
    }

    .share-actions {
        display: flex;
        flex-direction: column;
        gap: vars.$spacing-xxs;

        &__btn {
            display: flex;
            align-items: center;
            gap: vars.$spacing-sm;
            padding: vars.$spacing-sm vars.$spacing-md;
            background: fn.color-alpha(vars.$primary-color, 0.04);
            border: 1px solid fn.color-alpha(vars.$border-color, 0.08);
            border-radius: vars.$border-radius-md;
            color: vars.$text-secondary;
            font-size: vars.$font-size-sm;
            font-weight: vars.$font-weight-medium;
            cursor: pointer;
            transition: all 0.2s ease;

            &:hover {
                background: fn.color-alpha(vars.$primary-color, 0.08);
                border-color: fn.color-alpha(vars.$primary-color, 0.15);
                color: vars.$primary-color;
            }
        }
    }
</style>
