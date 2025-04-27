<template>
	<div class="alert-list" :class="positionClass">
		<transition-group name="alert-transition">
			<AlertItem v-for="alert in alerts" :key="alert.id" :alert="alert" @close="removeAlert" />
		</transition-group>
	</div>
</template>

<script setup lang="ts">
	import { useAlertStore } from '@/store/alert';
	import { computed } from 'vue';
	import AlertItem from './AlertItem.vue';

	const props = withDefaults(
		defineProps<{
			position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left' | 'top-center' | 'bottom-center';
		}>(),
		{
			position: 'top-right',
		}
	);

	const alertStore = useAlertStore();

	const alerts = computed(() => alertStore.alerts);

	const positionClass = computed(() => {
		return `alert-list--${props.position}`;
	});

	function removeAlert(id: string) {
		alertStore.remove(id);
	}
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.alert-list {
		position: fixed;
		z-index: func.z('dropdown') + 100;
		padding: vars.$spacing-md;
		display: flex;
		flex-direction: column;
		pointer-events: none;
		max-width: 100%;

		> * {
			pointer-events: auto;
		}

		// Positions
		&--top-right {
			top: 0;
			right: 0;
		}

		&--top-left {
			top: 0;
			left: 0;
		}

		&--bottom-right {
			bottom: 0;
			right: 0;
		}

		&--bottom-left {
			bottom: 0;
			left: 0;
		}

		&--top-center {
			top: 0;
			left: 50%;
			transform: translateX(-50%);
		}

		&--bottom-center {
			bottom: 0;
			left: 50%;
			transform: translateX(-50%);
		}
	}

	// Animations pour les transitions
	.alert-transition-enter-active {
		transition: all 0.3s ease-out;
	}

	.alert-transition-leave-active {
		transition: all 0.3s ease-in;
		position: absolute;
		width: 100%;
	}

	.alert-transition-enter-from {
		opacity: 0;
		transform: translateX(50px);
	}

	.alert-transition-leave-to {
		opacity: 0;
		transform: translateX(50px);
	}
</style>
