<!--
  AuthorInfo.vue
  Composant pour afficher les informations de l'auteur d'un article
-->
<template>
	<Card class="author-info">
		<div class="author-info__content">
			<Avatar :src="avatar" size="large" class="author-info__avatar" />
			<h3 class="author-info__name">
				{{ name }}
			</h3>
			<p class="author-info__bio">
				{{ bio }}
			</p>
			<div class="author-info__social">
				<a
					v-if="github"
					:href="github"
					target="_blank"
					rel="noopener noreferrer"
					aria-label="GitHub"
					class="author-info__social-link"
				>
					<BaseIcon name="github" :size="20" />
				</a>
				<a
					v-if="linkedin"
					:href="linkedin"
					target="_blank"
					rel="noopener noreferrer"
					aria-label="LinkedIn"
					class="author-info__social-link"
				>
					<BaseIcon name="linkedin" :size="20" />
				</a>
				<a
					v-if="twitter"
					:href="twitter"
					target="_blank"
					rel="noopener noreferrer"
					aria-label="Twitter"
					class="author-info__social-link"
				>
					<BaseIcon name="twitter" :size="20" />
				</a>
			</div>
		</div>
	</Card>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import Avatar from '@/components/ui/Avatar.vue';
	import Card from '@/components/ui/Card.vue';

	defineProps({
		name: {
			type: String,
			default: 'Juba Ait-Adda',
		},
		avatar: {
			type: String,
			default: '/api/placeholder/100/100',
		},
		bio: {
			type: String,
			default: 'Développeur Full-Stack et DevOps',
		},
		github: {
			type: String,
			default: '',
		},
		linkedin: {
			type: String,
			default: '',
		},
		twitter: {
			type: String,
			default: '',
		},
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.author-info {
		&__content {
			display: flex;
			flex-direction: column;
			align-items: center;
			text-align: center;
		}

		&__avatar {
			margin-bottom: vars.$spacing-md;
		}

		&__name {
			margin-bottom: vars.$spacing-sm;
			color: vars.$black-light;
		}

		&__bio {
			color: vars.$gray-dark;
			margin-bottom: vars.$spacing-md;
			line-height: 1.6;
		}

		&__social {
			display: flex;
			gap: vars.$spacing-md;
		}

		&__social-link {
			display: flex;
			align-items: center;
			justify-content: center;
			width: 36px;
			height: 36px;
			border-radius: 50%;
			background-color: vars.$white-dark;
			color: vars.$gray-dark;
			transition: all 0.3s ease;

			&:hover {
				background-color: vars.$primary-color;
				color: vars.$white;
				transform: translateY(-3px);
			}
		}
	}
</style>
