<template>
	<div class="swiper-container" :class="{ 'swiper--fullwidth': fullwidth }">
		<div v-if="showControls && slides > slidesToShow" class="swiper__controls">
			<button
				class="swiper__arrow swiper__arrow--prev"
				:disabled="!canGoBack"
				aria-label="Précédent"
				@click="prev"
			>
				<BaseIcon name="chevron-left" :size="24" />
			</button>
		</div>

		<div ref="swiperRef" class="swiper__wrapper">
			<div class="swiper__track" :style="{ transform: `translateX(-${translateX}px)` }">
				<div
					v-for="idx in slides"
					:key="idx - 1"
					class="swiper__slide"
					:class="{ 'swiper__slide--active': activeIndex === idx - 1 }"
					:style="slideStyles"
				>
					<slot :name="`slide-${idx - 1}`" :index="idx - 1" :active="activeIndex === idx - 1" />
				</div>
			</div>
		</div>

		<div v-if="showControls && slides > slidesToShow" class="swiper__controls">
			<button
				class="swiper__arrow swiper__arrow--next"
				:disabled="!canGoForward"
				aria-label="Suivant"
				@click="next"
			>
				<BaseIcon name="chevron-right" :size="24" />
			</button>
		</div>

		<div v-if="showDots && slides > slidesToShow" class="swiper__dots">
			<button
				v-for="idx in totalDots"
				:key="idx - 1"
				class="swiper__dot"
				:class="{ 'swiper__dot--active': isDotActive(idx - 1) }"
				:aria-label="`Diapositive ${idx}`"
				@click="goToSlide((idx - 1) * slidesToScroll)"
			/>
		</div>
	</div>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import { computed, onMounted, onUnmounted, ref, watch } from 'vue';

	const props = defineProps({
		// Nombre total de slides
		slides: {
			type: Number,
			required: true,
		},
		// Nombre de slides à afficher à la fois
		slidesToShow: {
			type: Number,
			default: 1,
		},
		// Nombre de slides à défiler
		slidesToScroll: {
			type: Number,
			default: 1,
		},
		// Afficher les contrôles de navigation
		showControls: {
			type: Boolean,
			default: true,
		},
		// Afficher les indicateurs de pagination
		showDots: {
			type: Boolean,
			default: true,
		},
		// Défilement automatique
		autoplay: {
			type: Boolean,
			default: false,
		},
		// Intervalle de défilement automatique (en ms)
		autoplayInterval: {
			type: Number,
			default: 5000,
		},
		// Défilement infini
		infinite: {
			type: Boolean,
			default: false,
		},
		// Prendre toute la largeur disponible
		fullwidth: {
			type: Boolean,
			default: false,
		},
		// Hauteur fixe des slides
		height: {
			type: [String, Number],
			default: undefined,
		},
		// Espacement entre les slides
		gap: {
			type: Number,
			default: 16,
		},
	});

	const emit = defineEmits(['change']);

	// État du swiper
	const activeIndex = ref(0);
	const swiperRef = ref<HTMLElement | null>(null);
	const slideWidth = ref(0);
	const translateX = ref(0);
	let autoplayTimer: number | null = null;

	// Calculer le nombre total de points de pagination
	const totalDots = computed(() => {
		return Math.ceil((props.slides - props.slidesToShow + 1) / props.slidesToScroll);
	});

	// Styles pour les slides
	const slideStyles = computed(() => {
		return {
			width:
				props.slidesToShow > 1
					? `calc((100% / ${props.slidesToShow}) - ${(props.gap * (props.slidesToShow - 1)) / props.slidesToShow}px)`
					: '100%',
			marginRight: `${props.gap}px`,
			height: props.height ? `${props.height}px` : 'auto',
		};
	});

	// Déterminer si on peut naviguer vers l'avant ou l'arrière
	const canGoBack = computed(() => {
		return props.infinite || activeIndex.value > 0;
	});

	const canGoForward = computed(() => {
		return props.infinite || activeIndex.value < props.slides - props.slidesToShow;
	});

	// Vérifier si un point de pagination est actif
	const isDotActive = (dotIndex: number) => {
		const startSlide = dotIndex * props.slidesToScroll;
		const endSlide = Math.min(startSlide + props.slidesToScroll - 1, props.slides - 1);
		return activeIndex.value >= startSlide && activeIndex.value <= endSlide;
	};

	// Navigation vers la slide précédente
	const prev = () => {
		if (activeIndex.value > 0) {
			goToSlide(activeIndex.value - props.slidesToScroll);
		} else if (props.infinite) {
			goToSlide(props.slides - props.slidesToShow);
		}
	};

	// Navigation vers la slide suivante
	const next = () => {
		if (activeIndex.value < props.slides - props.slidesToShow) {
			goToSlide(activeIndex.value + props.slidesToScroll);
		} else if (props.infinite) {
			goToSlide(0);
		}
	};

	// Navigation vers une slide spécifique
	const goToSlide = (index: number) => {
		// S'assurer que l'index est dans les limites
		const maxIndex = props.slides - props.slidesToShow;
		const newIndex = Math.max(0, Math.min(index, maxIndex));

		activeIndex.value = newIndex;
		updateTranslateX();
		emit('change', activeIndex.value);

		// Réinitialiser le timer d'autoplay si activé
		if (props.autoplay && autoplayTimer) {
			clearInterval(autoplayTimer);
			startAutoplay();
		}
	};

	// Mettre à jour la translation pour l'animation
	const updateTranslateX = () => {
		if (swiperRef.value) {
			const slideWidthWithGap = slideWidth.value + props.gap;
			translateX.value = activeIndex.value * slideWidthWithGap;
		}
	};

	// Démarrer le défilement automatique
	const startAutoplay = () => {
		if (props.autoplay && props.slides > props.slidesToShow) {
			autoplayTimer = window.setInterval(() => {
				if (activeIndex.value < props.slides - props.slidesToShow) {
					next();
				} else if (props.infinite) {
					goToSlide(0);
				} else {
					goToSlide(0); // Revenir au début si pas infini
				}
			}, props.autoplayInterval);
		}
	};

	// Arrêter le défilement automatique
	const stopAutoplay = () => {
		if (autoplayTimer) {
			clearInterval(autoplayTimer);
			autoplayTimer = null;
		}
	};

	// Calculer les dimensions initiales
	const calculateDimensions = () => {
		if (swiperRef.value) {
			const containerWidth = swiperRef.value.offsetWidth;
			// Pour slidesToShow > 1, on divise la largeur du conteneur
			slideWidth.value =
				props.slidesToShow > 1
					? (containerWidth - props.gap * (props.slidesToShow - 1)) / props.slidesToShow
					: containerWidth;
			updateTranslateX();
		}
	};

	// Gérer le redimensionnement de la fenêtre
	const handleResize = () => {
		calculateDimensions();
	};

	// Setup des événements au montage
	onMounted(() => {
		calculateDimensions();
		window.addEventListener('resize', handleResize);

		if (props.autoplay) {
			startAutoplay();
		}
	});

	// Nettoyer les événements au démontage
	onUnmounted(() => {
		window.removeEventListener('resize', handleResize);
		stopAutoplay();
	});

	// Regarder les changements de props
	watch(() => props.slides, calculateDimensions);
	watch(() => props.slidesToShow, calculateDimensions);
	watch(
		() => props.autoplay,
		(newVal) => {
			if (newVal) {
				startAutoplay();
			} else {
				stopAutoplay();
			}
		}
	);

	// Exposer les méthodes publiques
	defineExpose({
		prev,
		next,
		goToSlide,
		currentSlide: activeIndex,
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.swiper-container {
		position: relative;
		width: 100%;
		margin: 0 auto;
		overflow: hidden;

		&.swiper--fullwidth {
			width: 100vw;
			margin-left: calc(-50vw + 50%);
			margin-right: calc(-50vw + 50%);
		}
	}

	.swiper {
		&__wrapper {
			overflow: hidden;
			width: 100%;
		}

		&__track {
			display: flex;
			transition: transform 0.5s ease-in-out;
		}

		&__slide {
			flex-shrink: 0;
			padding: 10px;
			position: relative;

			&--active {
				z-index: 1;
			}
		}

		&__controls {
			position: absolute;
			top: 50%;
			transform: translateY(-50%);
			z-index: 10;
			width: 100%;
			display: flex;
			justify-content: space-between;
			pointer-events: none;

			.swiper__arrow {
				pointer-events: auto;
			}
		}

		&__arrow {
			display: flex;
			justify-content: center;
			align-items: center;
			width: 40px;
			height: 40px;
			border-radius: 50%;
			background: func.color-alpha(vars.$white, 0.8);
			color: vars.$primary-color;
			box-shadow: vars.$box-shadow;
			cursor: pointer;
			transition: all vars.$transition-base;
			border: none;

			&:hover:not(:disabled) {
				background: vars.$white;
				transform: scale(1.1);
			}

			&:disabled {
				opacity: 0.5;
				cursor: not-allowed;
				transform: scale(1);
			}

			&--prev {
				margin-left: 12px;
			}

			&--next {
				margin-right: 12px;
			}
		}

		&__dots {
			display: flex;
			justify-content: center;
			gap: 8px;
			margin: 8px 0;
		}

		&__dot {
			width: 10px;
			height: 10px;
			border-radius: 50%;
			background-color: func.color-alpha(vars.$primary-color, 0.3);
			border: none;
			padding: 0;
			cursor: pointer;
			transition: all vars.$transition-base;

			&:hover {
				background-color: func.color-alpha(vars.$primary-color, 0.6);
			}

			&--active {
				background-color: vars.$primary-color;
				transform: scale(1.2);
			}
		}
	}
</style>
