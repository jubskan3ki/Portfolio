<template>
    <div class="admin-card">
        <div class="admin-card__header">
            <h2 class="admin-card__title">
                <BaseIcon name="download" :size="20" />
                Exporter les données
            </h2>
        </div>
        <div class="admin-card__body">
            <p class="export-description">
                Exportez vos données dans le format de votre choix. Sélectionnez les modules à exporter.
            </p>

            <div class="export-modules">
                <label
                    v-for="module in modules"
                    :key="module.key"
                    class="export-module"
                    :class="{ 'export-module--selected': selectedModules.includes(module.key) }"
                >
                    <input
                        v-model="selectedModules"
                        type="checkbox"
                        :value="module.key"
                        class="export-module__checkbox"
                    />
                    <BaseIcon :name="module.icon" :size="24" class="export-module__icon" />
                    <span class="export-module__name">{{ module.name }}</span>
                    <small class="export-module__count">{{ module.count }}</small>
                </label>
            </div>

            <fieldset class="export-format">
                <legend class="form-group__label">Format d'export</legend>
                <div class="export-format__options">
                    <label
                        v-for="format in formats"
                        :key="format.value"
                        class="export-format__option"
                        :class="{ 'export-format__option--selected': selectedFormat === format.value }"
                    >
                        <input
                            v-model="selectedFormat"
                            type="radio"
                            :value="format.value"
                            class="export-format__radio"
                        />
                        <span class="export-format__label">{{ format.label }}</span>
                        <small class="export-format__desc">{{ format.description }}</small>
                    </label>
                </div>
            </fieldset>

            <BaseButton
                variant="primary"
                size="lg"
                :disabled="!selectedModules.length"
                :loading="isExporting"
                @click="handleExport"
            >
                <template #icon-left>
                    <BaseIcon name="download" :size="18" />
                </template>
                Exporter ({{ selectedModules.length }} module{{ selectedModules.length > 1 ? 's' : '' }})
            </BaseButton>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref } from 'vue';

    import BaseButton from '@/components/base/BaseButton.vue';

    import type { TransferModule, ExportFormat } from '@/composables/data/useTransfer';
    import type { TransferModuleInfo } from '@/types/components/admin';

    defineProps<{
        modules: TransferModuleInfo[];
        isExporting: boolean;
    }>();

    const emit = defineEmits<{
        export: [modules: TransferModule[], format: ExportFormat];
    }>();

    const selectedModules = ref<TransferModule[]>([]);
    const selectedFormat = ref<ExportFormat>('json');

    const formats = [
        { value: 'json', label: 'JSON', description: 'Format universel, idéal pour backup' },
        { value: 'csv', label: 'CSV', description: 'Compatible Excel et tableurs' },
        { value: 'xlsx', label: 'Excel', description: 'Format Microsoft Excel' },
    ];

    const handleExport = () => {
        emit('export', selectedModules.value, selectedFormat.value);
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

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

    .export-description {
        color: vars.$text-secondary;
        margin: 0;
    }

    .export-modules {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: vars.$spacing-xs;
    }

    .export-module {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: vars.$spacing-xxs;
        padding: vars.$spacing-md;
        border: 2px solid vars.$admin-border;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.2s ease;
        text-align: center;

        &:hover {
            border-color: vars.$primary-color;
            transform: translateY(-2px);
        }

        &--selected {
            border-color: vars.$primary-color;
            background: func.color-alpha(vars.$primary-color, 0.06);
            box-shadow: 0 4px 12px func.color-alpha(vars.$primary-color, 0.15);

            .export-module__icon {
                color: vars.$primary-color;
                transform: scale(1.1);
            }
        }

        &__checkbox {
            display: none;
        }

        &__icon {
            color: vars.$text-muted;
            transition: all 0.2s ease;
        }

        &__name {
            font-weight: vars.$font-weight-medium;
        }

        &__count {
            color: vars.$text-muted;
            padding: 2px 8px;
            background: vars.$bg-secondary;
            border-radius: 10px;
        }
    }

    .export-format {
        border: none;
        padding: 0;
        margin: 0;

        &__options {
            display: flex;
            gap: vars.$spacing-xs;
            margin-top: vars.$spacing-xxs;
        }

        &__option {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: vars.$spacing-xxs;
            flex: 1;
            padding: vars.$spacing-md;
            border: 2px solid vars.$admin-border;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: center;
            position: relative;

            &:hover {
                border-color: vars.$primary-color;
                transform: translateY(-2px);
            }

            &--selected {
                border-color: vars.$primary-color;
                background-color: func.color-alpha(vars.$primary-color, 0.06);
                box-shadow: 0 4px 12px func.color-alpha(vars.$primary-color, 0.15);

                &::after {
                    content: '';
                    position: absolute;
                    top: vars.$spacing-xxxs;
                    right: vars.$spacing-xxxs;
                    width: 20px;
                    height: 20px;
                    background: vars.$primary-color;
                    border-radius: 50%;
                    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='20 6 9 17 4 12'%3E%3C/polyline%3E%3C/svg%3E");
                    background-size: 12px;
                    background-repeat: no-repeat;
                    background-position: center;
                }
            }
        }

        &__radio {
            position: absolute;
            opacity: 0;
            width: 0;
            height: 0;
        }

        &__label {
            font-weight: vars.$font-weight-semibold;
        }

        &__desc {
            color: vars.$text-muted;
            line-height: 1.3;
        }
    }

    .form-group {
        &__label {
            display: block;
            font-weight: vars.$font-weight-medium;
            margin-bottom: vars.$spacing-xxs;
        }
    }
</style>
