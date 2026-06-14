<template>
    <nav v-if="items.length > 0" :class="breadcrumbClasses" aria-label="Fil d'Ariane">
        <ol class="breadcrumb__list" itemscope itemtype="https://schema.org/BreadcrumbList">
            <li
                v-for="(item, index) in items"
                :key="item.to ?? item.label"
                class="breadcrumb__item"
                itemprop="itemListElement"
                itemscope
                itemtype="https://schema.org/ListItem"
            >
                <NuxtLink v-if="index < items.length - 1" :to="item.to" class="breadcrumb__link" itemprop="item">
                    <BaseIcon v-if="item.icon" :name="item.icon" :size="14" class="breadcrumb__icon" />
                    <span itemprop="name">{{ item.label }}</span>
                </NuxtLink>

                <span v-else class="breadcrumb__current" aria-current="page" itemprop="item">
                    <BaseIcon v-if="item.icon" :name="item.icon" :size="14" class="breadcrumb__icon" />
                    <span itemprop="name">{{ item.label }}</span>
                </span>

                <meta itemprop="position" :content="String(index + 1)" />

                <!-- Separator rendered via CSS pseudo-element to avoid an inline SVG (saves ~3 DOM nodes per separator). -->
                <span
                    v-if="index < items.length - 1"
                    :class="separatorClass"
                    aria-hidden="true"
                >
                    <slot v-if="$slots.separator" name="separator"></slot>
                </span>
            </li>
        </ol>
    </nav>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';

    import type { BreadcrumbProps } from '@/types/components/navigation';

    type Props = BreadcrumbProps;

    const props = withDefaults(defineProps<Props>(), {
        variant: 'default',
        separator: 'dot',
        customClass: '',
    });

    const breadcrumbClasses = computed(() => ['breadcrumb', `breadcrumb--${props.variant}`, props.customClass]);

    const separatorClass = computed(() => {
        const variant = props.separator ?? 'dot';
        return ['breadcrumb__separator', `breadcrumb__separator--${variant}`];
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .breadcrumb {
        padding: vars.$spacing-xs 0;

        &__list {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: vars.$spacing-xxxs;
            list-style: none;
            margin: 0;
            padding: 0;
        }

        &__item {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xxxs;
            color: vars.$text-secondary;

            &:last-child {
                color: vars.$text-primary;
                font-weight: 500;
            }
        }

        &__link {
            position: relative;
            display: inline-flex;
            align-items: center;
            gap: vars.$spacing-xxxs;
            padding: vars.$spacing-xxxs vars.$spacing-xxs;
            color: vars.$text-secondary;
            text-decoration: none;
            border-radius: vars.$border-radius-sm;
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);

            &::before {
                content: '';
                position: absolute;
                inset: 0;
                background: transparent;
                border-radius: inherit;
                transition: background 0.3s ease;
                z-index: -1;
            }

            &:hover {
                color: vars.$primary-color;

                &::before {
                    background: func.color-alpha(vars.$primary-color, 0.08);
                }

                .breadcrumb__icon {
                    transform: scale(1.1);
                }
            }

            &:focus-visible {
                outline: 2px solid vars.$primary-color;
                outline-offset: 2px;
            }
        }

        &__current {
            display: inline-flex;
            align-items: center;
            gap: vars.$spacing-xxxs;
            padding: vars.$spacing-xxxs vars.$spacing-xxs;
            background: func.color-alpha(vars.$primary-color, 0.1);
            color: vars.$primary-color;
            border-radius: vars.$border-radius-sm;
            font-weight: 500;
        }

        &__separator {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: func.color-alpha(vars.$gray-light, 0.8);
            margin: 0 vars.$spacing-xxxs;
            line-height: 1;

            // Default character separators rendered via ::before - no SVG/path nodes.
            &--chevron::before {
                content: '\203A'; // ›
                font-size: 1.1em;
                line-height: 1;
            }

            &--slash::before {
                content: '/';
                line-height: 1;
            }

            &--arrow::before {
                content: '\2192'; // →
                line-height: 1;
            }

            &--dot::before {
                content: '';
                width: 4px;
                height: 4px;
                border-radius: 50%;
                background: linear-gradient(
                    135deg,
                    vars.$primary-color,
                    func.adjust-color-brightness(vars.$primary-color, 20%)
                );
                opacity: 0.6;
            }
        }

        &__icon {
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.3s ease;
        }

        // Variants
        &--pills {
            .breadcrumb__link {
                background: func.color-alpha(vars.$gray-light, 0.3);
                padding: vars.$spacing-xxs vars.$spacing-xs;

                &:hover {
                    background: func.color-alpha(vars.$primary-color, 0.1);
                }
            }

            .breadcrumb__current {
                background: vars.$primary-color;
                color: vars.$white;
                padding: vars.$spacing-xxs vars.$spacing-xs;
            }
        }

        &--minimal {
            .breadcrumb__link,
            .breadcrumb__current {
                padding: 0;
                background: transparent;
            }

            .breadcrumb__current {
                color: vars.$primary-color;
            }

            .breadcrumb__link:hover::before {
                background: transparent;
            }

            .breadcrumb__link:hover {
                text-decoration: underline;
                text-underline-offset: 3px;
            }
        }

        // Hero variant | tuned for dark/gradient hero backgrounds
        &--hero {
            padding: 0;

            .breadcrumb__list {
                justify-content: center;
            }

            .breadcrumb__item {
                color: func.color-alpha(vars.$white, 0.75);

                &:last-child {
                    color: vars.$white;
                }
            }

            .breadcrumb__link {
                color: func.color-alpha(vars.$white, 0.75);

                &::before {
                    background: transparent;
                }

                &:hover {
                    color: vars.$white;

                    &::before {
                        background: func.color-alpha(vars.$white, 0.12);
                    }
                }

                &:focus-visible {
                    outline-color: func.color-alpha(vars.$white, 0.7);
                }
            }

            .breadcrumb__current {
                background: func.color-alpha(vars.$white, 0.14);
                color: vars.$white;
                border: 1px solid func.color-alpha(vars.$white, 0.2);
            }

            .breadcrumb__separator {
                color: func.color-alpha(vars.$white, 0.4);
            }

            .breadcrumb__separator-dot {
                background: func.color-alpha(vars.$white, 0.5);
                opacity: 0.8;
            }
        }

        // Mobile responsive
        @include mix.responsive(mobile) {
            padding: vars.$spacing-xxs 0;

            &__list {
                gap: 0;
            }

            &__item {
                // Hide middle items on mobile, keep first and last two
                &:not(:nth-last-child(-n + 2), :first-child) {
                    display: none;
                }

                // Ellipsis indicator for hidden items
                &:nth-last-child(2):not(:first-child)::before {
                    content: '';
                    display: flex;
                    align-items: center;
                    gap: 2px;
                    margin-right: vars.$spacing-xxs;

                    &::after {
                        content: '...';
                        color: vars.$text-secondary;
                    }
                }
            }

            &__link,
            &__current {
                padding: vars.$spacing-xxxs;
            }
        }
    }
</style>
