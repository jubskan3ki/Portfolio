<template>
    <div ref="containerRef" :class="multiSelectClasses">
        <label v-if="label" :for="inputId" class="multi-select__label">
            {{ label }}
            <span v-if="required" class="multi-select__required">*</span>
        </label>

        <div class="multi-select__container" @click="focusInput" @keydown.enter="focusInput">
            <div ref="contentRef" class="multi-select__content">
                <TransitionGroup name="tag">
                    <span v-for="item in selectedItems" :key="getItemValue(item)" class="multi-select__tag">
                        <img
                            v-if="showImages && getItemImage(item)"
                            :src="getItemImage(item)"
                            :alt="getItemLabel(item)"
                            class="multi-select__tag-image"
                        />
                        <span class="multi-select__tag-text">{{ getItemLabel(item) }}</span>
                        <button
                            type="button"
                            class="multi-select__tag-remove"
                            :aria-label="`Supprimer ${getItemLabel(item)}`"
                            @mousedown.prevent
                            @click.stop="removeItem(item)"
                        >
                            <svg width="12" height="12" viewBox="0 0 24 24" fill="none">
                                <path
                                    d="M18 6L6 18M6 6L18 18"
                                    stroke="currentColor"
                                    stroke-width="2"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                />
                            </svg>
                        </button>
                    </span>
                </TransitionGroup>

                <input
                    :id="inputId"
                    ref="inputRef"
                    v-model="searchQuery"
                    type="text"
                    class="multi-select__input"
                    :placeholder="selectedItems.length ? '' : placeholder"
                    :disabled="disabled"
                    autocomplete="off"
                    @focus="handleFocus"
                    @blur="handleBlur($event)"
                    @keydown.enter.prevent="selectFirstFiltered"
                    @keydown.backspace="handleBackspace"
                    @keydown.escape="close"
                    @keydown.down.prevent="handleKeyDown"
                    @keydown.up.prevent="handleKeyUp"
                />
            </div>

            <div class="multi-select__actions">
                <button
                    v-if="selectedItems.length > 0"
                    type="button"
                    class="multi-select__clear"
                    aria-label="Tout effacer"
                    @mousedown.prevent
                    @click.stop="clearAll"
                >
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                        <path
                            d="M18 6L6 18M6 6L18 18"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                        />
                    </svg>
                </button>
                <div class="multi-select__arrow" :class="{ 'multi-select__arrow--active': isOpen }">
                    <svg width="12" height="8" viewBox="0 0 12 8" fill="none">
                        <path
                            d="M1 1.5L6 6.5L11 1.5"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                        />
                    </svg>
                </div>
            </div>
        </div>

        <Transition name="dropdown">
            <div v-if="isOpen" class="multi-select__dropdown">
                <div v-if="filteredOptions.length > 0" class="multi-select__options" role="listbox">
                    <button
                        v-for="(option, index) in filteredOptions"
                        :key="getItemValue(option)"
                        type="button"
                        class="multi-select__option"
                        :class="{
                            'multi-select__option--selected': isSelected(option),
                            'multi-select__option--highlighted': highlightedIndex === index,
                        }"
                        role="option"
                        :aria-selected="isSelected(option)"
                        @mousedown.prevent
                        @click="toggleItem(option)"
                        @mouseenter="highlightedIndex = index"
                    >
                        <img
                            v-if="showImages && getItemImage(option)"
                            :src="getItemImage(option)"
                            :alt="getItemLabel(option)"
                            class="multi-select__option-image"
                        />
                        <span class="multi-select__option-text">{{ getItemLabel(option) }}</span>
                        <svg
                            v-if="isSelected(option)"
                            class="multi-select__option-check"
                            width="16"
                            height="16"
                            viewBox="0 0 24 24"
                            fill="none"
                        >
                            <path
                                d="M20 6L9 17L4 12"
                                stroke="currentColor"
                                stroke-width="2"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                            />
                        </svg>
                    </button>
                </div>

                <div v-else class="multi-select__empty-text" @mousedown.prevent>
                    <span v-if="searchQuery">Aucun résultat pour "{{ searchQuery }}"</span>
                    <span v-else>Aucune option disponible</span>
                </div>

                <div v-if="allowCreate" class="multi-select__create-section">
                    <div class="multi-select__create-form">
                        <label :for="`${inputId}-create`" class="sr-only">{{ createPlaceholder }}</label>
                        <input
                            :id="`${inputId}-create`"
                            v-model="createValue"
                            type="text"
                            class="multi-select__create-input"
                            :placeholder="createPlaceholder"
                            @keydown.enter.prevent="handleCreate"
                            @keydown.stop
                        />
                        <button
                            type="button"
                            class="multi-select__create-btn"
                            :disabled="!createValue.trim()"
                            @mousedown.prevent
                            @click="handleCreate"
                        >
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                                <path
                                    d="M12 5v14M5 12h14"
                                    stroke="currentColor"
                                    stroke-width="2"
                                    stroke-linecap="round"
                                />
                            </svg>
                            {{ createLabel }}
                        </button>
                    </div>
                </div>
            </div>
        </Transition>

        <p v-if="error" class="multi-select__message multi-select__message--error">{{ error }}</p>
        <p v-else-if="hint" class="multi-select__message multi-select__message--hint">{{ hint }}</p>
    </div>
