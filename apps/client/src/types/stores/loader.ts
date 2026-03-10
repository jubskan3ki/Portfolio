// types/stores/loader.ts

// Types de positions disponibles pour les loaders
export type LoaderPosition = 'fullscreen' | 'container' | 'inline';

// Types d'affichage pour les loaders
export type LoaderType = 'circle' | 'dots';

// Tailles disponibles pour les loaders (compatible with SpinnerSize)
export type LoaderSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl';

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
