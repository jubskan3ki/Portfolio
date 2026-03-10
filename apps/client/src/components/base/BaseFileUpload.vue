<template>
    <div class="file-upload-group">
        <label v-if="label" :for="id" class="file-upload-group__label">
            {{ label }}
            <span v-if="required" class="file-upload-group__required">*</span>
        </label>

        <div
            :id="id"
            :class="uploadClasses"
            role="button"
            tabindex="0"
            :aria-label="ariaLabel"
            @click="triggerFileInput"
            @keydown.enter="triggerFileInput"
            @keydown.space.prevent="triggerFileInput"
            @dragover.prevent="handleDragOver"
            @dragleave.prevent="handleDragLeave"
            @drop.prevent="handleDrop"
        >
            <input
                ref="fileInputRef"
                type="file"
                class="file-upload__input"
                :accept="accept"
                :disabled="disabled"
                :aria-label="label || placeholderText"
                @change="handleFileChange"
            />

            <!-- Placeholder -->
            <div v-if="!preview" class="file-upload__placeholder">
                <BaseIcon :name="placeholderIcon" :size="32" class="file-upload__icon" />
                <p class="file-upload__text">{{ placeholderText }}</p>
                <small class="file-upload__hint">{{ hint }}</small>
            </div>

            <!-- Preview -->
            <div v-else class="file-upload__preview">
                <img :src="preview" :alt="previewAlt" />
                <button type="button" class="file-upload__remove" :aria-label="removeLabel" @click.stop="handleRemove">
                    <BaseIcon name="close" :size="14" />
                </button>
            </div>
        </div>

        <!-- Error -->
        <p v-if="error" class="file-upload-group__error">{{ error }}</p>
    </div>
</template>

<script setup lang="ts">
    import { ref, computed, watch } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';

    interface Props {
        modelValue?: File | null;
        preview?: string;
        id?: string;
        label?: string;
        accept?: string;
        maxSize?: number; // in MB
        required?: boolean;
        disabled?: boolean;
        error?: string;
        placeholderIcon?: string;
        placeholderText?: string;
        hint?: string;
        previewAlt?: string;
        removeLabel?: string;
    }

    const props = withDefaults(defineProps<Props>(), {
        modelValue: null,
        preview: '',
        id: 'file-upload',
        label: '',
        accept: 'image/*',
        maxSize: 5,
        required: false,
        disabled: false,
        error: '',
        placeholderIcon: 'image',
        placeholderText: 'Cliquez ou glissez une image',
        hint: 'PNG, JPG jusqu\'à 5MB',
        previewAlt: 'Aperçu',
        removeLabel: 'Supprimer l\'image',
    });

    const emit = defineEmits<{
        'update:modelValue': [file: File | null];
        'update:preview': [url: string];
        error: [message: string];
    }>();

    const fileInputRef = ref<HTMLInputElement | null>(null);
    const isDragging = ref(false);

    const ariaLabel = computed(() => (props.preview ? 'Modifier l\'image' : 'Ajouter une image'));

    const uploadClasses = computed(() => [
        'file-upload',
        {
            'file-upload--dragging': isDragging.value,
            'file-upload--disabled': props.disabled,
            'file-upload--error': !!props.error,
        },
    ]);

    const triggerFileInput = () => {
        if (props.disabled) {
            return;
        }
        fileInputRef.value?.click();
    };

    const validateFile = (file: File): boolean => {
        // Check size
        const maxSizeBytes = props.maxSize * 1024 * 1024;
        if (file.size > maxSizeBytes) {
            emit('error', `Le fichier dépasse la taille maximale de ${props.maxSize}MB`);
            return false;
        }

        // Check type
        if (props.accept && props.accept !== '*') {
            const acceptedTypes = props.accept.split(',').map((t) => t.trim());
            const fileType = file.type;
            const fileExtension = `.${file.name.split('.').pop()?.toLowerCase()}`;

            const isValid = acceptedTypes.some((type) => {
                if (type.startsWith('.')) {
                    return fileExtension === type.toLowerCase();
                }
                if (type.endsWith('/*')) {
                    return fileType.startsWith(type.replace('/*', '/'));
                }
                return fileType === type;
            });

            if (!isValid) {
                emit('error', 'Type de fichier non accepté');
                return false;
            }
        }

        return true;
    };

    const processFile = (file: File) => {
        if (!validateFile(file)) {
            return;
        }

        emit('update:modelValue', file);
        const previewUrl = URL.createObjectURL(file);
        emit('update:preview', previewUrl);
    };

    const handleFileChange = (event: Event) => {
        const file = (event.target as HTMLInputElement).files?.[0];
        if (file) {
            processFile(file);
        }
    };

    const handleDragOver = () => {
        if (props.disabled) {
            return;
        }
        isDragging.value = true;
    };

    const handleDragLeave = () => {
        isDragging.value = false;
    };

    const handleDrop = (event: DragEvent) => {
        isDragging.value = false;
        if (props.disabled) {
            return;
        }

        const file = event.dataTransfer?.files[0];
        if (file) {
            processFile(file);
        }
    };

    const handleRemove = () => {
        emit('update:modelValue', null);
        emit('update:preview', '');
        if (fileInputRef.value) {
            fileInputRef.value.value = '';
        }
    };

    // Cleanup preview URL on unmount
    watch(
        () => props.preview,
        (newVal, oldVal) => {
            if (oldVal && oldVal.startsWith('blob:') && oldVal !== newVal) {
                URL.revokeObjectURL(oldVal);
            }
        },
    );
