<template>
	<li class="pagination-item" :class="{ 'pagination-item--ellipsis': isEllipsis }">
		<button
			v-if="!isEllipsis"
			class="pagination-item__btn"
			:class="{ 'pagination-item__btn--active': isActive }"
			:aria-current="isActive ? 'page' : undefined"
			@click="$emit('click')"
		>
			{{ page }}
		</button>
		<span v-else class="pagination-item__ellipsis">...</span>
	</li>
</template>

<script setup lang="ts">
	defineProps({
		page: {
			type: Number,
			required: true,
		},
		isActive: {
			type: Boolean,
			default: false,
		},
		isEllipsis: {
			type: Boolean,
			default: false,
		},
	});

	defineEmits(['click']);
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.pagination-item {
		margin: 0 2px;

		&--ellipsis {
			margin: 0 vars.$spacing-xs;
		}

		&__btn {
			display: flex;
			align-items: center;
			justify-content: center;
			min-width: 36px;
			height: 36px;
			padding: 0 vars.$spacing-xs;
			border-radius: vars.$border-radius-md;
			color: vars.$black-light;
			background-color: transparent;
			border: none;
			cursor: pointer;
			transition: all vars.$transition-base;
			font-weight: 500;

			&:hover {
				background-color: vars.$white-dark;
			}

			&--active {
				background-color: vars.$primary-color;
				color: vars.$white;

				&:hover {
					background-color: func.adjust-color-brightness(vars.$primary-color, -10%);
				}
			}
		}

		&__ellipsis {
			color: vars.$gray;
			font-weight: 500;
		}
	}
</style>
