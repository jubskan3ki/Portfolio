<!-- src/components/footer/SocialLinks.vue -->
<template>
	<div class="social-links">
		<SectionHeading :title="title" />
		<div class="social-links__list">
			<BaseLink
				v-for="(social, index) in links"
				:key="index"
				:to="social.url"
				target="_blank"
				class="social-links__item"
				:aria-label="social.name"
			>
				<template #icon-left>
					<BaseIcon :name="social.icon" :size="20" />
				</template>
				<span class="social-links__name">{{ social.name }}</span>
			</BaseLink>
		</div>
	</div>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import BaseLink from '@/components/base/BaseLink.vue';
	import SectionHeading from '@/components/ui/SectionHeading.vue';
	import { SocialLink } from '@/config/footer';
	import { PropType } from 'vue';

	defineProps({
		title: {
			type: String,
			default: 'Suivez-moi',
		},
		links: {
			type: Array as PropType<SocialLink[]>,
			required: true,
		},
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.social-links {
		&__list {
			display: flex;
			flex-direction: column;
			gap: vars.$spacing-sm;
		}

		&__item {
			display: flex;
			align-items: center;
			gap: vars.$spacing-sm;
			color: vars.$gray-dark;
			background-color: vars.$white;
			padding: vars.$spacing-sm vars.$spacing-md;
			border-radius: vars.$border-radius-md;
			box-shadow: vars.$box-shadow;
			transition: all vars.$transition-base;
			text-decoration: none;

			&:hover {
				background-color: vars.$primary-color;
				color: vars.$white;
				transform: translateY(-3px);
			}
		}
	}
</style>
