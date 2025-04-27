// types/services/utils/debounce.ts

// Type pour une fonction debounce générique
export type DebouncedFunction<T extends (...args: any[]) => any> = (...args: Parameters<T>) => void;

// Type pour la fonction debounce
export type DebounceFunction = <T extends (...args: any[]) => any>(fn: T, delay?: number) => DebouncedFunction<T>;

// Type pour une fonction throttle générique
export type ThrottledFunction<T extends (...args: any[]) => any> = (...args: Parameters<T>) => void;

// Type pour la fonction throttle
export type ThrottleFunction = <T extends (...args: any[]) => any>(fn: T, limit?: number) => ThrottledFunction<T>;
