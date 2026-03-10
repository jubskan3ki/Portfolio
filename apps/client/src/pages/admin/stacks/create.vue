<template>
    <StackForm />
</template>

<script setup lang="ts">
    import StackForm from '@/components/feature/admin/forms/StackForm.vue';
    import { useSeo } from '@/composables/seo/useSeo';

    definePageMeta({ layout: 'admin', title: 'Nouvelle stack' });

    useSeo({
        title: 'Créer une Stack',
        description: 'Ajout d\'une nouvelle technologie',
        noindex: true,
    });
</script>
