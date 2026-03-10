<template>
    <div class="admin-page">
        <div class="admin-page__header">
            <div>
                <h1 class="admin-page__title">Import / Export</h1>
                <p class="admin-page__subtitle">Exportez ou importez vos données</p>
            </div>
        </div>

        <div class="import-export">
            <LazyExportSection :modules="modules" :is-exporting="isExporting" @export="handleExport" />

            <LazyImportSection
                ref="importSectionRef"
                :module-options="moduleOptions"
                :is-importing="isImporting"
                @import="handleImport"
            />
        </div>

        <RecentJobs :jobs="recentJobs" />
    </div>
</template>

<script setup lang="ts">
    import { ref } from 'vue';

    // ExportSection and ImportSection are lazy-loaded via Lazy prefix in template
    import RecentJobs from '@/components/feature/admin/transfer/RecentJobs.vue';
    import {
        useTransfer,
        type TransferModule,
        type ExportFormat,
        type ImportImage,
    } from '@/composables/data/useTransfer';
    import { useSeo } from '@/composables/seo/useSeo';

    import type ImportSection from '@/components/feature/admin/transfer/ImportSection.vue';

    definePageMeta({ layout: 'admin', title: 'Import / Export' });

    useSeo({
        title: 'Import / Export',
        description: 'Import et export des données du portfolio',
        noindex: true,
    });

    const { isExporting, isImporting, modules, moduleOptions, recentJobs, exportModules, importData } = useTransfer();

    const importSectionRef = ref<InstanceType<typeof ImportSection> | null>(null);

    const handleExport = async (selectedModules: TransferModule[], format: ExportFormat) => {
        await exportModules(selectedModules, format);
    };

    const handleImport = async (
        module: TransferModule,
        file: File,
        options: { updateExisting: boolean; skipErrors: boolean; images?: ImportImage[] },
    ) => {
        const success = await importData(module, file, options);
        if (success) {
            importSectionRef.value?.resetForm();
        }
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;

    .admin-page {
        &__header {
            margin-bottom: vars.$spacing-lg;
        }

        &__title {
            font-weight: vars.$font-weight-bold;
            margin-bottom: 4px;
            letter-spacing: -0.02em;
        }

        &__subtitle {
            color: vars.$text-muted;
        }
    }

    .import-export {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: vars.$spacing-lg;
        margin-bottom: vars.$spacing-lg;

        @include mix.responsive(tablet) {
            grid-template-columns: 1fr;
        }
    }
</style>
