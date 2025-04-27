<!-- src/components/layouts/Footer.vue -->
<template>
	<footer class="footer">
		<div class="container">
			<div class="footer__main">
				<!-- Bannière résumé du portfolio -->
				<PortfolioSummary :title="title" :description="description" :cta-links="ctaLinks" :stats="stats" />

				<!-- Coordonnées et contact -->
				<div class="footer__contact">
					<ContactInfo
						:title="footerData.contactTitle"
						:email="footerData.email"
						:phone="footerData.phone"
						:address="footerData.address"
						:is-available="footerData.isAvailable"
					/>

					<!-- Réseaux sociaux -->
					<SocialLinks title="Suivez-moi" :links="footerData.socialLinks" />
				</div>
			</div>

			<!-- Bas de page -->
			<div class="footer__bottom">
				<small class="footer__copyright">
					&copy; {{ currentYear }} {{ footerData.companyName }}. {{ footerData.copyrightText }}</small
				>

				<div v-if="footerData.legalLinks.length" class="footer__legal">
					<BaseLink
						v-for="(link, index) in footerData.legalLinks"
						:key="index"
						:to="link.url"
						class="footer__legal-link"
					>
						<small>{{ link.label }}</small>
					</BaseLink>
				</div>
			</div>
		</div>
	</footer>
</template>

<script setup lang="ts">
	import BaseLink from '@/components/base/BaseLink.vue';
	import ContactInfo from '@/components/layouts/FooterContact.vue';
	import SocialLinks from '@/components/layouts/FooterSocial.vue';
	import PortfolioSummary from '@/components/ui/PortfolioSummary.vue';
	import { CtaLinks, footerConfig, StatItem } from '@/config/footer';
	import { ROUTES } from '@/config/routes';
	import { computed } from 'vue';

	// Props pour surcharger les données par défaut
	const props = defineProps({
		footerData: {
			type: Object,
			default: () => footerConfig,
		},
	});

	// Données pour le PortfolioSummary
	const title = 'Donnez vie à vos idées avec des solutions digitales innovantes';
	const description =
		"Développeur Web & Mobile et futur Tech Lead, je combine expertise technique et vision stratégique pour créer des expériences digitales modernes, performantes et centrées sur l'utilisateur. Spécialisé en React, Vue, Flutter, Go et Django .";

	// Utiliser les données du config file ou les valeurs par défaut avec le système de routes
	const ctaLinks = computed<CtaLinks>(() => {
		return (
			props.footerData.ctaLinks || {
				primary: {
					label: 'Parlons de votre projet',
					url: ROUTES.CONTACT,
				},
				secondary: {
					label: 'Découvrir mes réalisations',
					url: ROUTES.PROJECTS,
				},
			}
		);
	});

	const stats = computed<StatItem[]>(
		() =>
			props.footerData.stats || [
				{ value: props.footerData.projectsCount, label: 'Projets réalisés' },
				{ value: props.footerData.yearsExperience, label: "Années d'expérience" },
				{ value: props.footerData.techCount, label: 'Technologies maîtrisées' },
			]
	);

	// Année actuelle pour le copyright
	const currentYear = computed(() => new Date().getFullYear());
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.footer {
		background: linear-gradient(
			to right,
			func.color-alpha(vars.$primary-color, 0.05),
			func.color-alpha(vars.$secondary-color, 0.05)
		);
		padding: vars.$spacing-xl 0;

		&__main {
			display: grid;
			grid-template-columns: 3fr 1fr;
			gap: vars.$spacing-lg;
			margin-bottom: vars.$spacing-lg;

			@include mix.responsive(tablet) {
				grid-template-columns: 1fr;
				gap: vars.$spacing-md;
			}
		}

		&__contact {
			display: flex;
			flex-direction: column;
			gap: vars.$spacing-lg;

			@include mix.responsive(tablet) {
				display: grid;
				grid-template-columns: 1fr 1fr;
				gap: vars.$spacing-md;
			}
		}

		&__bottom {
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding-top: vars.$spacing-md;
			border-top: 1px solid func.color-alpha(vars.$gray, 0.3);

			@include mix.responsive(mobile) {
				flex-direction: column;
				gap: vars.$spacing-sm;
				align-items: flex-start;
			}
		}

		&__copyright {
			color: vars.$gray-dark;
		}

		&__legal {
			display: flex;
			gap: vars.$spacing-md;

			@include mix.responsive(mobile) {
				flex-direction: column;
				gap: vars.$spacing-xs;
			}
		}

		&__legal-link {
			color: vars.$gray-dark;
			transition: color vars.$transition-base;

			&:hover {
				color: vars.$primary-color;
			}
		}
	}
</style>
