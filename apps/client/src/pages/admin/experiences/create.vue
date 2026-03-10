<template>
    <ExperienceForm />
</template>

<script setup lang="ts">
    import ExperienceForm from '@/components/feature/admin/forms/ExperienceForm.vue';
    import { useSeo } from '@/composables/seo/useSeo';

    definePageMeta({ layout: 'admin', title: 'Nouvelle expérience' });

    useSeo({
        title: 'Créer une Expérience',
        description: 'Ajout d\'une nouvelle expérience professionnelle ou formation',
        noindex: true,
    });
</script>