</script>

<style lang="scss" scoped>
    @use 'sass:color';
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;

    .file-upload-group {
        &__label {
            display: block;
            font-weight: vars.$font-weight-medium;
            color: vars.$text-primary;
            margin-bottom: vars.$spacing-xxs;
        }

        &__required {
            color: vars.$danger-color;
            margin-left: 2px;
        }

        &__error {
            margin-top: vars.$spacing-xxs;
            color: vars.$danger-color;
        }
    }

    .file-upload {
        border: 2px dashed vars.$border-color;
        border-radius: vars.$border-radius-lg;
        padding: vars.$spacing-xl;
        text-align: center;
        cursor: pointer;
        transition:
            border-color vars.$transition-fast,
            background-color vars.$transition-fast;

        &:hover:not(&--disabled) {
            border-color: vars.$primary-color;
            background-color: rgba(vars.$primary-color, 0.02);
        }

        &:focus-visible {
            outline: 2px solid vars.$primary-color;
            outline-offset: 2px;
        }

        &--dragging {
            border-color: vars.$primary-color;
            background-color: rgba(vars.$primary-color, 0.05);
        }

        &--disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        &--error {
            border-color: vars.$danger-color;
        }

        &__input {
            display: none;
        }

        &__placeholder {
            color: vars.$text-muted;
        }

        &__icon {
            color: vars.$text-muted;
            margin-bottom: vars.$spacing-xxs;
        }

        &__text {
            margin: vars.$spacing-xs 0 vars.$spacing-xxs;
        }

        &__hint {
            opacity: 0.8;
        }

        &__preview {
            position: relative;
            display: inline-block;

            img {
                max-width: 100%;
                max-height: 200px;
                border-radius: vars.$border-radius-md;
                object-fit: contain;
            }
        }

        &__remove {
            position: absolute;
            top: vars.$spacing-xs;
            right: vars.$spacing-xs;
            min-width: 28px;
            min-height: 28px;
            width: 28px;
            height: 28px;
            flex-shrink: 0;
            padding: 0;
            background-color: vars.$danger-color;
            color: vars.$white;
            border: 2px solid vars.$white;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25);
            transition:
                transform vars.$transition-fast,
                background-color vars.$transition-fast;

            &:hover {
                transform: scale(1.1);
                background-color: color.adjust(vars.$danger-color, $lightness: -10%);
            }

            &:focus-visible {
                outline: 2px solid vars.$primary-color;
                outline-offset: 2px;
            }
        }
    }
</style>
