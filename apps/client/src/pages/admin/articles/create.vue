<template>
    <ArticleForm />
</template>

<script setup lang="ts">
    import ArticleForm from '@/components/feature/admin/forms/ArticleForm.vue';
    import { useSeo } from '@/composables/seo/useSeo';

    definePageMeta({ layout: 'admin', title: 'Nouvel article' });

    useSeo({
        title: 'Créer un Article',
        description: 'Création d\'un nouvel article de blog',
        noindex: true,
    });
</script>
