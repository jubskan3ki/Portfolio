// src/composables/useLoader.ts
import { computed } from 'vue';

import { useLoaderStore } from '@/store/loader';
import type { LoaderOptions, UseLoaderReturn } from '@/types/store/loader';

/**
 * Composable pour la gestion des indicateurs de chargement
 */
export function useLoader(): UseLoaderReturn {
	const loaderStore = useLoaderStore();

	/**
	 * État global de chargement
	 */
	const isLoading = computed(() => loaderStore.isLoading);

	/**
	 * Liste des loaders actifs
	 */
	const activeLoaders = computed(() => loaderStore.loaders);

	/**
	 * Liste des loaders fullscreen actifs
	 */
	const fullscreenLoaders = computed(() => loaderStore.fullscreenLoaders);

	/**
	 * Liste des loaders container actifs
	 */
	const containerLoaders = computed(() => loaderStore.containerLoaders);

	/**
	 * Liste des loaders inline actifs
	 */
	const inlineLoaders = computed(() => loaderStore.inlineLoaders);

	/**
	 * Démarre un nouveau loader
	 */
	function startLoader(options: LoaderOptions = {}): string {
		return loaderStore.start(options);
	}

	/**
	 * Arrête un loader spécifique par son ID
	 */
	function stopLoader(id: string): void {
		loaderStore.stop(id);
	}

	/**
	 * Arrête tous les loaders
	 */
	function stopAllLoaders(): void {
		loaderStore.stopAll();
	}

	/**
	 * Vérifie si un loader spécifique est actif
	 */
	function isLoadingById(id: string): boolean {
		return loaderStore.isLoadingById(id);
	}

	/**
	 * Exécute une fonction asynchrone avec un loader
	 */
	async function withLoader<T>(fn: () => Promise<T>, options: LoaderOptions = {}): Promise<T> {
		const loaderId = startLoader(options);

		try {
			const result = await fn();
			return result;
		} finally {
			stopLoader(loaderId);
		}
	}

	/**
	 * Charge des données avec un loader
	 */
	async function loadData<T>(fn: () => Promise<T>, options: LoaderOptions = {}): Promise<T> {
		const defaultOptions: LoaderOptions = {
			position: 'container',
			delay: 300, // Délai par défaut pour éviter les flashs sur les chargements rapides
			...options,
		};

		return withLoader(fn, defaultOptions);
	}

	/**
	 * Démarre un loader fullscreen
	 */
	function startFullscreenLoader(options: Omit<LoaderOptions, 'position'> = {}): string {
		return startLoader({
			...options,
			position: 'fullscreen',
		});
	}

	/**
	 * Démarre un loader container
	 */
	function startContainerLoader(options: Omit<LoaderOptions, 'position'> = {}): string {
		return startLoader({
			...options,
			position: 'container',
		});
	}

	/**
	 * Démarre un loader inline
	 */
	function startInlineLoader(options: Omit<LoaderOptions, 'position'> = {}): string {
		return startLoader({
			...options,
			position: 'inline',
		});
	}

	return {
		isLoading,
		activeLoaders,
		fullscreenLoaders,
		containerLoaders,
		inlineLoaders,
		startLoader,
		stopLoader,
		stopAllLoaders,
		isLoadingById,
		withLoader,
		loadData,
		startFullscreenLoader,
		startContainerLoader,
		startInlineLoader,
	};
}

export default useLoader;
