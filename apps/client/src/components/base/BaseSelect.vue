<template>
	<div
		:class="[
			'select',
			{ 'select--disabled': disabled },
			{ 'select--error': error },
			{ 'select--success': success },
			{ 'select--focused': isFocused },
			{ 'select--multiple': multiple },
			customClass,
		]"
	>
		<label v-if="label" :for="selectId" class="select__label">
			{{ label }}
			<span v-if="required" class="select__required">*</span>
		</label>

		<div class="select__container">
			<select
				:id="selectId"
				:name="name"
				:value="modelValue"
				:disabled="disabled"
				:required="required"
				:multiple="multiple"
				class="select__field"
				@change="handleChange"
				@blur="handleBlur"
				@focus="handleFocus"
			>
				<option v-if="placeholder && !multiple" value="" disabled :selected="!modelValue">
					{{ placeholder }}
				</option>
				<option
					v-for="option in options"
					:key="option.value"
					:value="option.value"
					:selected="isSelected(option.value)"
					:disabled="option.disabled"
				>
					{{ option.label }}
				</option>
				<slot></slot>
			</select>

			<div class="select__arrow" :class="{ 'select__arrow--active': isFocused }">
				<svg width="12" height="8" viewBox="0 0 12 8" fill="none" xmlns="http://www.w3.org/2000/svg">
					<path
						d="M1 1.5L6 6.5L11 1.5"
						stroke="currentColor"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
				</svg>
			</div>
		</div>

		<p v-if="error" class="select__message select__message--error">{{ error }}</p>
		<p v-else-if="success" class="select__message select__message--success">{{ success }}</p>
		<p v-else-if="hint" class="select__message select__message--hint">{{ hint }}</p>
	</div>
</template>

<script setup lang="ts">
	import { computed, onMounted, ref } from 'vue';

	interface SelectOption {
		value: string | number;
		label: string;
		disabled?: boolean;
	}

	const props = defineProps({
		modelValue: {
			type: [String, Number, Array],
			default: '',
		},
		options: {
			type: Array as () => SelectOption[],
			default: () => [],
		},
		id: {
			type: String,
			default: '',
		},
		name: {
			type: String,
			default: '',
		},
		label: {
			type: String,
			default: '',
		},
		placeholder: {
			type: String,
			default: 'Sélectionnez une option',
		},
		required: {
			type: Boolean,
			default: false,
		},
		disabled: {
			type: Boolean,
			default: false,
		},
		multiple: {
			type: Boolean,
			default: false,
		},
		error: {
			type: String,
			default: '',
		},
		success: {
			type: String,
			default: '',
		},
		hint: {
			type: String,
			default: '',
		},
		customClass: {
			type: String,
			default: '',
		},
	});

	const emit = defineEmits(['update:modelValue', 'blur', 'focus']);
	const isFocused = ref(false);

	// Générer un ID stable qui sera le même côté serveur et client
	const componentId = ref('');

	onMounted(() => {
		// Utiliser une valeur unique mais stable pour l'attribut id
		if (!componentId.value) {
			componentId.value = `select-${Math.random().toString(36).substring(2, 9)}`;
		}
	});

	// Utiliser un ID calculé qui sera stable entre client et serveur
	const selectId = computed(() => {
		return props.id || componentId.value || 'select';
	});

	const isSelected = (value: string | number) => {
		if (Array.isArray(props.modelValue)) {
			return props.modelValue.includes(value);
		}
		return props.modelValue === value;
	};

	const handleChange = (event: Event) => {
		const target = event.target as HTMLSelectElement;

		if (target) {
			const value = props.multiple
				? Array.from(target.selectedOptions).map((option) => option.value)
				: target.value;

			emit('update:modelValue', value);
		}
	};

	const handleBlur = (event: FocusEvent) => {
		isFocused.value = false;
		emit('blur', event);
	};

	const handleFocus = (event: FocusEvent) => {
		isFocused.value = true;
		emit('focus', event);
	};
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.select {
		display: flex;
		flex-direction: column;
		margin-bottom: vars.$spacing-md;
		width: 100%;

		&__label {
			display: block;
			margin-bottom: vars.$spacing-xs;
			font-weight: 500;
			color: vars.$black-light;
		}

		&__required {
			color: vars.$danger-color;
			margin-left: 2px;
		}

		&__container {
			position: relative;
			display: flex;
			align-items: center;
		}

		&__field {
			width: 100%;
			border: none;
			border-bottom: 2px solid vars.$gray;
			padding: vars.$spacing-sm 0;
			padding-right: 30px; // Space for arrow
			background-color: transparent;
			color: vars.$black-light;
			appearance: none; // Remove default arrow
			cursor: pointer;
			font-family: vars.$font-family;
			height: 42px;

			@include mix.transition(border-color, box-shadow);
			@include mix.focus-outline;

			&:focus {
				outline: none;
				border-color: vars.$primary-color;
				box-shadow: 0 2px 0 rgba(vars.$primary-color, 0.2);
			}

			&:disabled {
				cursor: not-allowed;
				opacity: 0.6;
				background-color: func.color-alpha(vars.$gray-light, 0.1);
			}

			option {
				background-color: vars.$white;
				color: vars.$black-light;
				padding: vars.$spacing-sm vars.$spacing-md;

				&:disabled {
					color: vars.$gray;
				}
			}
		}

		&__arrow {
			position: absolute;
			right: 0;
			pointer-events: none;
			display: flex;
			align-items: center;
			color: vars.$gray-dark;
			transition:
				transform vars.$transition-base,
				color vars.$transition-base;

			&--active {
				transform: rotate(180deg);
				color: vars.$primary-color;
			}
		}

		&__message {
			margin-top: vars.$spacing-xs;

			&--error {
				color: vars.$danger-color;
			}

			&--success {
				color: vars.$success-color;
			}

			&--hint {
				color: vars.$gray;
			}
		}

		&--disabled {
			opacity: 0.7;

			.select__field,
			.select__arrow {
				cursor: not-allowed;
			}
		}

		&--error {
			.select__field {
				border-color: vars.$danger-color;
			}

			.select__arrow {
				color: vars.$danger-color;
			}
		}

		&--success {
			.select__field {
				border-color: vars.$success-color;
			}
		}

		&--focused {
			.select__label {
				color: vars.$primary-color;
			}
		}

		&--multiple {
			.select__field {
				height: auto;
				min-height: 42px;
				padding-top: vars.$spacing-xs;
				padding-bottom: vars.$spacing-xs;
			}
		}

		&:hover:not(&--disabled) {
			.select__field:not(:focus) {
				border-color: func.adjust-color-brightness(vars.$gray, -15%);
			}

			.select__arrow:not(.select__arrow--active) {
				color: func.adjust-color-brightness(vars.$gray-dark, -15%);
			}
		}

		@include mix.responsive(mobile) {
			.select__field {
				height: 38px;
			}
		}
	}
</style>
