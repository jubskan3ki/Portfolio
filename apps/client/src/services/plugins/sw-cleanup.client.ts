// Unregister SW + purge Cache Storage pour éviter de servir des assets périmés d'un ancien build PWA
export default defineNuxtPlugin(() => {
    if (typeof window === 'undefined') {
        return;
    }

    if ('serviceWorker' in navigator) {
        navigator.serviceWorker
            .getRegistrations()
            .then((regs) => Promise.all(regs.map((r) => r.unregister())))
            .then((results) => {
                if (results.length > 0) {
                    console.info('[sw-cleanup] Unregistered', results.length, 'service worker(s)');
                }
            })
            .catch(() => {});
    }

    if ('caches' in window) {
        caches
            .keys()
            .then((keys) => Promise.all(keys.map((k) => caches.delete(k))))
            .then((results) => {
                if (results.length > 0) {
                    console.info('[sw-cleanup] Deleted', results.length, 'cache(s)');
                }
            })
            .catch(() => {});
    }
});
