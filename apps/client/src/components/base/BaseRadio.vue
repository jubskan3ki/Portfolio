<template>
	<div :class="['radio', { 'radio--disabled': disabled, 'radio--error': error }, customClass]">
		<label class="radio__container" :for="id">
			<input
				:id="id"
				type="radio"
				:name="name"
				:value="value"
				:checked="modelValue === value"
				:disabled="disabled"
				class="radio__input"
				@change="$emit('update:modelValue', value)"
			/>
			<span class="radio__checkmark"></span>
			<span v-if="$slots.default || label" class="radio__label">
				<slot>{{ label }}</slot>
			</span>
		</label>

		<p v-if="error" class="radio__error">{{ error }}</p>
	</div>
</template>

<script setup lang="ts">
	defineProps({
		modelValue: {
			type: [String, Number, Boolean, Object],
			default: '',
		},
		value: {
			type: [String, Number, Boolean, Object],
			required: true,
		},
		id: {
			type: String,
			default: () => `radio-${Math.random().toString(36).substring(2, 9)}`,
		},
		name: {
			type: String,
			default: '',
		},
		label: {
			type: String,
			default: '',
		},
		disabled: {
			type: Boolean,
			default: false,
		},
		error: {
			type: String,
			default: '',
		},
		customClass: {
			type: String,
			default: '',
		},
	});

	defineEmits(['update:modelValue']);
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.radio {
		display: inline-block;
		margin-bottom: vars.$spacing-sm;

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

				&:after {
					transform: scale(1);
				}
			}

			&:focus ~ .radio__checkmark {
				@include mix.focus-outline;
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

			&:after {
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
			margin-left: vars.$spacing-sm;
			user-select: none;
			color: vars.$black-light;
		}

		&__error {
			margin-top: vars.$spacing-xs;
			color: vars.$danger-color;
		}

		&--disabled {
			opacity: 0.6;

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
