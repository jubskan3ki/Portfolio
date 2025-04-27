<!-- src/components/ui/SectionHeading.vue -->
<template>
	<div class="section-heading">
		<h4 class="section-heading__title">{{ title }}</h4>
		<div class="section-heading__separator"></div>
	</div>
</template>

<script setup lang="ts">
	defineProps({
		title: {
			type: String,
			required: true,
		},
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.section-heading {
		display: flex;
		align-items: center;
		margin-bottom: vars.$spacing-sm;

		&__title {
			margin-right: vars.$spacing-md;
			margin-bottom: 0;
		}

		&__separator {
			flex: 1;
			height: 1px;
			background: linear-gradient(
				to right,
				func.color-alpha(vars.$gray-light, 0.5),
				func.color-alpha(vars.$gray-light, 0.1)
			);
		}
	}
</style>
