<template>
	<Card :class="['stack-card', customClass]" :hoverable="hoverable" :flat="flat" :bordered="bordered">
		<template #header>
			<div class="stack-card__header">
				<div class="stack-card__icon">
					<img v-if="stack.logo" :src="stack.logo" :alt="`${stack.name} icon`" class="stack-card__image" />
					<div v-else class="stack-card__letter">
						{{ getFirstLetter(stack.name) }}
					</div>
				</div>

				<div class="stack-card__titles">
					<h3 class="stack-card__name">{{ stack.name }}</h3>
					<div class="stack-card__experience-info">
						<BaseIcon name="clock" :size="16" class="stack-card__experience-icon" />
						<span class="stack-card__experience-years">
							{{ stack.experience }} {{ stack.experience > 1 ? 'années' : 'année' }}
						</span>
					</div>
				</div>
			</div>
		</template>

		<div class="stack-card__content">
			<p v-if="stack.description" class="stack-card__description">
				{{ truncateText(stack.description, descriptionLength) }}
			</p>

			<div v-if="stack.tags && stack.tags.length > 0" class="stack-card__tags">
				<Badge
					v-for="(tag, index) in stack.tags.slice(0, 3)"
					:key="index"
					:text="tag"
					type="primary"
					variant="subtle"
					rounded
					class="stack-card__tag-badge"
				/>
			</div>

			<slot></slot>
		</div>

		<!-- Section d'expérience en footer -->
		<template v-if="stack.experience > 0" #footer>
			<div class="stack-card__experience">
				<div class="stack-card__expertise-level">
					<div class="stack-card__expertise-label">Niveau d'expertise</div>
					<div class="stack-card__expertise-dots">
						<RatingStars :model-value="stack.level" :max="5" readonly :size="14" :show-value="false" />
					</div>
				</div>
			</div>
		</template>
	</Card>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import Badge from '@/components/ui/Badge.vue';
	import Card from '@/components/ui/Card.vue';
	import RatingStars from '@/components/ui/RatingStars.vue';
	import type { Stack } from '@/types/feature/stacks';

	defineProps({
		stack: {
			type: Object as () => Stack,
			required: true,
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
			default: 200,
		},
		customClass: {
			type: String,
			default: '',
		},
	});

	// Extraire la première lettre du nom
	const getFirstLetter = (name: string) => {
		return name.charAt(0).toUpperCase();
	};

	// Tronquer le texte de description
	const truncateText = (text: string, length: number) => {
		if (!text || text.length <= length) return text;
		return text.slice(0, length) + '...';
	};
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.stack-card {
		height: 100%;
		display: flex;
		flex-direction: column;
		position: relative;
		overflow: hidden;
		cursor: pointer;

		&::before {
			content: '';
			position: absolute;
			top: 0;
			left: 0;
			width: 100%;
			height: 4px;
			background: linear-gradient(
				90deg,
				vars.$primary-color,
				func.adjust-color-brightness(vars.$primary-color, 20%)
			);
			z-index: 2;
			transform: translateY(-100%);
			transition: transform vars.$transition-base;
		}

		&:hover::before {
			transform: translateY(0);
		}

		:deep(.card__body) {
			flex: 1;
			display: flex;
			flex-direction: column;
		}

		:deep(.card__footer) {
			padding: vars.$spacing-sm vars.$spacing-md;
			background-color: func.color-alpha(vars.$white-dark, 0.5);
		}

		&__header {
			display: flex;
			align-items: flex-start;
			gap: vars.$spacing-md;
			position: relative;
		}

		&__icon {
			width: 52px;
			height: 52px;
			border-radius: vars.$border-radius-md;
			overflow: hidden;
			display: flex;
			align-items: center;
			justify-content: center;
			background-color: vars.$white-dark;
			flex-shrink: 0;
			box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
			transition:
				transform vars.$transition-base,
				box-shadow vars.$transition-base;

			.stack-card:hover & {
				transform: scale(1.08);
				box-shadow: 0 6px 12px rgba(0, 0, 0, 0.12);
			}
		}

		&__image {
			width: 75%;
			height: 75%;
			object-fit: contain;
		}

		&__letter {
			width: 100%;
			height: 100%;
			display: flex;
			align-items: center;
			justify-content: center;
			font-weight: 700;
			color: vars.$white;
			background-color: vars.$primary-color;
		}

		&__titles {
			flex: 1;
			padding-top: vars.$spacing-xxs;
		}

		&__name {
			margin: 0;
			color: vars.$black-light;
			font-weight: 600;
			transition: color vars.$transition-base;

			.stack-card:hover & {
				color: vars.$primary-color;
			}
		}

		&__level-container {
			display: flex;
			flex-direction: column;
			align-items: flex-end;
			gap: vars.$spacing-xxs;
			padding-top: vars.$spacing-xxs;
		}

		&__level-value {
			font-weight: 600;
			color: vars.$primary-color;
		}

		&__category {
			margin: vars.$spacing-xs 0 0 0;
		}

		&__content {
			flex: 1;
			display: flex;
			flex-direction: column;
		}

		&__description {
			color: vars.$gray-dark;
			line-height: 1.6;
			margin-bottom: vars.$spacing-md;
		}

		&__tags {
			display: flex;
			flex-wrap: wrap;
			gap: vars.$spacing-xs;
			margin-bottom: vars.$spacing-md;
		}

		&__tag-badge {
			font-weight: 400;
			transition: transform vars.$transition-fast;

			&:hover {
				transform: translateY(-2px);
			}
		}

		&__experience {
			display: flex;
			flex-direction: column;
			gap: vars.$spacing-sm;
		}

		&__expertise-level {
			display: flex;
			justify-content: space-between;
			align-items: center;
		}

		&__expertise-label {
			color: vars.$gray-dark;
		}

		&__expertise-dots {
			display: flex;
			gap: 4px;
		}

		&__expertise-dot {
			width: 10px;
			height: 10px;
			border-radius: 50%;
			background-color: vars.$white-dark;
			border: 1px solid vars.$gray-light;
			transition: all vars.$transition-base;

			&--active {
				background-color: vars.$primary-color;
				border-color: vars.$primary-color;
				transform: scale(1.1);
			}
		}

		&__experience-info {
			display: flex;
			align-items: center;
			gap: vars.$spacing-xs;
			color: vars.$black-light;
			font-weight: 500;
		}

		&__experience-icon {
			color: vars.$primary-color;
		}
	}
</style>
