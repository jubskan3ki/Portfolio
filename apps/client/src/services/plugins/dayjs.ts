// src/services/plugins/dayjs.ts
import dayjs from 'dayjs';
import 'dayjs/locale/fr';
import relativeTime from 'dayjs/plugin/relativeTime';
import type { NuxtApp } from 'nuxt/app';

import type { DayjsPluginFunctions, NuxtPluginDayjs } from '@/types/services/plugins/dayjs';

const dayjsPlugin: NuxtPluginDayjs = defineNuxtPlugin((_nuxtApp: NuxtApp) => {
	dayjs.extend(relativeTime);
	dayjs.locale('fr');

	return {
		provide: {
			dayjs,
			formatDate: (date: string | Date, format = 'DD/MM/YYYY') => dayjs(date).format(format),
			timeAgo: (date: string | Date) => dayjs(date).fromNow(),
			dateRange: (startDate: string | Date, endDate: string | Date | null) => {
				const start = dayjs(startDate).format('MMM YYYY');
				const end = endDate ? dayjs(endDate).format('MMM YYYY') : 'Présent';
				return `${start} - ${end}`;
			},
			experienceDuration: (startDate: string | Date, endDate: string | Date | null) => {
				const start = dayjs(startDate);
				const end = endDate ? dayjs(endDate) : dayjs();
				const years = end.diff(start, 'year');
				const months = end.diff(start, 'month') % 12;

				if (years === 0) {
					return `${months} mois`;
				} else if (months === 0) {
					return `${years} an${years > 1 ? 's' : ''}`;
				} else {
					return `${years} an${years > 1 ? 's' : ''} et ${months} mois`;
				}
			},
		} as DayjsPluginFunctions,
	};
});

export default dayjsPlugin;
