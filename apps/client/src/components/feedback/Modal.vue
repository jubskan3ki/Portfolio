<!-- src/components/feedback/Modal.vue -->
<template>
	<transition name="modal-fade">
		<div
			v-if="visible"
			class="modal"
			role="dialog"
			aria-modal="true"
			:aria-labelledby="options.title ? 'modal-title' : undefined"
			@keydown.esc="handleEscKey"
		>
			<div
				class="modal__overlay"
				tabindex="0"
				role="button"
				aria-label="Fermer la modale"
				@click="handleOverlayClick"
				@keydown.enter="handleOverlayClick"
				@keydown.space="handleOverlayClick"
			></div>

			<div class="modal__container" :class="`modal__container--${options.size || 'md'}`">
				<div class="modal__content">
					<div v-if="options.title || !options.hideCloseButton" class="modal__header">
						<h2 v-if="options.title" id="modal-title" class="modal__title">
							{{ options.title }}
						</h2>

						<button
							v-if="!options.hideCloseButton"
							class="modal__close"
							aria-label="Fermer"
							@click="closeModal"
						>
							<BaseIcon name="close" size="16" />
						</button>
					</div>

					<div class="modal__body">
						<!-- Contenu statique -->
						<p v-if="options.content">{{ options.content }}</p>

						<!-- Composant dynamique -->
						<component
							:is="resolveComponent(options.component)"
							v-else-if="options.component"
							v-bind="options.componentProps"
							@close="closeModal"
						/>
					</div>
				</div>
			</div>
		</div>
	</transition>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import { useModalStore } from '@/store/modal';
	import { computed, onMounted, onUnmounted, ref } from 'vue';

	const modalStore = useModalStore();

	// État de la modale depuis le store
	const visible = computed(() => modalStore.visible);
	const options = computed(() => modalStore.options);

	// Fermeture de la modale
	function closeModal() {
		if (options.value.closable !== false) {
			modalStore.close();
		}
	}

	// Gestion du clic sur l'overlay
	function handleOverlayClick() {
		if (options.value.closeOnClickOutside && !options.value.persistent) {
			closeModal();
		}
	}

	// Gestion de la touche ESC
	function handleEscKey(event: KeyboardEvent) {
		if (event.key === 'Escape' && !options.value.persistent) {
			closeModal();
		}
	}

	// Résolution du composant à injecter
	function resolveComponent(componentName: string) {
		// Cette fonction devrait être adaptée à votre logique d'importation de composants
		// Pour Nuxt, vous pourriez utiliser resolveComponent de Vue 3 ou une autre approche
		return componentName;
	}

	// Gestion du focus dans la modale
	const modalElement = ref<HTMLElement | null>(null);

	onMounted(() => {
		// Focus trap - garde le focus à l'intérieur de la modale
		document.addEventListener('keydown', handleTabKey);

		// Focus le premier élément focusable de la modale
		if (visible.value) {
			setTimeout(() => {
				const focusableElements = modalElement.value?.querySelectorAll(
					'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
				);
				if (focusableElements?.length) {
					(focusableElements[0] as HTMLElement).focus();
				}
			}, 100);
		}
	});

	onUnmounted(() => {
		document.removeEventListener('keydown', handleTabKey);
	});

	// Empêche le focus de sortir de la modale
	function handleTabKey(e: KeyboardEvent) {
		if (!visible.value || e.key !== 'Tab') return;

		const focusableElements = modalElement.value?.querySelectorAll(
			'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
		);

		if (!focusableElements?.length) return;

		const firstElement = focusableElements[0] as HTMLElement;
		const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;

		// Si shift+tab et premier élément est focus, aller au dernier élément
		if (e.shiftKey && document.activeElement === firstElement) {
			lastElement.focus();
			e.preventDefault();
		}
		// Si tab et dernier élément est focus, aller au premier élément
		else if (!e.shiftKey && document.activeElement === lastElement) {
			firstElement.focus();
			e.preventDefault();
		}
	}
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.modal {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: func.z('modal');
		padding: vars.$spacing-md;

		&__overlay {
			position: absolute;
			top: 0;
			left: 0;
			width: 100%;
			height: 100%;
			background-color: func.color-alpha(vars.$black, 0.5);
			cursor: pointer;

			&:focus {
				outline: none; // On supprime l'outline standard pour éviter un focus visible sur l'overlay
			}
		}

		&__container {
			position: relative;
			background-color: vars.$white;
			border-radius: vars.$border-radius-md;
			box-shadow: vars.$box-shadow-large;
			max-height: 90vh;
			max-width: 90vw;
			width: 100%;
			display: flex;
			flex-direction: column;
			overflow: hidden;

			// Tailles de modales
			&--sm {
				max-width: 400px;
			}

			&--md {
				max-width: 600px;
			}

			&--lg {
				max-width: 800px;
			}

			&--xl {
				max-width: 1000px;
			}

			&--full {
				max-width: 100%;
				height: 100%;
				border-radius: 0;
			}
		}

		&__content {
			display: flex;
			flex-direction: column;
			height: 100%;
		}

		&__header {
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding: vars.$spacing-md vars.$spacing-md vars.$spacing-sm;
			border-bottom: 1px solid vars.$white-dark;
		}

		&__title {
			font-weight: 600;
			margin: 0;
			color: vars.$black;
		}

		&__close {
			background: none;
			border: none;
			color: vars.$gray;
			width: 32px;
			height: 32px;
			border-radius: vars.$border-radius-full;
			display: flex;
			align-items: center;
			justify-content: center;
			@include mix.transition(color, background-color);

			&:hover {
				color: vars.$primary-color;
				background-color: vars.$white-dark;
			}
		}

		&__body {
			padding: vars.$spacing-md;
			overflow-y: auto;
			flex: 1;
		}
	}

	// Animations
	.modal-fade-enter-active,
	.modal-fade-leave-active {
		transition: opacity 0.3s ease;

		.modal__container {
			transition:
				transform 0.3s ease,
				opacity 0.3s ease;
		}
	}

	.modal-fade-enter-from,
	.modal-fade-leave-to {
		opacity: 0;

		.modal__container {
			transform: translateY(20px);
			opacity: 0;
		}
	}
</style>
