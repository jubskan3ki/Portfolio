<template>
    <div
        class="rating-stars"
        :class="[{ 'rating-stars--readonly': readonly }, customClass]"
        role="slider"
        :aria-valuenow="modelValue"
        :aria-valuemin="0"
        :aria-valuemax="max"
        :aria-label="label || 'Note'"
    >
        <div class="rating-stars__container">
            <button
                v-for="n in max"
                :key="n"
                type="button"
                class="rating-stars__star"
                :class="[
                    {
                        'rating-stars__star--filled': n <= roundedValue,
                        'rating-stars__star--half': !Number.isInteger(roundedValue) && n === Math.ceil(roundedValue),
                    },
                ]"
                :disabled="readonly"
                :aria-label="`${n} sur ${max}`"
                @click="!readonly && updateValue(n)"
                @keydown.enter.prevent="!readonly && updateValue(n)"
                @keydown.space.prevent="!readonly && updateValue(n)"
                @mouseover="!readonly && setHoverValue(n)"
                @mouseleave="!readonly && clearHoverValue()"
                @focus="!readonly && setHoverValue(n)"
                @blur="clearHoverValue()"
            >
                <BaseIcon :name="starIcon" :size="size" aria-hidden="true" />
            </button>
        </div>

        <small v-if="showValue" class="rating-stars__value">
            {{ displayValue }}
        </small>

        <small v-if="$slots.label || label" class="rating-stars__label">
            <slot name="label">{{ label }}</slot>
        </small>
    </div>
</template>

<script setup lang="ts">
    import { computed, ref } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';

    import type { RatingStarsProps } from '@/types/components/ui';

    type Props = RatingStarsProps;

    const props = withDefaults(defineProps<Props>(), {
        modelValue: 0,
        max: 5,
        size: 20,
        readonly: false,
        precision: 0.5,
        showValue: false,
        label: '',
        starIcon: 'star',
        customClass: '',
    });

    const emit = defineEmits<{
        'update:modelValue': [value: number];
    }>();

    const hoverValue = ref(0);

    const roundToNearest = (value: number, precision: number) => {
        return Math.round(value / precision) * precision;
    };

    const roundedValue = computed(() => {
        return hoverValue.value > 0 ? hoverValue.value : roundToNearest(props.modelValue, props.precision);
    });

    const displayValue = computed(() => {
        return roundedValue.value.toFixed(props.precision < 1 ? 1 : 0);
    });

    const setHoverValue = (value: number) => {
        hoverValue.value = value;
    };

    const clearHoverValue = () => {
        hoverValue.value = 0;
    };

    const updateValue = (value: number) => {
        emit('update:modelValue', value);
        clearHoverValue();
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as func;

    .rating-stars {
        display: inline-flex;
        flex-direction: column;
        gap: vars.$spacing-xxs;

        &__container {
            display: flex;
            align-items: center;
            gap: 2px;
        }

        &__star {
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0;
            margin: 0;
            background: none;
            border: none;
            color: vars.$gray-light;
            cursor: pointer;
            transition: all 0.15s ease;

            &:hover:not(:disabled) {
                transform: scale(1.2);
            }

            &:focus-visible {
                outline: 2px solid vars.$primary-color;
                outline-offset: 2px;
                border-radius: vars.$border-radius-sm;
            }

            &--filled {
                color: vars.$warning-color;
            }

            &--half {
                color: vars.$gray-light;

                &::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 50%;
                    height: 100%;
                    overflow: hidden;
                    color: vars.$warning-color;
                }
            }
        }

        &__value {
            font-weight: vars.$font-weight-medium;
            color: vars.$text-secondary;
        }

        &__label {
            color: vars.$text-secondary;
        }

        &--readonly {
            .rating-stars__star {
                cursor: default;

                &:hover {
                    transform: none;
                }
            }
        }
    }
</style>
