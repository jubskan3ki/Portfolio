<!-- src/components/footer/ContactItem.vue -->
<template>
	<div class="contact-item">
		<BaseIcon :name="icon" :size="18" />
		<BaseLink v-if="isLink" :to="linkHref" class="contact-item__link">
			{{ text }}
		</BaseLink>
		<p v-else>{{ text }}</p>
	</div>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import BaseLink from '@/components/base/BaseLink.vue';
	import { computed } from 'vue';

	const props = defineProps({
		icon: {
			type: String,
			required: true,
		},
		text: {
			type: String,
			required: true,
		},
		isLink: {
			type: Boolean,
			default: false,
		},
		linkType: {
			type: String,
			default: '',
			validator: (value: string) => ['email', 'phone', ''].includes(value),
		},
	});

	const linkHref = computed(() => {
		if (props.linkType === 'email') {
			return `mailto:${props.text}`;
		} else if (props.linkType === 'phone') {
			return `tel:${props.text}`;
		}
		return props.text;
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.contact-item {
		display: flex;
		align-items: center;
		gap: vars.$spacing-sm;
		color: vars.$gray-dark;
		transition: transform 0.2s ease;

		&:hover {
			transform: translateX(5px);
		}

		&__link {
			color: inherit;
			text-decoration: none;
			transition: color vars.$transition-base;

			&:hover {
				color: vars.$primary-color;
			}
		}
	}
</style>
