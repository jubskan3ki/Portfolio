// types/services/plugins/dayjs.ts

import type dayjs from 'dayjs';
import type { NuxtApp } from 'nuxt/app';

// Type pour les méthodes fournies par le plugin dayjs
export interface DayjsPluginFunctions {
	dayjs: typeof dayjs;
	formatDate: (date: string | Date, format?: string) => string;
	timeAgo: (date: string | Date) => string;
	dateRange: (startDate: string | Date, endDate: string | Date | null) => string;
	experienceDuration: (startDate: string | Date, endDate: string | Date | null) => string;
}

// Type pour le plugin Nuxt
export type NuxtPluginDayjs = (nuxtApp: NuxtApp) => {
	provide: DayjsPluginFunctions;
};
