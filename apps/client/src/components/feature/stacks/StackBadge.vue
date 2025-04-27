<template>
	<div
		:class="['stack-badge', `stack-badge--${size}`, { 'stack-badge--clickable': clickable }, customClass]"
		role="button"
		tabindex="0"
		@click="handleClick"
		@keydown.enter="handleClick"
		@keydown.space.prevent="handleClick"
	>
		<div class="stack-badge__icon" :style="iconStyle">
			<img v-if="stack.logo" :src="stack.logo" :alt="`${stack.name} icon`" class="stack-badge__image" />
			<div v-else-if="stack.color" class="stack-badge__letter" :style="{ backgroundColor: stack.color }">
				{{ getFirstLetter(stack.name) }}
			</div>
			<div v-else class="stack-badge__letter stack-badge__letter--default">
				{{ getFirstLetter(stack.name) }}
			</div>
		</div>

		<div v-if="showName" class="stack-badge__name">
			{{ stack.name }}
		</div>

		<div v-if="showLevel && stack.level" class="stack-badge__level" :style="levelStyle">
			<div class="stack-badge__level-bar" :style="levelBarStyle"></div>
		</div>
	</div>
</template>

<script setup lang="ts">
	import { computed } from 'vue';

	interface Stack {
		id: string | number;
		name: string;
		logo?: string;
		color?: string;
		level?: number;
		category?: string;
		[key: string]: any;
	}

	const props = defineProps({
		stack: {
			type: Object as () => Stack,
			required: true,
		},
		size: {
			type: String,
			default: 'medium',
			validator: (value: string) => ['small', 'medium', 'large'].includes(value),
		},
		showName: {
			type: Boolean,
			default: true,
		},
		showLevel: {
			type: Boolean,
			default: false,
		},
		clickable: {
			type: Boolean,
			default: false,
		},
		customClass: {
			type: String,
			default: '',
		},
	});

	const emit = defineEmits(['click']);

	// Gérer le clic
	const handleClick = () => {
		if (props.clickable) {
			emit('click', props.stack);
		}
	};

	// Extraire la première lettre du nom
	const getFirstLetter = (name: string) => {
		return name.charAt(0).toUpperCase();
	};

	// Style pour l'icône
	const iconStyle = computed(() => {
		if (props.stack.color && !props.stack.logo && !props.stack.icon) {
			return {
				backgroundColor: props.stack.color,
				color: getContrastColor(props.stack.color),
			};
		}
		return {};
	});

	// Style pour la barre de niveau
	const levelStyle = computed(() => {
		return {
			backgroundColor: props.stack.color
				? `${props.stack.color}33` // Ajouter transparence
				: 'var(--gray-light)',
		};
	});

	// Style pour la barre de niveau remplie
	const levelBarStyle = computed(() => {
		const level = props.stack.level || 0;
		const width = Math.min(Math.max(level, 0), 5) * 20; // 0-5 -> 0-100%

		return {
			width: `${width}%`,
			backgroundColor: props.stack.color || 'var(--primary-color)',
		};
	});

	// Calculer la couleur de contraste pour le texte
	const getContrastColor = (hexColor: string) => {
		// Supprimer le # si présent
		const color = hexColor.charAt(0) === '#' ? hexColor.substring(1, 7) : hexColor;

		// Convertir en RGB
		const r = parseInt(color.substring(0, 2), 16) || 0; // Rouge
		const g = parseInt(color.substring(2, 4), 16) || 0; // Vert
		const b = parseInt(color.substring(4, 6), 16) || 0; // Bleu

		// Calculer la luminosité
		const yiq = (r * 299 + g * 587 + b * 114) / 1000;

		// Retourner noir ou blanc selon la luminosité
		return yiq >= 128 ? '#000000' : '#ffffff';
	};
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.stack-badge {
		display: inline-flex;
		flex-direction: column;
		align-items: center;
		transition:
			transform vars.$transition-base,
			box-shadow vars.$transition-base;
		user-select: none;
		gap: vars.$spacing-xs;

		&--clickable {
			cursor: pointer;

			&:hover {
				transform: translateY(-2px);
				box-shadow: vars.$box-shadow-medium;
			}
		}

		// Tailles
		&--small {
			.stack-badge__icon {
				width: 42px;
				height: 42px;
			}

			.stack-badge__name {
				background-color: vars.$white;
				border-radius: vars.$border-radius-md;
				box-shadow: vars.$box-shadow;
				padding: vars.$spacing-xs;
			}

			.stack-badge__level {
				height: 3px;
			}
		}

		&--medium {
			.stack-badge__icon {
				width: 48px;
				height: 48px;
			}

			.stack-badge__name {
				margin-top: vars.$spacing-xs;
			}

			.stack-badge__level {
				height: 4px;
				margin-top: vars.$spacing-xs;
			}
		}

		&--large {
			.stack-badge__icon {
				width: 64px;
				height: 64px;
			}

			.stack-badge__name {
				margin-top: vars.$spacing-sm;
			}

			.stack-badge__level {
				height: 5px;
				margin-top: vars.$spacing-sm;
			}
		}

		&__icon {
			display: flex;
			align-items: center;
			justify-content: center;
			border-radius: vars.$border-radius-md;
			overflow: hidden;
			background-color: vars.$white-dark;
		}

		&__image {
			width: 100%;
			height: 100%;
			object-fit: contain;
			padding: 4px;
		}

		&__letter {
			width: 100%;
			height: 100%;
			display: flex;
			align-items: center;
			justify-content: center;
			font-weight: 600;
			color: vars.$white;

			&--default {
				background-color: vars.$primary-color;
			}
		}

		&__name {
			text-align: center;
			font-weight: 500;
			color: vars.$black-light;
			white-space: nowrap;
			max-width: 100px;
			overflow: hidden;
			text-overflow: ellipsis;
		}

		&__level {
			width: 100%;
			border-radius: vars.$border-radius-full;
			overflow: hidden;
		}

		&__level-bar {
			height: 100%;
			border-radius: vars.$border-radius-full;
		}
	}
</style>
