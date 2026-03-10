<template>
    <div :class="checkboxClasses">
        <label :for="checkboxId" class="checkbox__container">
            <input
                :id="checkboxId"
                v-model="model"
                type="checkbox"
                :name="name"
                :value="value"
                :disabled="disabled"
                :aria-invalid="!!error || undefined"
                :aria-describedby="errorId || undefined"
                class="checkbox__input"
            />
            <span class="checkbox__checkmark" aria-hidden="true"></span>
            <span v-if="$slots.default || $slots.label || label" class="checkbox__label">
                <slot name="label"><slot>{{ label }}</slot></slot>
            </span>
        </label>
        <p v-if="error" :id="errorId" class="checkbox__error" role="alert">{{ error }}</p>
    </div>
</template>

<script setup lang="ts">
    import { computed, useId } from 'vue';

    import type { CheckboxProps } from '@/types/components/base';

    type Props = CheckboxProps;

    const props = withDefaults(defineProps<Props>(), {
        id: '',
        name: '',
        value: '',
        label: '',
        disabled: false,
        error: '',
        customClass: '',
    });

    const model = defineModel<boolean>({ default: false });

    const generatedId = useId();
    const checkboxId = computed(() => props.id || generatedId);
    const errorId = computed(() => (props.error ? `${checkboxId.value}-error` : undefined));

    const checkboxClasses = computed(() => [
        'checkbox',
        {
            'checkbox--disabled': props.disabled,
            'checkbox--error': props.error,
        },
        props.customClass,
    ]);
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;

    .checkbox {
        display: inline-block;
        margin-bottom: vars.$spacing-xs;

        &__container {
            display: flex;
            align-items: center;
            position: relative;
            cursor: pointer;
            user-select: none;
        }

        &__input {
            position: absolute;
            opacity: 0;
            width: 0;
            height: 0;

            &:checked ~ .checkbox__checkmark {
                background-color: vars.$primary-color;
                border-color: vars.$primary-color;

                &::after {
                    opacity: 1;
                }
            }

            &:focus-visible ~ .checkbox__checkmark {
                outline: 2px solid vars.$primary-color;
                outline-offset: 2px;
            }

            &:disabled ~ .checkbox__checkmark {
                background-color: vars.$gray-light;
                border-color: vars.$gray;
                cursor: not-allowed;
            }

            &:disabled ~ .checkbox__label {
                color: vars.$gray;
                cursor: not-allowed;
            }
        }

        &__checkmark {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 18px;
            height: 18px;
            background-color: vars.$white;
            border: 2px solid vars.$gray-light;
            border-radius: vars.$border-radius-sm;
            transition: all vars.$transition-base;

            &::after {
                content: '';
                position: absolute;
                width: 5px;
                height: 10px;
                border: solid vars.$white;
                border-width: 0 2px 2px 0;
                transform: rotate(45deg);
                opacity: 0;
                transition: opacity vars.$transition-base;
            }
        }

        &__label {
            margin-left: vars.$spacing-xs;
            user-select: none;
            color: vars.$black-light;
        }

        &__error {
            margin-top: vars.$spacing-xxs;
            color: vars.$danger-color;
        }

        &--disabled {
            @include mix.form-disabled;

            .checkbox__container {
                cursor: not-allowed;
            }
        }

        &--error {
            .checkbox__checkmark {
                border-color: vars.$danger-color;
            }
        }
    }
</style>
