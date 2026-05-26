<!-- app.vue -->
<script setup lang="ts">
    const { googleSiteVerification } = useRuntimeConfig().public;

    if (googleSiteVerification) {
        useHead({
            meta: [{ name: 'google-site-verification', content: googleSiteVerification }],
        });
    }
</script>

<template>
	<NuxtLayout>
		<NuxtPage />
	</NuxtLayout>
</template>

<style lang="scss">
	@use 'src/styles/main';
</style>
