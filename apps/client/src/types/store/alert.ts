// types/store/alert.ts

// Types d'alertes disponibles
export type AlertType = 'success' | 'error' | 'warning' | 'info';

// Interface pour une alerte
export interface Alert {
	id: string;
	message: string;
	type: AlertType;
	title?: string;
	autoClose?: boolean;
	timeout?: number;
	dismissible?: boolean;
}

// Interface pour l'état du store d'alertes
export interface AlertState {
	alerts: Alert[];
	counter: number; // Pour générer des IDs uniques
}

// Interface pour les paramètres d'ajout d'une alerte (sans l'ID)
export type AlertOptions = Omit<Alert, 'id'>;

// Interface pour les getters du store d'alertes
export interface AlertGetters {
	// Actuellement pas de getters spécifiques
}

// Interface pour les actions du store d'alertes
export interface AlertActions {
	add(alert: AlertOptions): string;
	remove(id: string): void;
	clear(): void;
}

// Interface pour les paramètres de notifications simplifiés
export interface NotifyOptions {
	message: string;
	type?: AlertType;
	title?: string;
	autoClose?: boolean;
	timeout?: number;
	dismissible?: boolean;
}

// Interface pour le composable useAlert
export interface UseAlertReturn {
	notify: (options: NotifyOptions) => string;
	success: (message: string, title?: string, options?: Partial<NotifyOptions>) => string;
	error: (message: string, title?: string, options?: Partial<NotifyOptions>) => string;
	warning: (message: string, title?: string, options?: Partial<NotifyOptions>) => string;
	info: (message: string, title?: string, options?: Partial<NotifyOptions>) => string;
	removeNotification: (id: string) => void;
	clearAllNotifications: () => void;
}
