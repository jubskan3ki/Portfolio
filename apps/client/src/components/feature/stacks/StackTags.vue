<!--
  StackTags.vue
  Composant pour afficher les tags associés à la technologie
-->
<template>
	<div v-if="tags && tags.length > 0" class="stack-tags animate-fade-in delay-3">
		<h2>Tags associés</h2>
		<div class="stack-tags__list">
			<div v-for="tag in tags" :key="tag as string" class="stack-tags__item">
				<BaseIcon name="code" :size="14" />
				<span>{{ tag }}</span>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';

	defineProps({
		tags: {
			type: Array as () => string[] | readonly string[],
			default: () => [],
		},
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.stack-tags {
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
			flex-wrap: wrap;
			gap: vars.$spacing-sm;
			margin-top: vars.$spacing-md;
		}

		&__item {
			display: flex;
			align-items: center;
			gap: vars.$spacing-xs;
			padding: vars.$spacing-xs vars.$spacing-sm;
			background-color: vars.$white-dark;
			border-radius: vars.$border-radius-full;
			color: vars.$primary-color;
		}
	}
</style>
