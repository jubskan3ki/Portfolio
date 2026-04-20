<template>
    <div class="import-options">
        <BaseSwitch v-model="localUpdateExisting" label="Mettre à jour les enregistrements existants" />
        <BaseSwitch v-model="localSkipErrors" label="Ignorer les erreurs et continuer" />
    </div>

    <BaseButton
        variant="primary"
        size="lg"
        :disabled="!canImport"
        :loading="isImporting"
        @click="$emit('import')"
    >
        <template #icon-left>
            <BaseIcon name="upload" :size="18" />
        </template>
        Importer
        <template v-if="imagesCount > 0"> (+ {{ imagesCount }} image{{ imagesCount > 1 ? 's' : '' }}) </template>
    </BaseButton>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import BaseButton from '@/components/base/BaseButton.vue';
    import BaseSwitch from '@/components/base/BaseSwitch.vue';

    import type { ImportProgressProps } from '@/types/components/admin';

    const props = defineProps<ImportProgressProps>();

    const emit = defineEmits<{
        import: [];
        'update:updateExisting': [value: boolean];
        'update:skipErrors': [value: boolean];
    }>();

    const localUpdateExisting = computed({
        get: () => props.updateExisting,
        set: (value: boolean) => emit('update:updateExisting', value),
    });

    const localSkipErrors = computed({
        get: () => props.skipErrors,
        set: (value: boolean) => emit('update:skipErrors', value),
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;

    .import-options {
        display: flex;
        flex-direction: column;
        gap: vars.$spacing-xs;
    }
</style>
