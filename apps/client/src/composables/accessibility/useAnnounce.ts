import { onMounted, onUnmounted } from 'vue';

let globalAnnouncer: HTMLElement | null = null;
let announcerRefCount = 0;

// Crée le nœud DOM sans toucher au refcount (lecture seule du singleton).
function ensureAnnouncerNode(): HTMLElement | null {
    if (typeof document === 'undefined') {
        return null;
    }

    if (!globalAnnouncer) {
        globalAnnouncer = document.createElement('div');
        globalAnnouncer.id = 'sr-announcer';
        globalAnnouncer.setAttribute('role', 'status');
        globalAnnouncer.setAttribute('aria-live', 'polite');
        globalAnnouncer.setAttribute('aria-atomic', 'true');
        globalAnnouncer.className = 'sr-only';
        globalAnnouncer.style.cssText =
            'position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border: 0;';
        document.body.appendChild(globalAnnouncer);
    }

    return globalAnnouncer;
}

function acquireAnnouncer(): HTMLElement | null {
    const node = ensureAnnouncerNode();
    if (node) {
        announcerRefCount++;
    }
    return node;
}

function releaseAnnouncer() {
    announcerRefCount--;
    if (announcerRefCount <= 0 && globalAnnouncer?.parentNode) {
        globalAnnouncer.parentNode.removeChild(globalAnnouncer);
        globalAnnouncer = null;
        announcerRefCount = 0;
    }
}

export function useAnnounce() {
    let announcer: HTMLElement | null = null;
    let pendingTimer: ReturnType<typeof setTimeout> | null = null;
    // announce() ne doit pas re-bumper le refcount (sinon le nœud #sr-announcer fuit).
    let acquired = false;

    onMounted(() => {
        announcer = acquireAnnouncer();
        acquired = true;
    });

    const announce = (message: string, priority: 'polite' | 'assertive' = 'polite') => {
        if (!announcer) {
            announcer = ensureAnnouncerNode();
        }

        if (announcer) {
            announcer.setAttribute('aria-live', priority);
            announcer.textContent = '';
            if (pendingTimer) {
                clearTimeout(pendingTimer);
            }
            pendingTimer = setTimeout(() => {
                if (announcer) {
                    announcer.textContent = message;
                }
                pendingTimer = null;
            }, 100);
        }
    };

    const announceLoading = (resource: string) => {
        announce(`Chargement de ${resource} en cours...`, 'polite');
    };

    const announceLoaded = (resource: string, count?: number) => {
        const countText =
            count !== undefined ? `, ${count} résultat${count > 1 ? 's' : ''} trouvé${count > 1 ? 's' : ''}` : '';
        announce(`${resource} chargé${countText}`, 'polite');
    };

    const announceError = (message: string) => {
        announce(`Erreur: ${message}`, 'assertive');
    };

    const announceSuccess = (message: string) => {
        announce(message, 'polite');
    };

    const announceNavigation = (pageName: string) => {
        announce(`Navigation vers ${pageName}`, 'polite');
    };

    onUnmounted(() => {
        if (pendingTimer) {
            clearTimeout(pendingTimer);
            pendingTimer = null;
        }
        // Ne libère que si cette instance a acquis (évite la sur-décrémentation).
        if (acquired) {
            releaseAnnouncer();
            acquired = false;
        }
    });

    return {
        announce,
        announceLoading,
        announceLoaded,
        announceError,
        announceSuccess,
        announceNavigation,
    };
}
