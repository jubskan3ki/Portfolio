<!-- src/components/navigation/MobileMenuItem.vue -->
<template>
	<li class="mobile-menu-item">
		<div class="mobile-menu-item__wrapper">
			<NuxtLink
				:to="item.path"
				class="mobile-menu-item__link"
				:class="{ 'mobile-menu-item__link--active': isActive }"
				@click="closeMenu"
			>
				<span v-if="item.icon" class="mobile-menu-item__icon">
					<BaseIcon :name="item.icon" :size="20" />
				</span>
				<span class="mobile-menu-item__text">{{ item.label }}</span>
			</NuxtLink>

			<!-- Toggle pour le sous-menu (si des enfants existent) -->
			<button
				v-if="hasChildren"
				class="mobile-menu-item__toggle"
				:class="{ 'mobile-menu-item__toggle--expanded': isExpanded }"
				:aria-expanded="isExpanded"
				:aria-controls="`submenu-${index}`"
				@click="toggleSubmenu"
			>
				<BaseIcon
					name="chevron-down"
					:size="16"
					:class="{ 'mobile-menu-item__toggle-icon--expanded': isExpanded }"
				/>
			</button>
		</div>

		<!-- Sous-menu -->
		<transition name="submenu">
			<ul v-if="hasChildren && isExpanded" :id="`submenu-${index}`" class="mobile-menu-item__submenu">
				<li v-for="(subItem, subIndex) in item.children" :key="subIndex" class="mobile-menu-item__submenu-item">
					<NuxtLink
						:to="subItem.path"
						class="mobile-menu-item__submenu-link"
						:class="{
							'mobile-menu-item__submenu-link--active': isSubItemActive(subItem.path),
						}"
						@click="closeMenu"
					>
						<span v-if="subItem.icon" class="mobile-menu-item__submenu-icon">
							<BaseIcon :name="subItem.icon" :size="16" />
						</span>
						{{ subItem.label }}
					</NuxtLink>
				</li>
			</ul>
		</transition>
	</li>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import { isActiveRoute } from '@/config/navBar';
	import { useNavStore } from '@/store/navBar';
	import { NavItem } from '@/types/config/navBar';
	import { computed } from 'vue';
	import { useRoute } from 'vue-router';

	const props = defineProps({
		item: {
			type: Object as () => NavItem,
			required: true,
		},
		index: {
			type: Number,
			required: true,
		},
	});

	const route = useRoute();
	const navStore = useNavStore();

	// Computed properties
	const hasChildren = computed(() => props.item.children && props.item.children.length > 0);
	const isActive = computed(() => isActiveRoute(props.item.path, route.path));
	const isExpanded = computed(() => navStore.expandedSubmenuIndex === props.index);

	// Méthodes
	const closeMenu = () => {
		navStore.closeMobileMenu();
	};

	const toggleSubmenu = () => {
		navStore.toggleSubmenu(props.index);
	};

	const isSubItemActive = (path: string) => {
		return isActiveRoute(path, route.path);
	};
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.mobile-menu-item {
		position: relative;
		display: flex;
		flex-direction: column;
		width: 100%;

		&__wrapper {
			display: flex;
			align-items: center;
		}

		&__link {
			flex: 1;
			display: flex;
			align-items: center;
			padding: vars.$spacing-sm;
			border-radius: vars.$border-radius-md;
			color: vars.$black-light;
			font-weight: 500;
			transition: all vars.$transition-base;

			&:hover {
				background-color: vars.$white-dark;
			}

			&--active {
				color: vars.$primary-color;
				background-color: func.color-alpha(vars.$primary-color, 0.1);

				&:hover {
					background-color: func.color-alpha(vars.$primary-color, 0.15);
				}
			}
		}

		&__icon {
			margin-right: vars.$spacing-sm;
			display: flex;
			align-items: center;
		}

		&__toggle {
			display: flex;
			align-items: center;
			justify-content: center;
			min-width: 36px;
			height: 36px;
			margin: vars.$spacing-xs;
			border-radius: 50%;
			transition: all vars.$transition-base;

			&:hover {
				background-color: vars.$white-dark;
			}

			&--expanded {
				background-color: vars.$white-dark;
			}
		}

		&__toggle-icon {
			transition: transform 0.3s ease;

			&--expanded {
				transform: rotate(180deg);
			}
		}

		&__submenu {
			width: 100%;
			padding-left: vars.$spacing-lg;
			margin-top: vars.$spacing-xs;
			margin-bottom: vars.$spacing-xs;
		}

		&__submenu-item {
			margin-bottom: vars.$spacing-xs;

			&:last-child {
				margin-bottom: 0;
			}
		}

		&__submenu-link {
			display: flex;
			align-items: center;
			padding: vars.$spacing-xs vars.$spacing-sm;
			border-radius: vars.$border-radius-md;
			color: vars.$gray-dark;
			transition: all vars.$transition-base;

			&:hover {
				background-color: vars.$white-dark;
				color: vars.$black-light;
			}

			&--active {
				color: vars.$primary-color;
				font-weight: 500;
			}
		}

		&__submenu-icon {
			margin-right: vars.$spacing-sm;
			display: flex;
			align-items: center;
			opacity: 0.7;
		}
	}

	// Animation pour le sous-menu
	.submenu-enter-active,
	.submenu-leave-active {
		transition: all 0.3s ease;
		overflow: hidden;
	}

	.submenu-enter-from,
	.submenu-leave-to {
		opacity: 0;
		max-height: 0;
	}

	.submenu-enter-to,
	.submenu-leave-from {
		opacity: 1;
		max-height: 500px;
	}
</style>
