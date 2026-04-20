import { API_ENDPOINTS, getBaseUrl } from '@/config/api';

import type { AuthFailureHandler } from '@/types/services/api';

let authFailureHandler: AuthFailureHandler | null = null;

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
            // silent
        }
    }
}

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
        // Cooldown après trop d'échecs
        if (this.failedAttempts >= RefreshTokenManager.MAX_FAILED_ATTEMPTS) {
            const elapsed = Date.now() - this.lastFailTime;
            if (elapsed < RefreshTokenManager.COOLDOWN_MS) {
                return Promise.resolve(false);
            }
            this.failedAttempts = 0;
        }

        // Dédup: single-flight refresh (lecture/return atomique JS single-threaded)
        if (this.refreshPromise) {
            return this.refreshPromise;
        }

        // Assigner refreshPromise AVANT await pour que les appels concurrents partagent la même promise
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
