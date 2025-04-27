<template>
	<nav v-if="items.length > 0" :class="['breadcrumb', customClass]" aria-label="Fil d'Ariane">
		<ol class="breadcrumb__list">
			<li v-for="(item, index) in items" :key="index" class="breadcrumb__item">
				<NuxtLink v-if="index < items.length - 1" :to="item.to" class="breadcrumb__link">
					<BaseIcon v-if="item.icon" :name="item.icon" :size="16" class="breadcrumb__icon" />
					<span>{{ item.label }}</span>
				</NuxtLink>

				<span v-else class="breadcrumb__current">
					<BaseIcon v-if="item.icon" :name="item.icon" :size="16" class="breadcrumb__icon" />
					<span>{{ item.label }}</span>
				</span>

				<span v-if="index < items.length - 1" class="breadcrumb__separator" aria-hidden="true">
					<slot name="separator">
						<BaseIcon name="chevron-right" :size="14" />
					</slot>
				</span>
			</li>
		</ol>
	</nav>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';

	interface BreadcrumbItem {
		label: string;
		to: string;
		icon?: string;
	}

	defineProps({
		items: {
			type: Array as () => BreadcrumbItem[],
			required: true,
		},
		customClass: {
			type: String,
			default: '',
		},
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.breadcrumb {
		padding: vars.$spacing-sm 0;

		&__list {
			display: flex;
			flex-wrap: wrap;
			align-items: center;
		}

		&__item {
			display: flex;
			align-items: center;
			color: vars.$gray-dark;

			&:last-child {
				color: vars.$black-light;
				font-weight: 500;
			}
		}

		&__link {
			color: vars.$gray-dark;
			display: flex;
			align-items: center;
			transition: color vars.$transition-base;

			&:hover {
				color: vars.$primary-color;
				text-decoration: underline;
			}
		}

		&__current {
			display: flex;
			align-items: center;
		}

		&__separator {
			display: flex;
			align-items: center;
			margin: 0 vars.$spacing-xs;
			color: vars.$gray-light;
		}

		&__icon {
			margin-right: vars.$spacing-xxs;
		}

		@include mix.responsive(mobile) {
			padding: vars.$spacing-xs 0;

			// Sur mobile, on pourrait cacher tout sauf le dernier et le précédent
			&__item {
				&:not(:nth-last-child(-n + 2)):not(:first-child) {
					display: none;
				}

				// Ajouter un indicateur pour montrer qu'il y a des items cachés
				&:nth-last-child(2):not(:first-child)::before {
					content: '...';
					margin-right: vars.$spacing-xs;
				}
			}
		}
	}
</style>
