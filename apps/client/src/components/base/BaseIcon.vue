<template>
    <component
        :is="lucideComponent"
        v-if="lucideComponent"
        v-bind="$attrs"
        :size="numericSize"
        :stroke-width="strokeWidth"
        :class="iconClasses"
        :style="iconStyle"
        :aria-label="ariaLabel || name"
        aria-hidden="true"
    />
</template>

<script setup lang="ts">
    import { computed, defineAsyncComponent, type Component, type CSSProperties } from 'vue';

    import { ICON_ALIASES, ICON_REGISTRY } from '@/config/icons';

    import type { IconProps, Size } from '@/types/components/base';

    type Props = IconProps;
    type SizePreset = Size;

    const props = withDefaults(defineProps<Props>(), {
        size: 24,
        color: undefined,
        strokeWidth: 2,
        customClass: '',
        ariaLabel: '',
    });

    const DEFAULT_SIZE = 24;

    const SIZE_MAP: Record<SizePreset, number> = {
        xs: 12,
        sm: 16,
        md: 20,
        lg: 24,
        xl: 32,
        '': 40,
    };

    const parseSize = (size: number | string): number => {
        if (typeof size === 'number') {
            return size;
        }
        const mapped = SIZE_MAP[size as SizePreset];
        if (mapped !== undefined) {
            return mapped;
        }
        const parsed = parseInt(size, 10);
        return Number.isNaN(parsed) ? DEFAULT_SIZE : parsed;
    };

    const numericSize = computed(() => parseSize(props.size));

    const iconClasses = computed(() => {
        const classes = ['base-icon'];
        if (props.customClass) {
            classes.push(props.customClass);
        }
        return classes;
    });

    const toPascalCase = (str: string): string =>
        str
            .split('-')
            .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
            .join('');

    const asyncCache = new Map<string, Component>();

    const resolveKey = (name: string): string | null => {
        const aliasKey = ICON_ALIASES[name];
        if (aliasKey && aliasKey in ICON_REGISTRY) {
            return aliasKey;
        }
        const pascal = toPascalCase(name);
        if (pascal in ICON_REGISTRY) {
            return pascal;
        }
        if (name in ICON_REGISTRY) {
            return name;
        }
        return null;
    };

    const getAsyncIcon = (key: string): Component | null => {
        const cached = asyncCache.get(key);
        if (cached) {
            return cached;
        }
        const loader = ICON_REGISTRY[key];
        if (!loader) {
            return null;
        }
        const comp = defineAsyncComponent(loader);
        asyncCache.set(key, comp);
        return comp;
    };

    const lucideComponent = computed<Component | null>(() => {
        const key = resolveKey(props.name);
        if (key) {
            return getAsyncIcon(key);
        }

        if (import.meta.dev) {
            console.warn(`[BaseIcon] Icon "${props.name}" not found | check src/config/icons.ts`);
        }
        return getAsyncIcon('Info');
    });

    const iconStyle = computed<CSSProperties>(() => ({
        color: props.color || undefined,
    }));
</script>

<style lang="scss" scoped>
    .base-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        vertical-align: middle;
    }
</style>
