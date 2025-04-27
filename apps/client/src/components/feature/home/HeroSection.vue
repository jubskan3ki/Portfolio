<!-- components/feature/home/HeroSection.vue -->
<template>
	<section class="hero-section">
		<div class="container">
			<div class="hero-wrapper">
				<div class="hero-content">
					<h1 class="hero-title">
						Développeur <span class="text-primary">Web</span> &
						<span class="text-secondary">Mobile</span>
					</h1>
					<p class="hero-subtitle">
						Diplômé d'un Bachelor en Développement Web et actuellement en Mastère CTO & Tech Lead à HETIC,
						j'allie expertise technique et vision stratégique pour créer des solutions digitales modernes,
						performantes et innovantes.
					</p>
					<div class="hero-typing">
						<h2 class="hero-typing__prefix">Expert en</h2>
						<h2 class="hero-typing__text">{{ currentTypingText }}</h2>
						<h2 class="hero-typing__cursor"></h2>
					</div>
					<div class="hero-actions">
						<BaseButton :to="ROUTES.PROJECTS" variant="primary">
							<BaseIcon name="code" size="sm" class="mr-xs" />
							Voir mes projets
						</BaseButton>
						<BaseButton :to="ROUTES.CONTACT" variant="outline">
							<BaseIcon name="mail" size="sm" class="mr-xs" />
							Me contacter
						</BaseButton>
					</div>
				</div>

				<div class="hero-visual">
					<div class="hero-image-container">
						<img :src="images.others.profilePhoto" alt="Portrait" class="hero-image" />
					</div>
					<div class="hero-background-shape"></div>
					<div class="hero-tech-badges">
						<StackBadge
							v-for="(stack, index) in featuredStacks"
							:key="stack.id"
							:stack="stack"
							size="small"
							:class="['tech-badge', `tech-badge-${index + 1}`]"
						/>
					</div>
				</div>
			</div>
		</div>
	</section>
</template>

