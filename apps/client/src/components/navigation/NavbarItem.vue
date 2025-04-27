<!-- src/components/navigation/NavbarItem.vue -->
<template>
	<li class="navbar__item" @mouseenter="$emit('mouseenter', index)" @mouseleave="$emit('mouseleave')">
		<NuxtLink
			:to="item.path"
			:class="[
				'navbar__link',
				{ 'navbar__link--active': isActive },
				{ 'navbar__link--has-children': item.children },
			]"
		>
			<span v-if="item.icon" class="navbar__icon">
				<BaseIcon :name="item.icon" :size="16" />
			</span>
			{{ item.label }}
		</NuxtLink>
	</li>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';

	// Types
	interface NavChildItem {
		label: string;
		path: string;
		icon?: string;
	}

	interface NavItem {
		label: string;
		path: string;
		icon?: string;
		children?: NavChildItem[];
	}

	defineProps({
		item: {
			type: Object as () => NavItem,
			required: true,
		},
		index: {
			type: Number,
			required: true,
		},
		isActive: {
			type: Boolean,
			required: true,
		},
	});

	// Emits
	defineEmits(['mouseenter', 'mouseleave']);
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.navbar {
		&__item {
			position: relative;
		}

		&__link {
			display: flex;
			align-items: center;
			padding: vars.$spacing-xs vars.$spacing-sm;
			font-weight: 500;
			border-radius: vars.$border-radius-full;
			transition: all 0.3s ease;
			position: relative;

			&::after {
				content: '';
				position: absolute;
				bottom: -4px;
				left: 50%;
				width: 0;
				height: 2px;
				background-color: currentColor;
				transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
				transform: translateX(-50%);
				opacity: 0;
			}

			&:hover {
				transform: translateY(-2px);

				&::after {
					width: 30px;
					opacity: 1;
				}
			}

			&--active {
				font-weight: 600;

				&::after {
					width: 30px;
					opacity: 1;
				}
			}

			&--has-children {
				padding-right: vars.$spacing-lg;
			}
		}

		&__icon {
			margin-right: vars.$spacing-xs;
			display: flex;
			align-items: center;
			color: func.color-alpha(vars.$primary-color, 0.9);
		}
	}
</style>
