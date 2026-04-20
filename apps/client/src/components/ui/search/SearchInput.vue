<template>
    <div class="search-input">
        <BaseIcon name="search" :size="compact ? 14 : 16" class="search-input__icon" />
        <input
            ref="inputRef"
            :value="modelValue"
            type="search"
            :placeholder="placeholder"
            class="search-input__field"
            role="combobox"
            autocomplete="off"
            aria-haspopup="listbox"
            :aria-expanded="isExpanded"
            aria-label="Recherche globale"
            @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
            @focus="$emit('focus')"
            @keydown="$emit('keydown', $event)"
        />
        <Spinner v-if="loading" size="sm" class="search-input__loader" />
        <button
            v-else-if="modelValue"
            type="button"
            class="search-input__clear"
            aria-label="Effacer"
            @click="$emit('clear')"
        >
            <BaseIcon name="x" :size="14" />
        </button>
        <kbd v-else-if="shortcut" class="search-input__shortcut">
            <span>Alt</span>
            <span>{{ shortcut }}</span>
        </kbd>
    </div>
</template>

<script setup lang="ts">
    import { ref, onMounted, onUnmounted } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import Spinner from '@/components/loaders/Spinner.vue';

    import type { SearchInputProps } from '@/types/components/ui';

    const props = withDefaults(defineProps<SearchInputProps>(), {
        placeholder: 'Rechercher...',
        compact: false,
        loading: false,
        isExpanded: false,
        shortcut: undefined,
    });

    defineEmits<{
        'update:modelValue': [value: string];
        focus: [];
        clear: [];
        keydown: [event: KeyboardEvent];
    }>();

    const inputRef = ref<HTMLInputElement | null>(null);

    const focus = () => inputRef.value?.focus();
    const blur = () => inputRef.value?.blur();

    // Keyboard shortcut handler
    const handleKeydown = (event: KeyboardEvent) => {
        if (!props.shortcut) {
            return;
        }

        // Check if Alt key is pressed with the shortcut key
        if (event.altKey && event.key.toLowerCase() === props.shortcut.toLowerCase()) {
            event.preventDefault();
            focus();
        }
    };

    onMounted(() => {
        if (props.shortcut) {
            window.addEventListener('keydown', handleKeydown);
        }
    });

    onUnmounted(() => {
        if (props.shortcut) {
            window.removeEventListener('keydown', handleKeydown);
        }
    });

    defineExpose({ focus, blur });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as v;
    @use '@/styles/abstracts/functions' as fn;

    .search-input {
        position: relative;
        display: flex;
        align-items: center;
        width: 100%;

        :deep(.search-input__icon) {
            position: absolute;
            left: v.$spacing-xs;
            top: 50%;
            transform: translateY(-50%);
            color: v.$text-muted;
            pointer-events: none;
            transition: color v.$transition-fast;
        }

        &__field {
            width: 100%;
            height: 44px;
            padding: 0 v.$spacing-xxxl 0 38px;
            border: 1px solid;
            border-color: v.$border-color;
            border-radius: v.$border-radius-md;
            background-color: v.$white;
            color: v.$text-primary;
            font-family: v.$font-family;
            transition: all v.$transition-fast;

            &::-webkit-search-cancel-button,
            &::-webkit-search-decoration {
                -webkit-appearance: none;
                display: none;
            }

            &::placeholder {
                color: v.$text-muted;
            }

            &:hover:not(:focus) {
                border-color: v.$border-color;
            }

            &:focus {
                outline: none;
                border-color: v.$primary-color;
                box-shadow: 0 0 0 3px fn.color-alpha(v.$primary-color, 0.1);
            }
        }

        &:focus-within :deep(.search-input__icon) {
            color: v.$primary-color;
        }

        &__loader {
            position: absolute;
            right: v.$spacing-xs;
            top: 50%;
            transform: translateY(-50%);
        }

        &__clear {
            position: absolute;
            right: v.$spacing-xxs;
            top: 50%;
            transform: translateY(-50%);
            display: flex;
            align-items: center;
            justify-content: center;
            width: 28px;
            height: 28px;
            padding: 0;
            border: none;
            border-radius: v.$border-radius-md;
            background: transparent;
            color: v.$text-muted;
            cursor: pointer;
            transition: all v.$transition-fast;

            &:hover {
                background: v.$bg-secondary;
                color: v.$text-primary;
            }
        }

        &__shortcut {
            position: absolute;
            right: v.$spacing-xs;
            top: 50%;
            transform: translateY(-50%);
            display: flex;
            align-items: center;
            gap: v.$spacing-xxxs;
            pointer-events: none;

            span {
                display: flex;
                align-items: center;
                justify-content: center;
                height: 20px;
                min-width: 20px;
                padding: 0 v.$spacing-xxs;
                border: 1px solid v.$border-color;
                border-radius: v.$border-radius-sm;
                background: v.$bg-secondary;
                color: v.$text-muted;
                font-weight: v.$font-weight-medium;
            }
        }
    }
</style>
