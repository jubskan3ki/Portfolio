<template>
    <StackForm :id="stackId" />
</template>

<script setup lang="ts">
    import { computed } from 'vue';
    import { useRoute } from 'vue-router';

    import StackForm from '@/components/feature/admin/forms/StackForm.vue';
    import { useSeo } from '@/composables/seo/useSeo';

    definePageMeta({ layout: 'admin', title: 'Modifier la stack' });

    useSeo({
        title: 'Modifier une Stack',
        description: 'Édition d\'une technologie existante',
        noindex: true,
    });

    const route = useRoute();
    const stackId = computed(() => route.params.id as string);
</script>
