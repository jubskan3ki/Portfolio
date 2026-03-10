<template>
    <div :class="fieldClasses">
        <label v-if="label" :for="fieldId" class="form-field__label">
            {{ label }}
            <span v-if="required" class="form-field__required">*</span>
        </label>
        <div class="form-field__control">
            <slot></slot>
        </div>
        <p v-if="error" class="form-field__error">{{ error }}</p>
        <p v-else-if="hint" class="form-field__hint">{{ hint }}</p>
    </div>
</template>

<script setup lang="ts">
    import { computed, useId } from 'vue';

    import type { FormFieldProps } from '@/types/components/base';

    type Props = FormFieldProps;

    const props = withDefaults(defineProps<Props>(), {
        id: '',
        label: '',
        required: false,
        error: '',
        hint: '',
        customClass: '',
    });

    const generatedId = useId();
    const fieldId = computed(() => props.id || generatedId);

    const fieldClasses = computed(() => [
        'form-field',
        {
            'form-field--error': props.error,
        },
        props.customClass,
    ]);
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;

    .form-field {
        margin-bottom: vars.$spacing-md;

        &__label {
            display: block;
            margin-bottom: vars.$spacing-xxs;
            font-weight: vars.$font-weight-medium;
            color: vars.$black-light;
        }

        &__required {
            color: vars.$danger-color;
            margin-left: 2px;
        }

        &__control {
            width: 100%;
        }

        &__error {
            margin-top: vars.$spacing-xxs;
            color: vars.$danger-color;
        }

        &__hint {
            margin-top: vars.$spacing-xxs;
            color: vars.$gray;
        }

        &--error {
            .form-field__label {
                color: vars.$danger-color;
            }
        }
    }
</style>
