<template>
	<div class="contact-card">
		<div class="contact-card__header">
			<h2 class="contact-card__title">{{ title }}</h2>
			<p v-if="subtitle" class="contact-card__subtitle">{{ subtitle }}</p>
		</div>

		<div class="contact-card__content">
			<div v-if="address" class="contact-card__item">
				<div class="contact-card__icon-wrapper">
					<BaseIcon name="map-pin" :size="22" />
				</div>
				<div class="contact-card__info">
					<p class="contact-card__label">{{ addressTitle }}</p>
					<p class="contact-card__value">{{ address }}</p>
				</div>
			</div>

			<div v-if="email" class="contact-card__item">
				<div class="contact-card__icon-wrapper">
					<BaseIcon name="mail" :size="22" />
				</div>
				<div class="contact-card__info">
					<p class="contact-card__label">{{ emailTitle }}</p>
					<p class="contact-card__value">
						<BaseLink :to="`mailto:${email}`">{{ email }}</BaseLink>
					</p>
				</div>
			</div>

			<div v-if="phone" class="contact-card__item">
				<div class="contact-card__icon-wrapper">
					<BaseIcon name="phone" :size="22" />
				</div>
				<div class="contact-card__info">
					<p class="contact-card__label">{{ phoneTitle }}</p>
					<p class="contact-card__value">
						<BaseLink :to="`tel:${phone.replace(/\s+/g, '')}`">{{ phone }}</BaseLink>
					</p>
				</div>
			</div>
		</div>

		<div v-if="socialLinks && socialLinks.length > 0" class="contact-card__social">
			<h3 class="contact-card__social-title">{{ socialTitle }}</h3>
			<div class="contact-card__social-links">
				<BaseLink
					v-for="(social, index) in socialLinks"
					:key="index"
					:to="social.url"
					:aria-label="social.name"
					class="contact-card__social-button"
					target="_blank"
					rel="noopener noreferrer"
				>
					<BaseIcon :name="social.icon" :size="18" />
					<p class="contact-card__social-name">{{ social.name }}</p>
				</BaseLink>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import BaseLink from '@/components/base/BaseLink.vue';

	interface SocialLink {
		name: string;
		icon: string;
		url: string;
	}

	defineProps({
		title: {
			type: String,
			default: 'Contactez-moi',
		},
		subtitle: {
			type: String,
			default: '',
		},
		addressTitle: {
			type: String,
			default: 'Adresse',
		},
		emailTitle: {
			type: String,
			default: 'Email',
		},
		phoneTitle: {
			type: String,
			default: 'Téléphone',
		},
		socialTitle: {
			type: String,
			default: 'Suivez-moi',
		},
		address: {
			type: String,
			default: 'Paris, France',
		},
		email: {
			type: String,
			default: 'contact@aitaddajuba.fr',
		},
		phone: {
			type: String,
			default: '+33 6 95 21 71 97',
		},
		socialLinks: {
			type: Array as () => SocialLink[],
			default: () => [
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
			],
		},
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.contact-card {
		padding: vars.$spacing-lg;
		border-radius: vars.$border-radius-lg;
		background-color: vars.$white;
		box-shadow: vars.$box-shadow-large;
		height: 100%;

		&__header {
			margin-bottom: vars.$spacing-lg;
		}

		&__title {
			margin-bottom: vars.$spacing-xs;
			color: vars.$primary-color;
			position: relative;
		}

		&__subtitle {
			color: vars.$gray;
			margin-top: vars.$spacing-sm;
		}

		&__content {
			display: flex;
			flex-direction: column;
			gap: vars.$spacing-md;
		}

		&__item {
			display: flex;
			align-items: center;
			padding: vars.$spacing-md;
			border-radius: vars.$border-radius-md;
			background-color: func.color-alpha(vars.$primary-color, 0.03);
			transition:
				transform 0.3s ease,
				box-shadow 0.3s ease;

			&:hover {
				transform: translateY(-2px);
				box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
				background-color: func.color-alpha(vars.$primary-color, 0.06);
			}
		}

		&__icon-wrapper {
			display: flex;
			align-items: center;
			justify-content: center;
			width: 38px;
			height: 38px;
			border-radius: 50%;
			background-color: func.color-alpha(vars.$primary-color, 0.1);
			color: vars.$primary-color;
			margin-right: vars.$spacing-md;
			flex-shrink: 0;
		}

		&__info {
			flex: 1;
		}

		&__label {
			color: vars.$gray;
			margin: 0 0 vars.$spacing-xxs 0;
			text-transform: uppercase;
			letter-spacing: 1px;
			font-weight: 600;
		}

		&__value {
			margin: 0;
			color: vars.$black-light;

			a {
				color: vars.$primary-color;
				text-decoration: none;
				transition: color 0.2s ease;

				&:hover {
					color: func.adjust-color-brightness(vars.$primary-color, -15%);
					text-decoration: underline;
				}
			}
		}

		&__social {
			margin-top: vars.$spacing-lg;
			padding-top: vars.$spacing-md;
			border-top: 1px solid func.color-alpha(vars.$gray-light, 0.5);
		}

		&__social-title {
			color: vars.$black;
			margin: 0 0 vars.$spacing-md 0;
		}

		&__social-links {
			display: flex;
			gap: 8px;
			flex-direction: column;
		}

		&__social-button {
			display: flex;
			align-items: center;
			gap: vars.$spacing-sm;
			color: vars.$gray-dark;
			background-color: vars.$white;
			padding: vars.$spacing-sm vars.$spacing-md;
			border-radius: vars.$border-radius-md;
			box-shadow: vars.$box-shadow;
			transition: all vars.$transition-base;

			&:hover {
				background-color: vars.$primary-color;
				color: vars.$white;
				transform: translateY(-3px);
			}
		}
	}

	@include mix.responsive(mobile) {
		.contact-card {
			padding: vars.$spacing-md;

			&__item {
				padding: vars.$spacing-sm;
			}
		}
	}
</style>
