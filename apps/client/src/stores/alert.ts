// Store Pinia pour les alertes - utiliser useAlert composable
import { defineStore } from 'pinia';
import { ref } from 'vue';

import { TIMEOUTS } from '@/config/constants';
import { TimeoutManager } from '@/services/utils/timeoutManager';

import type { Alert, AlertOptions } from '@/types/stores/alert';

export const useAlertStore = defineStore('alert', () => {
    // State
    const alerts = ref<Alert[]>([]);
    const counter = ref(0);
    const alertTimeouts = new TimeoutManager();

    // Actions
    function add(alert: AlertOptions): string {
        const id = String(++counter.value);

        alerts.value.push({
            ...alert,
            id,
        });

        // Auto-suppression avec timeout trackable
        if (alert.autoClose !== false) {
            const timeout = alert.timeout || TIMEOUTS.ALERT_DEFAULT;
            alertTimeouts.set(
                id,
                () => {
                    remove(id);
                },
                timeout,
            );
        }

        return id;
    }

    function remove(id: string): void {
        alertTimeouts.clear(id);
        alerts.value = alerts.value.filter((a) => a.id !== id);
    }

    function clear(): void {
        alertTimeouts.clearAll();
        alerts.value = [];
    }

    return {
        alerts,
        add,
        remove,
        clear,
    };
});