<script setup lang="ts">
	import BaseButton from '@/components/base/BaseButton.vue';
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import StackBadge from '@/components/feature/stacks/StackBadge.vue';
	import { images } from '@/config/images';
	import { ROUTES } from '@/config/routes';
	import { onBeforeUnmount, onMounted, ref } from 'vue';

	withDefaults(defineProps<HeroSectionProps>(), {
		featuredStacks: () => [],
	});

	// Définition de l'interface Stack pour le typage
	interface Stack {
		id: string | number;
		name: string;
		icon?: string;
		color?: string;
		level?: number;
		category?: string;
		[key: string]: any;
	}

	interface HeroSectionProps {
		featuredStacks: Stack[];
	}

	// Effet de machine à écrire
	const typingTexts = ['React.ts', 'Vue.ts', 'Nest.ts', 'Go', 'Flutter', 'Django'];

	const currentTypingText = ref('');
	const currentTextIndex = ref(0);
	const isDeleting = ref(false);
	const typingSpeed = ref(150);
	let typingTimer: ReturnType<typeof setTimeout> | null = null;

	const typeText = () => {
		const currentText = typingTexts[currentTextIndex.value];

		if (isDeleting.value) {
			currentTypingText.value = currentText.substring(0, currentTypingText.value.length - 1);
			typingSpeed.value = 50;
		} else {
			currentTypingText.value = currentText.substring(0, currentTypingText.value.length + 1);
			typingSpeed.value = 150;
		}

		if (!isDeleting.value && currentTypingText.value === currentText) {
			// Pause à la fin de l'écriture complète
			isDeleting.value = true;
			typingSpeed.value = 1500;
		} else if (isDeleting.value && currentTypingText.value === '') {
			isDeleting.value = false;
			currentTextIndex.value = (currentTextIndex.value + 1) % typingTexts.length;
			typingSpeed.value = 500;
		}

		typingTimer = setTimeout(typeText, typingSpeed.value);
	};

	onMounted(() => {
		typeText();
	});

	onBeforeUnmount(() => {
		if (typingTimer) {
			clearTimeout(typingTimer);
		}
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.hero-section {
		position: relative;
		padding: vars.$spacing-xxl 0;
		overflow: hidden;
		background: linear-gradient(
			135deg,
			func.color-alpha(vars.$primary-color, 0.08) 0%,
			func.color-alpha(vars.$secondary-color, 0.03) 100%
		);
	}

	.hero-wrapper {
		display: grid;
		grid-template-columns: 1.2fr 1fr;
		gap: vars.$spacing-xl;
		align-items: center;

		@include mix.responsive(tablet) {
			grid-template-columns: 1fr;
		}
	}

	.hero-content {
		@include mix.responsive(tablet) {
			text-align: center;
			order: 2;
		}
	}

	.hero-title {
		line-height: 1.1;
		font-weight: 800;
		margin-bottom: vars.$spacing-sm;

		span {
			position: relative;
			display: inline-block;
			z-index: 1;

			&.text-primary {
				color: vars.$primary-color;
			}

			&.text-secondary {
				color: vars.$secondary-color;
			}

			&::after {
				content: '';
				position: absolute;
				left: -5px;
				bottom: 5px;
				height: 12px;
				width: calc(100% + 10px);
				background-color: func.color-alpha(vars.$primary-color, 0.2);
				z-index: -1;
				transform: skewX(-5deg);
			}

			&.text-secondary::after {
				background-color: func.color-alpha(vars.$secondary-color, 0.2);
			}
		}
	}

	.hero-subtitle {
		color: vars.$gray-dark;
		margin-bottom: vars.$spacing-lg;
	}

	.hero-actions {
		display: flex;
		gap: vars.$spacing-md;
		margin-top: vars.$spacing-lg;

		@include mix.responsive(tablet) {
			justify-content: center;
		}

		@include mix.responsive(mobile) {
			flex-direction: column;
			width: 100%;
		}
	}

	.hero-typing {
		display: flex;
		align-items: center;
		gap: vars.$spacing-xs;
		min-height: 2rem;

		@include mix.responsive(tablet) {
			justify-content: center;
		}

		&__prefix {
			font-weight: 500;
			color: vars.$gray-dark;
		}

		&__text {
			font-weight: 700;
			color: vars.$primary-color;
		}

		&__cursor {
			display: inline-block;
			width: 2px;
			height: 1.4em;
			background-color: vars.$primary-color;
			margin-left: 2px;
			animation: blink 0.7s infinite;
		}
	}

	.hero-visual {
		position: relative;
		height: 100%;
		display: flex;
		justify-content: center;

		@include mix.responsive(tablet) {
			order: 1;
			margin-bottom: vars.$spacing-lg;
		}
	}

	.hero-image-container {
		position: relative;
		width: 320px;
		height: 320px;
		border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
		overflow: hidden;
		box-shadow: vars.$box-shadow-medium;
		border: 4px solid vars.$white;
		z-index: 2;
		transform-origin: center;
		animation: morphing 15s ease-in-out infinite;

		@include mix.responsive(mobile) {
			width: 280px;
			height: 280px;
		}
	}

	.hero-image {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}

	.hero-background-shape {
		position: absolute;
		top: -10%;
		right: -10%;
		width: 100%;
		height: 100%;
		border-radius: 30% 70% 50% 50% / 40% 40% 60% 60%;
		background: linear-gradient(
			135deg,
			func.color-alpha(vars.$primary-color, 0.8),
			func.color-alpha(vars.$secondary-color, 0.8)
		);
		z-index: 1;
		animation: rotate 25s linear infinite;
	}

	.hero-tech-badges {
		position: absolute;
		width: 100%;
		height: 100%;
		top: 0;
		left: 0;
		z-index: 3;
	}

	.tech-badge {
		position: absolute;
		animation: float 3s ease-in-out infinite;

		&-1 {
			top: 10%;
			left: 0;
			animation-delay: 0s;
		}

		&-2 {
			top: 20%;
			right: 5%;
			animation-delay: 0.5s;
		}

		&-3 {
			bottom: 15%;
			right: 10%;
			animation-delay: 1s;
		}

		&-4 {
			bottom: 5%;
			left: 15%;
			animation-delay: 1.5s;
		}

		&-5 {
			top: 40%;
			left: -5%;
			animation-delay: 2s;
		}
	}

	@keyframes blink {
		0%,
		100% {
			opacity: 1;
		}
		50% {
			opacity: 0;
		}
	}

	@keyframes float {
		0%,
		100% {
			transform: translateY(0);
		}
		50% {
			transform: translateY(-10px);
		}
	}

	@keyframes rotate {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}

	@keyframes morphing {
		0% {
			border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
		}
		25% {
			border-radius: 58% 42% 75% 25% / 76% 46% 54% 24%;
		}
		50% {
			border-radius: 50% 50% 33% 67% / 55% 27% 73% 45%;
		}
		75% {
			border-radius: 33% 67% 58% 42% / 63% 68% 32% 37%;
		}
		100% {
			border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
		}
	}
</style>
