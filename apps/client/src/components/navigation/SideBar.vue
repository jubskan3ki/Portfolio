<template>
    <aside :class="sidebarClasses" role="navigation" :aria-label="ariaLabel">
        <header v-if="$slots.header" class="sidebar__header">
            <slot name="header"></slot>
        </header>

        <button
            v-if="collapsible"
            :class="toggleButtonClasses"
            :aria-label="isCollapsed ? 'Déplier le menu' : 'Replier le menu'"
            :aria-expanded="!isCollapsed"
            @click="toggleCollapse"
        >
            <BaseIcon :name="isCollapsed ? 'chevrons-right' : 'chevrons-left'" :size="14" />
        </button>

        <nav class="sidebar__nav">
            <template v-if="sections.length > 0">
                <div v-for="(section, sectionIndex) in sections" :key="sectionIndex" class="sidebar__section">
                    <Transition name="fade">
                        <h6 v-if="section.title && !isCollapsed" class="sidebar__section-title">
                            <span class="sidebar__section-dot" aria-hidden="true"></span>
                            {{ section.title }}
                        </h6>
                    </Transition>

                    <ul class="sidebar__list" role="menu">
                        <SideBarItem
                            v-for="item in section.items"
                            :key="item.to"
                            :text="item.text"
                            :to="item.to"
                            :icon="item.icon"
                            :badge="item.badge"
                            :is-collapsed="isCollapsed"
                        />
                    </ul>
                </div>
            </template>

            <slot v-else></slot>
        </nav>

        <footer v-if="$slots.footer" class="sidebar__footer">
            <slot name="footer"></slot>
        </footer>
    </aside>
</template>

<script setup lang="ts">
    import { computed, ref } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import SideBarItem from '@/components/navigation/SideBarItem.vue';

    import type { SideBarProps } from '@/types/components/navigation';

    type Props = SideBarProps;

    const props = withDefaults(defineProps<Props>(), {
        sections: () => [],
        variant: 'light',
        collapsible: false,
        defaultCollapsed: false,
        ariaLabel: 'Menu latéral',
        customClass: '',
    });

    const emit = defineEmits<{
        collapse: [];
        expand: [];
        'update:collapsed': [value: boolean];
    }>();

    const isCollapsed = ref(props.defaultCollapsed);

    const sidebarClasses = computed(() => [
        'sidebar',
        `sidebar--${props.variant}`,
        {
            'sidebar--collapsed': isCollapsed.value,
            'sidebar--collapsible': props.collapsible,
        },
        props.customClass,
    ]);

    const toggleButtonClasses = computed(() => [
        'sidebar__toggle',
        { 'sidebar__toggle--collapsed': isCollapsed.value },
    ]);

    const toggleCollapse = () => {
        isCollapsed.value = !isCollapsed.value;
        if (isCollapsed.value) {
            emit('collapse');
        } else {
            emit('expand');
        }
        emit('update:collapsed', isCollapsed.value);
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .sidebar {
        position: relative;
        display: flex;
        flex-direction: column;
        height: 100%;
        width: 260px;
        transition: width 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);

        &--collapsed {
            width: 72px;

            .sidebar__section-title {
                opacity: 0;
                visibility: hidden;
            }
        }

        &__header {
            padding: vars.$spacing-lg;
            border-bottom: 1px solid;
        }

        &__toggle {
            position: absolute;
            top: vars.$spacing-xl;
            right: -14px;
            z-index: 10;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 28px;
            height: 28px;
            border: none;
            border-radius: vars.$border-radius-full;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
            box-shadow: vars.$box-shadow-medium;

            &:hover {
                transform: scale(1.1);
            }

            &:focus-visible {
                outline: 2px solid vars.$primary-color;
                outline-offset: 2px;
            }

            &--collapsed {
                transform: rotate(180deg);

                &:hover {
                    transform: rotate(180deg) scale(1.1);
                }
            }
        }

        &__nav {
            flex: 1;
            overflow-y: auto;
            overflow-x: hidden;
            padding: vars.$spacing-md 0;

            &::-webkit-scrollbar {
                width: 4px;
            }

            &::-webkit-scrollbar-track {
                background: transparent;
            }

            &::-webkit-scrollbar-thumb {
                background: func.color-alpha(vars.$gray, 0.3);
                border-radius: vars.$border-radius-full;
            }
        }

        &__section {
            margin-bottom: vars.$spacing-lg;

            &:last-child {
                margin-bottom: 0;
            }
        }

        &__section-title {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xxs;
            padding: 0 vars.$spacing-lg;
            margin-bottom: vars.$spacing-xs;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            transition: all 0.3s ease;
        }

        &__section-dot {
            width: 4px;
            height: 4px;
            border-radius: 50%;
            background: currentcolor;
            opacity: 0.5;
        }

        &__list {
            list-style: none;
            margin: 0;
            padding: 0;
        }

        &__footer {
            padding: vars.$spacing-lg;
            border-top: 1px solid;
        }

        &--light {
            background: vars.$white;
            border-right: 1px solid func.color-alpha(vars.$gray-light, 0.5);

            .sidebar__header {
                border-bottom-color: func.color-alpha(vars.$gray-light, 0.5);
            }

            .sidebar__section-title {
                color: vars.$text-secondary;
            }

            .sidebar__toggle {
                background: vars.$white;
                color: vars.$text-secondary;
                border: 1px solid func.color-alpha(vars.$gray-light, 0.5);

                &:hover {
                    background: func.color-alpha(vars.$primary-color, 0.1);
                    color: vars.$primary-color;
                    border-color: vars.$primary-color;
                }
            }

            .sidebar__footer {
                border-top-color: func.color-alpha(vars.$gray-light, 0.5);
            }
        }

        &--dark {
            background: vars.$black-light;

            .sidebar__header {
                border-bottom-color: func.color-alpha(vars.$white, 0.1);
            }

            .sidebar__section-title {
                color: func.color-alpha(vars.$white, 0.6);
            }

            .sidebar__toggle {
                background: vars.$black-light;
                color: vars.$white;
                border: 1px solid func.color-alpha(vars.$white, 0.2);

                &:hover {
                    background: func.color-alpha(vars.$primary-color, 0.2);
                    color: vars.$primary-color;
                    border-color: vars.$primary-color;
                }
            }

            .sidebar__footer {
                border-top-color: func.color-alpha(vars.$white, 0.1);
            }
        }

        &--glass {
            background: func.color-alpha(vars.$white, 0.8);
            backdrop-filter: blur(20px);
            border-right: 1px solid func.color-alpha(vars.$white, 0.3);

            .sidebar__header {
                border-bottom-color: func.color-alpha(vars.$gray-light, 0.3);
            }

            .sidebar__section-title {
                color: vars.$text-secondary;
            }

            .sidebar__toggle {
                background: func.color-alpha(vars.$white, 0.9);
                color: vars.$text-secondary;
                border: 1px solid func.color-alpha(vars.$gray-light, 0.3);
                backdrop-filter: blur(10px);

                &:hover {
                    background: vars.$white;
                    color: vars.$primary-color;
                    border-color: vars.$primary-color;
                }
            }

            .sidebar__footer {
                border-top-color: func.color-alpha(vars.$gray-light, 0.3);
            }
        }
    }

    .fade-enter-active,
    .fade-leave-active {
        transition: opacity 0.2s ease;
    }

    .fade-enter-from,
    .fade-leave-to {
        opacity: 0;
    }
</style>
