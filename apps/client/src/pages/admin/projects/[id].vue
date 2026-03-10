<template>
    <ProjectForm :id="projectId" />
</template>

<script setup lang="ts">
    import { computed } from 'vue';
    import { useRoute } from 'vue-router';

    import ProjectForm from '@/components/feature/admin/forms/ProjectForm.vue';
    import { useSeo } from '@/composables/seo/useSeo';

    definePageMeta({ layout: 'admin', title: 'Modifier le projet' });

    useSeo({
        title: 'Modifier un Projet',
        description: 'Édition d\'un projet existant',
        noindex: true,
    });

    const route = useRoute();
    const projectId = computed(() => route.params.id as string);
</script>
