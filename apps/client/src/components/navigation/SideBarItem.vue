<template>
	<li class="side-bar-item">
		<NuxtLink
			:to="to"
			:class="[
				'side-bar-item__link',
				{ 'side-bar-item__link--active': isActive },
				{ 'side-bar-item__link--collapsed': isCollapsed },
			]"
			:title="isCollapsed ? text : undefined"
		>
			<span v-if="icon" class="side-bar-item__icon">
				<BaseIcon :name="icon" :size="20" />
			</span>
			<span v-if="!isCollapsed" class="side-bar-item__text">{{ text }}</span>
			<BaseIcon
				v-if="badge && !isCollapsed"
				:name="getBadgeIcon"
				:size="16"
				:class="['side-bar-item__badge', `side-bar-item__badge--${badge.type || 'info'}`]"
			/>
		</NuxtLink>
	</li>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import { computed } from 'vue';
	import { useRoute } from 'vue-router';

	interface Badge {
		type?: 'info' | 'success' | 'warning' | 'danger';
		value?: string | number;
	}

	const props = defineProps({
		text: {
			type: String,
			required: true,
		},
		to: {
			type: String,
			required: true,
		},
		icon: {
			type: String,
			default: '',
		},
		badge: {
			type: Object as () => Badge,
			default: undefined,
		},
		isCollapsed: {
			type: Boolean,
			default: false,
		},
	});

	const route = useRoute();

	// Vérifier si la route est active
	const isActive = computed(() => {
		if (props.to === '/' && route.path === '/') {
			return true;
		}
		return props.to !== '/' && route.path.startsWith(props.to);
	});

	// Déterminer l'icône du badge
	const getBadgeIcon = computed(() => {
		if (!props.badge) return '';

		const type = props.badge.type || 'info';

		switch (type) {
			case 'success':
				return 'check-circle';
			case 'warning':
				return 'alert-triangle';
			case 'danger':
				return 'alert-circle';
			case 'info':
			default:
				return 'info';
		}
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.side-bar-item {
		margin-bottom: 2px;

		&__link {
			display: flex;
			align-items: center;
			padding: vars.$spacing-sm vars.$spacing-md;
			transition: all vars.$transition-base;
			position: relative;

			&--collapsed {
				justify-content: center;
				padding: vars.$spacing-sm 0;
			}

			&--active {
				font-weight: 500;

				&::before {
					content: '';
					position: absolute;
					left: 0;
					top: 0;
					bottom: 0;
					width: 3px;
					background-color: vars.$primary-color;
				}
			}
		}

		&__icon {
			display: flex;
			align-items: center;
			justify-content: center;
			margin-right: vars.$spacing-sm;

			.side-bar-item__link--collapsed & {
				margin-right: 0;
			}
		}

		&__text {
			flex: 1;
			white-space: nowrap;
			overflow: hidden;
			text-overflow: ellipsis;
		}

		&__badge {
			margin-left: vars.$spacing-sm;

			&--info {
				color: vars.$info-color;
			}

			&--success {
				color: vars.$success-color;
			}

			&--warning {
				color: vars.$warning-color;
			}

			&--danger {
				color: vars.$danger-color;
			}
		}
	}
</style>
