// src/store/loader.ts
import { defineStore } from 'pinia';

import type { LoaderItem, LoaderOptions, LoaderPosition, LoaderState } from '@/types/store/loader';

export const useLoaderStore = defineStore('loader', {
	state: (): LoaderState => ({
		loaders: [],
		isLoading: false,
	}),

	getters: {
		/**
		 * Vérifie si un loader avec un ID spécifique est actif
		 */
		isLoadingById: (state) => (id: string) => {
			return state.loaders.some((loader) => loader.id === id);
		},

		/**
		 * Obtient tous les loaders fullscreen actifs
		 */
		fullscreenLoaders: (state) => {
			return state.loaders.filter((loader) => loader.position === 'fullscreen');
		},

		/**
		 * Obtient tous les loaders container actifs
		 */
		containerLoaders: (state) => {
			return state.loaders.filter((loader) => loader.position === 'container');
		},

		/**
		 * Obtient tous les loaders inline actifs
		 */
		inlineLoaders: (state) => {
			return state.loaders.filter((loader) => loader.position === 'inline');
		},
	},

	actions: {
		/**
		 * Démarre un nouveau loader
		 */
		start(options: LoaderOptions = {}): string {
			// Générer un ID unique si non fourni
			const id = options.id || `loader-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;

			// Créer le loader avec les options par défaut et personnalisées
			const loader: LoaderItem = {
				id,
				position: options.position || 'fullscreen',
				type: options.type || 'circle',
				size: options.size || 'medium',
				label: options.label || 'Chargement...',
				hasOverlay: options.hasOverlay !== undefined ? options.hasOverlay : true,
				delay: options.delay || 0,
				cancelable: options.cancelable || false,
				targetSelector: options.targetSelector,
				startTime: Date.now(),
			};

			// Si le loader a un délai, on l'ajoute après le délai
			if (loader.delay > 0) {
				setTimeout(() => {
					// Vérifier si le loader n'a pas déjà été stoppé
					if (!this.isLoadingById(id)) {
						this.loaders.push(loader);
						this.isLoading = true;
					}
				}, loader.delay);
			} else {
				// Ajouter le loader immédiatement
				this.loaders.push(loader);
				this.isLoading = true;
			}

			return id;
		},

		/**
		 * Arrête un loader spécifique par son ID
		 */
		stop(id: string): void {
			const index = this.loaders.findIndex((loader) => loader.id === id);

			if (index !== -1) {
				this.loaders.splice(index, 1);

				// Mettre à jour l'état global de chargement
				this.isLoading = this.loaders.length > 0;
			}
		},

		/**
		 * Arrête tous les loaders
		 */
		stopAll(): void {
			this.loaders = [];
			this.isLoading = false;
		},

		/**
		 * Arrête tous les loaders d'une position spécifique
		 */
		stopByPosition(position: LoaderPosition): void {
			this.loaders = this.loaders.filter((loader) => loader.position !== position);
			this.isLoading = this.loaders.length > 0;
		},
	},
});

export default useLoaderStore;
