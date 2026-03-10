<template>
    <div class="navigation-tabs" :class="[`navigation-tabs--${variant}`, customClass]">
        <div
            ref="trackRef"
            class="navigation-tabs__track"
            :class="{ 'navigation-tabs__track--ready': indicatorReady }"
            role="tablist"
        >
            <button
                v-for="(tab, index) in tabs"
                :id="`tab-${tab.key}`"
                :key="tab.key"
                :ref="(el) => setTabRef(index, el as HTMLButtonElement)"
                type="button"
                role="tab"
                class="navigation-tabs__btn"
                :class="{ 'navigation-tabs__btn--active': modelValue === tab.key }"
                :aria-selected="modelValue === tab.key"
                :aria-controls="`panel-${tab.key}`"
                :tabindex="modelValue === tab.key ? 0 : -1"
                @click="handleTabClick(tab.key)"
                @keydown="handleKeydown($event, index)"
            >
                <BaseIcon v-if="tab.icon" :name="tab.icon" :size="iconSize" />
                <span class="navigation-tabs__label">{{ tab.label }}</span>
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { computed, nextTick, ref } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import { useTabIndicator } from '@/composables/ui/useTabIndicator';

    interface Tab {
        key: string;
        label: string;
        icon?: string;
    }

    interface Props {
        tabs: Tab[];
        modelValue: string;
        variant?: 'default' | 'glass' | 'minimal';
        iconSize?: number;
        customClass?: string;
    }

    const props = withDefaults(defineProps<Props>(), {
        variant: 'glass',
        iconSize: 14,
        customClass: '',
    });

    const emit = defineEmits<{
        'update:modelValue': [value: string];
    }>();

    const trackRef = ref<HTMLElement | null>(null);
    const tabRefs = ref<Array<HTMLButtonElement | null>>([]);
    const activeIndex = computed(() => props.tabs.findIndex((t) => t.key === props.modelValue));

    const { setTabRef, indicatorReady } = useTabIndicator({
        trackRef,
        tabRefs,
        activeIndex,
        tabs: () => props.tabs,
        mode: 'css-vars',
    });

    const handleTabClick = (key: string) => {
        emit('update:modelValue', key);
    };

    const handleKeydown = (event: KeyboardEvent, currentIndex: number) => {
        const tabCount = props.tabs.length;
        let newIndex = currentIndex;

        switch (event.key) {
            case 'ArrowLeft':
                event.preventDefault();
                newIndex = currentIndex === 0 ? tabCount - 1 : currentIndex - 1;
                break;
            case 'ArrowRight':
                event.preventDefault();
                newIndex = currentIndex === tabCount - 1 ? 0 : currentIndex + 1;
                break;
            case 'Home':
                event.preventDefault();
                newIndex = 0;
                break;
            case 'End':
                event.preventDefault();
                newIndex = tabCount - 1;
                break;
            default:
                return;
        }

        const newTab = props.tabs[newIndex];
        if (newTab) {
            emit('update:modelValue', newTab.key);
            nextTick(() => tabRefs.value[newIndex]?.focus());
        }
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as fn;
    @use '@/styles/abstracts/mixins' as mix;

    .navigation-tabs {
        display: inline-flex;
        max-width: 100%;
        overflow-x: auto;
        overflow-y: hidden;
        scrollbar-width: none;

        &::-webkit-scrollbar {
            display: none;
        }

        &__track {
            --indicator-left: 0;
            --indicator-width: 0;

            position: relative;
            display: flex;
            gap: vars.$spacing-xxxxs;

            &::before {
                opacity: 0;
                transition: opacity 0.2s ease;
            }

            &--ready::before {
                opacity: 1;
            }
        }

        &__btn {
            position: relative;
            z-index: 1;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: vars.$spacing-xs;
            background: transparent;
            border: none;
            cursor: pointer;
            transition:
                color 0.2s ease,
                transform 0.15s ease;
            white-space: nowrap;

            &:focus-visible {
                outline: 2px solid vars.$primary-color;
                outline-offset: 2px;
                border-radius: vars.$border-radius-md;
            }
        }

        &__label {
            font-weight: vars.$font-weight-medium;
        }

        // Glass variant (default for page navigation)
        &--glass {
            padding: vars.$spacing-xxs;
            background: fn.color-alpha(vars.$white, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid fn.color-alpha(vars.$white, 0.8);
            border-radius: vars.$border-radius-xl;
            box-shadow:
                0 4px 24px fn.color-alpha(vars.$black, 0.06),
                0 1px 0 fn.color-alpha(vars.$white, 0.8) inset;

            .navigation-tabs__track {
                padding: 0;
                background: transparent;

                &::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: var(--indicator-left);
                    width: var(--indicator-width);
                    height: 100%;
                    background: linear-gradient(135deg, vars.$primary-color, vars.$primary-dark);
                    border-radius: vars.$border-radius-lg;
                    box-shadow: 0 4px 16px fn.color-alpha(vars.$primary-color, 0.35);
                    transition:
                        left 0.25s cubic-bezier(0.4, 0, 0.2, 1),
                        width 0.25s cubic-bezier(0.4, 0, 0.2, 1);
                    z-index: 0;
                }
            }

            .navigation-tabs__btn {
                padding: vars.$spacing-xs vars.$spacing-lg;
                color: vars.$text-secondary;
                border-radius: vars.$border-radius-lg;

                &:hover:not(.navigation-tabs__btn--active) {
                    color: vars.$text-inverted;
                }

                &--active {
                    color: vars.$white;
                }
            }
        }

        // Default variant
        &--default {
            .navigation-tabs__track {
                background: vars.$bg-secondary;
                border-radius: vars.$border-radius-md;
                padding: vars.$spacing-xxxs;

                &::before {
                    content: '';
                    position: absolute;
                    top: vars.$spacing-xxxs;
                    left: var(--indicator-left);
                    width: var(--indicator-width);
                    height: calc(100% - vars.$spacing-xxxs * 2);
                    background: vars.$white;
                    border-radius: vars.$border-radius-md;
                    box-shadow:
                        0 1px 3px fn.color-alpha(vars.$black, 0.1),
                        0 1px 2px fn.color-alpha(vars.$black, 0.06);
                    transition:
                        left 0.25s cubic-bezier(0.4, 0, 0.2, 1),
                        width 0.25s cubic-bezier(0.4, 0, 0.2, 1);
                    z-index: 0;
                }
            }

            .navigation-tabs__btn {
                padding: vars.$spacing-xxs vars.$spacing-xs;
                color: vars.$text-muted;
                border-radius: vars.$border-radius-md;

                &:hover {
                    color: vars.$text-inverted;
                }

                &--active {
                    color: vars.$text-inverted;
                }
            }
        }

        // Minimal variant
        &--minimal {
            .navigation-tabs__track {
                gap: vars.$spacing-md;
                border-bottom: 1px solid vars.$border-color;

                &::before {
                    content: '';
                    position: absolute;
                    bottom: -1px;
                    left: var(--indicator-left);
                    width: var(--indicator-width);
                    height: 2px;
                    background: vars.$primary-color;
                    border-radius: vars.$border-radius-sm;
                    transition:
                        left 0.25s cubic-bezier(0.4, 0, 0.2, 1),
                        width 0.25s cubic-bezier(0.4, 0, 0.2, 1);
                    z-index: 0;
                }
            }

            .navigation-tabs__btn {
                padding: vars.$spacing-sm vars.$spacing-xs;
                color: vars.$text-muted;

                &:hover:not(.navigation-tabs__btn--active) {
                    color: vars.$text-inverted;
                }

                &--active {
                    color: vars.$primary-color;
                }
            }
        }
    }

    // Responsive
    @include mix.responsive(tablet) {
        .navigation-tabs--glass {
            .navigation-tabs__btn {
                padding: vars.$spacing-xs vars.$spacing-md;
            }
        }
    }

    @include mix.responsive(mobile) {
        .navigation-tabs {
            width: 100%;

            &__label {
                font-size: vars.$font-size-sm;
            }
        }

        .navigation-tabs--glass {
            .navigation-tabs__btn {
                padding: vars.$spacing-xxs vars.$spacing-sm;
            }
        }
    }
</style>
