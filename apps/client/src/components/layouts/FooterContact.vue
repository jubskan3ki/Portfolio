<!-- src/components/footer/ContactInfo.vue -->
<template>
	<div class="contact-info">
		<SectionHeading :title="title" />

		<div class="contact-info__list">
			<ContactItem v-if="email" icon="mail" :text="email" :is-link="true" link-type="email" />

			<ContactItem v-if="phone" icon="phone" :text="phone" :is-link="true" link-type="phone" />

			<ContactItem v-if="address" icon="map-pin" :text="address" />
		</div>

		<div class="contact-info__availability">
			<div class="availability__indicator" :class="{ 'availability__indicator--available': isAvailable }"></div>
			<small>{{ availabilityText }}</small>
		</div>
	</div>
</template>

<script setup lang="ts">
	import ContactItem from '@/components/layouts/FooterContactItem.vue';
	import SectionHeading from '@/components/ui/SectionHeading.vue';
	import { computed } from 'vue';

	const props = defineProps({
		title: {
			type: String,
			default: 'Contact',
		},
		email: {
			type: String,
			default: '',
		},
		phone: {
			type: String,
			default: '',
		},
		address: {
			type: String,
			default: '',
		},
		isAvailable: {
			type: Boolean,
			default: true,
		},
	});

	// Texte d'état de disponibilité
	const availabilityText = computed(() =>
		props.isAvailable ? 'Disponible pour de nouveaux projets' : 'Non disponible pour le moment'
	);
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.contact-info {
		display: flex;
		flex-direction: column;

		&__list {
			display: flex;
			flex-direction: column;
			gap: vars.$spacing-sm;
			margin-bottom: vars.$spacing-md;
		}

		&__availability {
			display: flex;
			align-items: center;
			gap: vars.$spacing-sm;
			margin-top: vars.$spacing-sm;
			padding: vars.$spacing-xs vars.$spacing-sm;
			background-color: func.color-alpha(vars.$white-dark, 0.5);
			border-radius: vars.$border-radius-md;
		}

		.availability__indicator {
			width: 10px;
			height: 10px;
			border-radius: 50%;
			background-color: vars.$gray;

			&--available {
				background-color: vars.$success-color;
				animation: pulse 2s infinite;
			}
		}
	}

	@keyframes pulse {
		0% {
			box-shadow: 0 0 0 0 func.color-alpha(vars.$success-color, 0.7);
		}
		70% {
			box-shadow: 0 0 0 6px func.color-alpha(vars.$success-color, 0);
		}
		100% {
			box-shadow: 0 0 0 0 func.color-alpha(vars.$success-color, 0);
		}
	}
</style>
