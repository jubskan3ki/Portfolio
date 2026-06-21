<template>
    <p v-if="tag === 'p'" v-html="html"></p>
    <li v-else-if="tag === 'li'" v-html="html"></li>
    <th v-else-if="tag === 'th'" v-html="html"></th>
    <td v-else-if="tag === 'td'" v-html="html"></td>
    <div v-else-if="tag === 'div'" v-html="html"></div>
    <span v-else v-html="html"></span>
</template>

<script setup lang="ts">
    // SÉCURITÉ : ce composant n'assainit PAS le HTML ; `html` DOIT déjà être sûr côté appelant.
    withDefaults(
        defineProps<{
            html: string;
            tag?: 'span' | 'p' | 'li' | 'th' | 'td' | 'div';
        }>(),
        { tag: 'span' },
    );
</script>
