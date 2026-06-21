<template>
    <div class="contact-form-wrapper">
        <div class="contact-form-wrapper__dots contact-form-wrapper__dots--top"></div>
        <div class="contact-form-wrapper__dots contact-form-wrapper__dots--bottom"></div>

        <BaseForm
            :id="fixedFormId"
            :custom-class="`contact-form ${customClass}`"
            :loading="isSubmitting"
            @submit="submitForm"
        >
            <template #fields>
                <div v-if="title || $slots.header" class="contact-form__header">
                    <slot name="header">
                        <h2 class="contact-form__title">{{ title }}</h2>
                        <p v-if="subtitle" class="contact-form__subtitle">{{ subtitle }}</p>
                    </slot>
                </div>

                <div class="contact-form__body">
                    <!-- ARIA (aria-invalid/aria-describedby/role=alert) porté par le contrôle interne ; ne pas dupliquer sur BaseFormField. -->
                    <BaseFormField id="name" label="Nom" required>
                        <BaseInput
                            id="name"
                            v-model="form.name"
                            placeholder="Votre nom complet"
                            :disabled="isSubmitting"
                            :error="errors.name"
                            required
                            autocomplete="name"
                            @blur="validateField('name')"
                        >
                            <template #icon-left>
                                <BaseIcon name="user" :size="18" />
                            </template>
                        </BaseInput>
                    </BaseFormField>

                    <BaseFormField id="email" label="Email" required>
                        <BaseInput
                            id="email"
                            v-model="form.email"
                            type="email"
                            placeholder="votre@email.com"
                            :disabled="isSubmitting"
                            :error="errors.email"
                            required
                            autocomplete="email"
                            @blur="validateField('email')"
                        >
                            <template #icon-left>
                                <BaseIcon name="mail" :size="18" />
                            </template>
                        </BaseInput>
                    </BaseFormField>

                    <BaseFormField id="subject" label="Sujet">
                        <BaseSelect
                            id="subject"
                            v-model="form.subject"
                            placeholder="Sélectionnez un sujet"
                            aria-label="Sujet du message"
                            :disabled="isSubmitting"
                            :options="subjectOptions"
                        />
                    </BaseFormField>

                    <BaseFormField id="message" label="Message" required>
                        <BaseTextarea
                            id="message"
                            v-model="form.message"
                            placeholder="Décrivez votre projet ou votre demande..."
                            :disabled="isSubmitting"
                            :error="errors.message"
                            :rows="5"
                            show-count
                            :maxlength="1000"
                            required
                            @blur="validateField('message')"
                        />
                    </BaseFormField>

                    <div class="contact-form__privacy">
                        <BaseCheckbox
                            id="privacy"
                            v-model="form.privacyPolicy"
                            :error="errors.privacyPolicy"
                            :disabled="isSubmitting"
                            @change="validateField('privacyPolicy')"
                        >
                            <template #label>
                                <span class="contact-form__privacy-text">
                                    En soumettant ce formulaire, j'accepte la
                                    <BaseLink
                                        :to="ROUTES.PRIVACY"
                                        target="_blank"
                                    >politique de confidentialité</BaseLink>.
                                </span>
                            </template>
                        </BaseCheckbox>
                    </div>

                    <Transition name="fade">
                        <div
                            v-if="formStatus.message"
                            class="contact-form__status"
                            :class="`contact-form__status--${formStatus.type}`"
                            role="alert"
                        >
                            <BaseIcon :name="statusIcon" :size="20" />
                            <p>{{ formStatus.message }}</p>
                        </div>
                    </Transition>
                </div>
            </template>

            <template #actions>
                <div class="contact-form__footer">
                    <BaseButton
                        type="submit"
                        :loading="isSubmitting"
                        :disabled="isSubmitting || !isFormValid"
                        size="lg"
                        full-width
                    >
                        <BaseIcon v-if="!isSubmitting" name="send" size="sm" />
                        {{ isSubmitting ? 'Envoi en cours...' : 'Envoyer le message' }}
                    </BaseButton>

                    <slot name="footer"></slot>
                </div>
            </template>
        </BaseForm>
    </div>
