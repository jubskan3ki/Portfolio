import { API_ENDPOINTS, getBaseUrl } from '@/config/api';

type AuthFailureHandler = () => void | Promise<void>;

let authFailureHandler: AuthFailureHandler | null = null;

// Register callback for authentication failure (after token refresh fails)
export function onAuthFailure(handler: AuthFailureHandler): () => void {
    authFailureHandler = handler;
    return () => {
        authFailureHandler = null;
    };
}

export async function notifyAuthFailure(): Promise<void> {
    if (authFailureHandler) {
        try {
            await authFailureHandler();
        } catch {
            // Silent fail
        }
    }
}

// Token Refresh Manager (Singleton)
class RefreshTokenManager {
    private static instance: RefreshTokenManager;
    private isRefreshing = false;
    private refreshPromise: Promise<boolean> | null = null;
    private failedAttempts = 0;
    private lastFailTime = 0;
    private static readonly MAX_FAILED_ATTEMPTS = 2;
    private static readonly COOLDOWN_MS = 30000;

    static getInstance(): RefreshTokenManager {
        if (!RefreshTokenManager.instance) {
            RefreshTokenManager.instance = new RefreshTokenManager();
        }
        return RefreshTokenManager.instance;
    }

    refresh(): Promise<boolean> {
        // Check cooldown after too many failures
        if (this.failedAttempts >= RefreshTokenManager.MAX_FAILED_ATTEMPTS) {
            const elapsed = Date.now() - this.lastFailTime;
            if (elapsed < RefreshTokenManager.COOLDOWN_MS) {
                return Promise.resolve(false);
            }
            this.failedAttempts = 0;
        }

        // Si un refresh est déjà en cours, retourner la promise existante
        // Note: Cette vérification est atomique dans le contexte JS single-threaded
        // car la lecture de refreshPromise et le return sont synchrones
        if (this.refreshPromise) {
            return this.refreshPromise;
        }

        // Créer la promise AVANT d'assigner isRefreshing pour éviter les race conditions
        // Tout appel concurrent verra refreshPromise défini et attendra la même promise
        this.refreshPromise = (async () => {
            this.isRefreshing = true;
            try {
                const result = await this.performRefresh();
                if (result) {
                    this.failedAttempts = 0;
                } else {
                    this.failedAttempts++;
                    this.lastFailTime = Date.now();
                }
                return result;
            } finally {
                this.isRefreshing = false;
                this.refreshPromise = null;
            }
        })();

        return this.refreshPromise;
    }

    private async performRefresh(): Promise<boolean> {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000);

        try {
            const response = await fetch(`${getBaseUrl()}${API_ENDPOINTS.USERS.REFRESH}`, {
                method: 'POST',
                credentials: 'include',
                signal: controller.signal,
            });

            clearTimeout(timeoutId);
            return response.ok;
        } catch {
            clearTimeout(timeoutId);
            return false;
        }
    }

    get refreshing(): boolean {
        return this.isRefreshing;
    }

    reset(): void {
        this.failedAttempts = 0;
        this.lastFailTime = 0;
        this.isRefreshing = false;
        this.refreshPromise = null;
    }

    get isLikelyInvalid(): boolean {
        return this.failedAttempts >= RefreshTokenManager.MAX_FAILED_ATTEMPTS;
    }
}

export const refreshTokenManager = RefreshTokenManager.getInstance();
