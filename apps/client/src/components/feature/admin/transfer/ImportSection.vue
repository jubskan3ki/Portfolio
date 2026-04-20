<template>
    <div class="admin-card">
        <div class="admin-card__header">
            <h2 class="admin-card__title">
                <BaseIcon name="upload" :size="20" />
                Importer des données
            </h2>
        </div>
        <div class="admin-card__body">
            <p class="import-description">
                Importez des données depuis un fichier JSON, CSV ou Excel. Les données existantes seront mises à jour.
            </p>

            <BaseSelect
                id="import-module"
                v-model="importModule"
                label="Module cible"
                placeholder="Sélectionner un module"
                :options="moduleOptions"
            />

            <FileDropZone
                id="import-file"
                :file="importFile"
                :error="fileError"
                accept=".json,.csv,.xlsx,.xls"
                accept-label="JSON, CSV, Excel (.xlsx) - Max 10MB"
                :max-size="MAX_FILE_SIZE"
                @update:file="handleFileUpdate"
                @update:error="fileError = $event"
            />

            <FilePreviewList
                :show="!!importModule"
                :images="images"
                @add-images="addImages"
                @remove-image="removeImage"
            />

            <ImportProgress
                :is-importing="isImporting"
                :can-import="!!importFile && !!importModule"
                :images-count="images.length"
                :update-existing="updateExisting"
                :skip-errors="skipErrors"
                @update:update-existing="updateExisting = $event"
                @update:skip-errors="skipErrors = $event"
                @import="handleImport"
            />
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref, reactive, onBeforeUnmount, toRaw } from 'vue';

    import BaseSelect from '@/components/base/BaseSelect.vue';
    import { formatFileSize, type TransferModule, type ImportImage } from '@/composables/data/useTransfer';

    import FileDropZone from './FileDropZone.vue';
    import FilePreviewList from './FilePreviewList.vue';
    import ImportProgress from './ImportProgress.vue';

    import type { ImageItem } from './FilePreviewList.vue';
    import type { SelectOption } from '@/types/components/base';

    defineProps<{
        moduleOptions: SelectOption[];
        isImporting: boolean;
    }>();

    const emit = defineEmits<{
        import: [
            module: TransferModule,
            file: File,
            options: { updateExisting: boolean; skipErrors: boolean; images?: ImportImage[] },
        ];
    }>();

    const fileError = ref<string | null>(null);
    const importModule = ref<TransferModule | ''>('');
    const importFile = ref<File | null>(null);
    const images = reactive<ImageItem[]>([]);
    const updateExisting = ref(true);
    const skipErrors = ref(false);

    // Validation constants
    const MAX_FILE_SIZE = 10 * 1024 * 1024;
    const MAX_IMAGE_SIZE = 5 * 1024 * 1024;
    const ALLOWED_EXTENSIONS = ['.json', '.csv', '.xlsx', '.xls'];
    const ALLOWED_MIME_TYPES = [
        'application/json',
        'text/csv',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-excel',
    ];
    const ALLOWED_IMAGE_TYPES = ['image/png', 'image/jpeg', 'image/jpg', 'image/webp', 'image/gif', 'image/svg+xml'];

    const validateFile = (file: File): string | null => {
        const extension = `.${file.name.split('.').pop()?.toLowerCase()}`;
        if (!ALLOWED_EXTENSIONS.includes(extension)) {
            return `Format non supporté. Formats acceptés: ${ALLOWED_EXTENSIONS.join(', ')}`;
        }
        if (!ALLOWED_MIME_TYPES.includes(file.type) && file.type !== 'text/plain') {
            return `Type de fichier non reconnu: ${file.type || 'inconnu'}`;
        }
        if (file.size > MAX_FILE_SIZE) {
            return `Le fichier est trop volumineux (max ${formatFileSize(MAX_FILE_SIZE)})`;
        }
        if (file.size === 0) {
            return 'Le fichier est vide';
        }
        return null;
    };

    const validateImage = (file: File): string | null => {
        if (!ALLOWED_IMAGE_TYPES.includes(file.type)) {
            return 'Type d\'image non supporté';
        }
        if (file.size > MAX_IMAGE_SIZE) {
            return `Image trop volumineuse (max ${formatFileSize(MAX_IMAGE_SIZE)})`;
        }
        return null;
    };

    const generateId = () => `img_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

    // File handling
    const handleFileUpdate = (file: File | null) => {
        if (!file) {
            importFile.value = null;
            fileError.value = null;
            return;
        }
        const error = validateFile(file);
        if (error) {
            fileError.value = error;
            importFile.value = null;
            return;
        }
        fileError.value = null;
        importFile.value = file;
    };

    // Images handling
    const addImages = (files: File[]) => {
        files.forEach((file) => {
            const error = validateImage(file);
            images.push({
                id: generateId(),
                file,
                preview: URL.createObjectURL(file),
                key: file.name.replace(/\.[^/.]+$/, ''),
                error: error || undefined,
            });
        });
    };

    const removeImage = (index: number) => {
        const img = images[index];
        if (img?.preview) {
            URL.revokeObjectURL(img.preview);
        }
        images.splice(index, 1);
    };

    const clearImages = () => {
        images.forEach((img) => {
            if (img.preview) {
                URL.revokeObjectURL(img.preview);
            }
        });
        images.length = 0;
    };

    // Import handler
    const handleImport = () => {
        if (!importFile.value || !importModule.value) {
            return;
        }

        const rawFile = toRaw(importFile.value);
        const validImages: ImportImage[] = images
            .filter((img) => !img.error)
            .map((img) => ({ key: img.key, file: toRaw(img.file) }));

        emit('import', importModule.value, rawFile, {
            updateExisting: updateExisting.value,
            skipErrors: skipErrors.value,
            images: validImages.length > 0 ? validImages : undefined,
        });
    };

    const resetForm = () => {
        importFile.value = null;
        fileError.value = null;
        clearImages();
        importModule.value = '';
    };

    onBeforeUnmount(() => {
        clearImages();
    });

    defineExpose({ resetForm });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;

    .admin-card {
        background: vars.$white;
        border-radius: 16px;
        border: 1px solid vars.$admin-border;
        padding: vars.$spacing-lg;
        box-shadow:
            0 1px 3px rgba(0, 0, 0, 0.02),
            0 4px 12px rgba(0, 0, 0, 0.02);

        &__header {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xxxxs;
            margin-bottom: vars.$spacing-lg;
            padding-bottom: vars.$spacing-xxxxs;
            border-bottom: 1px solid vars.$admin-border;
        }

        &__title {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xxxxs;
            font-weight: vars.$font-weight-semibold;
        }

        &__body {
            display: flex;
            flex-direction: column;
            gap: vars.$spacing-lg;
        }
    }

    .import-description {
        color: vars.$text-secondary;
        margin: 0;
    }
</style>
