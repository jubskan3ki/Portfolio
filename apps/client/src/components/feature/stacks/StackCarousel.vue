<template>
	<div class="stack-carousel">
		<div v-if="isLoading" class="stack-carousel__loader">
			<Spinner type="circle" label="Chargement des technologies..." />
		</div>

		<div v-else-if="error" class="stack-carousel__error">
			<p>{{ error }}</p>
		</div>

		<div v-else-if="stacks.length === 0" class="stack-carousel__empty">
			<EmptyState title="Aucune technologie" description="Aucune technologie n'est disponible pour le moment." />
		</div>

		<div v-else class="stack-carousel__content">
			<Swiper
				:slides="stacks.length"
				:slides-to-show="slidesToShow"
				:slides-to-scroll="1"
				:gap="4"
				:autoplay="autoplay"
				:autoplay-interval="5000"
				:show-controls="false"
				:show-dots="true"
			>
				<template v-for="(stack, index) in stacks" :key="stack.id" v-slot:[`slide-${index}`]>
					<StackCard :stack="stack" />
				</template>
			</Swiper>
		</div>
	</div>
</template>

<script setup lang="ts">
	import EmptyState from '@/components/feedback/EmptyState.vue';
	import Spinner from '@/components/loaders/Spinner.vue';
	import Swiper from '@/components/ui/Swiper.vue';
	import { useMock } from '@/services/api/useMock';
	import { computed, onMounted, onUnmounted, watch } from 'vue';
	import StackCard from './StackCard.vue';

	const props = defineProps({
		// Limite le nombre de technologies à afficher
		limit: {
			type: Number,
			default: undefined,
		},
		// Filtre par catégorie
		category: {
			type: String,
			default: undefined,
		},
		// Autoplay du carousel
		autoplay: {
			type: Boolean,
			default: true,
		},
	});

	// Utilisez le service useMock pour récupérer les données
	const { stacks, isLoading, error, fetchStacks } = useMock();

	// Calculer le nombre de slides à afficher en fonction de la largeur d'écran
	const slidesToShow = computed(() => {
		// Vérifie si window est défini (pour SSR)
		if (typeof window === 'undefined') return 1;

		const width = window.innerWidth;
		if (width < 768) return 1;
		if (width < 1024) return 2;
		return 4;
	});

	// Gestionnaire de redimensionnement
	const handleResize = () => {
		// Le calcul se fait automatiquement grâce à la propriété calculée
	};

	// Charger les technologies au montage du composant
	onMounted(async () => {
		window.addEventListener('resize', handleResize);
		await fetchStacks(props.limit);
	});

	// Nettoyer les event listeners
	onUnmounted(() => {
		window.removeEventListener('resize', handleResize);
	});

	// Recharger les technologies si les props changent
	watch(
		() => [props.limit, props.category],
		async () => {
			await fetchStacks(props.limit);
		}
	);
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;

	.stack-carousel {
		&__loader,
		&__error,
		&__empty {
			display: flex;
			justify-content: center;
			align-items: center;
			min-height: 200px;
		}
	}
</style>
