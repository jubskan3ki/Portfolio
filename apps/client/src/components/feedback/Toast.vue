<template>
	<transition name="toast">
		<div
			v-if="isVisible"
			:class="['toast', `toast--${type}`, { 'toast--with-action': $slots.action }, customClass]"
			role="alert"
		>
			<div v-if="showIcon" class="toast__icon">
				<BaseIcon :name="getIconName" :size="20" />
			</div>

			<div class="toast__content">
				<div v-if="title" class="toast__title">{{ title }}</div>
				<div class="toast__message">
					<slot>{{ message }}</slot>
				</div>
			</div>

			<div v-if="$slots.action" class="toast__action">
				<slot name="action"></slot>
			</div>

			<button v-if="dismissible" class="toast__close" aria-label="Fermer la notification" @click="dismiss">
				<BaseIcon name="close" :size="16" />
			</button>

			<div v-if="autoClose && progress" class="toast__progress">
				<div class="toast__progress-bar" :style="{ width: `${progressValue}%` }"></div>
			</div>
		</div>
	</transition>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue';

	const props = defineProps({
		type: {
			type: String,
			default: 'info',
			validator: (value: string) => ['info', 'success', 'warning', 'error'].includes(value),
		},
		title: {
			type: String,
			default: '',
		},
		message: {
			type: String,
			default: '',
		},
		autoClose: {
			type: Boolean,
			default: true,
		},
		duration: {
			type: Number,
			default: 5000,
		},
		dismissible: {
			type: Boolean,
			default: true,
		},
		showIcon: {
			type: Boolean,
			default: true,
		},
		progress: {
			type: Boolean,
			default: true,
		},
		customClass: {
			type: String,
			default: '',
		},
	});

	const emit = defineEmits(['close']);

	const isVisible = ref(true);
	const progressValue = ref(100);
	let timer: number | null = null;
	let progressTimer: number | null = null;

	const getIconName = computed(() => {
		switch (props.type) {
			case 'success':
				return 'success';
			case 'warning':
				return 'warning';
			case 'error':
				return 'error';
			default:
				return 'info';
		}
	});

	const dismiss = () => {
		isVisible.value = false;
		clearTimers();
		emit('close');
	};

	const startProgressTimer = () => {
		if (!props.autoClose || !props.progress) return;

		const stepTime = 10; // update every 10ms
		const steps = props.duration / stepTime;
		const decrement = 100 / steps;

		progressValue.value = 100;

		progressTimer = window.setInterval(() => {
			progressValue.value = Math.max(0, progressValue.value - decrement);

			if (progressValue.value <= 0) {
				clearInterval(progressTimer!);
			}
		}, stepTime);
	};

	const clearTimers = () => {
		if (timer) {
			clearTimeout(timer);
			timer = null;
		}

		if (progressTimer) {
			clearInterval(progressTimer);
			progressTimer = null;
		}
	};

	watch(
		() => props.duration,
		() => {
			clearTimers();
			if (props.autoClose) {
				timer = window.setTimeout(dismiss, props.duration);
				startProgressTimer();
			}
		}
	);

	onMounted(() => {
		if (props.autoClose) {
			timer = window.setTimeout(dismiss, props.duration);
			startProgressTimer();
		}
	});

	onBeforeUnmount(() => {
		clearTimers();
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.toast {
		position: relative;
		display: flex;
		align-items: flex-start;
		width: 100%;
		max-width: 400px;
		padding: vars.$spacing-md;
		border-radius: vars.$border-radius-md;
		background-color: vars.$white;
		box-shadow: vars.$box-shadow-medium;
		overflow: hidden;

		&__icon {
			flex-shrink: 0;
			margin-right: vars.$spacing-sm;
			margin-top: 2px;
		}

		&__content {
			flex: 1;
		}

		&__title {
			font-weight: 600;
			margin-bottom: vars.$spacing-xxs;
		}

		&__message {
			color: vars.$gray-dark;
		}

		&__action {
			margin-left: vars.$spacing-sm;
			align-self: center;
		}

		&__close {
			flex-shrink: 0;
			background: none;
			border: none;
			padding: vars.$spacing-xxs;
			margin: -vars.$spacing-xxs;
			cursor: pointer;
			color: vars.$gray;
			transition: color vars.$transition-fast;

			&:hover {
				color: vars.$black-light;
			}
		}

		&__progress {
			position: absolute;
			left: 0;
			bottom: 0;
			width: 100%;
			height: 3px;
			background-color: rgba(0, 0, 0, 0.1);
		}

		&__progress-bar {
			height: 100%;
			transition: width linear 10ms;
		}

		// Types de toast
		&--info {
			border-left: 4px solid vars.$info-color;

			.toast__icon {
				color: vars.$info-color;
			}

			.toast__progress-bar {
				background-color: vars.$info-color;
			}
		}

		&--success {
			border-left: 4px solid vars.$success-color;

			.toast__icon {
				color: vars.$success-color;
			}

			.toast__progress-bar {
				background-color: vars.$success-color;
			}
		}

		&--warning {
			border-left: 4px solid vars.$warning-color;

			.toast__icon {
				color: vars.$warning-color;
			}

			.toast__progress-bar {
				background-color: vars.$warning-color;
			}
		}

		&--error {
			border-left: 4px solid vars.$danger-color;

			.toast__icon {
				color: vars.$danger-color;
			}

			.toast__progress-bar {
				background-color: vars.$danger-color;
			}
		}

		// Animation
		&-enter-active,
		&-leave-active {
			transition:
				transform vars.$transition-base,
				opacity vars.$transition-base;
		}

		&-enter-from,
		&-leave-to {
			transform: translateY(-20px);
			opacity: 0;
		}
	}
</style>
