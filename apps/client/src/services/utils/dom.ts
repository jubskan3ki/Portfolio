// Compteur volontairement muté côté client uniquement : au niveau module il serait
// partagé entre toutes les requêtes SSR (dérive du compteur entre utilisateurs).
let overflowLockCount = 0;

export function lockBodyOverflow(): void {
    if (!import.meta.client) {
        return;
    }
    overflowLockCount++;
    if (overflowLockCount === 1) {
        document.body.style.overflow = 'hidden';
    }
}

export function unlockBodyOverflow(): void {
    if (!import.meta.client) {
        return;
    }
    overflowLockCount = Math.max(0, overflowLockCount - 1);
    if (overflowLockCount === 0) {
        document.body.style.overflow = '';
    }
}

export function resetBodyOverflow(): void {
    overflowLockCount = 0;
    if (import.meta.client) {
        document.body.style.overflow = '';
    }
}

export function downloadFile(blob: Blob, filename: string): void {
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}
