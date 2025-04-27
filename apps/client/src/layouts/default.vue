<!-- src/components/layouts/AppShell.vue -->
<template>
	<div class="default-layout">
		<Header />

		<main class="default-layout__main">
			<slot></slot>
		</main>

		<Footer />

		<AlertList position="top-right" />
		<Modal />
		<Loader />
	</div>
</template>

<script setup lang="ts">
	import AlertList from '@/components/feedback/AlertList.vue';
	import Modal from '@/components/feedback/Modal.vue';
	import Footer from '@/components/layouts/Footer.vue';
	import Header from '@/components/layouts/Header.vue';
	import Loader from '@/components/loaders/Loader.vue';
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;

	.default-layout {
		display: flex;
		flex-direction: column;
		min-height: 100vh;

		&__main {
			flex: 1;
			padding-top: 75px;
		}
	}
</style>
