// types/services/utils/httpClient.ts

// Méthodes HTTP supportées
export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

// Type pour les réponses d'erreur API
export interface ApiErrorResponse {
	detail?: string;
	error?: string;
	message?: string;
	status?: number;
}

// Type pour la fonction de construction d'URL
export type BuildUrlFunction = (endpoint: string, params?: Record<string, any>) => string;

// Type pour la fonction principale de requête API
export type FetchApiFunction = <T>(
	endpoint: string,
	method?: HttpMethod,
	data?: any,
	params?: Record<string, any>
) => Promise<T>;

// Interface pour le client API
export interface ApiClient {
	get: <T = any>(endpoint: string, params?: Record<string, any>) => Promise<T>;
	post: <T = any>(endpoint: string, data?: any) => Promise<T>;
	put: <T = any>(endpoint: string, data?: any) => Promise<T>;
	patch: <T = any>(endpoint: string, data?: any) => Promise<T>;
	delete: <T = any>(endpoint: string) => Promise<T>;
	uploadForm: <T = any>(endpoint: string, formData: FormData, method?: 'POST' | 'PUT' | 'PATCH') => Promise<T>;
}
