<template>
	<div :class="['switch', { 'switch--disabled': disabled, 'switch--error': error }, customClass]">
		<label class="switch__container" :for="id">
			<input
				:id="id"
				type="checkbox"
				:name="name"
				:checked="modelValue"
				:disabled="disabled"
				class="switch__input"
				@change="handleChange"
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
	defineProps({
		modelValue: {
			type: Boolean,
			default: false,
		},
		id: {
			type: String,
			default: () => `switch-${Math.random().toString(36).substring(2, 9)}`,
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

	.switch {
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

			&:checked ~ .switch__toggle {
				background-color: vars.$primary-color;

				&:after {
					transform: translateX(16px);
				}
			}

			&:focus ~ .switch__toggle {
				@include mix.focus-outline;
			}

			&:disabled ~ .switch__toggle {
				background-color: vars.$gray-light;
				cursor: not-allowed;

				&:after {
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

			&:after {
				content: '';
				position: absolute;
				top: 2px;
				left: 2px;
				width: 16px;
				height: 16px;
				background-color: vars.$white;
				border-radius: 50%;
				transition: transform vars.$transition-base;
				box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
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