</template>

<script setup lang="ts">
    import { computed, reactive, ref } from 'vue';

    import BaseButton from '@/components/base/BaseButton.vue';
    import BaseCheckbox from '@/components/base/BaseCheckbox.vue';
    import BaseForm from '@/components/base/BaseForm.vue';
    import BaseFormField from '@/components/base/BaseFormField.vue';
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import BaseInput from '@/components/base/BaseInput.vue';
    import BaseLink from '@/components/base/BaseLink.vue';
    import BaseSelect from '@/components/base/BaseSelect.vue';
    import BaseTextarea from '@/components/base/BaseTextarea.vue';
    import { ROUTES } from '@/config/routes';
    import { useSubmitContact } from '@/services/api/modules/contact';

    import type { ContactFormProps } from '@/types/feature/contact';

    type Props = ContactFormProps;

    const props = withDefaults(defineProps<Props>(), {
        title: '',
        subtitle: '',
        customClass: '',
        formId: '',
    });

    const emit = defineEmits(['submit', 'success', 'error']);

    const fixedFormId = computed(() => props.formId || 'contact-form-fixed');

    const submitContactMutation = useSubmitContact();

    const form = reactive({
        name: '',
        email: '',
        subject: '' as 'general' | 'project' | 'job' | 'feedback' | 'other' | '',
        message: '',
        privacyPolicy: false,
    });

    const errors = reactive<Record<string, string | undefined>>({
        name: undefined,
        email: undefined,
        message: undefined,
        privacyPolicy: undefined,
    });

    const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    const validateField = (field: string): void => {
        switch (field) {
            case 'name':
                if (!form.name) {
                    errors.name = 'Le nom est requis';
                } else if (form.name.length < 2) {
                    errors.name = 'Le nom doit comporter au moins 2 caractères';
                } else if (form.name.length > 100) {
                    // Aligné sur Contact.name = CharField(max_length=100) côté backend.
                    errors.name = 'Le nom ne peut pas dépasser 100 caractères';
                } else {
                    errors.name = undefined;
                }
                break;
            case 'email':
                if (!form.email) {
                    errors.email = 'L\'email est requis';
                } else if (!EMAIL_REGEX.test(form.email)) {
                    errors.email = 'Veuillez entrer une adresse email valide';
                } else {
                    errors.email = undefined;
                }
                break;
            case 'message':
                if (!form.message) {
                    errors.message = 'Le message est requis';
                } else if (form.message.length < 10) {
                    errors.message = 'Le message doit comporter au moins 10 caractères';
                } else if (form.message.length > 1000) {
                    // Aligné sur :maxlength="1000" (contournable) et le backend.
                    errors.message = 'Le message ne peut pas dépasser 1000 caractères';
                } else {
                    errors.message = undefined;
                }
                break;
            case 'privacyPolicy':
                errors.privacyPolicy = !form.privacyPolicy
                    ? 'Vous devez accepter la politique de confidentialité'
                    : undefined;
                break;
        }
    };

    const validate = (): boolean => {
        validateField('name');
        validateField('email');
        validateField('message');
        validateField('privacyPolicy');
        return !Object.values(errors).some((error) => error);
    };

    const clearErrors = (): void => {
        errors.name = undefined;
        errors.email = undefined;
        errors.message = undefined;
        errors.privacyPolicy = undefined;
    };

    const isSubmitting = ref(false);
    const formStatus = reactive({
        type: '' as '' | 'success' | 'error' | 'info',
        message: '',
    });

    const subjectOptions = [
        { value: 'general', label: 'Information générale' },
        { value: 'project', label: 'Demande de projet' },
        { value: 'job', label: 'Opportunité d\'emploi' },
        { value: 'feedback', label: 'Commentaires' },
        { value: 'other', label: 'Autre' },
    ];

    const statusIcon = computed(() => {
        switch (formStatus.type) {
            case 'success':
                return 'check-circle';
            case 'error':
                return 'alert-circle';
            case 'info':
                return 'info';
            default:
                return 'info';
        }
    });

    const resetForm = () => {
        form.name = '';
        form.email = '';
        form.subject = '';
        form.message = '';
        form.privacyPolicy = false;
        clearErrors();
    };

    const isFormValid = computed(() => {
        return (
            form.name
            && form.email
            && form.message
            && form.privacyPolicy
            && !Object.values(errors).some((error) => error)
        );
    });

    const submitForm = async () => {
        if (!validate()) {
            return;
        }

        isSubmitting.value = true;
        formStatus.type = 'info';
        formStatus.message = 'Envoi en cours...';

        try {
            const response = await submitContactMutation.mutateAsync({
                name: form.name.trim(),
                email: form.email.trim(),
                subject: form.subject || 'general',
                message: form.message.trim(),
            });

            formStatus.type = 'success';
            formStatus.message
                = 'Votre message a été envoyé avec succès. Je vous répondrai dans les plus brefs délais.';

            resetForm();
            emit('success', response);
        } catch (error) {
            formStatus.type = 'error';
            formStatus.message = 'Une erreur s\'est produite lors de l\'envoi du message. Veuillez réessayer.';
            emit('error', error);
        } finally {
            isSubmitting.value = false;
            emit('submit', { ...form });
        }
    };
