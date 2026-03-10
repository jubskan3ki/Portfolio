<template>
    <ArticleForm :id="articleId" />
</template>

<script setup lang="ts">
    import { computed } from 'vue';
    import { useRoute } from 'vue-router';

    import ArticleForm from '@/components/feature/admin/forms/ArticleForm.vue';
    import { useSeo } from '@/composables/seo/useSeo';

    definePageMeta({ layout: 'admin', title: 'Modifier l\'article' });

    useSeo({
        title: 'Modifier Article',
        description: 'Édition d\'un article existant',
        noindex: true,
    });

    const route = useRoute();
    const articleId = computed(() => route.params.id as string);
</script>
