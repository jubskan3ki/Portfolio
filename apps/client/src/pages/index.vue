<template>
	<div class="home-page">
		<!-- Hero Section -->
		<HeroSection :featured-stacks="featuredStacks" />

		<!-- Stats Section -->
		<section class="stats-section">
			<div class="container">
				<div class="expertise-grid">
					<ExpertiseCard
						title="Front-end"
						description="Création d'interfaces utilisateur modernes, réactives et accessibles avec React, Vue, Svelte et CSS/SASS."
						icon="layout"
						color="#673c5c"
					/>
					<ExpertiseCard
						title="Back-end"
						description="Développement d'APIs robustes et évolutives avec Go, Node.js et Django, associées aux bases de données SQL/NoSQL."
						icon="server"
						color="#43889d"
					/>
					<ExpertiseCard
						title="Mobile"
						description="Conception d'applications mobiles natives et cross-platform performantes avec React Native et Flutter."
						icon="smartphone"
						color="#ac72a0"
					/>
					<ExpertiseCard
						title="DevOps"
						description="Mise en place d'infrastructures cloud scalables et sécurisées avec Docker, Kubernetes, Terraform et Ansible."
						icon="cloud"
						color="#ff2453"
					/>
				</div>
			</div>
		</section>

		<!-- Experience Section -->
		<Section
			id="Experiences"
			title="Expériences récentes"
			subtitle="Parcours professionnel et réalisations marquantes"
			animation-type="scale"
			animated
		>
			<div class="container">
				<div class="project-timeline">
					<ExperienceTimeline :experiences="professionalExperiences" :limit="3" :compact="true" />

					<div class="section-actions">
						<BaseButton :to="ROUTES.EXPERIENCE" variant="outline">
							<BaseIcon name="grid" size="sm" class="mr-xs" />
							Voir mon parcours complet
						</BaseButton>
					</div>
				</div>
			</div>
		</Section>

		<!-- Projets Section -->
		<Section
			id="projects"
			title="Projets récents"
			subtitle="Solutions digitales innovantes et impactantes"
			animation-type="fade"
			animated
			light
		>
			<div class="container">
				<ProjectCarousel :projects="featuredProjects" :limit="5" :autoplay="true" />

				<div class="section-actions">
					<BaseButton :to="ROUTES.PROJECTS" variant="primary">
						<BaseIcon name="grid" size="sm" class="mr-xs" />
						Explorer tous mes projets
					</BaseButton>
				</div>
			</div>
		</Section>

		<!-- Technologies Section -->
		<Section
			id="technologies"
			title="Technologies"
			subtitle="Mon expertise technique polyvalente"
			animation-type="slide"
			animated
		>
			<div class="container">
				<StackCarousel :stacks="stacks" :limit="10" :autoplay="true" :slides-per-view="6" :show-level="true" />

				<div class="section-actions">
					<BaseButton :to="ROUTES.STACKS" variant="outline">
						<BaseIcon name="layers" size="sm" class="mr-xs" />
						Découvrir toutes mes technologies
					</BaseButton>
				</div>
			</div>
		</Section>

		<!-- Blog Preview Section -->
		<Section
			id="blog"
			title="Articles récents"
			subtitle="Partage de connaissances et veille technologique"
			animation-type="scale"
			animated
			light
		>
			<div class="container">
				<ArticleCarousel
					:articles="articles"
					:limit="4"
					:autoplay="true"
					:autoplay-speed="6000"
					:show-author="true"
					:show-stats="true"
					:show-dots="true"
				/>

				<div class="section-actions">
					<BaseButton :to="ROUTES.BLOG" variant="primary">
						<BaseIcon name="book-open" size="sm" class="mr-xs" />
						Lire tous mes articles
					</BaseButton>
				</div>
			</div>
		</Section>

		<!-- Section Contact -->
		<Section
			id="contact"
			title="Travaillons ensemble"
			subtitle="Transformons vos idées en solutions digitales"
			size="large"
			animated
		>
			<div class="container">
				<div class="contact-wrapper">
					<div class="contact-wrapper__form">
						<ContactForm form-id="contact-form-fixed" />
					</div>
					<div class="contact-wrapper__info">
						<ContactInfos
							title="Mes coordonnées"
							subtitle="Discutons de vos besoins et objectifs"
							address="Paris, France"
							email="contact@aitaddajuba.fr"
							phone="+33 6 95 21 71 97"
							:social-links="socialMediaLinks"
							custom-class="contact-page-infos"
						/>
					</div>
				</div>
			</div>
		</Section>
	</div>
</template>

