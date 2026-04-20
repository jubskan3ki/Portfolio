<template>
    <div ref="containerRef" :class="selectClasses">
        <label v-if="label" :id="`${inputId}-label`" :for="inputId" class="select__label">
            {{ label }}
            <span v-if="required" class="select__required">*</span>
        </label>

        <div
            class="select__trigger"
            role="combobox"
            tabindex="0"
            :aria-expanded="isOpen"
            aria-haspopup="listbox"
            :aria-controls="isOpen ? `${inputId}-listbox` : undefined"
            :aria-activedescendant="activeDescendant"
            :aria-labelledby="triggerLabelledBy"
            :aria-label="triggerAriaLabel"
            :aria-invalid="!!error || undefined"
            :aria-describedby="messageId || undefined"
            :aria-required="required || undefined"
            :aria-disabled="disabled || undefined"
            @click="toggleDropdown"
            @focus="handleFocus"
            @blur="handleBlur"
            @keydown.enter.prevent="toggleDropdown"
            @keydown.space.prevent="toggleDropdown"
            @keydown.escape="close"
            @keydown.down.prevent="handleKeyDown"
            @keydown.up.prevent="handleKeyUp"
            @keydown.home.prevent="handleHome"
            @keydown.end.prevent="handleEnd"
            @keydown.tab="close"
        >
            <div class="select__value">
                <img
                    v-if="showImage && selectedOption?.image"
                    :src="selectedOption.image"
                    :alt="selectedOption.label"
                    class="select__value-image"
                />
                <span v-if="selectedOption" class="select__value-text">{{ selectedOption.label }}</span>
                <span v-else class="select__placeholder">{{ placeholder }}</span>
            </div>

            <div class="select__icons">
                <button
                    v-if="model && !required"
                    type="button"
                    class="select__clear"
                    aria-label="Effacer"
                    @mousedown.prevent
                    @click.stop="clearSelection"
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
                <div class="select__arrow" :class="{ 'select__arrow--active': isOpen }">
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
            <div v-if="isOpen" class="select__dropdown">
                <div
                    :id="`${inputId}-listbox`"
                    ref="optionsRef"
                    class="select__options"
                    role="listbox"
                    :aria-labelledby="triggerLabelledBy"
                    :aria-label="triggerLabelledBy ? undefined : triggerAriaLabel"
                >
                    <button
                        v-for="(option, index) in options"
                        :id="`${inputId}-option-${index}`"
                        :key="String(option.value)"
                        type="button"
                        class="select__option"
                        :class="{
                            'select__option--selected': isSelected(option),
                            'select__option--highlighted': highlightedIndex === index,
                        }"
                        role="option"
                        :aria-selected="isSelected(option)"
                        @mousedown.prevent
                        @click="selectOption(option)"
                        @mouseenter="highlightedIndex = index"
                    >
                        <img
                            v-if="showImage && option.image"
                            :src="option.image"
                            :alt="option.label"
                            class="select__option-image"
                        />
                        <span class="select__option-text">{{ option.label }}</span>
                        <svg
                            v-if="isSelected(option)"
                            class="select__option-check"
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

                    <div v-if="options.length === 0" class="select__empty" @mousedown.prevent>
                        Aucune option disponible
                    </div>
                </div>

                <div v-if="allowCreate" class="select__create-section">
                    <div class="select__create-form">
                        <label :for="`${inputId}-create`" class="sr-only">{{ createPlaceholder }}</label>
                        <input
                            :id="`${inputId}-create`"
                            ref="createInputRef"
                            v-model="newItemName"
                            type="text"
                            class="select__create-input"
                            :placeholder="createPlaceholder"
                            @keydown.enter.prevent="handleCreate"
                            @keydown.stop
                        />
                        <button
                            type="button"
                            class="select__create-btn"
                            :disabled="!newItemName.trim()"
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

        <p v-if="error" :id="messageId" class="select__message select__message--error" role="alert">{{ error }}</p>
        <p v-else-if="success" :id="messageId" class="select__message select__message--success">{{ success }}</p>
        <p v-else-if="hint" :id="messageId" class="select__message select__message--hint">{{ hint }}</p>
    </div>
