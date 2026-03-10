<template>
    <div v-if="show" class="images-upload-section">
        <div class="images-upload-header">
            <h3 class="images-upload-title">
                <BaseIcon name="image" :size="18" />
                Images associées
            </h3>
            <small class="images-upload-hint"> Ajoutez les images référencées dans votre fichier d'import </small>
        </div>

        <div
            class="images-upload"
            :class="{ 'images-upload--dragover': isDraggingImages }"
            @dragover.prevent="isDraggingImages = true"
            @dragleave.prevent="isDraggingImages = false"
            @drop.prevent="handleImagesDrop"
        >
            <input
                id="images-input"
                ref="imagesInput"
                type="file"
                class="images-upload__input"
                accept="image/*"
                multiple
                @change="handleImagesSelect"
            />
            <div
                class="images-upload__dropzone"
                role="button"
                tabindex="0"
                @click="triggerImagesInput"
                @keydown.enter="triggerImagesInput"
                @keydown.space.prevent="triggerImagesInput"
            >
                <BaseIcon name="images" :size="32" class="images-upload__icon" />
                <p class="images-upload__text">Glissez vos images ici ou cliquez pour sélectionner</p>
                <small class="images-upload__formats">PNG, JPG, WebP, SVG - Max 5MB par image</small>
            </div>
        </div>

        <!-- Images preview grid -->
        <div v-if="images.length > 0" class="images-grid">
            <div
                v-for="(img, index) in images"
                :key="img.id"
                class="image-item"
                :class="{ 'image-item--error': img.error }"
            >
                <div class="image-item__preview">
                    <img :src="img.preview" :alt="img.file.name" />
                </div>
                <div class="image-item__info">
                    <input
                        v-model="img.key"
                        type="text"
                        class="image-item__key"
                        :placeholder="img.file.name"
                        title="Clé d'image (utilisée dans le JSON)"
                        aria-label="Clé d'image"
                    />
                    <small class="image-item__size">{{ formatFileSize(img.file.size) }}</small>
                </div>
                <button
                    type="button"
                    class="image-item__remove"
                    :aria-label="`Supprimer ${img.file.name}`"
                    @click="$emit('removeImage', index)"
                >
                    <BaseIcon name="x" :size="14" />
                </button>
                <p v-if="img.error" class="image-item__error">{{ img.error }}</p>
            </div>
        </div>

        <p v-if="images.length > 0" class="images-mapping-hint">
            <BaseIcon name="info" :size="14" />
            Les clés d'images seront mappées aux champs "logo" ou "image" de votre fichier d'import
        </p>
    </div>
</template>

<script setup lang="ts">
    import { ref } from 'vue';

    import { formatFileSize } from '@/composables/data/useTransfer';

    export interface ImageItem {
        id: string;
        file: File;
        preview: string;
        key: string;
        error?: string;
    }

    interface FilePreviewListProps {
        /** Whether to show the section */
        show: boolean;
        /** List of image items to display */
        images: ImageItem[];
    }

    defineProps<FilePreviewListProps>();

    const emit = defineEmits<{
        addImages: [files: File[]];
        removeImage: [index: number];
    }>();

    const isDraggingImages = ref(false);
    const imagesInput = ref<HTMLInputElement | null>(null);

    const triggerImagesInput = () => imagesInput.value?.click();

    const handleImagesSelect = (event: Event) => {
        const files = (event.target as HTMLInputElement).files;
        if (files) {
            emit('addImages', Array.from(files));
        }
        if (imagesInput.value) {
            imagesInput.value.value = '';
        }
    };

    const handleImagesDrop = (event: DragEvent) => {
        isDraggingImages.value = false;
        const files = event.dataTransfer?.files;
        if (files) {
            emit(
                'addImages',
                Array.from(files).filter((f) => f.type.startsWith('image/')),
            );
        }
    };
</script>

<style lang="scss" scoped>
    @use 'sass:color';
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as func;

    .images-upload-section {
        display: flex;
        flex-direction: column;
        gap: vars.$spacing-md;
        padding: vars.$spacing-md;
        background: vars.$bg-secondary;
        border-radius: 12px;
        border: 1px solid vars.$admin-border;
    }

    .images-upload-header {
        display: flex;
        flex-direction: column;
        gap: vars.$spacing-xxxs;
    }

    .images-upload-title {
        display: flex;
        align-items: center;
        gap: vars.$spacing-xxs;
        font-weight: vars.$font-weight-semibold;
        margin: 0;
    }

    .images-upload-hint {
        color: vars.$text-muted;
    }

    .images-upload {
        position: relative;

        &__input {
            display: none;
        }

        &__dropzone {
            border: 2px dashed vars.$admin-border;
            border-radius: 12px;
            padding: vars.$spacing-lg;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease;
            background: vars.$white;

            &:hover {
                border-color: vars.$primary-color;
                background: func.color-alpha(vars.$primary-color, 0.02);
            }
        }

        &--dragover .images-upload__dropzone {
            border-color: vars.$primary-color;
            background: func.color-alpha(vars.$primary-color, 0.06);
            transform: scale(1.01);
        }

        &__icon {
            color: vars.$text-muted;
            opacity: 0.6;
            margin-bottom: vars.$spacing-xxs;
        }

        &__text {
            margin: 0 0 vars.$spacing-xxxs;
            color: vars.$text-secondary;
        }

        &__formats {
            color: vars.$text-muted;
        }
    }

    .images-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
        gap: vars.$spacing-sm;
    }

    .image-item {
        position: relative;
        background: vars.$white;
        border-radius: 10px;
        border: 1px solid vars.$admin-border;
        overflow: hidden;
        transition: all 0.2s ease;

        &:hover {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);

            .image-item__remove {
                opacity: 1;
            }
        }

        &--error {
            border-color: vars.$danger-color;
        }

        &__preview {
            aspect-ratio: 1;
            overflow: hidden;
            background: vars.$bg-tertiary;

            img {
                width: 100%;
                height: 100%;
                object-fit: cover;
            }
        }

        &__info {
            padding: vars.$spacing-xxs;
            display: flex;
            flex-direction: column;
            gap: 2px;
        }

        &__key {
            width: 100%;
            padding: 4px 6px;
            border: 1px solid vars.$admin-border;
            border-radius: 4px;
            font-size: 0.75rem;
            background: vars.$bg-secondary;
            transition: border-color 0.2s ease;

            &:focus {
                outline: none;
                border-color: vars.$primary-color;
            }

            &::placeholder {
                color: vars.$text-muted;
            }
        }

        &__size {
            color: vars.$text-muted;
            font-size: 0.7rem;
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
            opacity: 0;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25);
            transition:
                opacity 0.2s ease,
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

        &__error {
            padding: vars.$spacing-xxxs vars.$spacing-xxs;
            margin: 0;
            font-size: 0.7rem;
            color: vars.$danger-color;
            background: func.color-alpha(vars.$danger-color, 0.1);
        }
    }

    .images-mapping-hint {
        display: flex;
        align-items: center;
        gap: vars.$spacing-xxs;
        margin: 0;
        padding: vars.$spacing-xs vars.$spacing-sm;
        background: func.color-alpha(vars.$info-color, 0.1);
        color: vars.$info-color;
        border-radius: 8px;
        font-size: 0.85rem;
    }
</style>
