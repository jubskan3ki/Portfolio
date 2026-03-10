<template>
    <div :class="switchClasses">
        <label class="switch__container" :for="switchId">
            <input
                :id="switchId"
                v-model="model"
                type="checkbox"
                :name="name"
                :disabled="disabled"
                class="switch__input"
            />
            <span class="switch__toggle"></span>
            <span v-if="$slots.default || label" class="switch__label">
                <slot>{{ label }}</slot>
            </span>
        </label>
        <p v-if="error" class="switch__error">{{ error }}</p>
    </div>
</template>

<script setup lang="ts">
    import { computed, useId } from 'vue';

    interface Props {
        id?: string;
        name?: string;
        label?: string;
        disabled?: boolean;
        customClass?: string;
        error?: string;
    }

    const props = withDefaults(defineProps<Props>(), {
        id: '',
        name: '',
        label: '',
        disabled: false,
        error: '',
        customClass: '',
    });

    const model = defineModel<boolean>({ default: false });

    const generatedId = useId();
    const switchId = computed(() => props.id || generatedId);

    const switchClasses = computed(() => [
        'switch',
        {
            'switch--disabled': props.disabled,
            'switch--error': props.error,
        },
        props.customClass,
    ]);
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;

    .switch {
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

            &:checked ~ .switch__toggle {
                background-color: vars.$primary-color;

                &::after {
                    transform: translateX(16px);
                }
            }

            &:focus-visible ~ .switch__toggle {
                outline: 2px solid vars.$primary-color;
                outline-offset: 2px;
            }

            &:disabled ~ .switch__toggle {
                background-color: vars.$gray-light;
                cursor: not-allowed;

                &::after {
                    background-color: vars.$gray;
                }
            }

            &:disabled ~ .switch__label {
                color: vars.$gray;
                cursor: not-allowed;
            }
        }

        &__toggle {
            display: inline-block;
            width: 36px;
            height: 20px;
            background-color: vars.$gray-light;
            border-radius: vars.$border-radius-full;
            position: relative;
            transition: background-color vars.$transition-base;

            &::after {
                content: '';
                position: absolute;
                top: 2px;
                left: 2px;
                width: 16px;
                height: 16px;
                background-color: vars.$white;
                border-radius: vars.$border-radius-full;
                transition: transform vars.$transition-base;
                box-shadow: vars.$box-shadow-xs;
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

            .switch__container {
                cursor: not-allowed;
            }
        }

        &--error {
            .switch__toggle {
                border: 1px solid vars.$danger-color;
            }
        }
    }
</style>
