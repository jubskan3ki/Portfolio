<template>
	<div>
		<!-- En-tête de contact avec le composant Hero -->
		<Hero
			title="Contact"
			description="Vous avez un projet en tête ou souhaitez discuter d'une opportunité professionnelle ? N'hésitez pas à me contacter."
			variant="primary"
			show-title-underline
		/>

		<!-- Contenu principal avec formulaire et infos -->
		<Section class="contact-content">
			<div class="container">
				<div class="contact-content__wrapper">
					<!-- Formulaire de contact -->
					<div class="contact-content__form animate-fade-in-up">
						<ContactForm form-id="contact-form-fixed" />
					</div>

					<!-- Informations de contact -->
					<div class="contact-content__info animate-fade-in-up delay-2">
						<ContactInfos
							title="Mes coordonnées"
							subtitle="N'hésitez pas à me contacter par ces moyens"
							address="Paris, France"
							email="contact@aitaddajuba.fr"
							phone="+33 6 95 21 71 97"
							:social-links="socialMediaLinks"
							custom-class="contact-page-infos"
						/>
					</div>
				</div>
			</div>
		</Section>

		<!-- FAQ - Questions fréquentes -->
		<Section class="contact-faq" variant="light">
			<div class="container">
				<h2 class="contact-faq__title animate-fade-in">Questions fréquentes</h2>

				<div class="faq-list animate-fade-in delay-1">
					<div v-for="(faq, index) in faqs" :key="index" class="faq-item">
						<div
							class="faq-item__question"
							:class="{ 'faq-item__question--active': expandedFaq === index }"
							role="button"
							tabindex="0"
							@click="toggleFaq(index)"
							@keydown.enter.space.prevent="toggleFaq(index)"
						>
							<h3>{{ faq.question }}</h3>
							<BaseIcon :name="expandedFaq === index ? 'chevron-up' : 'chevron-down'" :size="16" />
						</div>
						<div class="faq-item__answer" :class="{ 'faq-item__answer--active': expandedFaq === index }">
							<p>{{ faq.answer }}</p>
						</div>
					</div>
				</div>
			</div>
		</Section>
	</div>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import ContactForm from '@/components/feature/contact/ContactForm.vue';
	import ContactInfos from '@/components/feature/contact/ContactInfos.vue';
	import Section from '@/components/layouts/Section.vue';
	import Hero from '@/components/ui/Hero.vue';
	import { useAlert } from '@/composables/useAlert';
	import { useMock } from '@/services/api/useMock';
	import { onMounted, ref } from 'vue';

	// Service de mock pour récupérer et soumettre des données
	const { fetchFaqs, faqs } = useMock();

	// État
	const expandedFaq = ref<number | null>(null);

	// Notification
	const notification = useAlert();

	// Chargement initial des données
	onMounted(async () => {
		try {
			// Charger les FAQs depuis le service useMock
			await fetchFaqs();
		} catch (error) {
			console.error('Erreur lors du chargement des FAQs:', error);
			notification.error('Une erreur est survenue lors du chargement des questions fréquentes.', 'Erreur');
		}
	});

	// Configuration des liens sociaux
	const socialMediaLinks = [
		{
			name: 'LinkedIn',
			icon: 'linkedin',
			url: 'https://www.linkedin.com/in/juba-aitadda/',
		},
		{
			name: 'GitHub',
			icon: 'github',
			url: 'https://github.com/jubskan3ki',
		},
	];

	// Méthodes
	const toggleFaq = (index: number) => {
		if (expandedFaq.value === index) {
			expandedFaq.value = null;
		} else {
			expandedFaq.value = index;
		}
	};
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	// Contenu principal
	.contact-content {
		padding: vars.$spacing-xl 0;

		&__wrapper {
			display: grid;
			grid-template-columns: 1fr 1fr;
			gap: vars.$spacing-xl;

			@include mix.responsive(tablet) {
				grid-template-columns: 1fr;
			}
		}

		&__form {
			background-color: vars.$white;
			border-radius: vars.$border-radius-lg;
			padding: vars.$spacing-lg;
			box-shadow: vars.$box-shadow-medium;

			.contact-form__title {
				margin-bottom: vars.$spacing-lg;
				padding-bottom: vars.$spacing-sm;
				border-bottom: 2px solid vars.$primary-color;
				position: relative;
				color: vars.$primary-color;

				&::after {
					content: '';
					position: absolute;
					bottom: -2px;
					left: 0;
					width: 60px;
					height: 2px;
					background-color: vars.$secondary-color;
				}
			}
		}

		&__info {
			display: flex;
			flex-direction: column;
			gap: vars.$spacing-lg;
		}
	}

	// FAQ - Questions fréquentes
	.contact-faq {
		padding: vars.$spacing-xl 0;

		&__title {
			text-align: center;
			margin-bottom: vars.$spacing-xl;
			position: relative;
			color: vars.$primary-color;

			&::after {
				content: '';
				position: absolute;
				bottom: -10px;
				left: 50%;
				transform: translateX(-50%);
				width: 60px;
				height: 3px;
				background-color: vars.$primary-color;
				border-radius: vars.$border-radius-full;
			}
		}
	}

	.faq-list {
		max-width: 800px;
		margin: 0 auto;
	}

	.faq-item {
		margin-bottom: vars.$spacing-md;
		border-radius: vars.$border-radius-md;
		overflow: hidden;
		box-shadow: vars.$box-shadow;
		background-color: vars.$white;

		&__question {
			padding: vars.$spacing-md;
			background-color: vars.$white;
			cursor: pointer;
			display: flex;
			justify-content: space-between;
			align-items: center;
			transition: background-color 0.3s ease;

			&:hover {
				background-color: vars.$white-dark;
			}

			&--active {
				background-color: func.color-alpha(vars.$primary-color, 0.1);

				h3 {
					color: vars.$primary-color;
				}
			}

			h3 {
				margin: 0;
				transition: color 0.3s ease;
			}
		}

		&__answer {
			max-height: 0;
			overflow: hidden;
			transition:
				max-height 0.3s ease,
				padding 0.3s ease;

			&--active {
				max-height: 500px;
				padding: vars.$spacing-md;
				border-top: 1px solid vars.$white-dark;
			}

			p {
				margin: 0;
				color: vars.$gray-dark;
				line-height: 1.6;
			}
		}
	}

	// Newsletter et réseaux sociaux
	.contact-newsletter {
		padding: vars.$spacing-xl 0;
		position: relative;

		&::before {
			content: '';
			position: absolute;
			top: 0;
			left: 0;
			width: 100%;
			height: 100%;
			background: linear-gradient(
				135deg,
				func.color-alpha(vars.$primary-color, 0.9),
				func.color-alpha(vars.$secondary-color, 0.8)
			);
			z-index: -1;
		}
	}

	.newsletter {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: vars.$spacing-xl;
		margin-bottom: vars.$spacing-xl;

		@include mix.responsive(tablet) {
			flex-direction: column;
			gap: vars.$spacing-lg;
		}

		&__content {
			flex: 1;
		}

		&__title {
			color: vars.$white;
			margin-bottom: vars.$spacing-md;
		}

		&__description {
			color: func.color-alpha(vars.$white, 0.9);
			line-height: 1.6;
		}

		&__form {
			flex: 1;
		}

		&__input-group {
			display: flex;
			gap: vars.$spacing-sm;
			margin-bottom: vars.$spacing-sm;

			@include mix.responsive(mobile) {
				flex-direction: column;
			}
		}

		&__input {
			flex: 1;
		}

		&__privacy {
			color: func.color-alpha(vars.$white, 0.7);
		}

		&__link {
			color: vars.$white;
			text-decoration: underline;
			transition: opacity 0.3s ease;

			&:hover {
				opacity: 0.8;
			}
		}
	}

	.social {
		text-align: center;
		border-top: 1px solid func.color-alpha(vars.$white, 0.2);
		padding-top: vars.$spacing-lg;

		&__title {
			color: vars.$white;
			margin-bottom: vars.$spacing-md;
		}

		&__links {
			display: flex;
			justify-content: center;
			gap: vars.$spacing-md;
		}

		&__link {
			display: flex;
			align-items: center;
			justify-content: center;
			width: 50px;
			height: 50px;
			border-radius: 50%;
			background-color: func.color-alpha(vars.$white, 0.2);
			color: vars.$white;
			transition: all 0.3s ease;

			&:hover {
				background-color: func.color-alpha(vars.$white, 0.3);
				transform: translateY(-3px);
			}
		}
	}

	// Animation pour l'apparition des éléments
	.animate-fade-in {
		animation: fadeIn vars.$transition-base forwards;
	}

	.animate-fade-in-up {
		animation: fadeInUp vars.$transition-base forwards;
	}

	.delay-1 {
		animation-delay: 0.1s;
	}

	.delay-2 {
		animation-delay: 0.2s;
	}
</style>
