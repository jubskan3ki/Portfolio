let overflowLockCount = 0;

export function lockBodyOverflow(): void {
    overflowLockCount++;
    if (import.meta.client && overflowLockCount === 1) {
        document.body.style.overflow = 'hidden';
    }
}

export function unlockBodyOverflow(): void {
    overflowLockCount = Math.max(0, overflowLockCount - 1);
    if (import.meta.client && overflowLockCount === 0) {
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
