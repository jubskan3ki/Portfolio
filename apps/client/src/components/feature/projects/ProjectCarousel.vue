<template>
	<div class="project-carousel">
		<div v-if="isLoading" class="project-carousel__loader">
			<Spinner type="circle" label="Chargement des projets..." />
		</div>

		<div v-else-if="error" class="project-carousel__error">
			<p>{{ error }}</p>
		</div>

		<div v-else-if="projects.length === 0" class="project-carousel__empty">
			<EmptyState title="Aucun projet" description="Aucun projet n'est disponible pour le moment." />
		</div>

		<div v-else class="project-carousel__content">
			<Swiper
				:slides="projects.length"
				:slides-to-show="slidesToShow"
				:slides-to-scroll="1"
				:gap="4"
				:autoplay="autoplay"
				:autoplay-interval="5000"
				:show-controls="false"
				:show-dots="true"
			>
				<template v-for="(project, index) in projects" :key="project.id" v-slot:[`slide-${index}`]>
					<ProjectCard :project="project" />
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
	import ProjectCard from './ProjectCard.vue';

	const props = defineProps({
		// Limite le nombre de projets à afficher
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
	const { projects, isLoading, error, fetchProjects } = useMock();

	// Calculer le nombre de slides à afficher en fonction de la largeur d'écran
	const slidesToShow = computed(() => {
		// Vérifie si window est défini (pour SSR)
		if (typeof window === 'undefined') return 1;

		const width = window.innerWidth;
		if (width < 768) return 1;
		if (width < 1024) return 2;
		return 3;
	});

	// Gestionnaire de redimensionnement
	const handleResize = () => {
		// Le calcul se fait automatiquement grâce à la propriété calculée
	};

	// Charger les projets au montage du composant
	onMounted(async () => {
		window.addEventListener('resize', handleResize);
		await fetchProjects(props.limit, props.category);
	});

	// Nettoyer les event listeners
	onUnmounted(() => {
		window.removeEventListener('resize', handleResize);
	});

	// Recharger les projets si les props changent
	watch(
		() => [props.limit, props.category],
		async () => {
			await fetchProjects(props.limit, props.category);
		}
	);
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;

	.project-carousel {
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
