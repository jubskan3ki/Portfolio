<template>
    <div :class="tabsClasses" role="tablist" :aria-orientation="vertical ? 'vertical' : 'horizontal'">
        <div ref="navRef" :class="navClasses">
            <TabsItem
                v-for="tab in tabs"
                :id="tab.id"
                :key="`tab-${tab.id}`"
                :tabs-id="tabsId"
                :is-active="activeTab === tab.id"
                is-tab
                :label="tab.label"
                :icon="tab.icon"
                :disabled="tab.disabled"
                :badge="tab.badge"
                @select="setActiveTab(tab.id)"
            />

            <div
                v-if="!vertical && showIndicator"
                class="tabs__indicator"
                :style="indicatorStyle"
                aria-hidden="true"
            ></div>
        </div>

        <div class="tabs__panels">
            <Transition :name="animated ? 'tab-fade' : undefined" mode="out-in">
                <TabsItem
                    v-if="activeTabData"
                    :id="activeTabData.id"
                    :key="`panel-${activeTabData.id}`"
                    :tabs-id="tabsId"
                    is-active
                >
                    <slot :name="`tab-${activeTabIndex}`">
                        <!-- Using v-text for XSS safety - use slot for rich content -->
                        <div v-if="activeTabData.content" v-text="activeTabData.content"></div>
                    </slot>
                </TabsItem>
            </Transition>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { computed, nextTick, onBeforeUnmount, onMounted, ref, useId, watch } from 'vue';

    import TabsItem from '@/components/navigation/TabsItem.vue';

    import type { TabsProps } from '@/types/components/navigation';

    type Props = TabsProps;

    const props = withDefaults(defineProps<Props>(), {
        modelValue: '',
        tabs: () => [],
        variant: 'default',
        vertical: false,
        align: 'left',
        scrollable: false,
        fullWidth: false,
        showIndicator: true,
        animated: true,
        customClass: '',
    });

    const emit = defineEmits<{
        'update:modelValue': [value: string | number];
        tabChange: [id: string | number];
    }>();

    const id = useId();
    const navRef = ref<HTMLElement | null>(null);
    const indicatorStyle = ref({ width: '0px', transform: 'translateX(0px)' });

    const tabsId = computed(() => {
        if (props.tabs.length > 0) {
            return `tabs-${id}`;
        }
        return 'default-tabs';
    });

    const tabsClasses = computed(() => [
        'tabs',
        `tabs--${props.variant}`,
        {
            'tabs--vertical': props.vertical,
            'tabs--animated': props.animated,
        },
        props.customClass,
    ]);

    const navClasses = computed(() => [
        'tabs__nav',
        `tabs__nav--${props.align}`,
        {
            'tabs__nav--scrollable': props.scrollable,
            'tabs__nav--full-width': props.fullWidth,
        },
    ]);

    const getDefaultActiveTab = () => {
        if (props.tabs.length === 0) {
            return '';
        }
        const firstEnabledTab = props.tabs.find((tab) => !tab.disabled);
        const firstTab = props.tabs[0];
        return firstEnabledTab ? firstEnabledTab.id : (firstTab?.id ?? '');
    };

    const activeTab = ref(props.modelValue || getDefaultActiveTab());

    const activeTabIndex = computed(() => props.tabs.findIndex((tab) => tab.id === activeTab.value));

    const activeTabData = computed(() => props.tabs.find((tab) => tab.id === activeTab.value));

    const setActiveTab = (tabId: string | number) => {
        const tab = props.tabs.find((t) => t.id === tabId);
        if (tab?.disabled) {
            return;
        }

        activeTab.value = tabId;
        emit('update:modelValue', tabId);
        emit('tabChange', tabId);
        updateIndicator();
    };

    const updateIndicator = async () => {
        if (props.vertical || !props.showIndicator || !navRef.value) {
            return;
        }

        await nextTick();
        const tabElements = navRef.value.querySelectorAll('.tabs-item__tab');
        const activeIndex = props.tabs.findIndex((tab) => tab.id === activeTab.value);

        if (activeIndex === -1) {
            return;
        }

        const activeTabElement = tabElements[activeIndex] as HTMLElement;
        if (activeTabElement) {
            indicatorStyle.value = {
                width: `${activeTabElement.offsetWidth}px`,
                transform: `translateX(${activeTabElement.offsetLeft}px)`,
            };
        }
    };

    watch(
        () => props.modelValue,
        (newValue) => {
            if (newValue !== activeTab.value) {
                activeTab.value = newValue;
                updateIndicator();
            }
        },
    );

    watch(
        () => props.tabs,
        async () => {
            await nextTick();
            updateIndicator();
        },
        { deep: true },
    );

    onMounted(async () => {
        await nextTick();
        updateIndicator();
        window.addEventListener('resize', updateIndicator);
    });

    onBeforeUnmount(() => {
        window.removeEventListener('resize', updateIndicator);
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .tabs {
        display: flex;
        flex-direction: column;
        width: 100%;

        &--vertical {
            flex-direction: row;

            .tabs__nav {
                flex-direction: column;
                width: 220px;
                flex-shrink: 0;
                border-right: 1px solid func.color-alpha(vars.$gray-light, 0.5);
                border-bottom: none;
                padding-right: vars.$spacing-md;
                gap: vars.$spacing-xxxs;
            }

            .tabs__panels {
                flex: 1;
                padding-left: vars.$spacing-lg;
            }
        }

        &__nav {
            position: relative;
            display: flex;
            gap: vars.$spacing-xxxs;
            border-bottom: 1px solid func.color-alpha(vars.$gray-light, 0.5);
            padding-bottom: vars.$spacing-xxs;

            &--center {
                justify-content: center;
            }

            &--right {
                justify-content: flex-end;
            }

            &--scrollable {
                overflow-x: auto;
                scroll-behavior: smooth;
                -webkit-overflow-scrolling: touch;
                scrollbar-width: none;

                &::-webkit-scrollbar {
                    display: none;
                }
            }

            &--full-width {
                :deep(.tabs-item__tab) {
                    flex: 1;
                }
            }
        }

        &__indicator {
            position: absolute;
            bottom: 0;
            height: 2px;
            background: vars.$primary-color;
            border-radius: vars.$border-radius-full;
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        }

        &__panels {
            flex: 1;
            position: relative;
            padding-top: vars.$spacing-md;
        }

        // Variants
        &--outline {
            .tabs__nav {
                border-bottom: none;
                gap: vars.$spacing-xxs;
            }

            :deep(.tabs-item__tab) {
                border: 1px solid func.color-alpha(vars.$gray-light, 0.5);
                border-radius: vars.$border-radius-lg;
            }

            :deep(.tabs-item__tab--active) {
                border-color: vars.$primary-color;
                background: func.color-alpha(vars.$primary-color, 0.05);
            }
        }

        &--pills {
            .tabs__nav {
                border-bottom: none;
                gap: vars.$spacing-xxs;
                background: func.color-alpha(vars.$gray-light, 0.3);
                padding: vars.$spacing-xxxs;
                border-radius: vars.$border-radius-lg;
            }

            :deep(.tabs-item__tab) {
                border-radius: vars.$border-radius-md;
            }

            :deep(.tabs-item__tab--active) {
                background: vars.$white;
                box-shadow: vars.$box-shadow-medium;
            }
        }

        &--segmented {
            .tabs__nav {
                border-bottom: none;
                background: func.color-alpha(vars.$gray-light, 0.4);
                padding: 4px;
                border-radius: vars.$border-radius-lg;
                gap: 0;
            }

            :deep(.tabs-item__tab) {
                border-radius: vars.$border-radius-md;
            }

            :deep(.tabs-item__tab--active) {
                background: vars.$white;
                box-shadow: 0 1px 3px func.color-alpha(vars.$black, 0.1);
            }
        }

        &--underlined {
            .tabs__indicator {
                height: 3px;
            }

            :deep(.tabs-item__tab--active) {
                font-weight: 600;
            }
        }
    }

    // Tab transition
    .tab-fade-enter-active,
    .tab-fade-leave-active {
        transition: all 0.2s ease;
    }

    .tab-fade-enter-from {
        opacity: 0;
        transform: translateY(10px);
    }

    .tab-fade-leave-to {
        opacity: 0;
        transform: translateY(-10px);
    }
</style>
