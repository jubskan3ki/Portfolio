<!-- src/components/feedback/AlertItem.vue -->
<template>
	<div
		class="alert-item"
		:class="[`alert-item--${alert.type}`, { 'alert-item--closing': isClosing }]"
		role="alert"
		@mouseenter="pauseAutoClose"
		@mouseleave="resumeAutoClose"
	>
		<div class="alert-item__icon">
			<BaseIcon :name="iconName" />
		</div>

		<div class="alert-item__content">
			<h4 v-if="alert.title" class="alert-item__title">
				{{ alert.title }}
			</h4>
			<p class="alert-item__message">{{ alert.message }}</p>
		</div>

		<button v-if="alert.dismissible" class="alert-item__close" aria-label="Fermer" @click="close">
			<BaseIcon name="close" size="16" />
		</button>
	</div>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import type { Alert } from '@/types/store/alert';
	import { computed, onBeforeUnmount, ref } from 'vue';

	const props = defineProps<{
		alert: Alert;
	}>();

	const emit = defineEmits<{
		(e: 'close', id: string): void;
	}>();

	// Animation de fermeture
	const isClosing = ref(false);

	// Gestion de l'auto-fermeture
	let closeTimeout: ReturnType<typeof setTimeout> | null = null;
	let remainingTime = props.alert.timeout || 5000;
	let startTime: number;

	// Icône en fonction du type d'alerte
	const iconName = computed(() => {
		switch (props.alert.type) {
			case 'success':
				return 'success';
			case 'error':
				return 'error';
			case 'warning':
				return 'warning';
			case 'info':
				return 'info';
			default:
				return 'info';
		}
	});

	// Configuration de l'auto-fermeture si nécessaire
	function setupAutoClose() {
		if (props.alert.autoClose !== false) {
			startTime = Date.now();
			closeTimeout = setTimeout(() => {
				close();
			}, remainingTime);
		}
	}

	// Pause de l'auto-fermeture lorsque la souris est sur l'alerte
	function pauseAutoClose() {
		if (closeTimeout && props.alert.autoClose !== false) {
			clearTimeout(closeTimeout);
			closeTimeout = null;

			// Calculer le temps restant
			const elapsedTime = Date.now() - startTime;
			remainingTime = Math.max(0, (props.alert.timeout || 5000) - elapsedTime);
		}
	}

	// Reprise de l'auto-fermeture lorsque la souris quitte l'alerte
	function resumeAutoClose() {
		if (props.alert.autoClose !== false && !closeTimeout && remainingTime > 0) {
			startTime = Date.now();
			closeTimeout = setTimeout(() => {
				close();
			}, remainingTime);
		}
	}

	// Fermeture de l'alerte
	function close() {
		if (closeTimeout) {
			clearTimeout(closeTimeout);
			closeTimeout = null;
		}

		// Animation de fermeture
		isClosing.value = true;

		// Attendre la fin de l'animation avant d'émettre l'événement de fermeture
		setTimeout(() => {
			emit('close', props.alert.id);
		}, 300);
	}

	// Configuration de l'auto-fermeture au montage
	setupAutoClose();

	// Nettoyage avant la destruction
	onBeforeUnmount(() => {
		if (closeTimeout) {
			clearTimeout(closeTimeout);
		}
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.alert-item {
		position: relative;
		display: flex;
		align-items: flex-start;
		padding: vars.$spacing-md;
		border-radius: vars.$border-radius-md;
		margin-bottom: vars.$spacing-sm;
		box-shadow: vars.$box-shadow;
		background-color: vars.$white;
		max-width: 400px;
		width: 100%;
		opacity: 1;
		transform: translateX(0);
		transition:
			transform 0.3s ease,
			opacity 0.3s ease;

		&--closing {
			transform: translateX(100%);
			opacity: 0;
		}

		&__icon {
			flex-shrink: 0;
			margin-right: vars.$spacing-sm;
			color: vars.$white;
			border-radius: vars.$border-radius-full;
			width: 32px;
			height: 32px;
			display: flex;
			align-items: center;
			justify-content: center;
		}

		&__content {
			flex: 1;
			min-width: 0;
		}

		&__title {
			font-weight: 600;
			margin-bottom: vars.$spacing-xs;
		}

		&__message {
			margin-bottom: 0;
			@include mix.truncate(3);
		}

		&__close {
			flex-shrink: 0;
			margin-left: vars.$spacing-sm;
			color: vars.$gray;
			padding: vars.$spacing-xxs;
			@include mix.transition(color);

			&:hover {
				color: vars.$black;
			}
		}

		// Styles spécifiques selon le type d'alerte
		&--success {
			border-left: 4px solid vars.$success-color;

			.alert-item__icon {
				background-color: vars.$success-color;
			}

			.alert-item__title {
				color: func.adjust-color-brightness(vars.$success-color, -30%);
			}
		}

		&--error {
			border-left: 4px solid vars.$danger-color;

			.alert-item__icon {
				background-color: vars.$danger-color;
			}

			.alert-item__title {
				color: func.adjust-color-brightness(vars.$danger-color, -20%);
			}
		}

		&--warning {
			border-left: 4px solid vars.$warning-color;

			.alert-item__icon {
				background-color: vars.$warning-color;
			}

			.alert-item__title {
				color: func.adjust-color-brightness(vars.$warning-color, -30%);
			}
		}

		&--info {
			border-left: 4px solid vars.$info-color;

			.alert-item__icon {
				background-color: vars.$info-color;
			}

			.alert-item__title {
				color: func.adjust-color-brightness(vars.$info-color, -30%);
			}
		}
	}
</style>
