<template>
	<div
		:class="[
			'input',
			{ 'input--disabled': disabled },
			{ 'input--error': error },
			{ 'input--success': success },
			{ 'input--with-icon-left': $slots['icon-left'] },
			{ 'input--with-icon-right': $slots['icon-right'] || (clearable && modelValue) },
			{ 'input--focused': isFocused },
			customClass,
		]"
	>
		<label v-if="label" :for="inputId" class="input__label">
			{{ label }}
			<span v-if="required" class="input__required">*</span>
		</label>

		<div class="input__container">
			<div v-if="$slots['icon-left']" class="input__icon input__icon--left">
				<slot name="icon-left"></slot>
			</div>

			<input
				:id="inputId"
				:type="type"
				:name="name"
				:value="modelValue"
				:placeholder="placeholder"
				:disabled="disabled"
				:required="required"
				:readonly="readonly"
				:min="min"
				:max="max"
				:maxlength="maxlength"
				:autocomplete="autocomplete"
				class="input__field"
				@input="handleInput"
				@blur="handleBlur"
				@focus="handleFocus"
			/>

			<div v-if="$slots['icon-right'] || (clearable && modelValue)" class="input__icon input__icon--right">
				<button
					v-if="clearable && modelValue"
					type="button"
					class="input__clear"
					aria-label="Clear input"
					@click="handleClear"
				>
					<svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
						<path
							d="M18 6L6 18M6 6L18 18"
							stroke="currentColor"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
					</svg>
				</button>
				<slot v-else name="icon-right"></slot>
			</div>
		</div>

		<p v-if="error" class="input__message input__message--error">{{ error }}</p>
		<p v-else-if="success" class="input__message input__message--success">{{ success }}</p>
		<p v-else-if="hint" class="input__message input__message--hint">{{ hint }}</p>
	</div>
</template>

<script setup lang="ts">
	import { computed, onMounted, ref } from 'vue';

	const props = defineProps({
		modelValue: {
			type: [String, Number],
			default: '',
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
		type: {
			type: String,
			default: 'text',
			validator: (value: string) =>
				[
					'text',
					'password',
					'email',
					'number',
					'tel',
					'url',
					'search',
					'date',
					'time',
					'datetime-local',
					'month',
					'week',
					'color',
				].includes(value),
		},
		placeholder: {
			type: String,
			default: '',
		},
		required: {
			type: Boolean,
			default: false,
		},
		disabled: {
			type: Boolean,
			default: false,
		},
		readonly: {
			type: Boolean,
			default: false,
		},
		min: {
			type: [String, Number],
			default: undefined,
		},
		max: {
			type: [String, Number],
			default: undefined,
		},
		maxlength: {
			type: [String, Number],
			default: undefined,
		},
		autocomplete: {
			type: String,
			default: 'off',
		},
		clearable: {
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

	const emit = defineEmits(['update:modelValue', 'blur', 'focus', 'clear']);

	// ID unique généré côté client uniquement
	const uniqueId = ref('');
	const isFocused = ref(false);

	// Computed inputId stable pour hydratation côté client et serveur
	const inputId = computed(() => {
		return props.id || uniqueId.value || 'input';
	});

	// Générer l'ID unique uniquement après le montage du composant (côté client)
	onMounted(() => {
		if (!props.id && !uniqueId.value) {
			uniqueId.value = `input-${Math.random().toString(36).substring(2, 9)}`;
		}
	});

	const handleInput = (event: Event) => {
		const target = event.target as HTMLInputElement;
		if (target) {
			emit('update:modelValue', target.value);
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

	const handleClear = () => {
		emit('update:modelValue', '');
		emit('clear');
	};
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.input {
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
			background-color: transparent;
			color: vars.$black-light;
			font-family: vars.$font-family;
			height: 42px;

			@include mix.transition(border-color, box-shadow);
			@include mix.focus-outline;

			&:focus {
				outline: none;
				border-color: vars.$primary-color;
				box-shadow: 0 2px 0 rgba(vars.$primary-color, 0.2);
			}

			&::placeholder {
				color: vars.$gray;
				opacity: 0.7;
			}

			&:disabled {
				cursor: not-allowed;
				opacity: 0.6;
				background-color: func.color-alpha(vars.$gray-light, 0.1);
			}
		}

		&__icon {
			position: absolute;
			display: flex;
			align-items: center;
			justify-content: center;
			pointer-events: none;
			color: vars.$gray;
			transition: color vars.$transition-base;

			&--left {
				left: 0;
			}

			&--right {
				right: 0;
				pointer-events: auto; // Pour permettre le clic sur l'icône clear
			}
		}

		&__clear {
			background: none;
			border: none;
			padding: 0;
			margin: 0;
			width: 24px;
			height: 24px;
			display: flex;
			align-items: center;
			justify-content: center;
			border-radius: 50%;
			color: vars.$gray;
			cursor: pointer;
			transition: all vars.$transition-base;

			&:hover {
				background-color: vars.$gray-light;
				color: vars.$black-light;
				transform: scale(1.1);
			}

			&:active {
				transform: scale(0.95);
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

		&--with-icon-left {
			.input__field {
				padding-left: 28px;
			}
		}

		&--with-icon-right {
			.input__field {
				padding-right: 28px;
			}
		}

		&--disabled {
			opacity: 0.7;
			cursor: not-allowed;
		}

		&--error {
			.input__field {
				border-color: vars.$danger-color;
			}

			.input__icon {
				color: vars.$danger-color;
			}
		}

		&--success {
			.input__field {
				border-color: vars.$success-color;
			}

			.input__icon {
				color: vars.$success-color;
			}
		}

		&--focused {
			.input__label {
				color: vars.$primary-color;
			}

			.input__icon {
				color: vars.$primary-color;
			}
		}

		&:hover:not(&--disabled) {
			.input__field:not(:focus) {
				border-color: func.adjust-color-brightness(vars.$gray, -15%);
			}
		}

		@include mix.responsive(mobile) {
			.input__field {
				height: 38px;
			}
		}
	}
</style>
