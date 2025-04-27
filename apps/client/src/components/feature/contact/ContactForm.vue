<!-- ContactForm.vue -->
<template>
	<BaseForm :form-id="fixedFormId" :form-custom-class="`contact-form ${customClass}`" @submit="submitForm">
		<!-- En-tête du formulaire -->
		<template #fields>
			<div v-if="title || $slots.header" class="contact-form__header">
				<slot name="header">
					<h2 class="contact-form__title">{{ title }}</h2>
					<p v-if="subtitle" class="contact-form__subtitle">{{ subtitle }}</p>
				</slot>
			</div>

			<div class="contact-form__body">
				<!-- Nom -->
				<FormField id="name" label="Nom" :error="errors.name" :required="true">
					<BaseInput
						id="name"
						v-model="form.name"
						placeholder="Votre nom"
						:disabled="isSubmitting"
						:error="errors.name"
						required
						@blur="validateField('name')"
					/>
				</FormField>

				<!-- Email -->
				<FormField id="email" label="Email" :error="errors.email" :required="true">
					<BaseInput
						id="email"
						v-model="form.email"
						type="email"
						placeholder="Votre adresse email"
						:disabled="isSubmitting"
						:error="errors.email"
						required
						@blur="validateField('email')"
					>
						<template #icon-right>
							<BaseIcon name="mail" :size="18" />
						</template>
					</BaseInput>
				</FormField>

				<!-- Sujet -->
				<FormField id="subject" label="Sujet" :error="errors.subject">
					<BaseSelect
						id="subject"
						v-model="form.subject"
						placeholder="Sélectionnez un sujet"
						:disabled="isSubmitting"
						:error="errors.subject"
						@blur="validateField('subject')"
					>
						<option v-for="option in subjectOptions" :key="option.value" :value="option.value">
							{{ option.label }}
						</option>
					</BaseSelect>
				</FormField>

				<!-- Message -->
				<FormField id="message" label="Message" :error="errors.message" :required="true">
					<BaseTextarea
						id="message"
						v-model="form.message"
						placeholder="Votre message ici..."
						:disabled="isSubmitting"
						:error="errors.message"
						:rows="5"
						:show-count="true"
						:maxlength="1000"
						required
						@blur="validateField('message')"
					/>
				</FormField>

				<!-- Statut du formulaire -->
				<div
					v-if="formStatus.message"
					:class="['contact-form__status', `contact-form__status--${formStatus.type}`]"
				>
					<BaseIcon :name="formStatus.type" :size="18" />
					<p>{{ formStatus.message }}</p>
				</div>
			</div>
		</template>

		<template #actions>
			<div class="contact-form__footer">
				<BaseButton
					type="submit"
					:loading="isSubmitting"
					:disabled="isSubmitting || !isFormValid"
					size="large"
					full-width
				>
					{{ isSubmitting ? 'Envoi en cours...' : 'Envoyer' }}
				</BaseButton>

				<slot name="footer"></slot>
			</div>
		</template>
	</BaseForm>
</template>

