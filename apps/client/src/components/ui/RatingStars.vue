<template>
	<div :class="['rating-stars', { 'rating-stars--readonly': readonly }, customClass]">
		<div class="rating-stars__container">
			<div
				v-for="n in max"
				:key="n"
				role="button"
				tabindex="0"
				:class="[
					'rating-stars__star',
					{
						'rating-stars__star--filled': n <= roundedValue,
						'rating-stars__star--half': !Number.isInteger(roundedValue) && n === Math.ceil(roundedValue),
					},
				]"
				@click="!readonly && updateValue(n)"
				@keydown.enter.prevent="!readonly && updateValue(n)"
				@keydown.space.prevent="!readonly && updateValue(n)"
				@mouseover="!readonly && setHoverValue(n)"
				@mouseleave="!readonly && clearHoverValue()"
			>
				<BaseIcon :name="starIcon" :size="size" />
			</div>
		</div>

		<div v-if="showValue" class="rating-stars__value">
			{{ displayValue }}
		</div>

		<div v-if="$slots.label || label" class="rating-stars__label">
			<slot name="label">{{ label }}</slot>
		</div>
	</div>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import { computed, ref } from 'vue';

	const props = defineProps({
		modelValue: {
			type: Number,
			default: 0,
		},
		max: {
			type: Number,
			default: 5,
		},
		size: {
			type: [Number, String],
			default: 20,
		},
		readonly: {
			type: Boolean,
			default: false,
		},
		precision: {
			type: Number,
			default: 0.5,
		},
		showValue: {
			type: Boolean,
			default: false,
		},
		label: {
			type: String,
			default: '',
		},
		starIcon: {
			type: String,
			default: 'star',
		},
		customClass: {
			type: String,
			default: '',
		},
	});

	const emit = defineEmits(['update:modelValue']);

	const hoverValue = ref(0);

	// Arrondir la valeur selon la précision
	const roundToNearest = (value: number, precision: number) => {
		return Math.round(value / precision) * precision;
	};

	const roundedValue = computed(() => {
		return hoverValue.value > 0 ? hoverValue.value : roundToNearest(props.modelValue, props.precision);
	});

	const displayValue = computed(() => {
		return roundedValue.value.toFixed(props.precision < 1 ? 1 : 0);
	});

	// Fonctions de gestion du hover et du clic
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
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.rating-stars {
		display: inline-flex;
		flex-direction: column;

		&__container {
			display: flex;
			align-items: center;
			gap: 2px;
		}

		&__star {
			position: relative;
			color: vars.$gray-light;
			cursor: pointer;
			transition: transform vars.$transition-fast;

			&:hover {
				transform: scale(1.15);
			}

			&--filled {
				color: vars.$primary-color;
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
					color: vars.$primary-color;
				}
			}
		}

		&__value {
			margin-top: vars.$spacing-xs;
			font-weight: 500;
			color: vars.$gray-dark;
		}

		&__label {
			margin-top: vars.$spacing-xs;
			color: vars.$gray-dark;
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
