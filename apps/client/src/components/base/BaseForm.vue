<!-- BaseForm.vue -->
<template>
	<form :id="formId" :class="['form', formCustomClass]" @submit.prevent="handleSubmit">
		<slot name="fields">
			<!-- Emplacement pour les FormField générés par les props fields si fournis -->
			<div
				v-for="(field, index) in fields"
				:key="`field-${index}`"
				:class="['form-field', { 'form-field--error': field.error }, field.customClass]"
			>
				<label v-if="field.label" :for="field.id || `field-${index}`" class="form-field__label">
					{{ field.label }}
					<span v-if="field.required" class="form-field__required">*</span>
				</label>
				<div class="form-field__control">
					<slot :name="`field-${index}`">
						<!-- Contenu par défaut du champ si aucun slot spécifique n'est fourni -->
					</slot>
				</div>
				<p v-if="field.error" class="form-field__error">{{ field.error }}</p>
				<p v-else-if="field.hint" class="form-field__hint">{{ field.hint }}</p>
			</div>
		</slot>
		<slot name="actions"></slot>
	</form>
</template>

<script setup lang="ts">
	interface FieldProps {
		id?: string;
		label?: string;
		required?: boolean;
		error?: string;
		hint?: string;
		customClass?: string;
	}

	// Import onServerPrefetch uniquement en mode SSR
	import { onServerPrefetch, ref } from 'vue';

	const props = defineProps({
		// Props du formulaire
		formId: {
			type: String,
			default: '',
		},
		formCustomClass: {
			type: String,
			default: '',
		},

		// Props pour les champs (si utilisés directement)
		fields: {
			type: Array as () => FieldProps[],
			default: () => [],
		},
	});

	const emit = defineEmits(['submit']);

	// ID côté serveur stocké dans une ref pour l'hydratation
	const serverFormId = ref('');

	// Générer un ID côté serveur et utiliser la même valeur côté client
	let resolvedFormId = props.formId;
	if (!resolvedFormId) {
		// Si nous sommes côté serveur, générer un ID qui sera réutilisé
		if (typeof window === 'undefined') {
			serverFormId.value = `form-${Math.random().toString(36).substring(2, 9)}`;
			resolvedFormId = serverFormId.value;

			// Assurer que l'ID du serveur est disponible pendant l'hydratation
			onServerPrefetch(() => {
				serverFormId.value = resolvedFormId;
			});
		} else {
			// Côté client, utiliser l'ID du serveur si disponible ou en générer un nouveau
			resolvedFormId = serverFormId.value || `form-${Math.random().toString(36).substring(2, 9)}`;
		}
	}

	const handleSubmit = (event: Event) => {
		emit('submit', event);
	};
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.form {
		width: 100%;
	}

	.form-field {
		margin-bottom: vars.$spacing-md;

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

		&__error {
			margin-top: vars.$spacing-xs;
			color: vars.$danger-color;
		}

		&__hint {
			margin-top: vars.$spacing-xs;
			color: vars.$gray;
		}

		&--error {
			.form-field__label {
				color: vars.$danger-color;
			}
		}
	}
</style>