</template>

<script setup lang="ts">
    import { computed, nextTick, ref, watch, useId, toRef } from 'vue';

    import { useDropdown } from '@/composables/ui/useDropdown';

    import type { MultiSelectOption, MultiSelectProps } from '@/types/components/base';

    type Props = MultiSelectProps;

    const props = withDefaults(defineProps<Props>(), {
        options: () => [],
        id: '',
        label: '',
        placeholder: 'Rechercher...',
        required: false,
        disabled: false,
        error: '',
        hint: '',
        valueKey: 'value',
        labelKey: 'label',
        imageKey: 'image',
        showImages: false,
        allowCreate: false,
        createLabel: 'Créer',
        createPlaceholder: 'Nouveau...',
        maxItems: undefined,
    });

    const emit = defineEmits<{
        create: [value: string];
    }>();

    const model = defineModel<Array<string | number>>({ default: () => [] });

    const containerRef = ref<HTMLElement | null>(null);
    const contentRef = ref<HTMLElement | null>(null);
    const inputRef = ref<HTMLInputElement | null>(null);
    const searchQuery = ref('');
    const createValue = ref('');
    const isFocused = ref(false);
    const generatedId = useId();

    const { isOpen, highlightedIndex, open, close, navigate } = useDropdown(containerRef, {
        disabled: toRef(props, 'disabled'),
        closeOnSelect: false,
        onClose: () => {
            isFocused.value = false;
        },
    });

    const inputId = computed(() => props.id || generatedId);

    const selectedItems = computed(() => {
        return props.options.filter((opt) => model.value.includes(getItemValue(opt)));
    });

    const filteredOptions = computed(() => {
        const query = searchQuery.value.toLowerCase().trim();
        if (!query) {
            return props.options;
        }
        return props.options.filter((opt) => getItemLabel(opt).toLowerCase().includes(query));
    });

    const multiSelectClasses = computed(() => [
        'multi-select',
        {
            'multi-select--disabled': props.disabled,
            'multi-select--error': props.error,
            'multi-select--focused': isFocused.value,
            'multi-select--open': isOpen.value,
        },
    ]);

    const getItemValue = (item: MultiSelectOption): string | number => {
        return item[props.valueKey] as string | number;
    };

    const getItemLabel = (item: MultiSelectOption): string => {
        return String(item[props.labelKey] || '');
    };

    const getItemImage = (item: MultiSelectOption): string | undefined => {
        return item[props.imageKey] as string | undefined;
    };

    const isSelected = (item: MultiSelectOption): boolean => {
        return model.value.includes(getItemValue(item));
    };

    const toggleItem = (item: MultiSelectOption) => {
        const value = getItemValue(item);
        if (isSelected(item)) {
            model.value = model.value.filter((v) => v !== value);
        } else {
            if (props.maxItems && model.value.length >= props.maxItems) {
                return;
            }
            model.value = [...model.value, value];
        }
        searchQuery.value = '';
        // Keep dropdown open for multiple selections
        open();
        isFocused.value = true;

        nextTick(() => {
            if (contentRef.value) {
                contentRef.value.scrollTop = contentRef.value.scrollHeight;
            }
        });
    };

    const removeItem = (item: MultiSelectOption) => {
        model.value = model.value.filter((v) => v !== getItemValue(item));
    };

    const clearAll = () => {
        model.value = [];
        searchQuery.value = '';
        inputRef.value?.focus();
    };

    const selectFirstFiltered = () => {
        const option = filteredOptions.value[highlightedIndex.value] ?? filteredOptions.value[0];
        if (option) {
            toggleItem(option);
        }
    };

    const handleCreate = () => {
        if (!createValue.value.trim()) {
            return;
        }
        emit('create', createValue.value.trim());
        createValue.value = '';
    };

    const handleBackspace = () => {
        if (!searchQuery.value) {
            const lastItem = selectedItems.value.at(-1);
            if (lastItem) {
                removeItem(lastItem);
            }
        }
    };

    const handleKeyDown = () => {
        if (!isOpen.value) {
            open();
        } else {
            navigate(1, filteredOptions.value.length);
        }
    };

    const handleKeyUp = () => {
        if (isOpen.value) {
            navigate(-1, filteredOptions.value.length);
        }
    };

    const focusInput = () => {
        if (!props.disabled) {
            inputRef.value?.focus();
        }
    };

    const handleFocus = () => {
        isFocused.value = true;
        open();
    };

    const handleBlur = (event: FocusEvent) => {
        // Ne ferme pas si le focus reste dans le container
        const relatedTarget = event.relatedTarget as Node | null;
        if (containerRef.value?.contains(relatedTarget)) {
            return;
        }
        isFocused.value = false;
    };

    watch(searchQuery, () => {
        highlightedIndex.value = 0;
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;
    @use '@/styles/components/select' as sel;

    .multi-select {
        position: relative;
        display: flex;
        flex-direction: column;
        margin-bottom: vars.$spacing-md;
        width: 100%;

        @include mix.form-field-chrome;

        &__container {
            display: flex;
            align-items: flex-start;
            gap: vars.$spacing-xxs;
            min-height: 48px;
            padding: 6px vars.$spacing-xs 6px vars.$spacing-xxs;
            border: 1px solid vars.$border-color;
            border-radius: vars.$border-radius-md;
            background-color: vars.$bg-primary;
            cursor: text;
            transition:
                border-color vars.$transition-base,
                box-shadow vars.$transition-base,
                background-color vars.$transition-base;
        }

        &__content {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 4px;
            flex: 1;
            min-width: 0;
            max-height: 60px;
            overflow-y: auto;
            padding: 2px 0;
        }

        &__tag {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            height: 26px;
            padding: 0 6px 0 8px;
            background-color: func.color-alpha(vars.$primary-color, 0.08);
            border: 1px solid func.color-alpha(vars.$primary-color, 0.2);
            color: vars.$primary-color;
            border-radius: vars.$border-radius-sm;
            font-weight: vars.$font-weight-medium;
            max-width: 150px;
        }

        &__tag-image {
            @include sel.option-image(14px);
        }

        &__tag-text {
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            line-height: 1;
        }

        &__tag-remove {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 16px;
            height: 16px;
            padding: 0;
            margin-left: 2px;
            background: none;
            border: none;
            border-radius: 50%;
            color: func.color-alpha(vars.$primary-color, 0.45);
            cursor: pointer;
            transition:
                color vars.$transition-fast,
                background-color vars.$transition-fast;

            &:hover {
                color: vars.$white;
                background-color: vars.$primary-color;
            }
        }

        &__input {
            flex: 1;
            min-width: 80px;
            border: none;
            outline: none;
            background: transparent;
            color: vars.$text-primary;
            font-family: vars.$font-family;
            padding: 6px 0;

            &::placeholder {
                color: vars.$text-muted;
            }

            &:disabled {
                cursor: not-allowed;
            }
        }

        &__actions {
            display: flex;
            align-items: center;
            align-self: center;
            gap: vars.$spacing-xxs;
            flex-shrink: 0;
        }

        &__clear {
            @include sel.clear-button;
        }
        &__arrow {
            @include sel.arrow-icon;
        }

        &__dropdown {
            @include sel.dropdown-panel;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
        }

        &__options {
            @include sel.options-list;
        }
        &__option {
            @include sel.option-item('multi-select');
        }
        &__option-image {
            @include sel.option-image(20px);
        }
        &__option-text {
            @include sel.option-text;
        }
        &__option-check {
            @include sel.option-check;
        }
        &__empty-text {
            @include sel.empty-state;
        }

        &__create-section {
            @include sel.create-section;
        }
        &__create-form {
            @include sel.create-form;
        }
        &__create-input {
            @include sel.create-input;
        }
        &__create-btn {
            @include sel.create-button;
        }

        // States
        &--focused {
            .multi-select__container {
                border-color: vars.$primary-color;
                box-shadow: 0 0 0 3px func.color-alpha(vars.$primary-color, 0.12);
                background-color: vars.$white;
            }

            .multi-select__label {
                color: vars.$primary-color;
            }
        }

        &--error {
            @include sel.state-error('.multi-select__container');

            &.multi-select--focused .multi-select__container {
                box-shadow: 0 0 0 3px func.color-alpha(vars.$danger-color, 0.12);
            }
        }

        &--disabled {
            @include sel.state-disabled('.multi-select__container');
        }

        &:hover:not(&--disabled, &--focused) {
            .multi-select__container {
                border-color: vars.$text-muted;
            }
        }

        @include mix.responsive(mobile) {
            &__container {
                min-height: 44px;
            }

            &__input {
                font-size: 1rem;
            }
        }
    }

    // Tag transitions (specifique au multi-select)
    .tag-enter-active,
    .tag-leave-active {
        transition: all 0.2s ease;
    }

    .tag-enter-from,
    .tag-leave-to {
        opacity: 0;
        transform: scale(0.8);
    }

    @include sel.dropdown-transition;
</style>
