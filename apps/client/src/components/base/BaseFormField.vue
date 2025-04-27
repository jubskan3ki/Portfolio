<!-- FormField.vue -->
<template>
	<div :class="['form-field', { 'form-field--error': error }, customClass]">
		<label v-if="label" :for="fieldId" class="form-field__label">
			{{ label }}
			<span v-if="required" class="form-field__required">*</span>
		</label>
		<div class="form-field__control">
			<slot></slot>
		</div>
	</div>
</template>

<script setup lang="ts">
	import { computed } from 'vue';

	const props = defineProps({
		id: {
			type: String,
			default: () => `field-${Math.random().toString(36).substring(2, 9)}`,
		},
		label: {
			type: String,
			default: '',
		},
		required: {
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

	// Create a computed property for the ID to ensure it's always available
	const fieldId = computed(() => props.id);
</script>
