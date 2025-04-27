<template>
	<div :class="['side-bar', `side-bar--${variant}`, { 'side-bar--collapsed': isCollapsed }, customClass]">
		<div v-if="$slots.header" class="side-bar__header">
			<slot name="header"></slot>
		</div>

		<div v-if="collapsible" class="side-bar__toggle">
			<button
				class="side-bar__toggle-btn"
				:aria-label="isCollapsed ? 'Déplier le menu' : 'Replier le menu'"
				@click="toggleCollapse"
			>
				<BaseIcon :name="isCollapsed ? 'chevron-right' : 'chevron-left'" :size="16" />
			</button>
		</div>

		<nav class="side-bar__nav">
			<template v-if="sections.length > 0">
				<div v-for="(section, sectionIndex) in sections" :key="sectionIndex" class="side-bar__section">
					<h3 v-if="section.title && !isCollapsed" class="side-bar__section-title">
						{{ section.title }}
					</h3>

					<ul class="side-bar__list">
						<SideBarItem
							v-for="(item, itemIndex) in section.items"
							:key="itemIndex"
							:text="item.text"
							:to="item.to"
							:icon="item.icon"
							:badge="item.badge"
							:is-collapsed="isCollapsed"
						/>
					</ul>
				</div>
			</template>

			<slot v-else></slot>
		</nav>

		<div v-if="$slots.footer" class="side-bar__footer">
			<slot name="footer"></slot>
		</div>
	</div>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import SideBarItem from '@/components/navigation/SideBarItem.vue';
	import { ref } from 'vue';

	interface NavItem {
		text: string;
		to: string;
		icon?: string;
		badge?: {
			type?: 'info' | 'success' | 'warning' | 'danger';
			value?: string | number;
		};
	}

	interface NavSection {
		title?: string;
		items: NavItem[];
	}

	const props = defineProps({
		sections: {
			type: Array as () => NavSection[],
			default: () => [],
		},
		variant: {
			type: String,
			default: 'light',
			validator: (value: string) => ['light', 'dark'].includes(value),
		},
		collapsible: {
			type: Boolean,
			default: false,
		},
		defaultCollapsed: {
			type: Boolean,
			default: false,
		},
		customClass: {
			type: String,
			default: '',
		},
	});

	const emit = defineEmits(['collapse', 'expand']);

	const isCollapsed = ref(props.defaultCollapsed);

	// Basculer l'état de repli
	const toggleCollapse = () => {
		isCollapsed.value = !isCollapsed.value;
		emit(isCollapsed.value ? 'collapse' : 'expand');
	};
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.side-bar {
		display: flex;
		flex-direction: column;
		height: 100%;
		width: 240px;
		transition: width vars.$transition-base;
		position: relative;

		&--collapsed {
			width: 64px;

			.side-bar__section-title {
				height: 0;
				margin: 0;
				overflow: hidden;
			}
		}

		&__header {
			padding: vars.$spacing-md;
			border-bottom: 1px solid;
		}

		&__toggle {
			position: absolute;
			top: vars.$spacing-lg;
			right: -12px;
			z-index: 1;
		}

		&__toggle-btn {
			display: flex;
			align-items: center;
			justify-content: center;
			width: 24px;
			height: 24px;
			border-radius: 50%;
			border: 1px solid;
			cursor: pointer;
			transition: all vars.$transition-base;
		}

		&__nav {
			flex: 1;
			overflow-y: auto;
			padding: vars.$spacing-md 0;
		}

		&__section {
			margin-bottom: vars.$spacing-md;

			&:last-child {
				margin-bottom: 0;
			}
		}

		&__section-title {
			padding: 0 vars.$spacing-md;
			margin-bottom: vars.$spacing-xs;
			font-weight: 600;
			text-transform: uppercase;
			transition: all vars.$transition-base;
		}

		&__list {
			list-style: none;
			padding: 0;
		}

		&__footer {
			padding: vars.$spacing-md;
			border-top: 1px solid;
		}

		// Variante claire
		&--light {
			background-color: vars.$white;
			border-right: 1px solid vars.$white-dark;

			.side-bar__header {
				border-bottom-color: vars.$white-dark;
			}

			.side-bar__section-title {
				color: vars.$gray;
			}

			:deep(.side-bar-item__link) {
				color: vars.$black-light;

				&:hover {
					background-color: vars.$white-dark;
					color: vars.$primary-color;
				}

				&--active {
					background-color: func.color-alpha(vars.$primary-color, 0.1);
					color: vars.$primary-color;
				}
			}

			.side-bar__toggle-btn {
				background-color: vars.$white;
				border-color: vars.$white-dark;
				color: vars.$gray-dark;

				&:hover {
					background-color: vars.$white-dark;
					color: vars.$primary-color;
				}
			}

			.side-bar__footer {
				border-top-color: vars.$white-dark;
			}
		}

		// Variante sombre
		&--dark {
			background-color: vars.$black-light;

			.side-bar__header {
				border-bottom-color: func.color-alpha(vars.$white, 0.1);
			}

			.side-bar__section-title {
				color: vars.$gray-light;
			}

			:deep(.side-bar-item__link) {
				color: vars.$white;

				&:hover {
					background-color: func.color-alpha(vars.$white, 0.05);
				}

				&--active {
					background-color: func.color-alpha(vars.$primary-color, 0.2);
					color: vars.$primary-color;
				}
			}

			.side-bar__toggle-btn {
				background-color: vars.$black-light;
				border-color: func.color-alpha(vars.$white, 0.2);
				color: vars.$white;

				&:hover {
					background-color: func.color-alpha(vars.$white, 0.1);
				}
			}

			.side-bar__footer {
				border-top-color: func.color-alpha(vars.$white, 0.1);
			}
		}
	}
</style>
