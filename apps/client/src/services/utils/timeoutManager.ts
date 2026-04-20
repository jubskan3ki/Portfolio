// Map timeouts nommés + cleanup (utilisé par stores alert/loader/modal)
export class TimeoutManager {
    private timeouts = new Map<string, ReturnType<typeof setTimeout>>();

    set(id: string, callback: () => void, delay: number): void {
        this.clear(id);
        const timeoutId = setTimeout(callback, delay);
        this.timeouts.set(id, timeoutId);
    }

    clear(id: string): void {
        const timeout = this.timeouts.get(id);
        if (timeout !== undefined) {
            clearTimeout(timeout);
            this.timeouts.delete(id);
        }
    }

    has(id: string): boolean {
        return this.timeouts.has(id);
    }

    delete(id: string): void {
        this.timeouts.delete(id);
    }

    clearAll(): void {
        this.timeouts.forEach((timeoutId) => clearTimeout(timeoutId));
        this.timeouts.clear();
    }

    clearByIds(ids: string[]): void {
        ids.forEach((id) => this.clear(id));
    }
}
