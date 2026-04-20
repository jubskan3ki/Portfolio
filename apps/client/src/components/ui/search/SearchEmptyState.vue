<template>
    <div class="search-empty">
        <span class="search-empty__icon">
            <BaseIcon name="inbox" :size="32" />
        </span>
        <p>Aucun resultat</p>
        <small>Aucun element trouve pour "{{ query }}"</small>
    </div>
</template>

<script setup lang="ts">
    import BaseIcon from '@/components/base/BaseIcon.vue';

    import type { SearchEmptyStateProps } from '@/types/components/ui';

    defineProps<SearchEmptyStateProps>();
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as v;

    .search-empty {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: v.$spacing-xxl;
        text-align: center;

        p {
            margin: 0 0 v.$spacing-xxs;
            font-weight: v.$font-weight-semibold;
            color: v.$text-primary;
        }

        small {
            color: v.$text-muted;
        }

        &__icon {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 56px;
            height: 56px;
            margin-bottom: v.$spacing-md;
            border-radius: v.$border-radius-full;
            background: v.$bg-secondary;
            color: v.$text-muted;
        }
    }
</style>
