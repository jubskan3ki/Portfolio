import { useAlertStore } from '@/stores/alert';

import type { NotifyOptions, UseAlertReturn } from '@/types/stores/alert';

export function useAlert(): UseAlertReturn {
    const alertStore = useAlertStore();

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

    function removeNotification(id: string): void {
        alertStore.remove(id);
    }

    function clearAllNotifications(): void {
        alertStore.clear();
    }

    function success(message: string, title?: string, options: Partial<NotifyOptions> = {}): string {
        return notify({
            message,
            title,
            type: 'success',
            ...options,
        });
    }

    function error(message: string, title?: string, options: Partial<NotifyOptions> = {}): string {
        return notify({
            message,
            title,
            type: 'error',
            ...options,
        });
    }

    function warning(message: string, title?: string, options: Partial<NotifyOptions> = {}): string {
        return notify({
            message,
            title,
            type: 'warning',
            ...options,
        });
    }

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
