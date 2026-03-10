<template>
    <div :class="textareaClasses">
        <label v-if="label" :for="textareaId" class="textarea__label">
            {{ label }}
            <span v-if="required" class="textarea__required">*</span>
        </label>

        <div class="textarea__container">
            <textarea
                :id="textareaId"
                ref="textareaRef"
                v-model="model"
                :name="name"
                :placeholder="placeholder"
                :disabled="disabled"
                :required="required"
                :readonly="readonly"
                :rows="rows"
                :maxlength="maxlength"
                :autocomplete="autocomplete"
                :aria-required="required || undefined"
                :aria-invalid="!!error || undefined"
                :aria-describedby="messageId || undefined"
                class="textarea__field"
                @blur="handleBlur"
                @focus="handleFocus"
            ></textarea>

            <div
                v-if="showCount && maxlength"
                class="textarea__counter"
                :class="{ 'textarea__counter--limit': isNearLimit }"
            >
                {{ String(model).length }}/{{ maxlength }}
            </div>
        </div>

        <p v-if="error" :id="messageId" class="textarea__message textarea__message--error" role="alert">{{ error }}</p>
        <p v-else-if="success" class="textarea__message textarea__message--success">{{ success }}</p>
        <p v-else-if="hint" class="textarea__message textarea__message--hint">{{ hint }}</p>
    </div>
</template>

<script setup lang="ts">
    import { computed, ref, useId } from 'vue';

    interface Props {
        id?: string;
        name?: string;
        label?: string;
        placeholder?: string;
        required?: boolean;
        disabled?: boolean;
        readonly?: boolean;
        rows?: number;
        maxlength?: string | number;
        autocomplete?: string;
        resizable?: boolean;
        showCount?: boolean;
        error?: string;
        success?: string;
        hint?: string;
        customClass?: string;
    }

    const props = withDefaults(defineProps<Props>(), {
        id: '',
        name: '',
        label: '',
        placeholder: '',
        rows: 4,
        required: false,
        disabled: false,
        readonly: false,
        maxlength: undefined,
        autocomplete: 'off',
        resizable: true,
        showCount: false,
        error: '',
        success: '',
        hint: '',
        customClass: '',
    });

    const emit = defineEmits<{
        blur: [event: FocusEvent];
        focus: [event: FocusEvent];
    }>();

    const model = defineModel<string>({ default: '' });

    const textareaRef = ref<HTMLTextAreaElement | null>(null);
    const isFocused = ref(false);
    const generatedId = useId();

    const textareaId = computed(() => props.id || generatedId);
    const messageId = computed(() =>
        props.error || props.success || props.hint ? `${textareaId.value}-message` : undefined,
    );

    const isNearLimit = computed(() => {
        if (!props.maxlength) {
            return false;
        }
        const maxLength = Number(props.maxlength);
        return String(model.value).length >= maxLength * 0.9;
    });

    const textareaClasses = computed(() => [
        'textarea',
        {
            'textarea--disabled': props.disabled,
            'textarea--error': props.error,
            'textarea--success': props.success,
            'textarea--resizable': props.resizable,
            'textarea--focused': isFocused.value,
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

    defineExpose({
        focus: () => textareaRef.value?.focus(),
        blur: () => textareaRef.value?.blur(),
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .textarea {
        display: flex;
        flex-direction: column;
        width: 100%;

        @include mix.form-field-chrome;

        &__container {
            position: relative;
        }

        &__field {
            width: 100%;
            border: 1px solid vars.$border-color;
            border-radius: vars.$border-radius-md;
            padding: vars.$spacing-xs vars.$spacing-md;
            background-color: vars.$bg-primary;
            color: vars.$text-primary;
            font-family: vars.$font-family;
            line-height: vars.$line-height-base;
            min-height: 120px;
            resize: none;
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

        &__counter {
            position: absolute;
            right: vars.$spacing-xs;
            bottom: vars.$spacing-xs;
            color: vars.$text-muted;
            background-color: vars.$bg-primary;
            padding: 2px vars.$spacing-xxs;
            border-radius: vars.$border-radius-sm;
            transition: all vars.$transition-base;

            &--limit {
                color: vars.$warning-color;
                font-weight: vars.$font-weight-medium;
            }
        }

        &--disabled {
            @include mix.form-disabled;
        }

        &--error {
            @include mix.form-field-state('.textarea__field', vars.$danger-color);
        }

        &--success {
            @include mix.form-field-state('.textarea__field', vars.$success-color);
        }

        &--focused {
            .textarea__label {
                color: vars.$primary-color;
            }
        }

        &--resizable {
            .textarea__field {
                resize: vertical;
            }
        }

        &:hover:not(&--disabled) {
            .textarea__field:not(:focus) {
                border-color: vars.$text-muted;
            }
        }

        @include mix.responsive(mobile) {
            .textarea__field {
                min-height: 100px;
                font-size: 1rem;
            }
        }
    }
</style>
