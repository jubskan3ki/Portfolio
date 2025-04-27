<!--
  StackResources.vue
  Composant pour afficher les ressources utiles liées à la technologie
-->
<template>
	<div v-if="resources && resources.length > 0" class="stack-resources animate-fade-in delay-4">
		<h2>Ressources utiles</h2>
		<div class="stack-resources__list">
			<div v-for="(resource, index) in resources" :key="index" class="stack-resources__item">
				<h3 class="stack-resources__item-title">
					{{ resource.title }}
				</h3>
				<p class="stack-resources__item-description">
					{{ resource.description }}
				</p>
				<BaseLink :to="resource.url" target="_blank" class="stack-resources__item-link">
					<BaseIcon name="external-link" :size="14" />
					<span>Consulter</span>
				</BaseLink>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import BaseLink from '@/components/base/BaseLink.vue';

	interface Resource {
		title: string;
		description: string;
		url: string;
	}

	defineProps({
		resources: {
			type: Array as () => Resource[] | readonly Resource[],
			default: () => [],
		},
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.stack-resources {
		background-color: vars.$white;
		border-radius: vars.$border-radius-lg;
		padding: vars.$spacing-lg;
		box-shadow: vars.$box-shadow-small;

		h2 {
			margin-bottom: vars.$spacing-md;
			position: relative;
			padding-bottom: vars.$spacing-sm;
			color: vars.$primary-color;

			&::after {
				content: '';
				position: absolute;
				bottom: 0;
				left: 0;
				width: 60px;
				height: 3px;
				background-color: vars.$primary-color;
				border-radius: vars.$border-radius-full;
			}
		}

		&__list {
			display: flex;
			flex-direction: column;
			gap: vars.$spacing-md;
			margin-top: vars.$spacing-md;
		}

		&__item {
			padding: vars.$spacing-md;
			border-radius: vars.$border-radius-md;
			background-color: vars.$white-dark;
			border-left: 4px solid vars.$primary-color;
		}

		&__item-title {
			color: vars.$primary-color;
			margin-bottom: vars.$spacing-xs;
		}

		&__item-description {
			margin-bottom: vars.$spacing-sm;
			color: vars.$gray-dark;
		}

		&__item-link {
			display: inline-flex;
			align-items: center;
			gap: vars.$spacing-xs;
			color: vars.$primary-color;
			font-weight: 500;

			&:hover {
				text-decoration: underline;
			}
		}
	}
</style>
