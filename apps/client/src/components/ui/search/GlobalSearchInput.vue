<template>
    <SearchInput
        ref="searchInputRef"
        :model-value="modelValue"
        :placeholder="placeholder"
        :compact="compact"
        :loading="loading"
        :is-expanded="isExpanded"
        shortcut="K"
        @update:model-value="$emit('update:modelValue', $event)"
        @focus="$emit('focus')"
        @clear="$emit('clear')"
        @keydown="$emit('keydown', $event)"
    />
</template>

<script setup lang="ts">
    import { ref } from 'vue';

    import SearchInput from './SearchInput.vue';

    import type { GlobalSearchInputProps } from '@/types/components/ui';

    withDefaults(defineProps<GlobalSearchInputProps>(), {
        placeholder: 'Rechercher...',
        compact: false,
        loading: false,
        isExpanded: false,
    });

    defineEmits<{
        'update:modelValue': [value: string];
        focus: [];
        clear: [];
        keydown: [event: KeyboardEvent];
    }>();

    const searchInputRef = ref<InstanceType<typeof SearchInput> | null>(null);

    const focus = () => searchInputRef.value?.focus();
    const blur = () => searchInputRef.value?.blur();

    defineExpose({ focus, blur });
</script>

<style scoped>
    /* Styles inherited from SearchInput */
</style>
