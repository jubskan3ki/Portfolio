class FormDataBuilder {
    private formData: FormData;

    constructor() {
        this.formData = new FormData();
    }

    append(key: string, value: string | Blob): this {
        this.formData.append(key, value);
        return this;
    }

    appendIfPresent(key: string, value: string | number | null | undefined): this {
        if (value !== null && value !== undefined && value !== '') {
            this.formData.append(key, String(value));
        }
        return this;
    }

    appendFile(key: string, file: File | Blob | null | undefined): this {
        if (file instanceof File || file instanceof Blob) {
            this.formData.append(key, file);
        }
        return this;
    }

    appendArray(key: string, array: unknown[] | null | undefined): this {
        if (array && Array.isArray(array) && array.length > 0) {
            this.formData.append(key, JSON.stringify(array));
        }
        return this;
    }

    appendIds(key: string, items: Array<{ id: number | string } | number | string> | null | undefined): this {
        if (items && Array.isArray(items) && items.length > 0) {
            const ids = items.map((item) => (typeof item === 'object' ? item.id : item));
            this.formData.append(key, JSON.stringify(ids));
        }
        return this;
    }

    appendBoolean(key: string, value: boolean | null | undefined): this {
        if (value !== null && value !== undefined) {
            this.formData.append(key, value ? 'true' : 'false');
        }
        return this;
    }

    appendObject(key: string, obj: Record<string, unknown> | null | undefined): this {
        if (obj && typeof obj === 'object' && Object.keys(obj).length > 0) {
            this.formData.append(key, JSON.stringify(obj));
        }
        return this;
    }

    appendDate(key: string, date: Date | string | null | undefined): this {
        if (date) {
            const isoDate = date instanceof Date ? (date.toISOString().split('T')[0] ?? '') : date;
            this.formData.append(key, isoDate);
        }
        return this;
    }

    appendIf(condition: boolean, key: string, value: string | Blob): this {
        if (condition) {
            this.formData.append(key, value);
        }
        return this;
    }

    appendFromObject(
        obj: Record<string, unknown>,
        options: {
            exclude?: string[];
            include?: string[];
        } = {},
    ): this {
        const { exclude = [], include } = options;

        for (const [key, value] of Object.entries(obj)) {
            if (exclude.includes(key)) {
                continue;
            }
            if (include && !include.includes(key)) {
                continue;
            }
            if (value === null || value === undefined || value === '') {
                continue;
            }

            if (value instanceof File || value instanceof Blob) {
                this.formData.append(key, value);
            } else if (Array.isArray(value)) {
                this.formData.append(key, JSON.stringify(value));
            } else if (typeof value === 'boolean') {
                this.formData.append(key, value ? 'true' : 'false');
            } else if (typeof value === 'object') {
                this.formData.append(key, JSON.stringify(value));
            } else {
                this.formData.append(key, String(value));
            }
        }
        return this;
    }

    build(): FormData {
        return this.formData;
    }

    buildAndReset(): FormData {
        const result = this.formData;
        this.formData = new FormData();
        return result;
    }
}

export function createFormData(): FormDataBuilder {
    return new FormDataBuilder();
}
