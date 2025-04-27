<template>
	<div v-if="totalPages > 1" :class="['pagination', customClass]">
		<!-- Bouton Précédent -->
		<button
			class="pagination__btn pagination__btn--prev"
			:disabled="currentPage <= 1"
			aria-label="Page précédente"
			@click="handlePrevious"
		>
			<BaseIcon name="chevron-left" :size="16" />
			<span v-if="showText" class="pagination__btn-text">Précédent</span>
		</button>

		<!-- Pages -->
		<ul class="pagination__list">
			<!-- Première page -->
			<PaginationItem
				v-if="showFirstPage"
				:page="1"
				:is-active="currentPage === 1"
				@click="handlePageChange(1)"
			/>

			<!-- Ellipsis gauche -->
			<PaginationItem v-if="leftEllipsisVisible" :page="0" :is-ellipsis="true" />

			<!-- Pages du milieu incluant la page courante -->
			<PaginationItem
				v-for="page in centerPages"
				:key="page"
				:page="page"
				:is-active="currentPage === page"
				@click="handlePageChange(page)"
			/>

			<!-- Ellipsis droite -->
			<PaginationItem v-if="rightEllipsisVisible" :page="0" :is-ellipsis="true" />

			<!-- Dernière page -->
			<PaginationItem
				v-if="showLastPage"
				:page="totalPages"
				:is-active="currentPage === totalPages"
				@click="handlePageChange(totalPages)"
			/>
		</ul>

		<!-- Bouton Suivant -->
		<button
			class="pagination__btn pagination__btn--next"
			:disabled="currentPage >= totalPages"
			aria-label="Page suivante"
			@click="handleNext"
		>
			<span v-if="showText" class="pagination__btn-text">Suivant</span>
			<BaseIcon name="chevron-right" :size="16" />
		</button>
	</div>
</template>

<script setup lang="ts">
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import PaginationItem from '@/components/navigation/PaginationItem.vue';
	import { computed } from 'vue';

	const props = defineProps({
		currentPage: {
			type: Number,
			required: true,
			validator: (value: number) => value >= 1,
		},
		totalPages: {
			type: Number,
			required: true,
			validator: (value: number) => value >= 1,
		},
		maxVisiblePages: {
			type: Number,
			default: 5,
			validator: (value: number) => value >= 3,
		},
		showText: {
			type: Boolean,
			default: true,
		},
		customClass: {
			type: String,
			default: '',
		},
	});

	const emit = defineEmits(['update:currentPage', 'page-change']);

	// Calcul des pages centrales à afficher
	const centerPages = computed(() => {
		const { currentPage, totalPages, maxVisiblePages } = props;

		// Si peu de pages, afficher toutes les pages
		if (totalPages <= maxVisiblePages) {
			return Array.from({ length: totalPages }, (_, i) => i + 1);
		}

		// Sinon, calculer un sous-ensemble centré autour de la page courante
		const sidePages = Math.floor(maxVisiblePages / 2);
		let startPage = Math.max(1, currentPage - sidePages);
		let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);

		// Ajuster startPage si on est proche de la fin
		if (endPage === totalPages) {
			startPage = Math.max(1, endPage - maxVisiblePages + 1);
		}

		return Array.from({ length: endPage - startPage + 1 }, (_, i) => startPage + i);
	});

	// Afficher la première page ou non
	const showFirstPage = computed(() => {
		if (props.totalPages <= props.maxVisiblePages) return false;
		return !centerPages.value.includes(1);
	});

	// Afficher la dernière page ou non
	const showLastPage = computed(() => {
		if (props.totalPages <= props.maxVisiblePages) return false;
		return !centerPages.value.includes(props.totalPages);
	});

	// Afficher l'ellipsis de gauche si nécessaire
	const leftEllipsisVisible = computed(() => {
		if (centerPages.value.length === 0) return false;
		return showFirstPage.value && centerPages.value[0] > 2;
	});

	// Afficher l'ellipsis de droite si nécessaire
	const rightEllipsisVisible = computed(() => {
		if (centerPages.value.length === 0) return false;
		const lastCenterPage = centerPages.value[centerPages.value.length - 1];
		return showLastPage.value && lastCenterPage < props.totalPages - 1;
	});

	// Changer de page
	const handlePageChange = (page: number) => {
		if (page !== props.currentPage && page >= 1 && page <= props.totalPages) {
			emit('update:currentPage', page);
			emit('page-change', page);
		}
	};

	// Aller à la page précédente
	const handlePrevious = () => {
		if (props.currentPage > 1) {
			handlePageChange(props.currentPage - 1);
		}
	};

	// Aller à la page suivante
	const handleNext = () => {
		if (props.currentPage < props.totalPages) {
			handlePageChange(props.currentPage + 1);
		}
	};
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.pagination {
		display: flex;
		align-items: center;
		justify-content: center;
		margin: vars.$spacing-lg 0;

		&__list {
			display: flex;
			align-items: center;
			list-style: none;
			margin: 0 vars.$spacing-sm;
			padding: 0;
		}

		&__btn {
			display: flex;
			align-items: center;
			justify-content: center;
			height: 36px;
			padding: 0 vars.$spacing-sm;
			border-radius: vars.$border-radius-md;
			background-color: vars.$white-dark;
			border: none;
			color: vars.$black-light;
			cursor: pointer;
			transition: all vars.$transition-base;

			&:hover:not(:disabled) {
				background-color: func.color-alpha(vars.$primary-color, 0.1);
				color: vars.$primary-color;
			}

			&:disabled {
				opacity: 0.5;
				cursor: not-allowed;
			}

			&--prev {
				.pagination__btn-text {
					margin-left: vars.$spacing-xxs;
				}
			}

			&--next {
				.pagination__btn-text {
					margin-right: vars.$spacing-xxs;
				}
			}
		}

		&__btn-text {
			@include mix.responsive(mobile) {
				display: none;
			}
		}
	}
</style>
