<template>
	<div class="experience-card">
		<div class="experience-card__header">
			<div v-if="logo" class="experience-card__logo">
				<img :src="logo" :alt="company" class="experience-card__logo-img" />
			</div>
			<div class="experience-card__header-content">
				<h3 class="experience-card__title">{{ title }}</h3>
				<div class="experience-card__company">
					{{ company }}
					<span v-if="location" class="experience-card__location">
						<BaseIcon name="map-pin" :size="14" />
						{{ location }}
					</span>
				</div>
				<div class="experience-card__period">
					<BaseIcon name="calendar" :size="14" />
					{{ displayPeriod }}
				</div>
			</div>
		</div>

		<div class="experience-card__body">
			<p v-if="description" class="experience-card__description">{{ description }}</p>

			<div v-if="skillsArray && skillsArray.length" class="experience-card__skills">
				<div class="experience-card__section-title">Compétences</div>
				<div class="experience-card__skills-list">
					<Badge v-for="(skill, index) in skillsArray" :key="index" :text="String(skill)" variant="filled" />
				</div>
			</div>

			<div v-if="achievementsArray && achievementsArray.length" class="experience-card__achievements">
				<div class="experience-card__section-title">Réalisations</div>
				<ul class="experience-card__achievements-list">
					<li
						v-for="(achievement, index) in achievementsArray"
						:key="index"
						class="experience-card__achievement-item"
					>
						{{ achievement }}
					</li>
				</ul>
			</div>
		</div>

		<div v-if="$slots.footer" class="experience-card__footer">
			<slot name="footer"></slot>
		</div>
	</div>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import Badge from '@/components/ui/Badge.vue';
	import { computed } from 'vue';

	// Type personnalisé pour les tableaux qui peuvent être en lecture seule
	type ReadonlyOrRegularArray<T> = T[] | readonly T[];

	const props = defineProps({
		title: {
			type: String,
			required: true,
		},
		company: {
			type: String,
			required: true,
		},
		logo: {
			type: String,
			default: '',
		},
		location: {
			type: String,
			default: '',
		},
		startDate: {
			type: String,
			required: true,
		},
		endDate: {
			type: String,
			default: '',
		},
		period: {
			type: String,
			default: '',
		},
		description: {
			type: String,
			default: '',
		},
		skills: {
			type: [String, Array] as unknown as () => string | ReadonlyOrRegularArray<string>,
			default: () => [],
		},
		achievements: {
			type: [String, Array] as unknown as () => string | ReadonlyOrRegularArray<string>,
			default: () => [],
		},
		dateFormat: {
			type: String,
			default: 'MMM yyyy',
		},
		currentText: {
			type: String,
			default: 'Présent',
		},
	});

	// Formater une date
	const formatDate = (dateString: string, format: string): string => {
		if (!dateString) return '';

		try {
			const date = new Date(dateString);

			// Format simple - mois année
			if (format === 'MMM yyyy') {
				const month = date.toLocaleString('fr-FR', { month: 'short' });
				const year = date.getFullYear();
				return `${month} ${year}`;
			}

			// Format complet
			if (format === 'full') {
				return date.toLocaleDateString('fr-FR', {
					year: 'numeric',
					month: 'long',
					day: 'numeric',
				});
			}

			// Format par défaut
			return date.toLocaleDateString('fr-FR');
		} catch (error) {
			console.error('Error formatting date:', error);
			return dateString;
		}
	};

	// Période d'affichage
	const displayPeriod = computed(() => {
		if (props.period) {
			return props.period;
		}

		const start = formatDate(props.startDate, props.dateFormat);
		const end = props.endDate ? formatDate(props.endDate, props.dateFormat) : props.currentText;

		return `${start} - ${end}`;
	});

	// Convertir les compétences en tableau de strings
	const skillsArray = computed((): string[] => {
		if (Array.isArray(props.skills)) {
			return [...props.skills].map((skill) => String(skill));
		}

		if (typeof props.skills === 'string' && props.skills.trim() !== '') {
			return props.skills.split(',').map((skill) => skill.trim());
		}

		return [];
	});

	// Convertir les réalisations en tableau
	const achievementsArray = computed((): string[] => {
		if (Array.isArray(props.achievements)) {
			return [...props.achievements].map((achievement) => String(achievement));
		}

		if (typeof props.achievements === 'string' && props.achievements.trim() !== '') {
			return props.achievements
				.split('\n')
				.map((line) => line.trim())
				.filter((line) => line !== '');
		}

		return [];
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;

	// Fonction color-alpha pour remplacer la fonction SASS
	@function color-alpha($color, $alpha) {
		@return rgba($color, $alpha);
	}

	.experience-card {
		padding: vars.$spacing-md;
		background-color: vars.$white;
		border-radius: vars.$border-radius-md;
		box-shadow: vars.$box-shadow;
		transition:
			transform vars.$transition-base,
			box-shadow vars.$transition-base;

		&:hover {
			transform: translateY(-2px);
			box-shadow: vars.$box-shadow-medium;
		}

		&__header {
			display: flex;
			gap: vars.$spacing-md;
			margin-bottom: vars.$spacing-md;
		}

		&__logo {
			flex-shrink: 0;
			width: 50px;
			height: 50px;
			display: flex;
			align-items: center;
			justify-content: center;
			background-color: vars.$white-dark;
			border-radius: vars.$border-radius-md;
			overflow: hidden;

			&-img {
				max-width: 100%;
				max-height: 100%;
				object-fit: contain;
			}
		}

		&__header-content {
			flex: 1;
		}

		&__title {
			margin-bottom: vars.$spacing-xs;
			font-weight: 600;
			color: vars.$black;
		}

		&__company {
			display: flex;
			flex-wrap: wrap;
			align-items: center;
			gap: vars.$spacing-sm;
			margin-bottom: vars.$spacing-xs;
			font-weight: 500;
			color: vars.$gray-dark;
		}

		&__location {
			display: inline-flex;
			align-items: center;
			gap: vars.$spacing-xs;
			color: vars.$gray;
		}

		&__period {
			display: flex;
			align-items: center;
			gap: vars.$spacing-xs;
			color: vars.$gray;
		}

		&__body {
			margin-bottom: vars.$spacing-md;
		}

		&__description {
			margin-bottom: vars.$spacing-md;
			line-height: 1.5;
		}

		&__section-title {
			font-weight: 600;
			margin-bottom: vars.$spacing-sm;
			color: vars.$black-light;
		}

		&__skills {
			margin-bottom: vars.$spacing-md;
		}

		&__skills-list {
			display: flex;
			flex-wrap: wrap;
			gap: vars.$spacing-xs;
		}

		&__achievements {
			margin-bottom: vars.$spacing-md;
		}

		&__achievements-list {
			list-style-type: none;
			padding-left: 0;
		}

		&__achievement-item {
			position: relative;
			padding-left: 1.5rem;
			margin-bottom: vars.$spacing-xs;
			line-height: 1.4;

			&::before {
				content: '';
				position: absolute;
				left: 0;
				top: 0.5rem;
				width: 6px;
				height: 6px;
				border-radius: 50%;
				background-color: vars.$primary-color;
			}
		}

		&__footer {
			margin-top: vars.$spacing-md;
			padding-top: vars.$spacing-sm;
			border-top: 1px solid rgba(vars.$gray-light, 0.5);
		}
	}
</style>
