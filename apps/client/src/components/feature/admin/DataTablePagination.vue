<template>
    <div class="data-table-pagination">
        <!-- Info -->
        <div class="data-table-pagination__info">
            <small>Affichage {{ startItem }}-{{ endItem }} sur {{ totalItems }}</small>
        </div>

        <!-- Per page selector -->
        <div class="data-table-pagination__per-page">
            <small>Par page:</small>
            <select
                :value="perPage"
                class="data-table-pagination__select"
                aria-label="Elements par page"
                @change="handlePerPageChange"
            >
                <option v-for="option in perPageOptions" :key="option" :value="option">
                    {{ option }}
                </option>
            </select>
        </div>

        <!-- Navigation -->
        <div class="data-table-pagination__nav">
            <BaseButton
                variant="ghost"
                size="icon"
                :disabled="currentPage === 1"
                aria-label="Première page"
                @click="goToPage(1)"
            >
                <template #icon-left>
                    <BaseIcon name="chevrons-left" :size="16" />
                </template>
            </BaseButton>
            <BaseButton
                variant="ghost"
                size="icon"
                :disabled="currentPage === 1"
                aria-label="Page précédente"
                @click="goToPage(currentPage - 1)"
            >
                <template #icon-left>
                    <BaseIcon name="chevron-left" :size="16" />
                </template>
            </BaseButton>

            <!-- Page numbers -->
            <div class="data-table-pagination__pages">
                <button
                    v-for="page in visiblePages"
                    :key="page"
                    class="data-table-pagination__page"
                    :class="{ 'data-table-pagination__page--active': page === currentPage }"
                    :disabled="page === '...'"
                    :aria-label="typeof page === 'number' ? `Page ${page}` : undefined"
                    :aria-current="page === currentPage ? 'page' : undefined"
                    @click="typeof page === 'number' && goToPage(page)"
                >
                    {{ page }}
                </button>
            </div>

            <BaseButton
                variant="ghost"
                size="icon"
                :disabled="currentPage === totalPages"
                aria-label="Page suivante"
                @click="goToPage(currentPage + 1)"
            >
                <template #icon-left>
                    <BaseIcon name="chevron-right" :size="16" />
                </template>
            </BaseButton>
            <BaseButton
                variant="ghost"
                size="icon"
                :disabled="currentPage === totalPages"
                aria-label="Dernière page"
                @click="goToPage(totalPages)"
            >
                <template #icon-left>
                    <BaseIcon name="chevrons-right" :size="16" />
                </template>
            </BaseButton>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import BaseButton from '@/components/base/BaseButton.vue';
    import BaseIcon from '@/components/base/BaseIcon.vue';

    const props = withDefaults(
        defineProps<{
            currentPage: number;
            totalPages: number;
            totalItems: number;
            perPage: number;
            perPageOptions?: number[];
        }>(),
        {
            perPageOptions: () => [10, 25, 50, 100],
        },
    );

    const emit = defineEmits<{
        pageChange: [page: number];
        perPageChange: [perPage: number];
    }>();

    // Computed
    const startItem = computed(() => {
        return (props.currentPage - 1) * props.perPage + 1;
    });

    const endItem = computed(() => {
        return Math.min(props.currentPage * props.perPage, props.totalItems);
    });

    const visiblePages = computed(() => {
        const pages: Array<number | string> = [];
        const total = props.totalPages;
        const current = props.currentPage;
        const delta = 2;

        if (total <= 7) {
            for (let i = 1; i <= total; i++) {
                pages.push(i);
            }
        } else {
            pages.push(1);

            if (current > delta + 2) {
                pages.push('...');
            }

            const start = Math.max(2, current - delta);
            const end = Math.min(total - 1, current + delta);

            for (let i = start; i <= end; i++) {
                pages.push(i);
            }

            if (current < total - delta - 1) {
                pages.push('...');
            }

            pages.push(total);
        }

        return pages;
    });

    // Methods
    const goToPage = (page: number) => {
        if (page >= 1 && page <= props.totalPages && page !== props.currentPage) {
            emit('pageChange', page);
        }
    };

    const handlePerPageChange = (event: Event) => {
        const select = event.target as HTMLSelectElement;
        emit('perPageChange', Number(select.value));
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;

    .data-table-pagination {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: vars.$spacing-md;
        padding: vars.$spacing-md;
        border-top: 1px solid rgba(vars.$admin-border, 0.6);
        flex-wrap: wrap;

        &__info {
            color: vars.$text-secondary;
        }

        &__per-page {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xxs;
            color: vars.$text-secondary;
        }

        &__select {
            padding: vars.$spacing-xxxs vars.$spacing-xs;
            border: 1px solid vars.$admin-border;
            border-radius: vars.$border-radius-sm;
            cursor: pointer;

            &:focus {
                outline: none;
                border-color: vars.$primary-color;
            }
        }

        &__nav {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xxxs;
        }

        &__pages {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xxxs;
        }

        &__page {
            min-width: 32px;
            height: 32px;
            padding: 0 vars.$spacing-xxs;
            background: none;
            border: 1px solid transparent;
            border-radius: vars.$border-radius-sm;
            cursor: pointer;
            color: vars.$text-secondary;
            transition: all vars.$transition-fast;

            &:hover:not(:disabled) {
                border-color: vars.$admin-border;
            }

            &--active {
                background-color: vars.$primary-color;
                color: vars.$white;
                border-color: vars.$primary-color;

                &:hover {
                    border-color: vars.$primary-color;
                }
            }

            &:disabled {
                cursor: default;
            }
        }
    }
</style>
