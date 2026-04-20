<template>
    <div class="card card--small">
        <div class="card__header">
            <div class="card__title-group">
                <BaseIcon name="pie-chart" :size="18" class="card__icon" />
                <h4 class="card__title">Répartition</h4>
            </div>
        </div>
        <div class="donut-container">
            <canvas ref="canvasRef"></canvas>
            <div class="donut-center">
                <p class="donut-center__value">{{ totalContent }}</p>
                <p class="donut-center__label">contenus</p>
            </div>
        </div>
        <div class="donut-legend">
            <div v-for="item in distribution" :key="item.label" class="donut-legend__item">
                <small class="donut-legend__dot" :style="{ backgroundColor: item.color }"></small>
                <small class="donut-legend__label">{{ item.label }}</small>
                <small class="donut-legend__value">{{ item.count }}</small>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { computed, watch, onMounted, nextTick, ref } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import { useChartLifecycle } from '@/composables/ui/useChartLifecycle';

    import type { DashboardDonutChartProps } from '@/types/components/admin';

    const props = defineProps<DashboardDonutChartProps>();
    const isMounted = ref(false);

    const totalContent = computed(() => {
        if (!props.distribution || props.distribution.length === 0) {
            return 0;
        }
        return props.distribution.reduce((sum, item) => sum + (item.count || 0), 0);
    });

    // Check if we have real data (not all zeros)
    const hasRealData = computed(() => {
        if (!props.distribution || props.distribution.length === 0) {
            return false;
        }
        return props.distribution.some((item) => item.count > 0);
    });

    const getChartData = () => {
        const data = props.distribution || [];

        // Always use actual values from props
        return {
            labels: data.map((d) => d.label),
            datasets: [
                {
                    data: data.map((d) => d.count || 0),
                    backgroundColor: data.map((d) => d.color),
                    borderWidth: 0,
                    hoverOffset: 6,
                    borderRadius: 6,
                },
            ],
        };
    };

    const { canvasRef, initChart, updateData, isInitialized } = useChartLifecycle({
        type: 'doughnut',
        defaultOptions: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '68%',
            spacing: 4,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#1f2937',
                    titleColor: '#ffffff',
                    bodyColor: '#d1d5db',
                    padding: 14,
                    cornerRadius: 10,
                    titleFont: { size: 13, weight: 'bold' },
                    bodyFont: { size: 12 },
                    displayColors: true,
                    boxPadding: 6,
                    callbacks: {
                        label: (ctx) => {
                            const dataset = ctx.dataset.data as number[];
                            const total = dataset.reduce((sum, val) => sum + val, 0);
                            const percentage = total > 0 ? Math.round((ctx.parsed / total) * 100) : 0;
                            return ` ${ctx.parsed} (${percentage}%)`;
                        },
                    },
                },
            },
            animation: {
                animateRotate: true,
                animateScale: true,
            },
        },
    });
    void canvasRef; // Used as template ref

    // Initialize chart after mount only if we have real data
    onMounted(async () => {
        isMounted.value = true;
        await nextTick();
        if (hasRealData.value) {
            await initChart(getChartData());
        }
    });

    // Update chart when distribution changes (after initial mount)
    watch(
        () => props.distribution,
        async (newVal, oldVal) => {
            if (!isMounted.value) {
                return;
            }

            // Skip if data hasn't really changed
            if (oldVal && JSON.stringify(newVal) === JSON.stringify(oldVal)) {
                return;
            }

            // Only proceed if we have real data
            if (!hasRealData.value) {
                return;
            }

            if (isInitialized.value) {
                updateData(getChartData());
            } else {
                await initChart(getChartData());
            }
        },
        { deep: true },
    );
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .card {
        background: vars.$white;
        border: 1px solid func.color-alpha(vars.$black, 0.06);
        border-radius: vars.$border-radius-xl;
        padding: vars.$spacing-lg;
        min-width: 0;

        @include mix.responsive(mobile) {
            padding: vars.$spacing-md;
        }

        &__header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: vars.$spacing-lg;
            gap: vars.$spacing-md;
            flex-wrap: wrap;
        }

        &__title-group {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;
        }

        &__icon {
            color: vars.$text-muted;
        }

        &__title {
            font-weight: vars.$font-weight-semibold;
            color: vars.$text-primary;
            margin: 0;
        }
    }

    .donut-container {
        position: relative;
        height: 180px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: vars.$spacing-lg;
    }

    .donut-center {
        position: absolute;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        pointer-events: none;
        width: 90px;
        height: 90px;
        border-radius: 50%;
        background: transparent;

        &__value {
            font-weight: vars.$font-weight-bold;
            color: vars.$primary-color;
            line-height: 1;
        }

        &__label {
            color: vars.$text-muted;
            margin-top: vars.$spacing-xxxxs;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
    }

    .donut-legend {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: vars.$spacing-xs;

        &__item {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xxs;
            padding: vars.$spacing-xxs vars.$spacing-xs;
            border-radius: vars.$border-radius-md;
            transition: background 0.15s;

            &:hover {
                background: vars.$bg-secondary;
            }
        }

        &__dot {
            width: 12px;
            height: 12px;
            border-radius: vars.$border-radius-sm;
            flex-shrink: 0;
        }

        &__label {
            flex: 1;
            color: vars.$text-secondary;
        }

        &__value {
            font-weight: vars.$font-weight-bold;
            color: vars.$text-primary;
            background: vars.$bg-secondary;
            padding: vars.$spacing-xxxxs vars.$spacing-xxs;
            border-radius: vars.$border-radius-full;
        }
    }
</style>
