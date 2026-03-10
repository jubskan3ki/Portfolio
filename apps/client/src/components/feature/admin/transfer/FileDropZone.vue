<template>
    <div class="file-drop-zone-wrapper">
        <label :id="labelId" :for="inputId" class="sr-only">
            <slot name="sr-label"> Sélectionner un fichier ({{ acceptLabel }}) </slot>
        </label>
        <div
            class="file-drop-zone"
            :class="{
                'file-drop-zone--dragover': isDragging,
                'file-drop-zone--error': !!error,
                'file-drop-zone--has-file': !!file,
            }"
            role="button"
            tabindex="0"
            :aria-labelledby="labelId"
            :aria-describedby="error ? errorId : undefined"
            @click="triggerInput"
            @keydown.enter="triggerInput"
            @keydown.space.prevent="triggerInput"
            @dragover.prevent="isDragging = true"
            @dragleave="isDragging = false"
            @drop.prevent="handleDrop"
        >
            <input
                :id="inputId"
                ref="inputRef"
                type="file"
                class="file-drop-zone__input"
                :accept="accept"
                :multiple="multiple"
                :aria-labelledby="labelId"
                @change="handleSelect"
            />
            <slot v-if="!file" name="placeholder">
                <div class="file-drop-zone__placeholder">
                    <BaseIcon :name="placeholderIcon" :size="40" class="file-drop-zone__icon" />
                    <p class="file-drop-zone__text">{{ placeholderText }}</p>
                    <small class="file-drop-zone__hint">{{ acceptLabel }}</small>
                </div>
            </slot>
            <slot v-else name="selected" :file="file" :remove="handleRemove">
                <div class="file-drop-zone__selected">
                    <BaseIcon name="file" :size="32" />
                    <div class="file-drop-zone__info">
                        <span class="file-drop-zone__filename">{{ file.name }}</span>
                        <small class="file-drop-zone__size">{{ formatFileSize(file.size) }}</small>
                    </div>
                    <button
                        type="button"
                        class="file-drop-zone__remove"
                        aria-label="Supprimer le fichier sélectionné"
                        @click.stop="handleRemove"
                    >
                        <BaseIcon name="x" :size="16" />
                    </button>
                </div>
            </slot>
        </div>
        <p v-if="error" :id="errorId" class="file-drop-zone__error" role="alert">
            <BaseIcon name="alert-circle" :size="14" />
            {{ error }}
        </p>
    </div>
</template>

<script setup lang="ts">
    import { ref, computed } from 'vue';

    import { formatFileSize } from '@/composables/data/useTransfer';

    export interface FileDropZoneProps {
        /** Accepted file types (HTML accept attribute) */
        accept?: string;
        /** Human-readable label for accepted formats */
        acceptLabel?: string;
        /** Maximum file size in bytes */
        maxSize?: number;
        /** Allow multiple files */
        multiple?: boolean;
        /** Custom placeholder text */
        placeholderText?: string;
        /** Custom placeholder icon name */
        placeholderIcon?: string;
        /** External error message */
        error?: string | null;
        /** Currently selected file (v-model) */
        file?: File | null;
        /** Unique id prefix for accessibility */
        id?: string;
    }

    const props = withDefaults(defineProps<FileDropZoneProps>(), {
        accept: '',
        acceptLabel: '',
        maxSize: 10 * 1024 * 1024,
        multiple: false,
        placeholderText: 'Glissez un fichier ici ou cliquez pour sélectionner',
        placeholderIcon: 'upload-cloud',
        error: null,
        file: null,
        id: 'file-drop-zone',
    });

    const emit = defineEmits<{
        'update:file': [file: File | null];
        'update:error': [error: string | null];
        filesSelected: [files: File[]];
    }>();

    const isDragging = ref(false);
    const inputRef = ref<HTMLInputElement | null>(null);

    const labelId = computed(() => `${props.id}-label`);
    const inputId = computed(() => `${props.id}-input`);
    const errorId = computed(() => `${props.id}-error`);

    const triggerInput = () => inputRef.value?.click();

    const processFiles = (files: FileList | File[] | undefined) => {
        if (!files || files.length === 0) {
            return;
        }

        if (props.multiple) {
            emit('filesSelected', Array.from(files));
        } else {
            const file = files instanceof FileList ? files[0] : files[0];
            if (file) {
                emit('update:error', null);
                emit('update:file', file);
            }
        }
    };

    const handleSelect = (event: Event) => {
        processFiles((event.target as HTMLInputElement).files ?? undefined);
    };

    const handleDrop = (event: DragEvent) => {
        isDragging.value = false;
        processFiles(event.dataTransfer?.files ?? undefined);
    };

    const handleRemove = () => {
        emit('update:file', null);
        emit('update:error', null);
        if (inputRef.value) {
            inputRef.value.value = '';
        }
    };

    defineExpose({ triggerInput });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as func;

    .sr-only {
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border: 0;
    }

    .file-drop-zone-wrapper {
        display: flex;
        flex-direction: column;
        gap: vars.$spacing-xxxs;
    }

    .file-drop-zone {
        border: 2px dashed vars.$admin-border;
        border-radius: 16px;
        padding: vars.$spacing-xl;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s ease;
        background: vars.$bg-secondary;

        &:hover,
        &--dragover {
            border-color: vars.$primary-color;
            background: func.color-alpha(vars.$primary-color, 0.04);
            transform: scale(1.01);
        }

        &--error {
            border-color: vars.$danger-color;
            background: func.color-alpha(vars.$danger-color, 0.04);
        }

        &__error {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xxxs;
            color: vars.$danger-color;
            margin: 0;
        }

        &__input {
            display: none;
        }

        &__placeholder {
            color: vars.$text-muted;
        }

        &__icon {
            margin-bottom: vars.$spacing-xs;
            color: vars.$text-muted;
            opacity: 0.6;
        }

        &__text {
            margin-bottom: vars.$spacing-xxxs;
        }

        &__hint {
            padding: 4px 12px;
            background: vars.$bg-secondary;
            border-radius: 6px;
            display: inline-block;
            margin-top: vars.$spacing-xs;
        }

        &__selected {
            display: flex;
            align-items: center;
            gap: vars.$spacing-md;
            text-align: left;
            padding: vars.$spacing-xs;
            background: vars.$white;
            border-radius: 10px;
            border: 1px solid vars.$admin-border;
        }

        &__info {
            flex: 1;
        }

        &__filename {
            display: block;
            font-weight: vars.$font-weight-medium;
        }

        &__size {
            color: vars.$text-muted;
        }

        &__remove {
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: transparent;
            border: none;
            cursor: pointer;
            color: vars.$text-muted;
            border-radius: 8px;
            transition: all 0.2s ease;

            &:hover {
                color: vars.$danger-color;
                background: func.color-alpha(vars.$danger-color, 0.1);
            }
        }
    }
</style>
