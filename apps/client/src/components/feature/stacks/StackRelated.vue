<!--
  StackRelated.vue
  Composant pour afficher les technologies similaires
-->
<template>
	<div v-if="stacks && stacks.length > 0" class="stack-related">
		<h3>Technologies similaires</h3>
		<div class="stack-related__list">
			<div v-for="stack in stacks" :key="stack.slug" class="stack-related__item">
				<BaseLink :to="`/stacks/${stack.slug}`" class="stack-related__link">
					<img :src="stack.logo" :alt="stack.name" class="stack-related__logo" />
					<div class="stack-related__info">
						<span class="stack-related__name">{{ stack.name }}</span>
						<small class="stack-related__category">{{ stack.category }}</small>
					</div>
				</BaseLink>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
	import BaseLink from '@/components/base/BaseLink.vue';

	interface RelatedStack {
		name: string;
		logo: string;
		slug: string;
		category: string;
	}

	defineProps({
		stacks: {
			type: Array as () => RelatedStack[] | readonly RelatedStack[],
			default: () => [],
		},
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.stack-related {
		background-color: vars.$white;
		border-radius: vars.$border-radius-lg;
		padding: vars.$spacing-lg;
		box-shadow: vars.$box-shadow-small;

		h3 {
			margin-bottom: vars.$spacing-md;
			color: vars.$primary-color;
			font-weight: 600;
			padding-bottom: vars.$spacing-xs;
			border-bottom: 1px solid vars.$white-dark;
		}

		&__list {
			display: flex;
			flex-direction: column;
			gap: vars.$spacing-sm;
		}

		&__item {
			border-bottom: 1px solid vars.$white-dark;
			padding-bottom: vars.$spacing-sm;

			&:last-child {
				border-bottom: none;
				padding-bottom: 0;
			}
		}

		&__link {
			display: flex;
			align-items: center;
			gap: vars.$spacing-sm;
			padding: vars.$spacing-xs;
			border-radius: vars.$border-radius-md;
			transition: all vars.$transition-base;

			&:hover {
				background-color: vars.$white-dark;
				transform: translateX(5px);
			}
		}

		&__logo {
			width: 40px;
			height: 40px;
			object-fit: contain;
		}

		&__info {
			display: flex;
			flex-direction: column;
		}

		&__name {
			font-weight: 500;
			color: vars.$black-light;
		}

		&__category {
			color: vars.$gray;
		}
	}
</style>
