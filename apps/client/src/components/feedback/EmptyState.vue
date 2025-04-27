<template>
	<div :class="['empty-state', customClass]">
		<div v-if="$slots.icon || icon" class="empty-state__icon">
			<slot name="icon">
				<BaseIcon :name="icon" :size="iconSize" />
			</slot>
		</div>

		<div class="empty-state__content">
			<h3 v-if="title" class="empty-state__title">{{ title }}</h3>

			<p v-if="$slots.default || description" class="empty-state__description">
				<slot>{{ description }}</slot>
			</p>

			<div v-if="$slots.action" class="empty-state__action">
				<slot name="action"></slot>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';

	defineProps({
		title: {
			type: String,
			default: '',
		},
		description: {
			type: String,
			default: '',
		},
		icon: {
			type: String,
			default: '',
		},
		iconSize: {
			type: [Number, String],
			default: 48,
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

	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		text-align: center;
		padding: vars.$spacing-lg;

		&__icon {
			margin-bottom: vars.$spacing-md;
			color: vars.$gray-light;
		}

		&__content {
			max-width: 400px;
		}

		&__title {
			margin-bottom: vars.$spacing-sm;
			color: vars.$black;
		}

		&__description {
			color: vars.$gray-dark;
			margin-bottom: vars.$spacing-md;
		}

		&__action {
			margin-top: vars.$spacing-md;
		}
	}
</style>
