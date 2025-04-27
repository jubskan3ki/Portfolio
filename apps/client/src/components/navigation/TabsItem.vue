<template>
	<!-- Si on est en mode onglet (navigation) -->
	<button
		v-if="isTab"
		:id="`tab-${tabsId}-${id}`"
		:class="['tabs-item__tab', { 'tabs-item__tab--active': isActive }]"
		:disabled="disabled"
		:aria-controls="`panel-${tabsId}-${id}`"
		:aria-selected="isActive"
		role="tab"
		@click="$emit('select')"
	>
		<span v-if="icon" class="tabs-item__tab-icon">
			<BaseIcon :name="icon" :size="16" />
		</span>
		<span class="tabs-item__tab-text">{{ label }}</span>
		<span v-if="badge" class="tabs-item__tab-badge">
			<Badge
				:text="String(badge.text)"
				:type="badge.type || 'primary'"
				size="small"
				:variant="badge.variant || 'filled'"
				rounded
			/>
		</span>
	</button>

	<!-- Si on est en mode panneau (contenu) -->
	<div
		v-else
		:id="`panel-${tabsId}-${id}`"
		:class="['tabs-item__panel', { 'tabs-item__panel--active': isActive }]"
		:aria-labelledby="`tab-${tabsId}-${id}`"
		role="tabpanel"
		tabindex="0"
	>
		<slot></slot>
	</div>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import Badge from '@/components/ui/Badge.vue';

	interface BadgeType {
		text: string | number;
		type?: string;
		variant?: string;
	}

	defineProps({
		// Props communs
		id: {
			type: String,
			required: true,
		},
		tabsId: {
			type: String,
			required: true,
		},
		isActive: {
			type: Boolean,
			default: false,
		},

		// Props pour le mode onglet
		isTab: {
			type: Boolean,
			default: false,
		},
		label: {
			type: String,
			default: '',
		},
		icon: {
			type: String,
			default: '',
		},
		disabled: {
			type: Boolean,
			default: false,
		},
		badge: {
			type: Object as () => BadgeType,
			default: null,
		},
	});

	defineEmits(['select']);
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	// Styles pour le mode onglet (navigation)
	.tabs-item__tab {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		padding: vars.$spacing-sm vars.$spacing-md;
		font-weight: 500;
		color: vars.$gray-dark;
		border: none;
		background: none;
		cursor: pointer;
		transition: all vars.$transition-base;
		position: relative;
		white-space: nowrap;

		&--active {
			color: vars.$primary-color;
		}

		&:hover:not(&--active):not(:disabled) {
			color: func.adjust-color-brightness(vars.$primary-color, -15%);
		}

		&:disabled {
			opacity: 0.5;
			cursor: not-allowed;
		}

		&-icon {
			margin-right: vars.$spacing-xs;
			display: flex;
			align-items: center;
		}

		&-badge {
			margin-left: vars.$spacing-xs;
		}
	}

	// Styles pour le mode panneau (contenu)
	.tabs-item__panel {
		display: none;
		padding: vars.$spacing-md 0;

		&--active {
			display: block;
		}
	}
</style>
