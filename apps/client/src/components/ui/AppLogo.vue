<template>
	<div :class="['app-logo', { 'app-logo--dark': dark }, customClass]">
		<slot>
			<span v-if="text" class="app-logo__text">{{ text }}</span>
			<img
				v-else-if="imagePath"
				:src="imagePath"
				:alt="alt"
				class="app-logo__image"
				:width="width"
				:height="height"
			/>
			<span v-else class="app-logo__default">
				<span class="app-logo__icon">
					<BaseIcon name="star" :size="iconSize" />
				</span>
				<span class="app-logo__name">{{ defaultName }}</span>
			</span>
		</slot>
	</div>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';

	defineProps({
		text: {
			type: String,
			default: '',
		},
		imagePath: {
			type: String,
			default: '',
		},
		alt: {
			type: String,
			default: 'Logo',
		},
		width: {
			type: [String, Number],
			default: 'auto',
		},
		height: {
			type: [String, Number],
			default: 'auto',
		},
		dark: {
			type: Boolean,
			default: false,
		},
		defaultName: {
			type: String,
			default: 'Juba Ait-adda',
		},
		iconSize: {
			type: [String, Number],
			default: 24,
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

	.app-logo {
		display: inline-flex;
		align-items: center;

		&__image {
			max-width: 100%;
			height: auto;
		}

		&__text {
			font-weight: 700;
			color: vars.$black;
		}

		&__default {
			display: flex;
			align-items: center;
			gap: vars.$spacing-xs;
		}

		&__icon {
			display: flex;
			align-items: center;
			justify-content: center;
			color: vars.$primary-color;
		}

		&__name {
			font-weight: 700;
			color: vars.$black;
		}

		// Variante sombre
		&--dark {
			.app-logo__text,
			.app-logo__name {
				color: vars.$white;
			}
		}
	}
</style>
