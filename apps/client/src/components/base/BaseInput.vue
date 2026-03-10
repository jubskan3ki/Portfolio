<template>
    <div :class="inputClasses">
        <label v-if="label" :for="inputId" class="input__label">
            {{ label }}
            <span v-if="required" class="input__required">*</span>
        </label>

        <div class="input__container">
            <div v-if="$slots['icon-left']" class="input__icon input__icon--left">
                <slot name="icon-left"></slot>
            </div>

            <input
                :id="inputId"
                ref="inputRef"
                v-model="model"
                :type="type"
                :name="name"
                :placeholder="placeholder"
                :disabled="disabled"
                :required="required"
                :readonly="readonly"
                :min="min"
                :max="max"
                :maxlength="maxlength"
                :autocomplete="autocomplete"
                :aria-required="required || undefined"
                :aria-invalid="!!error || undefined"
                :aria-describedby="messageId || undefined"
                class="input__field"
                @blur="handleBlur"
                @focus="handleFocus"
            />

            <div v-if="$slots['icon-right'] || (clearable && model)" class="input__icon input__icon--right">
                <button
                    v-if="clearable && model"
                    type="button"
                    class="input__clear"
                    aria-label="Effacer"
                    @click="handleClear"
                >
                    <svg
                        width="14"
                        height="14"
                        viewBox="0 0 24 24"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path
                            d="M18 6L6 18M6 6L18 18"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                        />
                    </svg>
                </button>
                <slot v-else name="icon-right"></slot>
            </div>
        </div>

        <p v-if="error" :id="messageId" class="input__message input__message--error" role="alert">{{ error }}</p>
        <p v-else-if="success" :id="messageId" class="input__message input__message--success">{{ success }}</p>
        <p v-else-if="hint" :id="messageId" class="input__message input__message--hint">{{ hint }}</p>
    </div>
</template>

<script setup lang="ts">
    import { computed, ref, useId, useSlots } from 'vue';

    import type { InputProps } from '@/types/components/base';

    type Props = InputProps;

    const props = withDefaults(defineProps<Props>(), {
        id: '',
        name: '',
        label: '',
        type: 'text',
        placeholder: '',
        required: false,
        disabled: false,
        readonly: false,
        min: undefined,
        max: undefined,
        maxlength: undefined,
        autocomplete: 'off',
        clearable: false,
        error: '',
        success: '',
        hint: '',
        customClass: '',
    });

    const emit = defineEmits<{
        blur: [event: FocusEvent];
        focus: [event: FocusEvent];
        clear: [];
    }>();

    const model = defineModel<string | number>({ default: '' });

    const slots = useSlots();

    const inputRef = ref<HTMLInputElement | null>(null);
    const isFocused = ref(false);
    const generatedId = useId();

    const inputId = computed(() => props.id || generatedId);
    const messageId = computed(() =>
        props.error || props.success || props.hint ? `${inputId.value}-message` : undefined,
    );

    const inputClasses = computed(() => [
        'input',
        {
            'input--disabled': props.disabled,
            'input--error': props.error,
            'input--success': props.success,
            'input--with-icon-left': !!slots['icon-left'],
            'input--with-icon-right': !!slots['icon-right'] || props.clearable,
            'input--focused': isFocused.value,
        },
        props.customClass,
    ]);

    const handleBlur = (event: FocusEvent) => {
        isFocused.value = false;
        emit('blur', event);
    };

    const handleFocus = (event: FocusEvent) => {
        isFocused.value = true;
        emit('focus', event);
    };

    const handleClear = () => {
        model.value = '';
        emit('clear');
        inputRef.value?.focus();
    };

    defineExpose({
        focus: () => inputRef.value?.focus(),
        blur: () => inputRef.value?.blur(),
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .input {
        display: flex;
        flex-direction: column;
        margin-bottom: vars.$spacing-md;
        width: 100%;

        @include mix.form-field-chrome;

        &__container {
            position: relative;
            display: flex;
            align-items: center;
        }

        &__field {
            width: 100%;
            border: 1px solid vars.$border-color;
            border-radius: vars.$border-radius-md;
            padding: vars.$spacing-xs vars.$spacing-md;
            background-color: vars.$bg-primary;
            color: vars.$text-primary;
            font-family: vars.$font-family;
            height: 48px;
            transition:
                border-color vars.$transition-base,
                box-shadow vars.$transition-base,
                background-color vars.$transition-base;

            &:focus {
                outline: none;
                border-color: vars.$primary-color;
                box-shadow: 0 0 0 3px func.color-alpha(vars.$primary-color, 0.12);
                background-color: vars.$white;
            }

            &::placeholder {
                color: vars.$text-muted;
            }

            &:disabled {
                cursor: not-allowed;
                opacity: 0.6;
                background-color: vars.$bg-secondary;
            }
        }

        &__icon {
            position: absolute;
            display: flex;
            align-items: center;
            justify-content: center;
            pointer-events: none;
            color: vars.$text-muted;
            transition: color vars.$transition-base;

            &--left {
                left: vars.$spacing-xs;
            }

            &--right {
                right: vars.$spacing-xs;
                pointer-events: auto;
            }
        }

        &__clear {
            background: none;
            border: none;
            padding: 0;
            margin: 0;
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: vars.$border-radius-full;
            color: vars.$text-muted;
            cursor: pointer;
            transition: all vars.$transition-base;

            &:hover {
                background-color: vars.$bg-secondary;
                color: vars.$text-primary;
            }

            &:active {
                transform: scale(0.95);
            }
        }

        &--with-icon-left {
            .input__field {
                padding-left: calc(vars.$spacing-xs + 24px);
            }
        }

        &--with-icon-right {
            .input__field {
                padding-right: calc(vars.$spacing-xs + 24px);
            }
        }

        &--disabled {
            @include mix.form-disabled;
        }

        &--error {
            @include mix.form-field-state('.input__field', vars.$danger-color);

            .input__icon {
                color: vars.$danger-color;
            }
        }

        &--success {
            @include mix.form-field-state('.input__field', vars.$success-color);

            .input__icon {
                color: vars.$success-color;
            }
        }

        &--focused {
            .input__label {
                color: vars.$primary-color;
            }

            .input__icon {
                color: vars.$primary-color;
            }
        }

        &:hover:not(&--disabled) {
            .input__field:not(:focus) {
                border-color: vars.$text-muted;
            }
        }

        @include mix.responsive(mobile) {
            .input__field {
                height: 44px;
                font-size: 1rem; // Prevent iOS zoom
            }
        }
    }
</style>
