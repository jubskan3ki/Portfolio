<template>
    <section class="stats-section">
        <div class="stats-grid">
            <StatsCard
                v-for="stat in statsCards"
                :key="stat.label"
                :label="stat.label"
                :value="stat.value"
                :icon="stat.icon"
                :trend="stat.trend"
                :color="stat.color"
                :loading="loading"
            />
        </div>
    </section>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import StatsCard from '@/components/feature/admin/StatsCard.vue';

    import type { DashboardStatsGridProps } from '@/types/components/admin';

    const props = withDefaults(defineProps<DashboardStatsGridProps>(), {
        loading: false,
    });

    const STATS_COLORS = {
        articles: '#673c5c',
        projects: '#ac72a0',
        stacks: '#22c55e',
        messages: '#f59e0b',
    } as const;

    const statsCards = computed(() => {
        const stats = props.stats;
        if (!stats) {
            return [
                { label: 'Articles', value: '0', icon: 'file-text', trend: '', color: STATS_COLORS.articles },
                { label: 'Projets', value: '0', icon: 'folder', trend: '', color: STATS_COLORS.projects },
                { label: 'Stacks', value: '0', icon: 'layers', trend: '', color: STATS_COLORS.stacks },
                { label: 'Messages', value: '0', icon: 'mail', trend: '', color: STATS_COLORS.messages },
            ];
        }

        const newMessages = stats.messages.new;
        const messageTrend = newMessages > 0 ? `+${newMessages} nouveau${newMessages > 1 ? 'x' : ''}` : '';

        return [
            {
                label: 'Articles',
                value: String(stats.articles.count),
                icon: 'file-text',
                trend: stats.articles.published > 0 ? `${stats.articles.published} publiés` : '',
                color: STATS_COLORS.articles,
            },
            {
                label: 'Projets',
                value: String(stats.projects.count),
                icon: 'folder',
                trend: stats.projects.totalViews > 0 ? `${stats.projects.totalViews} vues` : '',
                color: STATS_COLORS.projects,
            },
            {
                label: 'Stacks',
                value: String(stats.stacks.count),
                icon: 'layers',
                trend: '',
                color: STATS_COLORS.stacks,
            },
            {
                label: 'Messages',
                value: String(stats.messages.count),
                icon: 'mail',
                trend: messageTrend,
                color: STATS_COLORS.messages,
            },
        ];
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;

    .stats-section {
        margin-bottom: vars.$spacing-xl;
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
</style>
