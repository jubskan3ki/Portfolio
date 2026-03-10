// Constants pour la gestion d'erreurs

import type { ApiErrorCode } from '@/types/api/common';

export interface ErrorInfo {
    message: string;
    code: ApiErrorCode | 'UNKNOWN';
    status: number;
    details?: Record<string, string[]>;
    isRetryable: boolean;
}

export const API_ERROR_MESSAGES: Record<ApiErrorCode | 'UNKNOWN', string> = {
    VALIDATION_ERROR: 'Veuillez vérifier les informations saisies',
    AUTH_ERROR: 'Authentification requise',
    FORBIDDEN: 'Action non autorisée',
    NOT_FOUND: 'Ressource introuvable',
    RATE_LIMITED: 'Trop de requêtes, veuillez réessayer plus tard',
    SERVER_ERROR: 'Erreur serveur, veuillez réessayer plus tard',
    NETWORK_ERROR: 'Erreur de connexion, vérifiez votre connexion internet',
    TIMEOUT: 'La requête a expiré, veuillez réessayer',
    UNKNOWN: 'Une erreur inattendue est survenue',
};

export const RETRYABLE_ERRORS: ApiErrorCode[] = ['SERVER_ERROR', 'NETWORK_ERROR', 'TIMEOUT', 'RATE_LIMITED'];
