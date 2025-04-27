<template>
	<div
		:class="[
			'textarea',
			{ 'textarea--disabled': disabled },
			{ 'textarea--error': error },
			{ 'textarea--success': success },
			{ 'textarea--resizable': resizable },
			{ 'textarea--focused': isFocused },
			customClass,
		]"
	>
		<label v-if="label" :for="textareaId" class="textarea__label">
			{{ label }}
			<span v-if="required" class="textarea__required">*</span>
		</label>

		<div class="textarea__container">
			<textarea
				:id="textareaId"
				:name="name"
				:value="modelValue"
				:placeholder="placeholder"
				:disabled="disabled"
				:required="required"
				:readonly="readonly"
				:rows="rows"
				:maxlength="maxlength"
				:autocomplete="autocomplete"
				class="textarea__field"
				@input="handleInput"
				@blur="handleBlur"
				@focus="handleFocus"
			></textarea>

			<div
				v-if="showCount && maxlength"
				class="textarea__counter"
				:class="{ 'textarea__counter--limit': isNearLimit }"
			>
				{{ modelValue.length }}/{{ maxlength }}
			</div>
		</div>

		<p v-if="error" class="textarea__message textarea__message--error">{{ error }}</p>
		<p v-else-if="success" class="textarea__message textarea__message--success">{{ success }}</p>
		<p v-else-if="hint" class="textarea__message textarea__message--hint">{{ hint }}</p>
	</div>
</template>

<script setup lang="ts">
	import { computed, onMounted, ref } from 'vue';

	const props = defineProps({
		modelValue: {
			type: String,
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
		placeholder: {
			type: String,
			default: '',
		},
		rows: {
			type: [String, Number],
			default: 3,
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
		maxlength: {
			type: [String, Number],
			default: undefined,
		},
		autocomplete: {
			type: String,
			default: 'off',
		},
		resizable: {
			type: Boolean,
			default: true,
		},
		showCount: {
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
	const uniqueId = ref('');

	// Générer un ID stable pour l'hydratation côté serveur et client
	const textareaId = computed(() => {
		return props.id || uniqueId.value || 'textarea';
	});

	// Vérifier si on s'approche de la limite de caractères (90%)
	const isNearLimit = computed(() => {
		if (!props.maxlength) return false;
		const maxLength = Number(props.maxlength);
		return props.modelValue.length >= maxLength * 0.9;
	});

	onMounted(() => {
		if (!props.id && !uniqueId.value) {
			uniqueId.value = `textarea-${Math.random().toString(36).substring(2, 9)}`;
		}
	});

	const handleInput = (event: Event) => {
		const target = event.target as HTMLTextAreaElement;
		emit('update:modelValue', target.value);
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

	.textarea {
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
		}

		&__field {
			width: 100%;
			border: none;
			border-bottom: 2px solid vars.$gray;
			padding: vars.$spacing-sm 0;
			background-color: transparent;
			color: vars.$black-light;
			resize: none; // Default to no resize
			min-height: 90px;
			font-family: vars.$font-family;
			line-height: 1.5;

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

		&__counter {
			position: absolute;
			right: 0;
			bottom: 8px;
			color: vars.$gray;
			padding: vars.$spacing-xs;
			border-radius: vars.$border-radius-sm;
			transition: all vars.$transition-base;

			&--limit {
				color: vars.$warning-color;
				font-weight: 500;
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
			cursor: not-allowed;
		}

		&--error {
			.textarea__field {
				border-color: vars.$danger-color;
			}
		}

		&--success {
			.textarea__field {
				border-color: vars.$success-color;
			}
		}

		&--focused {
			.textarea__label {
				color: vars.$primary-color;
			}
		}

		&--resizable {
			.textarea__field {
				resize: vertical;
			}
		}

		&:hover:not(&--disabled) {
			.textarea__field:not(:focus) {
				border-color: func.adjust-color-brightness(vars.$gray, -15%);
			}
		}

		@include mix.responsive(mobile) {
			.textarea__field {
				min-height: 80px;
			}
		}
	}
</style>
