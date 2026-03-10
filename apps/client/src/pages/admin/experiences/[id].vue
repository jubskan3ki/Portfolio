<template>
    <ExperienceForm :id="experienceId" />
</template>

<script setup lang="ts">
    import { computed } from 'vue';
    import { useRoute } from 'vue-router';

    import ExperienceForm from '@/components/feature/admin/forms/ExperienceForm.vue';
    import { useSeo } from '@/composables/seo/useSeo';

    definePageMeta({ layout: 'admin', title: 'Modifier expérience' });

    useSeo({
        title: 'Modifier une Expérience',
        description: 'Modification d\'une expérience professionnelle ou formation',
        noindex: true,
    });

    const route = useRoute();
    const experienceId = computed(() => route.params.id as string);
</script>
