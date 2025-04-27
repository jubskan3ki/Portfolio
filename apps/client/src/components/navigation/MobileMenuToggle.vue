<template>
	<button
		class="mobile-menu-toggle"
		:class="{ 'mobile-menu-toggle--active': isActive }"
		aria-label="Ouvrir le menu de navigation"
		@click="$emit('toggle')"
	>
		<span class="mobile-menu-toggle__icon"></span>
	</button>
</template>

<script setup lang="ts">
	defineProps({
		isActive: {
			type: Boolean,
			default: false,
		},
	});

	defineEmits(['toggle']);
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.mobile-menu-toggle {
		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;
		width: 40px;
		height: 40px;
		border-radius: 50%;
		background-color: func.color-alpha(vars.$white, 0.1);
		backdrop-filter: blur(5px);
		transition: all 0.3s ease;
		z-index: func.z('navbar') + 20;
		padding: 0;
		cursor: pointer;

		@include mix.responsive(tablet-up) {
			display: none;
		}

		&:hover {
			background-color: func.color-alpha(vars.$white, 0.2);
		}

		&--active {
			background-color: func.color-alpha(vars.$primary-color, 0.15);

			.mobile-menu-toggle__icon {
				background-color: transparent;

				&::before {
					transform: translateY(0) rotate(45deg);
				}

				&::after {
					transform: translateY(0) rotate(-45deg);
				}
			}
		}

		&__icon {
			position: relative;
			width: 20px;
			height: 2px;
			background-color: vars.$black-light;
			transition: all 0.3s ease;

			&::before,
			&::after {
				content: '';
				position: absolute;
				left: 0;
				width: 100%;
				height: 100%;
				background-color: vars.$black-light;
				transition: all 0.3s ease;
			}

			&::before {
				transform: translateY(-6px);
			}

			&::after {
				transform: translateY(6px);
			}
		}
	}
</style>
