// src/store/alert.ts
import { defineStore } from 'pinia';

import type { Alert, AlertOptions, AlertState } from '@/types/store/alert';

export const useAlertStore = defineStore('alert', {
	state: (): AlertState => ({
		alerts: [] as Alert[],
		counter: 0, // Pour générer des IDs uniques
	}),

	actions: {
		add(alert: AlertOptions): string {
			const id = String(++this.counter);

			// Ajouter l'alerte avec un ID unique
			this.alerts.push({
				...alert,
				id,
			});

			// Auto-suppression si autoClose est actif
			if (alert.autoClose !== false) {
				const timeout = alert.timeout || 5000;
				setTimeout(() => {
					this.remove(id);
				}, timeout);
			}

			return id;
		},

		remove(id: string): void {
			this.alerts = this.alerts.filter((a) => a.id !== id);
		},

		clear(): void {
			this.alerts = [];
		},
	},
});

export default useAlertStore;