</script>

<style lang="scss" scoped>
    @use 'sass:color';
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;

    .contact-form-wrapper {
        position: relative;

        &__dots {
            position: absolute;
            width: 100px;
            height: 100px;
            @include mix.dots-pattern(fn.color-alpha(vars.$primary-color, 0.06), 2px, 14px);
            pointer-events: none;

            &--top {
                top: -20px;
                right: -20px;
                mask-image: radial-gradient(circle at top right, black, transparent 70%);
            }

            &--bottom {
                bottom: -20px;
                left: -20px;
                mask-image: radial-gradient(circle at bottom left, black, transparent 70%);
            }
        }
    }

    .contact-form {
        display: flex;
        flex-direction: column;
        gap: vars.$spacing-lg;
        width: 100%;

        &__header {
            text-align: center;
            margin-bottom: vars.$spacing-xs;
        }

        &__title {
            font-weight: vars.$font-weight-semibold;
            color: vars.$text-primary;
            margin-bottom: vars.$spacing-xxs;
        }

        &__subtitle {
            color: vars.$text-secondary;
            margin: 0;
        }

        &__body {
            display: flex;
            flex-direction: column;
        }

        &__privacy {
            margin-top: vars.$spacing-xxs;
        }

        &__privacy-text {
            color: vars.$text-secondary;

            a {
                color: vars.$primary-color;
                text-decoration: underline;
                transition: color 0.2s ease;

                &:hover {
                    color: vars.$primary-dark;
                }
            }
        }

        &__status {
            display: flex;
            align-items: flex-start;
            gap: vars.$spacing-xs;
            padding: vars.$spacing-md;
            border-radius: vars.$border-radius-lg;
            margin-top: vars.$spacing-xs;

            p {
                margin: 0;
                line-height: vars.$line-height-relaxed;
            }

            &--success {
                background: fn.color-alpha(vars.$success-color, 0.1);
                border: 1px solid fn.color-alpha(vars.$success-color, 0.2);
                color: color.adjust(vars.$success-color, $lightness: -15%);
            }

            &--error {
                background: fn.color-alpha(vars.$danger-color, 0.1);
                border: 1px solid fn.color-alpha(vars.$danger-color, 0.2);
                color: color.adjust(vars.$danger-color, $lightness: -10%);
            }

            &--info {
                background: fn.color-alpha(vars.$info-color, 0.1);
                border: 1px solid fn.color-alpha(vars.$info-color, 0.2);
                color: color.adjust(vars.$info-color, $lightness: -15%);
            }
        }

        &__footer {
            margin-top: vars.$spacing-md;
        }
    }

    .fade-enter-active,
    .fade-leave-active {
        transition: opacity 0.3s ease;
    }

    .fade-enter-from,
    .fade-leave-to {
        opacity: 0;
    }
</style>
