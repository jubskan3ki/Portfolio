<template>
    <ProjectForm />
</template>

<script setup lang="ts">
    import ProjectForm from '@/components/feature/admin/forms/ProjectForm.vue';
    import { useSeo } from '@/composables/seo/useSeo';

    definePageMeta({ layout: 'admin', title: 'Nouveau projet' });

    useSeo({
        title: 'Créer un Projet',
        description: 'Création d\'un nouveau projet',
        noindex: true,
    });
</script>
