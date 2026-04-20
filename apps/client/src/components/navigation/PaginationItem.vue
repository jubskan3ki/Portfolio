<template>
    <li :class="itemClasses">
        <button
            v-if="!isEllipsis"
            :class="buttonClasses"
            :aria-current="isActive ? 'page' : undefined"
            :aria-label="`Aller à la page ${page}`"
            @click="emit('click')"
        >
            <span class="pagination-item__number">{{ page }}</span>
            <span v-if="isActive" class="pagination-item__indicator" aria-hidden="true"></span>
        </button>
        <span v-else class="pagination-item__ellipsis" aria-hidden="true">
            <span class="pagination-item__dot"></span>
            <span class="pagination-item__dot"></span>
            <span class="pagination-item__dot"></span>
        </span>
    </li>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import type { PaginationItemProps } from '@/types/components/navigation';

    const props = withDefaults(defineProps<PaginationItemProps>(), {
        isActive: false,
        isEllipsis: false,
    });

    const emit = defineEmits<{
        click: [];
    }>();

    const itemClasses = computed(() => [
        'pagination-item',
        {
            'pagination-item--ellipsis': props.isEllipsis,
            'pagination-item--active': props.isActive,
        },
    ]);

    const buttonClasses = computed(() => ['pagination-item__btn', { 'pagination-item__btn--active': props.isActive }]);
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .pagination-item {
        list-style: none;

        &__btn {
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            min-width: 40px;
            height: 40px;
            padding: 0 vars.$spacing-xxs;
            border: none;
            border-radius: vars.$border-radius-lg;
            background: transparent;
            color: vars.$text-secondary;
            font-weight: 500;
            cursor: pointer;
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);

            &::before {
                content: '';
                position: absolute;
                inset: 0;
                background: func.color-alpha(vars.$gray-light, 0);
                border-radius: inherit;
                transition: background 0.3s ease;
                z-index: -1;
            }

            &:hover {
                color: vars.$text-primary;
                transform: translateY(-2px);

                &::before {
                    background: func.color-alpha(vars.$gray-light, 0.5);
                }
            }

            &:focus-visible {
                outline: 2px solid vars.$primary-color;
                outline-offset: 2px;
            }

            &--active {
                color: vars.$white;

                &::before {
                    background: vars.$primary-color;
                }

                &:hover {
                    transform: translateY(-2px) scale(1.05);

                    &::before {
                        background: vars.$primary-dark;
                    }
                }
            }
        }

        &__number {
            position: relative;
            z-index: 1;
        }

        &__indicator {
            position: absolute;
            bottom: 4px;
            left: 50%;
            transform: translateX(-50%);
            width: 4px;
            height: 4px;
            background: vars.$white;
            border-radius: 50%;
            opacity: 0.8;
        }

        &__ellipsis {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 3px;
            min-width: 40px;
            height: 40px;
            color: vars.$text-secondary;
        }

        &__dot {
            width: 3px;
            height: 3px;
            border-radius: 50%;
            background: currentcolor;
            opacity: 0.5;
            animation: dot-bounce 1.5s ease-in-out infinite;

            &:nth-child(2) {
                animation-delay: 0.1s;
            }

            &:nth-child(3) {
                animation-delay: 0.2s;
            }
        }
    }

    @keyframes dot-bounce {
        0%,
        100% {
            transform: translateY(0);
            opacity: 0.5;
        }

        50% {
            transform: translateY(-2px);
            opacity: 1;
        }
    }
</style>
