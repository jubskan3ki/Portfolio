// src/services/utils/httpClient.ts
import { API_BASE_URL } from '@/config/api';
import type {
	ApiClient,
	ApiErrorResponse,
	BuildUrlFunction,
	FetchApiFunction,
	HttpMethod,
} from '@/types/services/utils/httpClient';

// Options par défaut pour les requêtes fetch
const defaultOptions: RequestInit = {
	headers: {
		'Content-Type': 'application/json',
	},
	credentials: 'same-origin',
};

// Fonction d'aide pour construire des URLs
const buildUrl: BuildUrlFunction = (endpoint: string, params?: Record<string, any>): string => {
	const url = new URL(`${API_BASE_URL}${endpoint}`);

	if (params) {
		Object.entries(params).forEach(([key, value]) => {
			if (value !== undefined && value !== null) {
				url.searchParams.append(key, String(value));
			}
		});
	}

	return url.toString();
};

// Fonction principale pour les requêtes
const fetchApi: FetchApiFunction = async <T>(
	endpoint: string,
	method: HttpMethod = 'GET',
	data?: any,
	params?: Record<string, any>
): Promise<T> => {
	const url = buildUrl(endpoint, params);

	const options: RequestInit = {
		...defaultOptions,
		method,
	};

	// Ajouter le corps de la requête pour les méthodes autres que GET
	if (data && method !== 'GET') {
		options.body = JSON.stringify(data);
	}

	const response = await fetch(url, options);

	// Vérifier si la réponse est OK (statut 2xx)
	if (!response.ok) {
		let errorData: ApiErrorResponse;

		try {
			errorData = await response.json();
		} catch (e) {
			console.error('Error parsing JSON response:', e);
			errorData = {
				status: response.status,
				message: response.statusText,
			};
		}

		throw errorData;
	}

	// Pour les réponses 204 No Content
	if (response.status === 204) {
		return {} as T;
	}

	return response.json();
};

// API simplifiée
export const api: ApiClient = {
	get: <T = any>(endpoint: string, params?: Record<string, any>): Promise<T> => {
		return fetchApi<T>(endpoint, 'GET', undefined, params);
	},

	post: <T = any>(endpoint: string, data?: any): Promise<T> => {
		return fetchApi<T>(endpoint, 'POST', data);
	},

	put: <T = any>(endpoint: string, data?: any): Promise<T> => {
		return fetchApi<T>(endpoint, 'PUT', data);
	},

	patch: <T = any>(endpoint: string, data?: any): Promise<T> => {
		return fetchApi<T>(endpoint, 'PATCH', data);
	},

	delete: <T = any>(endpoint: string): Promise<T> => {
		return fetchApi<T>(endpoint, 'DELETE');
	},

	// Gestion des formulaires et des fichiers
	uploadForm: <T = any>(
		endpoint: string,
		formData: FormData,
		method: 'POST' | 'PUT' | 'PATCH' = 'POST'
	): Promise<T> => {
		const url = buildUrl(endpoint);

		const options: RequestInit = {
			method,
			credentials: 'same-origin',
			body: formData,
			// Ne pas spécifier Content-Type pour que le navigateur ajoute le boundary correct
		};

		return fetch(url, options).then((response) => {
			if (!response.ok) {
				return response.json().then((errorData) => {
					throw errorData;
				});
			}

			return response.json();
		});
	},
};

export default api;
