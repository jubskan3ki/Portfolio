<template>
    <div :class="radioClasses">
        <label class="radio__container" :for="radioId">
            <input
                :id="radioId"
                type="radio"
                :name="name"
                :value="value"
                :checked="modelValue === value"
                :disabled="disabled"
                :aria-invalid="!!error || undefined"
                :aria-describedby="errorId || undefined"
                class="radio__input"
                @change="emit('update:modelValue', value)"
            />
            <span class="radio__checkmark" aria-hidden="true"></span>
            <span v-if="$slots.default || label" class="radio__label">
                <slot>{{ label }}</slot>
            </span>
        </label>

        <p v-if="error" :id="errorId" class="radio__error" role="alert">{{ error }}</p>
    </div>
</template>

<script setup lang="ts">
    import { computed, useId } from 'vue';

    import type { RadioItemProps } from '@/types/components/base';

    type Props = RadioItemProps;

    const props = withDefaults(defineProps<Props>(), {
        modelValue: '',
        id: '',
        name: '',
        label: '',
        disabled: false,
        error: '',
        customClass: '',
    });

    const emit = defineEmits<{
        'update:modelValue': [value: string | number | boolean | object];
    }>();

    const generatedId = useId();
    const radioId = computed(() => props.id || generatedId);
    const errorId = computed(() => (props.error ? `${radioId.value}-error` : undefined));

    const radioClasses = computed(() => [
        'radio',
        {
            'radio--disabled': props.disabled,
            'radio--error': props.error,
        },
        props.customClass,
    ]);
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;

    .radio {
        display: inline-block;
        margin-bottom: vars.$spacing-xs;

        &__container {
            display: flex;
            align-items: center;
            position: relative;
            cursor: pointer;
        }

        &__input {
            position: absolute;
            opacity: 0;
            width: 0;
            height: 0;

            &:checked ~ .radio__checkmark {
                border-color: vars.$primary-color;

                &::after {
                    transform: scale(1);
                }
            }

            &:focus-visible ~ .radio__checkmark {
                outline: 2px solid vars.$primary-color;
                outline-offset: 2px;
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
            border-radius: vars.$border-radius-full;
            transition: all vars.$transition-base;

            &::after {
                content: '';
                width: 10px;
                height: 10px;
                border-radius: vars.$border-radius-full;
                background-color: vars.$primary-color;
                transform: scale(0);
                transition: transform vars.$transition-base;
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

            .radio__container {
                cursor: not-allowed;
            }
        }

        &--error {
            .radio__checkmark {
                border-color: vars.$danger-color;
            }
        }
    }
</style>
