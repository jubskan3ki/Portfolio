<template>
	<span
		:class="[
			'badge',
			`badge--${type}`,
			`badge--${variant}`,
			{ 'badge--rounded': rounded },
			{ 'badge--dot': dot },
			customClass,
		]"
	>
		<span v-if="icon && !dot" class="badge__icon">
			<BaseIcon :name="icon" :size="iconSize" />
		</span>
		<slot v-if="!dot">{{ text }}</slot>
	</span>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';

	defineProps({
		text: {
			type: String,
			default: '',
		},
		type: {
			type: String,
			default: 'primary',
			validator: (value: string) =>
				['primary', 'secondary', 'success', 'danger', 'warning', 'info'].includes(value),
		},
		variant: {
			type: String,
			default: 'filled',
			validator: (value: string) => ['filled', 'outlined', 'subtle'].includes(value),
		},
		rounded: {
			type: Boolean,
			default: false,
		},
		dot: {
			type: Boolean,
			default: false,
		},
		icon: {
			type: String,
			default: '',
		},
		iconSize: {
			type: [Number, String],
			default: 12,
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

	.badge {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		font-weight: 500;
		line-height: 1;
		padding: 0.25rem 0.5rem;
		border-radius: vars.$border-radius-sm;

		&__icon {
			margin-right: 0.25rem;
			display: flex;
			align-items: center;
			justify-content: center;
		}

		// Types
		&--primary {
			&.badge--filled {
				background-color: vars.$primary-color;
				color: vars.$white;
			}

			&.badge--outlined {
				background-color: transparent;
				border: 1px solid vars.$primary-color;
				color: vars.$primary-color;
			}

			&.badge--subtle {
				background-color: func.color-alpha(vars.$primary-color, 0.1);
				color: vars.$primary-color;
			}
		}

		&--secondary {
			&.badge--filled {
				background-color: vars.$secondary-color;
				color: vars.$white;
			}

			&.badge--outlined {
				background-color: transparent;
				border: 1px solid vars.$secondary-color;
				color: vars.$secondary-color;
			}

			&.badge--subtle {
				background-color: func.color-alpha(vars.$secondary-color, 0.1);
				color: vars.$secondary-color;
			}
		}

		&--success {
			&.badge--filled {
				background-color: vars.$success-color;
				color: vars.$white;
			}

			&.badge--outlined {
				background-color: transparent;
				border: 1px solid vars.$success-color;
				color: vars.$success-color;
			}

			&.badge--subtle {
				background-color: func.color-alpha(vars.$success-color, 0.1);
				color: vars.$success-color;
			}
		}

		&--danger {
			&.badge--filled {
				background-color: vars.$danger-color;
				color: vars.$white;
			}

			&.badge--outlined {
				background-color: transparent;
				border: 1px solid vars.$danger-color;
				color: vars.$danger-color;
			}

			&.badge--subtle {
				background-color: func.color-alpha(vars.$danger-color, 0.1);
				color: vars.$danger-color;
			}
		}

		&--warning {
			&.badge--filled {
				background-color: vars.$warning-color;
				color: vars.$black;
			}

			&.badge--outlined {
				background-color: transparent;
				border: 1px solid vars.$warning-color;
				color: vars.$warning-color;
			}

			&.badge--subtle {
				background-color: func.color-alpha(vars.$warning-color, 0.1);
				color: vars.$warning-color;
			}
		}

		&--info {
			&.badge--filled {
				background-color: vars.$info-color;
				color: vars.$white;
			}

			&.badge--outlined {
				background-color: transparent;
				border: 1px solid vars.$info-color;
				color: vars.$info-color;
			}

			&.badge--subtle {
				background-color: func.color-alpha(vars.$info-color, 0.1);
				color: vars.$info-color;
			}
		}

		// Forme arrondie
		&--rounded {
			border-radius: vars.$border-radius-full;
		}

		// Variante dot
		&--dot {
			width: 8px;
			height: 8px;
			padding: 0;
			border-radius: 50%;
		}
	}
</style>
