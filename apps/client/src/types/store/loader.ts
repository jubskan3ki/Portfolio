// types/store/loader.ts
import type { ComputedRef } from 'vue';

// Types de positions disponibles pour les loaders
export type LoaderPosition = 'fullscreen' | 'container' | 'inline';

// Types d'affichage pour les loaders
export type LoaderType = 'circle' | 'dots' | 'pulse';

// Tailles disponibles pour les loaders
export type LoaderSize = 'small' | 'medium' | 'large';

// Interface pour les options de configuration d'un loader
export interface LoaderOptions {
	id?: string;
	position?: LoaderPosition;
	type?: LoaderType;
	size?: LoaderSize;
	label?: string;
	hasOverlay?: boolean;
	delay?: number;
	cancelable?: boolean;
	targetSelector?: string;
}

// Interface pour un loader actif dans le store
export interface LoaderItem {
	id: string;
	position: LoaderPosition;
	type: LoaderType;
	size: LoaderSize;
	label: string;
	hasOverlay: boolean;
	delay: number;
	cancelable: boolean;
	targetSelector?: string;
	startTime: number;
}

// Interface pour l'état du store de loaders
export interface LoaderState {
	loaders: LoaderItem[];
	isLoading: boolean;
}

// Interface pour les getters du store de loaders
export interface LoaderGetters {
	isLoadingById: (id: string) => boolean;
	fullscreenLoaders: LoaderItem[];
	containerLoaders: LoaderItem[];
	inlineLoaders: LoaderItem[];
}

// Interface pour les actions du store de loaders
export interface LoaderActions {
	start(options?: LoaderOptions): string;
	stop(id: string): void;
	stopAll(): void;
	stopByPosition(position: LoaderPosition): void;
}

// Interface de retour pour le composable useLoader
export interface UseLoaderReturn {
	isLoading: ComputedRef<boolean>;
	activeLoaders: ComputedRef<LoaderItem[]>;
	fullscreenLoaders: ComputedRef<LoaderItem[]>;
	containerLoaders: ComputedRef<LoaderItem[]>;
	inlineLoaders: ComputedRef<LoaderItem[]>;
	startLoader: (options?: LoaderOptions) => string;
	stopLoader: (id: string) => void;
	stopAllLoaders: () => void;
	isLoadingById: (id: string) => boolean;
	withLoader: <T>(fn: () => Promise<T>, options?: LoaderOptions) => Promise<T>;
	loadData: <T>(fn: () => Promise<T>, options?: LoaderOptions) => Promise<T>;
	startFullscreenLoader: (options?: Omit<LoaderOptions, 'position'>) => string;
	startContainerLoader: (options?: Omit<LoaderOptions, 'position'>) => string;
	startInlineLoader: (options?: Omit<LoaderOptions, 'position'>) => string;
}
