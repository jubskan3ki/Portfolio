<template>
	<BaseLink v-if="projectLink" :to="projectLink" class="project-card-link">
		<Card
			:class="['project-card', { 'project-card--featured': featured }, customClass]"
			:hoverable="hoverable"
			:flat="flat"
			:bordered="bordered"
		>
			<template v-if="project.image" #image>
				<div class="project-card__image">
					<img :src="project.image" :alt="project.title" />
					<div class="project-card__image-overlay">
						<div class="project-card__category">
							<Badge :text="project.category" type="primary" variant="filled" rounded />
						</div>
					</div>
				</div>
			</template>

			<template #header>
				<div class="project-card__header">
					<h3 class="project-card__title">{{ project.title }}</h3>
				</div>
			</template>

			<div class="project-card__content">
				<p v-if="project.description" class="project-card__description">
					{{ truncateText(project.description, descriptionLength) }}
				</p>

				<div v-if="hasTechnologies" class="project-card__technologies">
					<Badge
						v-for="tech in displayedTechnologies"
						:key="tech"
						:text="tech"
						type="secondary"
						variant="subtle"
						rounded
						class="project-card__tech-badge"
					/>
					<span v-if="hasMoreTechnologies" class="project-card__tech-more">
						+{{ project.technologies.length - maxTechnologies }}
					</span>
				</div>

				<div class="project-card__date">
					<BaseIcon name="calendar" :size="14" />
					<span>{{ formatDate(project.date) }}</span>
				</div>
			</div>
		</Card>
	</BaseLink>

	<Card
		v-else
		:class="['project-card', { 'project-card--featured': featured }, customClass]"
		:hoverable="hoverable"
		:flat="flat"
		:bordered="bordered"
	>
		<template v-if="project.image" #image>
			<div class="project-card__image">
				<img :src="project.image" :alt="project.title" />
				<div class="project-card__image-overlay">
					<div class="project-card__category">
						<Badge :text="project.category" type="primary" variant="filled" rounded />
					</div>
				</div>
			</div>
		</template>

		<template #header>
			<div class="project-card__header">
				<h3 class="project-card__title">{{ project.title }}</h3>
			</div>
		</template>

		<div class="project-card__content">
			<p v-if="project.description" class="project-card__description">
				{{ truncateText(project.description, descriptionLength) }}
			</p>

			<div v-if="hasTechnologies" class="project-card__technologies">
				<Badge
					v-for="tech in displayedTechnologies"
					:key="tech"
					:text="tech"
					type="secondary"
					variant="subtle"
					rounded
					class="project-card__tech-badge"
				/>
				<span v-if="hasMoreTechnologies" class="project-card__tech-more">
					+{{ project.technologies.length - maxTechnologies }}
				</span>
			</div>

			<div class="project-card__date">
				<BaseIcon name="calendar" :size="14" />
				<span>{{ formatDate(project.date) }}</span>
			</div>
		</div>
	</Card>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import BaseLink from '@/components/base/BaseLink.vue';
	import Badge from '@/components/ui/Badge.vue';
	import Card from '@/components/ui/Card.vue';
	import type { Project } from '@/types/feature/project';
	import { computed } from 'vue';

	const props = defineProps({
		project: {
			type: Object as () => Project,
			required: true,
		},
		featured: {
			type: Boolean,
			default: false,
		},
		hoverable: {
			type: Boolean,
			default: true,
		},
		flat: {
			type: Boolean,
			default: false,
		},
		bordered: {
			type: Boolean,
			default: false,
		},
		descriptionLength: {
			type: Number,
			default: 150,
		},
		maxTechnologies: {
			type: Number,
			default: 3,
		},
		customClass: {
			type: String,
			default: '',
		},
	});

	// Calculer le lien vers la page détaillée du projet
	const projectLink = computed(() => {
		if (props.project.slug) {
			return `/projects/${props.project.slug}`;
		}
		return '';
	});

	// Vérifier s'il y a des technologies
	const hasTechnologies = computed(() => {
		return !!(props.project.technologies && props.project.technologies.length > 0);
	});

	// Technologies à afficher (limitées)
	const displayedTechnologies = computed(() => {
		if (!props.project.technologies) return [];
		return props.project.technologies.slice(0, props.maxTechnologies);
	});

	// Vérifier s'il y a plus de technologies que le maximum affiché
	const hasMoreTechnologies = computed(() => {
		return !!(props.project.technologies && props.project.technologies.length > props.maxTechnologies);
	});

	// Tronquer le texte de description
	const truncateText = (text: string, length: number) => {
		if (!text || text.length <= length) return text;
		return text.slice(0, length) + '...';
	};

	// Formater la date
	const formatDate = (date: string | Date) => {
		try {
			const dateObj = date instanceof Date ? date : new Date(date);
			return dateObj.toLocaleDateString('fr-FR', {
				year: 'numeric',
				month: 'long',
			});
		} catch (e) {
			return String(date);
		}
	};
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.project-card-link {
		display: block;
		height: 100%;
		text-decoration: none;
		color: inherit;
	}

	.project-card {
		height: 100%;
		display: flex;
		flex-direction: column;
		position: relative;
		overflow: hidden;

		// Barre colorée supérieure
		&::before {
			content: '';
			position: absolute;
			top: 0;
			left: 0;
			width: 100%;
			height: 3px;
			background: linear-gradient(
				90deg,
				vars.$primary-color,
				func.adjust-color-brightness(vars.$primary-color, 20%)
			);
			z-index: 2;
			opacity: 0;
			transition: opacity vars.$transition-base;
		}

		.project-card-link:hover &::before,
		&:hover::before {
			opacity: 1;
		}

		&--featured {
			border-top: 3px solid vars.$primary-color;

			&::before {
				opacity: 1;
				height: 0;
			}
		}

		:deep(.card__body) {
			flex: 1;
			display: flex;
			flex-direction: column;
		}

		&__image {
			position: relative;
			overflow: hidden;
			height: 180px;

			img {
				width: 100%;
				height: 100%;
				object-fit: cover;
				transition: transform vars.$transition-base;

				.project-card-link:hover &,
				.project-card:hover & {
					transform: scale(1.05);
				}
			}
		}

		&__image-overlay {
			position: absolute;
			top: 0;
			left: 0;
			right: 0;
			bottom: 0;
			background: linear-gradient(to bottom, rgba(0, 0, 0, 0.4), transparent 40%);
			display: flex;
			justify-content: flex-start;
			align-items: flex-start;
			padding: vars.$spacing-sm;
		}

		&__category {
			:deep(.badge) {
				font-weight: 500;
				box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
			}
		}

		&__header {
			position: relative;
		}

		&__title {
			margin: 0;
			margin-bottom: vars.$spacing-xs;
			line-height: 1.3;
			color: vars.$black-light;
			transition: color vars.$transition-base;

			.project-card-link:hover &,
			.project-card:hover & {
				color: vars.$primary-color;
			}
		}

		&__content {
			flex: 1;
			display: flex;
			flex-direction: column;
		}

		&__description {
			color: vars.$gray-dark;
			margin-bottom: vars.$spacing-md;
			line-height: 1.6;
			@include mix.truncate(3);
		}

		&__technologies {
			display: flex;
			flex-wrap: wrap;
			gap: vars.$spacing-xs;
			margin-bottom: vars.$spacing-md;
			pointer-events: auto;
		}

		&__tech-badge {
			transition: transform vars.$transition-fast;
			z-index: 1;

			&:hover {
				transform: translateY(-2px);
			}
		}

		&__tech-more {
			display: inline-flex;
			align-items: center;
			justify-content: center;
			padding: 0 vars.$spacing-xs;
			height: 20px;
			background: func.color-alpha(vars.$gray-light, 0.3);
			color: vars.$gray-dark;
			border-radius: vars.$border-radius-full;
		}

		&__date {
			margin-top: auto;
			padding-top: vars.$spacing-md;
			display: flex;
			align-items: center;
			gap: vars.$spacing-xs;
			color: vars.$gray-dark;
			border-top: 1px dashed func.color-alpha(vars.$gray-light, 0.5);
		}

		&__actions {
			display: flex;
			flex-wrap: wrap;
			gap: vars.$spacing-sm;
			justify-content: space-between;

			@include mix.responsive(mobile) {
				flex-direction: column;
				align-items: stretch;
			}
		}

		&__action-btn {
			display: inline-flex;
			align-items: center;
			gap: vars.$spacing-xs;
			transition: transform vars.$transition-fast;

			&:hover {
				transform: translateY(-2px);
			}
		}
	}
</style>
