<template>
    <nav v-if="totalPages > 1" :class="paginationClasses" role="navigation" :aria-label="ariaLabel">
        <button
            :class="prevButtonClasses"
            :disabled="currentPage <= 1"
            :aria-label="currentPage <= 1 ? 'Première page atteinte' : 'Aller à la page précédente'"
            @click="handlePrevious"
        >
            <BaseIcon name="chevron-left" :size="16" />
            <span v-if="showText" class="pagination__btn-text">Précédent</span>
        </button>

        <ul class="pagination__list" role="list">
            <PaginationItem
                v-if="showFirstPage"
                :page="1"
                :is-active="currentPage === 1"
                @click="handlePageChange(1)"
            />

            <PaginationItem v-if="leftEllipsisVisible" :page="0" is-ellipsis />

            <PaginationItem
                v-for="page in centerPages"
                :key="page"
                :page="page"
                :is-active="currentPage === page"
                @click="handlePageChange(page)"
            />

            <PaginationItem v-if="rightEllipsisVisible" :page="0" is-ellipsis />

            <PaginationItem
                v-if="showLastPage"
                :page="totalPages"
                :is-active="currentPage === totalPages"
                @click="handlePageChange(totalPages)"
            />
        </ul>

        <button
            :class="nextButtonClasses"
            :disabled="currentPage >= totalPages"
            :aria-label="currentPage >= totalPages ? 'Dernière page atteinte' : 'Aller à la page suivante'"
            @click="handleNext"
        >
            <span v-if="showText" class="pagination__btn-text">Suivant</span>
            <BaseIcon name="chevron-right" :size="16" />
        </button>

        <div v-if="showInfo" class="pagination__info">
            <span class="pagination__info-text">
                Page <strong>{{ currentPage }}</strong> sur <strong>{{ totalPages }}</strong>
            </span>
        </div>
    </nav>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import PaginationItem from '@/components/navigation/PaginationItem.vue';

    import type { PaginationProps } from '@/types/components/navigation';

    type Props = PaginationProps;

    const props = withDefaults(defineProps<Props>(), {
        maxVisiblePages: 5,
        showText: true,
        showInfo: false,
        size: 'md',
        variant: 'default',
        ariaLabel: 'Pagination',
        customClass: '',
    });

    const emit = defineEmits<{
        'update:currentPage': [page: number];
        pageChange: [page: number];
    }>();

    const paginationClasses = computed(() => [
        'pagination',
        `pagination--${props.size}`,
        `pagination--${props.variant}`,
        props.customClass,
    ]);

    const prevButtonClasses = computed(() => [
        'pagination__btn',
        'pagination__btn--prev',
        { 'pagination__btn--disabled': props.currentPage <= 1 },
    ]);

    const nextButtonClasses = computed(() => [
        'pagination__btn',
        'pagination__btn--next',
        { 'pagination__btn--disabled': props.currentPage >= props.totalPages },
    ]);

    const centerPages = computed(() => {
        const { currentPage, totalPages, maxVisiblePages } = props;

        if (totalPages <= maxVisiblePages) {
            return Array.from({ length: totalPages }, (_, i) => i + 1);
        }

        const sidePages = Math.floor(maxVisiblePages / 2);
        let startPage = Math.max(1, currentPage - sidePages);
        const endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);

        if (endPage === totalPages) {
            startPage = Math.max(1, endPage - maxVisiblePages + 1);
        }

        return Array.from({ length: endPage - startPage + 1 }, (_, i) => startPage + i);
    });

    const showFirstPage = computed(() => {
        if (props.totalPages <= props.maxVisiblePages) {
            return false;
        }
        return !centerPages.value.includes(1);
    });

    const showLastPage = computed(() => {
        if (props.totalPages <= props.maxVisiblePages) {
            return false;
        }
        return !centerPages.value.includes(props.totalPages);
    });

    const leftEllipsisVisible = computed(() => {
        if (centerPages.value.length === 0) {
            return false;
        }
        const firstCenterPage = centerPages.value[0];
        return showFirstPage.value && firstCenterPage !== undefined && firstCenterPage > 2;
    });

    const rightEllipsisVisible = computed(() => {
        if (centerPages.value.length === 0) {
            return false;
        }
        const lastCenterPage = centerPages.value[centerPages.value.length - 1];
        return showLastPage.value && lastCenterPage !== undefined && lastCenterPage < props.totalPages - 1;
    });

    const handlePageChange = (page: number) => {
        if (page !== props.currentPage && page >= 1 && page <= props.totalPages) {
            emit('update:currentPage', page);
            emit('pageChange', page);
        }
    };

    const handlePrevious = () => {
        if (props.currentPage > 1) {
            handlePageChange(props.currentPage - 1);
        }
    };

    const handleNext = () => {
        if (props.currentPage < props.totalPages) {
            handlePageChange(props.currentPage + 1);
        }
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .pagination {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-wrap: wrap;
        gap: vars.$spacing-xxs;
        margin: vars.$spacing-lg 0;

        &__list {
            display: flex;
            align-items: center;
            gap: 4px;
            list-style: none;
            margin: 0;
            padding: 0;
        }

        &__btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: vars.$spacing-xxs;
            height: 40px;
            padding: 0 vars.$spacing-md;
            border: none;
            border-radius: vars.$border-radius-lg;
            background: func.color-alpha(vars.$gray-light, 0.5);
            color: vars.$text-primary;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);

            &:hover:not(:disabled) {
                background: func.color-alpha(vars.$primary-color, 0.1);
                color: vars.$primary-color;
                transform: translateY(-1px);
            }

            &:focus-visible {
                outline: 2px solid vars.$primary-color;
                outline-offset: 2px;
            }

            &:disabled {
                opacity: 0.4;
                cursor: not-allowed;
                transform: none;
            }

            &--prev:not(:disabled):hover {
                padding-left: vars.$spacing-xs;
            }

            &--next:not(:disabled):hover {
                padding-right: vars.$spacing-xs;
            }
        }

        &__btn-text {
            @include mix.responsive(mobile) {
                display: none;
            }
        }

        &__info {
            display: flex;
            align-items: center;
            margin-left: vars.$spacing-md;
            padding-left: vars.$spacing-md;
            border-left: 1px solid func.color-alpha(vars.$gray-light, 0.5);

            @include mix.responsive(mobile) {
                width: 100%;
                justify-content: center;
                margin-left: 0;
                margin-top: vars.$spacing-xs;
                padding-left: 0;
                border-left: none;
            }
        }

        &__info-text {
            color: vars.$text-secondary;

            strong {
                color: vars.$text-primary;
                font-weight: 600;
            }
        }

        &--sm {
            .pagination__btn {
                height: 32px;
                padding: 0 vars.$spacing-xs;
            }
        }

        &--lg {
            .pagination__btn {
                height: 48px;
                padding: 0 vars.$spacing-lg;
            }
        }

        &--rounded {
            .pagination__btn {
                border-radius: vars.$border-radius-full;
            }
        }

        &--minimal {
            .pagination__btn {
                background: transparent;

                &:hover:not(:disabled) {
                    background: func.color-alpha(vars.$gray-light, 0.5);
                }
            }
        }
    }
</style>
