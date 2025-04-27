<template>
	<div :class="['tooltip', customClass]" @mouseenter="show" @mouseleave="hide" @focus="show" @blur="hide">
		<div ref="trigger" class="tooltip__trigger">
			<slot></slot>
		</div>

		<Teleport to="body">
			<Transition name="tooltip">
				<div
					v-if="isVisible"
					ref="tooltip"
					:class="['tooltip__content', `tooltip__content--${position}`, `tooltip__content--${type}`]"
					:style="tooltipStyle"
					role="tooltip"
				>
					<div class="tooltip__arrow"></div>
					<div class="tooltip__body">
						<slot name="content">{{ content }}</slot>
					</div>
				</div>
			</Transition>
		</Teleport>
	</div>
</template>

<script setup lang="ts">
	import { nextTick, onBeforeUnmount, onMounted, ref } from 'vue';

	const props = defineProps({
		content: {
			type: String,
			default: '',
		},
		position: {
			type: String,
			default: 'top',
			validator: (value: string) => ['top', 'bottom', 'left', 'right'].includes(value),
		},
		trigger: {
			type: String,
			default: 'hover',
			validator: (value: string) => ['hover', 'click', 'focus'].includes(value),
		},
		delay: {
			type: Number,
			default: 200,
		},
		type: {
			type: String,
			default: 'dark',
			validator: (value: string) => ['dark', 'light', 'primary'].includes(value),
		},
		offset: {
			type: Number,
			default: 10,
		},
		customClass: {
			type: String,
			default: '',
		},
	});

	const isVisible = ref(false);
	const trigger = ref<HTMLElement | null>(null);
	const tooltip = ref<HTMLElement | null>(null);
	const tooltipStyle = ref({
		top: '0px',
		left: '0px',
	});

	let showTimer: number | null = null;
	let hideTimer: number | null = null;

	const show = () => {
		if (props.trigger !== 'hover') return;

		clearTimeout(hideTimer!);

		showTimer = window.setTimeout(() => {
			isVisible.value = true;
			nextTick(() => updatePosition());
		}, props.delay);
	};

	const hide = () => {
		if (props.trigger !== 'hover') return;

		clearTimeout(showTimer!);

		hideTimer = window.setTimeout(() => {
			isVisible.value = false;
		}, props.delay);
	};

	const toggle = () => {
		isVisible.value = !isVisible.value;
		if (isVisible.value) {
			nextTick(() => updatePosition());
		}
	};

	const updatePosition = () => {
		if (!trigger.value || !tooltip.value) return;

		const triggerRect = trigger.value.getBoundingClientRect();
		const tooltipRect = tooltip.value.getBoundingClientRect();

		const scrollTop = window.scrollY || document.documentElement.scrollTop;
		const scrollLeft = window.scrollX || document.documentElement.scrollLeft;

		let top = 0;
		let left = 0;

		switch (props.position) {
			case 'top':
				top = triggerRect.top + scrollTop - tooltipRect.height - props.offset;
				left = triggerRect.left + scrollLeft + triggerRect.width / 2 - tooltipRect.width / 2;
				break;
			case 'bottom':
				top = triggerRect.bottom + scrollTop + props.offset;
				left = triggerRect.left + scrollLeft + triggerRect.width / 2 - tooltipRect.width / 2;
				break;
			case 'left':
				top = triggerRect.top + scrollTop + triggerRect.height / 2 - tooltipRect.height / 2;
				left = triggerRect.left + scrollLeft - tooltipRect.width - props.offset;
				break;
			case 'right':
				top = triggerRect.top + scrollTop + triggerRect.height / 2 - tooltipRect.height / 2;
				left = triggerRect.right + scrollLeft + props.offset;
				break;
		}

		// Vérifier les limites de l'écran
		const viewportWidth = window.innerWidth;
		const viewportHeight = window.innerHeight;

		// Empêcher le tooltip de sortir de l'écran
		left = Math.max(props.offset, Math.min(left, viewportWidth - tooltipRect.width - props.offset));
		top = Math.max(props.offset, Math.min(top, viewportHeight + scrollTop - tooltipRect.height - props.offset));

		tooltipStyle.value = {
			top: `${top}px`,
			left: `${left}px`,
		};
	};

	// Gestionnaires d'événements pour le déclencheur de clic
	const handleClickTrigger = (event: MouseEvent) => {
		if (props.trigger !== 'click') return;

		const target = event.target as Node;
		const targetIsTrigger = trigger.value?.contains(target);

		if (targetIsTrigger) {
			toggle();
			event.stopPropagation();
		}
	};

	const handleClickOutside = (event: MouseEvent) => {
		if (!isVisible.value) return;

		const target = event.target as Node;
		const clickedOutside = !tooltip.value?.contains(target) && !trigger.value?.contains(target);

		if (clickedOutside) {
			isVisible.value = false;
		}
	};

	// Gestionnaires pour le redimensionnement et le défilement
	const handleResize = () => {
		if (isVisible.value) {
			updatePosition();
		}
	};

	const handleScroll = () => {
		if (isVisible.value) {
			updatePosition();
		}
	};

	// Cycle de vie
	onMounted(() => {
		if (props.trigger === 'click') {
			document.addEventListener('click', handleClickOutside);
			trigger.value?.addEventListener('click', handleClickTrigger);
		}

		window.addEventListener('resize', handleResize);
		window.addEventListener('scroll', handleScroll);
	});

	onBeforeUnmount(() => {
		if (props.trigger === 'click') {
			document.removeEventListener('click', handleClickOutside);
			trigger.value?.removeEventListener('click', handleClickTrigger);
		}

		window.removeEventListener('resize', handleResize);
		window.removeEventListener('scroll', handleScroll);

		clearTimeout(showTimer!);
		clearTimeout(hideTimer!);
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.tooltip {
		display: inline-block;
		position: relative;

		&__trigger {
			display: inline-block;
		}

		&__content {
			position: fixed;
			z-index: func.z('tooltip');
			max-width: 300px;
			padding: vars.$spacing-sm vars.$spacing-md;
			border-radius: vars.$border-radius-md;
			box-shadow: vars.$box-shadow;
			pointer-events: none;

			// Variantes
			&--dark {
				background-color: vars.$black;
				color: vars.$white;

				.tooltip__arrow {
					border-color: vars.$black;
				}
			}

			&--light {
				background-color: vars.$white;
				color: vars.$black-light;

				.tooltip__arrow {
					border-color: vars.$white;
				}
			}

			&--primary {
				background-color: vars.$primary-color;
				color: vars.$white;

				.tooltip__arrow {
					border-color: vars.$primary-color;
				}
			}

			// Flèche
			&--top .tooltip__arrow {
				bottom: -4px;
				left: 50%;
				transform: translateX(-50%) rotate(45deg);
				border-bottom: 1px solid;
				border-right: 1px solid;
			}

			&--bottom .tooltip__arrow {
				top: -4px;
				left: 50%;
				transform: translateX(-50%) rotate(45deg);
				border-top: 1px solid;
				border-left: 1px solid;
			}

			&--left .tooltip__arrow {
				right: -4px;
				top: 50%;
				transform: translateY(-50%) rotate(45deg);
				border-top: 1px solid;
				border-right: 1px solid;
			}

			&--right .tooltip__arrow {
				left: -4px;
				top: 50%;
				transform: translateY(-50%) rotate(45deg);
				border-bottom: 1px solid;
				border-left: 1px solid;
			}
		}

		&__arrow {
			position: absolute;
			width: 8px;
			height: 8px;
			background-color: inherit;
		}

		&__body {
			position: relative;
			z-index: 1;
		}
	}

	// Animation
	.tooltip-enter-active,
	.tooltip-leave-active {
		transition:
			opacity 0.15s,
			transform 0.15s;
	}

	.tooltip-enter-from,
	.tooltip-leave-to {
		opacity: 0;
		transform: scale(0.9);
	}
</style>