<script setup lang="ts">
	import BaseButton from '@/components/base/BaseButton.vue';
	import BaseIcon from '@/components/base/BaseIcon.vue';
	import ArticleCarousel from '@/components/feature/blog/ArticleCarousel.vue';
	import ContactForm from '@/components/feature/contact/ContactForm.vue';
	import ContactInfos from '@/components/feature/contact/ContactInfos.vue';
	import ExperienceTimeline from '@/components/feature/experience/ExperienceTimeline.vue';
	import ExpertiseCard from '@/components/feature/home/ExpertiseCard.vue';
	import HeroSection from '@/components/feature/home/HeroSection.vue';
	import ProjectCarousel from '@/components/feature/projects/ProjectCarousel.vue';
	import StackCarousel from '@/components/feature/stacks/StackCarousel.vue';
	import Section from '@/components/layouts/Section.vue';
	import { ROUTES } from '@/config/routes';
	import { useMock } from '@/services/api/useMock';
	import { computed, onMounted } from 'vue';

	const {
		fetchProjects,
		fetchExperience,
		fetchStacks,
		fetchArticles,
		projects,
		stacks,
		professionalExperiences,
		articles,
	} = useMock();

	// Projets mis en avant
	const featuredProjects = computed(() => {
		return projects.value.slice(0, 5);
	});

	// Technologies mises en avant
	const featuredStacks = computed(() => {
		return stacks.value.slice(0, 5);
	});

	// Configuration des liens sociaux
	const socialMediaLinks = [
		{
			name: 'LinkedIn',
			icon: 'linkedin',
			url: 'https://www.linkedin.com/in/juba-aitadda/',
		},
		{
			name: 'GitHub',
			icon: 'github',
			url: 'https://github.com/jubskan3ki',
		},
	];

	// Préchargement des données
	onMounted(async () => {
		try {
			await Promise.all([fetchProjects(10), fetchExperience(), fetchStacks(10), fetchArticles()]);
		} catch (err) {
			console.error('Erreur lors du préchargement des données:', err);
		}
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	// Element racine pour l'encapsulation
	.home-page {
		display: block;
		width: 100%;
	}

	// Stats Section
	.stats-section {
		margin-top: -80px;
		position: relative;
		z-index: 5;
		padding-bottom: vars.$spacing-xl;
	}

	.stats-grid {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: vars.$spacing-md;

		@include mix.responsive(tablet) {
			grid-template-columns: repeat(2, 1fr);
		}

		@include mix.responsive(mobile) {
			grid-template-columns: 1fr;
		}
	}

	// Expertise Section
	.expertise-intro {
		max-width: 800px;
		margin: 0 auto vars.$spacing-xl;
		text-align: center;

		&__text {
			color: vars.$gray-dark;
			line-height: 1.8;
		}
	}

	.expertise-grid {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: vars.$spacing-md;

		@include mix.responsive(tablet) {
			grid-template-columns: repeat(2, 1fr);
		}

		@include mix.responsive(mobile) {
			grid-template-columns: 1fr;
		}
	}

	// Project Timeline
	.project-timeline {
		&__title {
			text-align: center;
			margin-bottom: vars.$spacing-xl;
			position: relative;

			&::after {
				content: '';
				position: absolute;
				bottom: -10px;
				left: 50%;
				transform: translateX(-50%);
				width: 60px;
				height: 3px;
				background-color: vars.$primary-color;
			}
		}
	}

	// Tech Categories
	.tech-categories {
		margin-top: vars.$spacing-xxl;
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
		gap: vars.$spacing-xl;
	}

	.tech-category {
		&__title {
			font-weight: 600;
			margin-bottom: vars.$spacing-md;
			padding-bottom: vars.$spacing-xs;
			border-bottom: 2px solid func.color-alpha(vars.$primary-color, 0.2);
			position: relative;

			&::after {
				content: '';
				position: absolute;
				bottom: -2px;
				left: 0;
				width: 60px;
				height: 2px;
				background-color: vars.$primary-color;
			}
		}

		&__items {
			display: flex;
			flex-wrap: wrap;
			gap: vars.$spacing-sm;
		}
	}

	// Blog Section
	.blog-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
		gap: vars.$spacing-lg;

		@include mix.responsive(mobile) {
			grid-template-columns: 1fr;
		}
	}

	// Contact Wrapper
	.contact-wrapper {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: vars.$spacing-xl;

		@include mix.responsive(tablet) {
			grid-template-columns: 1fr;
		}

		&__form {
			background-color: vars.$white;
			border-radius: vars.$border-radius-lg;
			padding: vars.$spacing-lg;
			box-shadow: vars.$box-shadow-medium;
		}

		&__info {
			color: vars.$white;
		}
	}

	// Shared Section Actions
	.section-actions {
		display: flex;
		justify-content: center;
		margin-top: vars.$spacing-lg;
	}
</style>
