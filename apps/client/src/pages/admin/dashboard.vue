<template>
    <div class="dashboard">
        <DashboardHeader
            :user-name="authStore.fullName || 'Admin'"
            :is-refreshing="isRefetching"
            @refresh="refreshDashboard"
        />

        <DashboardStatsGrid :stats="dashboardData?.stats ?? null" :loading="isLoading" />

        <section class="dashboard__row">
            <ClientOnly>
                <LazyDashboardViewsChart
                    :data="dashboardData?.charts?.viewsOverTime ?? []"
                    :total-views="dashboardData?.quickStats?.totalViews"
                />
            </ClientOnly>
            <DashboardActivityFeed :activities="recentActivities" :loading="isLoading" />
        </section>

        <section class="dashboard__row dashboard__row--reverse">
            <ClientOnly>
                <LazyDashboardDonutChart :distribution="contentDistribution" />
            </ClientOnly>
            <DashboardTopContent
                :articles="topArticles"
                :projects="topProjects"
                :stacks="topStacks"
                :loading="isLoading"
            />
        </section>
    </div>
</template>

<script setup lang="ts">
    import { useQueryClient } from '@tanstack/vue-query';
    import { computed } from 'vue';

    import {
        DashboardHeader,
        DashboardStatsGrid,
        DashboardActivityFeed,
        DashboardTopContent,
    } from '@/components/feature/admin/dashboard';
    import { useSeo } from '@/composables/seo/useSeo';
    import { usePopularArticles, articleKeys } from '@/services/api/modules/articles';
    import { useFeaturedProjects, projectKeys } from '@/services/api/modules/projects';
    import { useFeaturedStacks, stackKeys } from '@/services/api/modules/stacks';
    import { statsKeys, useDashboardOverview } from '@/services/api/modules/stats';
    import { useAuthStore } from '@/stores/auth';

    import type { DashboardTopItem } from '@/types/components/admin';

    definePageMeta({
        layout: 'admin',
        title: 'Dashboard',
    });

    useSeo({
        title: 'Dashboard Admin',
        description: 'Panneau d\'administration du portfolio',
        noindex: true,
        url: '/admin/dashboard',
    });

    const authStore = useAuthStore();
    const queryClient = useQueryClient();

    // TanStack Query | overview (stats, charts, activity, quickStats)
    const { data: dashboardData, isLoading, isRefetching } = useDashboardOverview();

    // TanStack Query | top content
    const { data: articlesData } = usePopularArticles(5);
    const { data: projectsData } = useFeaturedProjects(5);
    const { data: stacksData } = useFeaturedStacks(5);

    // Map API types to DashboardTopItem
    const topArticles = computed<DashboardTopItem[]>(() =>
        (articlesData.value ?? []).map((a) => ({
            id: a.id,
            title: a.title,
            slug: a.slug,
            views: a.views ?? 0,
            category: a.category,
            type: 'article' as const,
        })),
    );

    const topProjects = computed<DashboardTopItem[]>(() =>
        (projectsData.value ?? []).map((p) => ({
            id: p.id,
            title: p.title,
            slug: p.slug,
            views: p.views ?? 0,
            category: p.category,
            type: 'project' as const,
        })),
    );

    const topStacks = computed<DashboardTopItem[]>(() =>
        (stacksData.value ?? []).map((s) => ({
            id: s.id,
            title: s.name,
            slug: s.slug,
            views: 0,
            level: s.level ?? 0,
            category: s.category,
            type: 'stack' as const,
        })),
    );

    // Distribution colors
    const DISTRIBUTION_COLORS = {
        articles: '#673c5c',
        projects: '#ac72a0',
        stacks: '#0ea5e9',
        experiences: '#111827',
    } as const;

    const recentActivities = computed(() => {
        if (!dashboardData.value?.activity) {
            return [];
        }
        return dashboardData.value.activity.slice(0, 5).map((item) => ({
            id: item.id,
            type: item.type,
            text: item.title,
            date: new Date(item.timestamp),
        }));
    });

    const contentDistribution = computed(() => {
        const stats = dashboardData.value?.stats;
        if (!stats) {
            return [
                { label: 'Articles', count: 0, color: DISTRIBUTION_COLORS.articles },
                { label: 'Projets', count: 0, color: DISTRIBUTION_COLORS.projects },
                { label: 'Stacks', count: 0, color: DISTRIBUTION_COLORS.stacks },
                { label: 'Experiences', count: 0, color: DISTRIBUTION_COLORS.experiences },
            ];
        }

        return [
            { label: 'Articles', count: stats.articles.count || 0, color: DISTRIBUTION_COLORS.articles },
            { label: 'Projets', count: stats.projects.count || 0, color: DISTRIBUTION_COLORS.projects },
            { label: 'Stacks', count: stats.stacks.count || 0, color: DISTRIBUTION_COLORS.stacks },
            { label: 'Experiences', count: stats.experiences.count || 0, color: DISTRIBUTION_COLORS.experiences },
        ];
    });

    const refreshDashboard = () => {
        queryClient.invalidateQueries({ queryKey: statsKeys.all });
        queryClient.invalidateQueries({ queryKey: articleKeys.all });
        queryClient.invalidateQueries({ queryKey: projectKeys.all });
        queryClient.invalidateQueries({ queryKey: stackKeys.all });
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;

    .dashboard {
        animation: fade-in 0.3s ease-out;
    }

    .dashboard__row {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: vars.$spacing-lg;
        margin-bottom: vars.$spacing-xl;

        &--reverse {
            grid-template-columns: 1fr 2fr;
        }

        @include mix.responsive(tablet) {
            grid-template-columns: 1fr;

            &--reverse {
                grid-template-columns: 1fr;

                > :first-child {
                    order: 2;
                }

                > :last-child {
                    order: 1;
                }
            }
        }
    }

    @keyframes fade-in {
        from {
            opacity: 0;
        }

        to {
            opacity: 1;
        }
    }
</style>
