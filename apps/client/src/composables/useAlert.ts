// src/composables/useAlert.ts
import { useAlertStore } from '@/store/alert';
import type { NotifyOptions, UseAlertReturn } from '@/types/store/alert';

/**
 * Composable pour la gestion des alertes et notifications
 */
export function useAlert(): UseAlertReturn {
	const alertStore = useAlertStore();

	/**
	 * Affiche une notification avec les options spécifiées
	 */
	function notify(options: NotifyOptions): string {
		return alertStore.add({
			message: options.message,
			type: options.type || 'info',
			title: options.title,
			autoClose: options.autoClose,
			timeout: options.timeout,
			dismissible: options.dismissible !== false,
		});
	}

	/**
	 * Supprime une notification par son ID
	 */
	function removeNotification(id: string): void {
		alertStore.remove(id);
	}

	/**
	 * Supprime toutes les notifications
	 */
	function clearAllNotifications(): void {
		alertStore.clear();
	}

	/**
	 * Affiche une notification de succès
	 */
	function success(message: string, title?: string, options: Partial<NotifyOptions> = {}): string {
		return notify({
			message,
			title,
			type: 'success',
			...options,
		});
	}

	/**
	 * Affiche une notification d'erreur
	 */
	function error(message: string, title?: string, options: Partial<NotifyOptions> = {}): string {
		return notify({
			message,
			title,
			type: 'error',
			...options,
		});
	}

	/**
	 * Affiche une notification d'avertissement
	 */
	function warning(message: string, title?: string, options: Partial<NotifyOptions> = {}): string {
		return notify({
			message,
			title,
			type: 'warning',
			...options,
		});
	}

	/**
	 * Affiche une notification d'information
	 */
	function info(message: string, title?: string, options: Partial<NotifyOptions> = {}): string {
		return notify({
			message,
			title,
			type: 'info',
			...options,
		});
	}

	return {
		notify,
		success,
		error,
		warning,
		info,
		removeNotification,
		clearAllNotifications,
	};
}

export default useAlert;
