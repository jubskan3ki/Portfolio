// Kill-switch SW: unregisters a lingering prod SW in dev (it would serve stale
// /_nuxt/* with wrong MIME and break hydration). Clears caches then reloads clients.
export default defineEventHandler((event) => {
    setHeader(event, 'Content-Type', 'application/javascript; charset=utf-8');
    setHeader(event, 'Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0');
    setHeader(event, 'Service-Worker-Allowed', '/');
    return `
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (event) => {
    event.waitUntil((async () => {
        try {
            const keys = await caches.keys();
            await Promise.all(keys.map((k) => caches.delete(k)));
        } catch (e) {}
        try {
            await self.registration.unregister();
        } catch (e) {}
        const clientsList = await self.clients.matchAll({ type: 'window' });
        clientsList.forEach((client) => client.navigate(client.url));
    })());
});
`;
});