<script setup lang="ts">
	import BaseButton from '@/components/base/BaseButton.vue';
	import BaseForm from '@/components/base/BaseForm.vue';
	import FormField from '@/components/base/BaseFormField.vue';
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import BaseInput from '@/components/base/BaseInput.vue';
	import BaseSelect from '@/components/base/BaseSelect.vue';
	import BaseTextarea from '@/components/base/BaseTextarea.vue';
	import { useContact } from '@/services/api/useContact';
	import { computed, onMounted, reactive, ref } from 'vue';

	// Props
	const props = defineProps({
		title: {
			type: String,
			default: '',
		},
		subtitle: {
			type: String,
			default: '',
		},
		customClass: {
			type: String,
			default: '',
		},
		formId: {
			type: String,
			default: '',
		},
	});

	// Émits
	const emit = defineEmits(['submit', 'success', 'error']);

	const fixedFormId = ref('contact-form-fixed');

	// Services
	const contactService = useContact();

	// État du formulaire
	const form = reactive({
		name: '',
		email: '',
		subject: '' as 'general' | 'project' | 'job' | 'other' | '',
		message: '',
		privacyPolicy: false,
	});

	const errors = reactive({
		name: '',
		email: '',
		subject: '',
		message: '',
		privacyPolicy: '',
	});

	const isSubmitting = ref(false);
	const formStatus = reactive({
		type: '',
		message: '',
	});

	// Options du menu déroulant
	const subjectOptions = [
		{ value: 'general', label: 'Information générale' },
		{ value: 'project', label: 'Demande de projet' },
		{ value: 'job', label: "Opportunité d'emploi" },
		{ value: 'feedback', label: 'Commentaires' },
		{ value: 'other', label: 'Autre' },
	];

	// Validation
	const validateField = (fieldName: keyof typeof form) => {
		errors[fieldName] = '';

		switch (fieldName) {
			case 'name':
				if (!form.name.trim()) {
					errors.name = 'Le nom est requis';
				} else if (form.name.length < 2) {
					errors.name = 'Le nom doit comporter au moins 2 caractères';
				}
				break;

			case 'email':
				if (!form.email.trim()) {
					errors.email = "L'email est requis";
				} else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
					errors.email = 'Veuillez entrer une adresse email valide';
				}
				break;

			case 'message':
				if (!form.message.trim()) {
					errors.message = 'Le message est requis';
				} else if (form.message.length < 10) {
					errors.message = 'Le message doit comporter au moins 10 caractères';
				}
				break;

			case 'privacyPolicy':
				if (!form.privacyPolicy) {
					errors.privacyPolicy = 'Vous devez accepter la politique de confidentialité';
				}
				break;
		}
	};

	const validateForm = () => {
		validateField('name');
		validateField('email');
		validateField('message');
		validateField('privacyPolicy');

		// Vérifiez s'il y a des erreurs
		return !Object.values(errors).some((error) => error);
	};

	const resetForm = () => {
		form.name = '';
		form.email = '';
		form.subject = '';
		form.message = '';
		form.privacyPolicy = false;
	};

	const isFormValid = computed(() => {
		return (
			form.name &&
			form.email &&
			form.message &&
			form.privacyPolicy &&
			!Object.values(errors).some((error) => error)
		);
	});

	onMounted(() => {
		if (props.formId) {
			fixedFormId.value = props.formId;
		}
	});

	// Soumission du formulaire
	const submitForm = async () => {
		if (!validateForm()) return;

		isSubmitting.value = true;
		formStatus.type = 'info';
		formStatus.message = 'Envoi en cours...';

		try {
			const response = await contactService.sendMessage({
				name: form.name,
				email: form.email,
				subject: form.subject || 'general',
				message: form.message,
			});

			// Succès
			formStatus.type = 'success';
			formStatus.message =
				'Votre message a été envoyé avec succès. Nous vous répondrons dans les plus brefs délais.';

			// ✅ Réinitialisation propre
			resetForm();

			emit('success', response);
		} catch (error) {
			formStatus.type = 'error';
			formStatus.message = "Une erreur s'est produite lors de l'envoi du message. Veuillez réessayer plus tard.";

			emit('error', error);
		} finally {
			isSubmitting.value = false;
			emit('submit', { ...form });
		}
	};
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.contact-form {
		display: flex;
		flex-direction: column;
		gap: vars.$spacing-lg;
		width: 100%;
		max-width: 600px;
		margin: 0 auto;

		&__header {
			text-align: center;
			margin-bottom: vars.$spacing-md;
		}

		&__title {
			margin-bottom: vars.$spacing-sm;
		}

		&__subtitle {
			color: vars.$gray-dark;
		}

		&__body {
			display: flex;
			flex-direction: column;
			gap: vars.$spacing-md;
		}

		&__privacy {
			margin-top: vars.$spacing-sm;
		}

		&__status {
			display: flex;
			align-items: flex-start;
			gap: vars.$spacing-sm;
			padding: vars.$spacing-sm;
			border-radius: vars.$border-radius-md;
			margin-top: vars.$spacing-md;

			&--success {
				background-color: func.color-alpha(vars.$success-color, 0.1);
				color: func.adjust-color-brightness(vars.$success-color, -20%);
			}

			&--error {
				background-color: func.color-alpha(vars.$danger-color, 0.1);
				color: func.adjust-color-brightness(vars.$danger-color, -20%);
			}

			&--info {
				background-color: func.color-alpha(vars.$info-color, 0.1);
				color: func.adjust-color-brightness(vars.$info-color, -20%);
			}
		}

		&__footer {
			margin-top: vars.$spacing-md;
		}
	}
</style>
