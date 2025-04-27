<!-- src/components/loaders/Loader.vue -->
<template>
	<div class="loader-wrapper">
		<!-- Loader fullscreen -->
		<transition-group name="fade">
			<div
				v-for="loader in fullscreenLoaders"
				:key="loader.id"
				class="loader loader--fullscreen"
				:class="{ 'loader--with-overlay': loader.hasOverlay }"
			>
				<div class="loader__content">
					<Spinner :type="loader.type" :size="loader.size" :label="loader.label" />

					<button v-if="loader.cancelable" class="loader__cancel" @click="cancelLoader(loader.id)">
						Annuler
					</button>
				</div>
			</div>
		</transition-group>

		<!-- Loaders container pour les sections -->
		<teleport v-if="containerLoaders.length > 0" to="body">
			<div
				v-for="loader in containerLoaders"
				:key="loader.id"
				class="loader loader--container"
				:class="{ 'loader--with-overlay': loader.hasOverlay }"
				:style="getLoaderStyle(loader)"
			>
				<div class="loader__content">
					<Spinner :type="loader.type" :size="loader.size" :label="loader.label" />

					<button v-if="loader.cancelable" class="loader__cancel" @click="cancelLoader(loader.id)">
						Annuler
					</button>
				</div>
			</div>
		</teleport>

		<!-- Les loaders inline sont généralement gérés directement dans les composants -->
	</div>
</template>

<script setup lang="ts">
	import Spinner from '@/components/loaders/Spinner.vue';
	import { useLoaderStore } from '@/store/loader';
	import type { LoaderItem } from '@/types/store/loader';
	import { computed, onUnmounted } from 'vue';

	const loaderStore = useLoaderStore();

	// Obtenir les loaders actifs par type
	const fullscreenLoaders = computed(() => loaderStore.fullscreenLoaders);
	const containerLoaders = computed(() => loaderStore.containerLoaders);

	// Annuler un loader
	function cancelLoader(id: string) {
		loaderStore.stop(id);
	}

	// Calculer le style pour les loaders container basé sur le sélecteur cible
	function getLoaderStyle(loader: LoaderItem): Record<string, string> {
		if (!loader.targetSelector) {
			return {};
		}

		// Trouver l'élément cible
		const target = document.querySelector(loader.targetSelector);

		if (!target) {
			return {};
		}

		// Obtenir la position et les dimensions de l'élément cible
		const rect = target.getBoundingClientRect();

		return {
			position: 'absolute',
			top: `${rect.top + window.scrollY}px`,
			left: `${rect.left + window.scrollX}px`,
			width: `${rect.width}px`,
			height: `${rect.height}px`,
		};
	}

	// Nettoyage des loaders au démontage du composant
	onUnmounted(() => {
		// Optionnel : nettoyage des loaders au démontage
		// loaderStore.stopAll();
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.loader-wrapper {
		position: relative;
	}

	.loader {
		position: fixed;
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: func.z('modal') + 10; // Au-dessus des modales

		&--fullscreen {
			top: 0;
			left: 0;
			width: 100%;
			height: 100%;
		}

		&--container {
			border-radius: vars.$border-radius-md;
			overflow: hidden;
		}

		&--with-overlay {
			&::before {
				content: '';
				position: absolute;
				top: 0;
				left: 0;
				width: 100%;
				height: 100%;
				background-color: func.color-alpha(vars.$white, 0.8);
			}
		}

		&__content {
			position: relative;
			display: flex;
			flex-direction: column;
			align-items: center;
			justify-content: center;
			padding: vars.$spacing-md;
		}

		&__cancel {
			margin-top: vars.$spacing-md;
			padding: vars.$spacing-xs vars.$spacing-sm;
			border-radius: vars.$border-radius-sm;
			background-color: vars.$white;
			color: vars.$gray-dark;
			border: 1px solid vars.$gray-light;
			cursor: pointer;
			@include mix.transition(background-color, color);

			&:hover {
				background-color: vars.$white-dark;
				color: vars.$black;
			}
		}
	}

	// Animations
	.fade-enter-active,
	.fade-leave-active {
		transition: opacity 0.3s ease;
	}

	.fade-enter-from,
	.fade-leave-to {
		opacity: 0;
	}
</style>
