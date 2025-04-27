<template>
	<div :class="['checkbox', { 'checkbox--disabled': disabled }, { 'checkbox--error': error }, customClass]">
		<label :for="id" class="checkbox__container">
			<input
				:id="id"
				type="checkbox"
				:name="name"
				:value="value"
				:checked="modelValue"
				:disabled="disabled"
				class="checkbox__input"
				@change="handleChange"
			/>
			<span class="checkbox__checkmark"></span>
			<span v-if="$slots.default || label" class="checkbox__label">
				<slot>{{ label }}</slot>
			</span>
		</label>
		<p v-if="error" class="checkbox__error">{{ error }}</p>
	</div>
</template>

<script setup lang="ts">
	defineProps({
		modelValue: {
			type: Boolean,
			default: false,
		},
		id: {
			type: String,
			default: () => `checkbox-${Math.random().toString(36).substring(2, 9)}`,
		},
		name: {
			type: String,
			default: '',
		},
		value: {
			type: [String, Number, Boolean, Object],
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

	const emit = defineEmits(['update:modelValue']);

	const handleChange = (event: Event) => {
		const target = event.target as HTMLInputElement;
		if (target) {
			emit('update:modelValue', target.checked);
		}
	};
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.checkbox {
		display: inline-block;
		margin-bottom: vars.$spacing-sm;

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

				&:after {
					opacity: 1;
				}
			}

			&:focus ~ .checkbox__checkmark {
				@include mix.focus-outline;
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

			&:after {
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
