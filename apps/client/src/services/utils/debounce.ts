// src/services/utils/debounce.ts
import type {
	DebounceFunction,
	DebouncedFunction,
	ThrottleFunction,
	ThrottledFunction,
} from '@/types/services/utils/debounce';

/**
 * Crée une fonction qui retarde l'exécution de la fonction passée
 * jusqu'à ce que le délai spécifié se soit écoulé depuis la dernière fois
 * où la fonction debounce a été invoquée.
 */
export const debounce: DebounceFunction = <T extends (...args: any[]) => any>(
	fn: T,
	delay = 300
): DebouncedFunction<T> => {
	let timeoutId: ReturnType<typeof setTimeout> | null = null;

	return function (this: any, ...args: Parameters<T>): void {
		if (timeoutId) {
			clearTimeout(timeoutId);
		}

		timeoutId = setTimeout(() => {
			fn.apply(this, args);
			timeoutId = null;
		}, delay);
	};
};

/**
 * Crée une fonction qui n'est exécutée qu'une fois par intervalle de temps
 * spécifié, peu importe combien de fois la fonction est appelée pendant cet intervalle.
 */
export const throttle: ThrottleFunction = <T extends (...args: any[]) => any>(
	fn: T,
	limit = 300
): ThrottledFunction<T> => {
	let waiting = false;

	return function (this: any, ...args: Parameters<T>): void {
		if (!waiting) {
			fn.apply(this, args);
			waiting = true;
			setTimeout(() => {
				waiting = false;
			}, limit);
		}
	};
};
