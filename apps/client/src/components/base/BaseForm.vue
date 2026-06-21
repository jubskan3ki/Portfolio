<template>
    <form :id="formId" :class="formClasses" @submit.prevent="handleSubmit">
        <slot name="fields">
            <div
                v-for="(field, index) in fields"
                :key="`field-${index}`"
                class="form-field"
                :class="[{ 'form-field--error': field.error }, field.customClass]"
            >
                <label v-if="field.label" :for="field.id || `field-${index}`" class="form-field__label">
                    {{ field.label }}
                    <span v-if="field.required" class="form-field__required">*</span>
                </label>
                <div class="form-field__control">
                    <slot :name="`field-${index}`"></slot>
                </div>
                <p v-if="field.error" class="form-field__error">{{ field.error }}</p>
                <p v-else-if="field.hint" class="form-field__hint">{{ field.hint }}</p>
            </div>
        </slot>
        <slot name="actions" :loading="loading" :submit="handleSubmit"></slot>
    </form>
</template>

<script setup lang="ts">
    import { computed, useId } from 'vue';

    import type { FormProps } from '@/types/components/base';

    type Props = FormProps;

    const props = withDefaults(defineProps<Props>(), {
        id: '',
        customClass: '',
        fields: () => [],
        loading: false,
    });

    const emit = defineEmits<{
        submit: [event: Event];
    }>();

    const generatedId = useId();
    const formId = computed(() => props.id || generatedId);

    const formClasses = computed(() => ['form', props.customClass]);

    const handleSubmit = (event: Event) => {
        // Garde anti double-soumission : ignore tout submit tant qu'une requête est en cours.
        if (props.loading) {
            return;
        }
        emit('submit', event);
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;

    .form {
        width: 100%;
    }

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
