<template>
	<div
		:class="[
			'avatar',
			`avatar--${size}`,
			{ 'avatar--square': square },
			{ 'avatar--border': border },
			{ 'avatar--status': status },
			{ [`avatar--status-${status}`]: status },
			customClass,
		]"
	>
		<img v-if="src" class="avatar__image" :src="src" :alt="alt" @error="handleImageError" />

		<div v-if="status" class="avatar__status"></div>

		<div v-if="$slots.badge" class="avatar__badge">
			<slot name="badge"></slot>
		</div>
	</div>
</template>

<script setup lang="ts">
	import { ref } from 'vue';

	defineProps({
		src: {
			type: String,
			default: '',
		},
		alt: {
			type: String,
			default: 'Avatar',
		},
		size: {
			type: String,
			default: 'medium',
			validator: (value: string) => ['small', 'medium', 'large', 'xlarge'].includes(value),
		},
		square: {
			type: Boolean,
			default: false,
		},
		border: {
			type: Boolean,
			default: false,
		},
		status: {
			type: String,
			default: '',
			validator: (value: string) => ['', 'online', 'offline', 'busy', 'away'].includes(value),
		},
		customClass: {
			type: String,
			default: '',
		},
	});

	const imgError = ref(false);

	const handleImageError = () => {
		imgError.value = true;
	};
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.avatar {
		position: relative;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		border-radius: 50%;
		color: vars.$white;
		overflow: hidden;
		font-weight: 600;
		background-color: vars.$primary-color;

		// Tailles standard
		&--small {
			width: 32px;
			height: 32px;
		}

		&--medium {
			width: 40px;
			height: 40px;
		}

		&--large {
			width: 48px;
			height: 48px;
		}

		&--xlarge {
			width: 64px;
			height: 64px;
		}

		// Variante carrée
		&--square {
			border-radius: vars.$border-radius-md;
		}

		// Bordure
		&--border {
			border: 2px solid vars.$white;
			box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.05);
		}

		// Image
		&__image {
			width: 100%;
			height: 100%;
			object-fit: cover;
		}

		// Texte (initiales)
		&__text,
		&__icon {
			width: 100%;
			height: 100%;
			display: flex;
			align-items: center;
			justify-content: center;
		}

		// Status
		&__status {
			position: absolute;
			bottom: 0;
			right: 0;
			width: 25%;
			height: 25%;
			border-radius: 50%;
			border: 2px solid vars.$white;
			background-color: vars.$gray-light;
		}

		&--status-online &__status {
			background-color: vars.$success-color;
		}

		&--status-offline &__status {
			background-color: vars.$gray;
		}

		&--status-busy &__status {
			background-color: vars.$danger-color;
		}

		&--status-away &__status {
			background-color: vars.$warning-color;
		}

		// Badge
		&__badge {
			position: absolute;
			top: 0;
			right: 0;
			transform: translate(30%, -30%);
		}
	}
</style>
