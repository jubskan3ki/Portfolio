<template>
    <div class="project-list" :class="[`project-list--${layout}`, customClass]">
        <QueryStateHandler
            :loading="loading"
            :error="error"
            :empty="!projects || projects.length === 0"
            :loading-message="loadingText"
            :empty-title="emptyTitle"
            :empty-description="emptyDescription"
            empty-icon="folder"
            :retryable="retryable"
            :retry-text="retryText"
            @retry="$emit('retry')"
        >
            <template v-if="$slots['empty-action']" #empty-action>
                <slot name="empty-action"></slot>
            </template>

            <!-- Projects Grid -->
            <div class="project-list__grid">
                <template v-for="(project, index) in sortedProjects" :key="project.id ?? index">
                    <slot name="project" :project="project" :index="index">
                        <div class="project-list__item" :style="{ '--index': index }">
                            <ProjectCard
                                :project="project"
                                :featured="isFeatured(project)"
                                :hoverable="cardHoverable"
                                :description-length="descriptionLength"
                                :max-technologies="maxTechnologies"
                            />
                        </div>
                    </slot>
                </template>
            </div>
        </QueryStateHandler>

        <!-- Pagination -->
        <div v-if="showPagination && totalPages > 1" class="project-list__pagination">
            <Pagination
                :current-page="currentPage"
                :total-pages="totalPages"
                @update:current-page="$emit('update:currentPage', $event)"
                @page-change="$emit('pageChange', $event)"
            />
        </div>

        <!-- Footer Slot -->
        <div v-if="$slots.footer" class="project-list__footer">
            <slot name="footer"></slot>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import ProjectCard from '@/components/feature/projects/ProjectCard.vue';
    import QueryStateHandler from '@/components/feedback/QueryStateHandler.vue';
    import Pagination from '@/components/navigation/Pagination.vue';

    import type { Project, ProjectListProps } from '@/types/feature/project';

    type Props = ProjectListProps;

    const props = withDefaults(defineProps<Props>(), {
        projects: () => [],
        layout: 'grid',
        featuredProjects: () => [],
        loading: false,
        error: '',
        retryable: false,
        retryText: 'Réessayer',
        loadingText: 'Chargement...',
        emptyTitle: 'Aucun projet',
        emptyDescription: 'Aucun projet à afficher.',
        currentPage: 1,
        totalPages: 1,
        showPagination: false,
        cardHoverable: true,
        descriptionLength: 120,
        maxTechnologies: 3,
        customClass: '',
    });

    defineEmits<{
        'update:currentPage': [page: number];
        pageChange: [page: number];
        retry: [];
    }>();

    // Sort projects: featured first, then by date
    const sortedProjects = computed(() => {
        const validProjects = props.projects.filter((p): p is Project => p != null);

        return [...validProjects].sort((a, b) => {
            const aFeatured = isFeatured(a);
            const bFeatured = isFeatured(b);

            if (aFeatured && !bFeatured) {
                return -1;
            }
            if (!aFeatured && bFeatured) {
                return 1;
            }

            if (a.date && b.date) {
                return new Date(b.date).getTime() - new Date(a.date).getTime();
            }

            return 0;
        });
    });

    const isFeatured = (project: Project): boolean => {
        if (props.featuredProjects.length === 0) {
            return false;
        }
        return (
            props.featuredProjects.includes(project.id)
            || (typeof project.slug === 'string' && props.featuredProjects.includes(project.slug))
        );
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;

    .project-list {
        width: 100%;

        // Grid Layout
        &__grid {
            display: grid;
            gap: vars.$spacing-lg;
        }

        &--grid &__grid {
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));

            @include mix.responsive(mobile) {
                grid-template-columns: 1fr;
            }
        }

        &--list &__grid {
            grid-template-columns: 1fr;
        }

        &--compact &__grid {
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: vars.$spacing-md;
        }

        // Items with staggered animation
        &__item {
            opacity: 0;
            animation: slideUp 0.4s ease forwards;
            animation-delay: calc(var(--index, 0) * 50ms);
        }

        // Pagination
        &__pagination {
            margin-top: vars.$spacing-xl;
            display: flex;
            justify-content: center;
        }

        // Footer
        &__footer {
            margin-top: vars.$spacing-xl;
        }
    }

    /* Animation */
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
</style>
