import { onMounted, onUnmounted } from 'vue';

let globalAnnouncer: HTMLElement | null = null;
let announcerRefCount = 0;

function getOrCreateAnnouncer(): HTMLElement | null {
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
        globalAnnouncer.style.cssText
            = 'position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border: 0;';
        document.body.appendChild(globalAnnouncer);
    }

    announcerRefCount++;
    return globalAnnouncer;
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

    onMounted(() => {
        announcer = getOrCreateAnnouncer();
    });

    const announce = (message: string, priority: 'polite' | 'assertive' = 'polite') => {
        if (!announcer) {
            announcer = getOrCreateAnnouncer();
        }

        if (announcer) {
            announcer.setAttribute('aria-live', priority);
            announcer.textContent = '';
            setTimeout(() => {
                if (announcer) {
                    announcer.textContent = message;
                }
            }, 100);
        }
    };

    const announceLoading = (resource: string) => {
        announce(`Chargement de ${resource} en cours...`, 'polite');
    };

    const announceLoaded = (resource: string, count?: number) => {
        const countText
            = count !== undefined ? `, ${count} résultat${count > 1 ? 's' : ''} trouvé${count > 1 ? 's' : ''}` : '';
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
        releaseAnnouncer();
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