</template>

<script setup lang="ts">
    import { computed, ref, useId, toRef, watch } from 'vue';

    import { useDropdown } from '@/composables/ui/useDropdown';

    import type { SelectInitialValue, SelectOption, SelectProps } from '@/types/components/base';

    const props = withDefaults(defineProps<SelectProps>(), {
        options: () => [],
        id: '',
        label: '',
        ariaLabel: '',
        ariaLabelledby: '',
        placeholder: 'Sélectionner...',
        required: false,
        disabled: false,
        error: '',
        success: '',
        hint: '',
        showImage: false,
        allowCreate: false,
        createLabel: 'Créer nouveau',
        createPlaceholder: 'Nom...',
        initialValue: undefined,
    });

    const emit = defineEmits<{
        blur: [event: FocusEvent];
        focus: [event: FocusEvent];
        create: [value: string];
    }>();

    const model = defineModel<string | number>({ default: '' });

    const containerRef = ref<HTMLElement | null>(null);
    const optionsRef = ref<HTMLElement | null>(null);
    const newItemName = ref('');
    const generatedId = useId();

    const {
        isOpen,
        highlightedIndex,
        open: openDropdown,
        close,
        navigate,
        scrollToHighlighted,
        getActiveDescendant,
    } = useDropdown(containerRef, {
        disabled: toRef(props, 'disabled'),
        closeOnSelect: true,
        onClose: () => {
            newItemName.value = '';
        },
    });

    const inputId = computed(() => props.id || generatedId);
    const messageId = computed(() =>
        props.error || props.success || props.hint ? `${inputId.value}-message` : undefined,
    );

    const triggerLabelledBy = computed<string | undefined>(() => {
        if (props.ariaLabelledby) {
            return props.ariaLabelledby;
        }
        if (props.label) {
            return `${inputId.value}-label`;
        }
        return undefined;
    });

    const triggerAriaLabel = computed<string | undefined>(() => {
        if (triggerLabelledBy.value) {
            return undefined;
        }
        return props.ariaLabel || props.placeholder || undefined;
    });

    const selectedOption = computed(() => {
        if (!model.value && model.value !== 0) {
            return null;
        }
        return props.options.find((opt) => opt.value === model.value) || null;
    });

    const selectClasses = computed(() => [
        'select',
        {
            'select--disabled': props.disabled,
            'select--error': props.error,
            'select--success': props.success,
            'select--open': isOpen.value,
            'select--has-value': !!selectedOption.value,
        },
    ]);

    const activeDescendant = computed(() => getActiveDescendant(inputId.value));

    const isSelected = (option: SelectOption): boolean => {
        return model.value === option.value;
    };

    const selectOption = (option: SelectOption) => {
        if (option.disabled) {
            return;
        }
        model.value = option.value;
        close();
    };

    const clearSelection = () => {
        model.value = '';
    };

    const toggleDropdown = () => {
        if (props.disabled) {
            return;
        }
        if (isOpen.value) {
            close();
        } else {
            openDropdown();
            highlightedIndex.value = selectedOption.value
                ? props.options.findIndex((opt) => opt.value === model.value)
                : 0;
        }
    };

    const handleKeyDown = () => {
        if (!isOpen.value) {
            toggleDropdown();
        } else {
            navigate(1, props.options.length);
            scrollToHighlighted(optionsRef, 'select__option');
        }
    };

    const handleKeyUp = () => {
        if (isOpen.value) {
            navigate(-1, props.options.length);
            scrollToHighlighted(optionsRef, 'select__option');
        }
    };

    const handleHome = () => {
        if (!isOpen.value) {
            return;
        }
        if (props.options.length === 0) {
            return;
        }
        highlightedIndex.value = 0;
        scrollToHighlighted(optionsRef, 'select__option');
    };

    const handleEnd = () => {
        if (!isOpen.value) {
            return;
        }
        if (props.options.length === 0) {
            return;
        }
        highlightedIndex.value = props.options.length - 1;
        scrollToHighlighted(optionsRef, 'select__option');
    };

    const handleFocus = (event: FocusEvent) => {
        emit('focus', event);
    };

    const handleBlur = (event: FocusEvent) => {
        emit('blur', event);
    };

    const handleCreate = () => {
        if (!newItemName.value.trim()) {
            return;
        }
        emit('create', newItemName.value.trim());
        newItemName.value = '';
    };

    const resolveSelectInitialValue = (raw: SelectInitialValue, opts: SelectOption[]): SelectOption['value'] | null => {
        if (raw === undefined || raw === null || raw === '') {
            return null;
        }
        if (typeof raw === 'object') {
            const candidate = raw.id ?? raw.slug ?? raw.name;
            if (candidate === undefined) {
                return null;
            }
            return resolveSelectInitialValue(candidate as SelectInitialValue, opts);
        }
        const direct = opts.find((opt) => opt.value === raw);
        if (direct) {
            return direct.value;
        }
        if (typeof raw === 'string') {
            const byLabel = opts.find((opt) => opt.label === raw || String(opt.value) === raw);
            return byLabel?.value ?? null;
        }
        return null;
    };

    watch(
        [() => props.initialValue, () => props.options],
        ([raw, opts]) => {
            if (model.value !== '' && model.value !== undefined && model.value !== null) {
                return;
            }
            if (!opts || opts.length === 0) {
                return;
            }
            const resolved = resolveSelectInitialValue(raw, opts);
            if (resolved !== null) {
                model.value = resolved;
            }
        },
        { immediate: true },
    );

    defineExpose({
        focus: () => containerRef.value?.querySelector<HTMLElement>('.select__trigger')?.focus(),
        blur: () => containerRef.value?.querySelector<HTMLElement>('.select__trigger')?.blur(),
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;
    @use '@/styles/components/select' as sel;

    .select {
        position: relative;
        display: flex;
        flex-direction: column;
        width: 100%;

        @include mix.form-field-chrome;

        &__trigger {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: vars.$spacing-xs;
            height: 48px;
            padding: 0 vars.$spacing-md;
            border: 1px solid vars.$border-color;
            border-radius: vars.$border-radius-md;
            background-color: vars.$bg-primary;
            cursor: pointer;
            transition:
                border-color vars.$transition-base,
                box-shadow vars.$transition-base,
                background-color vars.$transition-base;

            &:focus {
                outline: none;
                border-color: vars.$primary-color;
                box-shadow: 0 0 0 3px func.color-alpha(vars.$primary-color, 0.12);
            }
        }

        &__value {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;
            flex: 1;
            min-width: 0;
        }

        &__value-image {
            @include sel.option-image(20px);
        }

        &__value-text {
            color: vars.$text-primary;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        &__placeholder {
            color: vars.$text-muted;
        }

        &__icons {
            display: flex;
            align-items: center;
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
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        }

        &__options {
            @include sel.options-list;
        }
        &__option {
            @include sel.option-item('select');
            &--selected {
                font-weight: vars.$font-weight-medium;
            }
        }
        &__option-image {
            @include sel.option-image(24px);
            border-radius: 4px;
        }
        &__option-text {
            @include sel.option-text;
        }
        &__option-check {
            @include sel.option-check;
        }
        &__empty {
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

        &--open {
            .select__trigger {
                border-color: vars.$primary-color;
                box-shadow: 0 0 0 3px func.color-alpha(vars.$primary-color, 0.12);
                background-color: vars.$white;
            }

            .select__label {
                color: vars.$primary-color;
            }
        }

        &--error {
            @include sel.state-error('.select__trigger');

            .select__trigger:focus {
                box-shadow: 0 0 0 3px func.color-alpha(vars.$danger-color, 0.12);
            }
        }

        &--success {
            .select__trigger {
                border-color: vars.$success-color;
                background-color: func.color-alpha(vars.$success-color, 0.03);
            }
        }

        &--disabled {
            @include sel.state-disabled('.select__trigger');
        }

        &:hover:not(&--disabled, &--open) {
            .select__trigger:not(:focus) {
                border-color: vars.$text-muted;
            }
        }

        @include mix.responsive(mobile) {
            &__trigger {
                height: 44px;
            }

            &__value-text,
            &__placeholder {
                font-size: 1rem;
            }
        }
    }

    @include sel.dropdown-transition;
</style>
