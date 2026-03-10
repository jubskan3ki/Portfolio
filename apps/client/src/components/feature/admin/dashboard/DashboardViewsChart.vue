<template>
    <div class="card card--large">
        <div class="card__header">
            <div class="card__title-group">
                <BaseIcon name="eye" :size="18" class="card__icon" />
                <h4 class="card__title">Statistiques de vues</h4>
            </div>
            <div class="card__actions">
                <DateRangePicker v-model="dateRange" :available-dates="availableDates" />
            </div>
        </div>
        <div v-if="!hasData" class="chart-container chart-container--empty">
            <div class="empty-state">
                <BaseIcon name="chart-line" :size="48" class="empty-state__icon" />
                <p class="empty-state__text">Aucune donnée de vues disponible</p>
            </div>
        </div>
        <div v-else class="chart-container">
            <canvas ref="canvasRef" class="chart-canvas"></canvas>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { watch, ref, computed, nextTick, onMounted, onUnmounted } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import DateRangePicker from '@/components/ui/DateRangePicker.vue';
    import { dayjs } from '@/services/utils/date';

    import type { DateRange } from '@/types/components/ui';
    import type { Chart } from 'chart.js';

    interface ViewData {
        date: string;
        views: number;
    }

    interface Props {
        data: ViewData[];
        totalViews?: number;
    }

    const props = withDefaults(defineProps<Props>(), {
        totalViews: 0,
    });

    const dateRange = ref<DateRange>({
        startDate: '',
        endDate: '',
    });
    const canvasRef = ref<HTMLCanvasElement | null>(null);
    const chart = ref<Chart | null>(null);
    const hasData = computed(() => props.data?.length > 0);

    // Extract available dates from data
    const availableDates = computed(() => {
        return props.data.map((d) => d.date);
    });

    // Filter data based on selected date range
    const filteredData = computed(() => {
        if (!dateRange.value.startDate || !dateRange.value.endDate) {
            return props.data;
        }

        return props.data.filter((d) => {
            const date = dayjs(d.date);
            const start = dayjs(dateRange.value.startDate);
            const end = dayjs(dateRange.value.endDate);
            return (
                (date.isAfter(start, 'day') || date.isSame(start, 'day'))
                && (date.isBefore(end, 'day') || date.isSame(end, 'day'))
            );
        });
    });

    let isInitializing = false;
    let isDestroyed = false;

    const initChart = async () => {
        if (isInitializing || isDestroyed || !hasData.value || !canvasRef.value || filteredData.value.length === 0) {
            return;
        }

        isInitializing = true;

        try {
            await nextTick();

            if (!canvasRef.value?.isConnected || isDestroyed) {
                return;
            }

            const {
                Chart: ChartJS,
                LineController,
                LineElement,
                PointElement,
                CategoryScale,
                LinearScale,
                Tooltip,
                Legend,
                Filler,
            } = await import('chart.js');
            ChartJS.register(
                LineController,
                LineElement,
                PointElement,
                CategoryScale,
                LinearScale,
                Tooltip,
                Legend,
                Filler,
            );

            if (isDestroyed || !canvasRef.value?.isConnected) {
                return;
            }

            if (chart.value) {
                chart.value.destroy();
                chart.value = null;
            }

            // Also destroy any existing chart on this canvas
            const existingChart = ChartJS.getChart(canvasRef.value);
            if (existingChart) {
                existingChart.destroy();
            }

            const labels = filteredData.value.map((d: ViewData) => {
                const [, month, day] = d.date.split('-');
                return `${day}/${month}`;
            });

            const values = filteredData.value.map((d: ViewData) => d.views);

            chart.value = new ChartJS(canvasRef.value, {
                type: 'line',
                data: {
                    labels,
                    datasets: [
                        {
                            label: 'Vues',
                            data: values,
                            borderColor: '#3b82f6',
                            backgroundColor: 'rgba(59, 130, 246, 0.1)',
                            fill: true,
                            tension: 0.4,
                            pointRadius: 3,
                            pointBackgroundColor: '#3b82f6',
                            pointBorderColor: '#fff',
                            pointBorderWidth: 2,
                            pointHoverRadius: 5,
                            borderWidth: 2,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: { intersect: false, mode: 'index' },
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { grid: { display: false }, ticks: { color: '#9ca3af', font: { size: 11 } } },
                        y: {
                            beginAtZero: true,
                            grid: { color: 'rgba(0, 0, 0, 0.04)' },
                            ticks: { color: '#9ca3af', font: { size: 11 } },
                        },
                    },
                },
            });
        } catch (error) {
            if (import.meta.dev) {
                console.error('Chart error:', error);
            }
        } finally {
            isInitializing = false;
        }
    };

    // Initialize on mount
    onMounted(() => {
        if (hasData.value && filteredData.value.length > 0) {
            initChart();
        }
    });

    // Re-init when filtered data changes (date range or data prop)
    watch(
        [filteredData, () => dateRange.value.startDate, () => dateRange.value.endDate],
        () => {
            if (hasData.value && canvasRef.value) {
                initChart();
            }
        },
        { flush: 'post' },
    );

    onUnmounted(() => {
        isDestroyed = true;
        if (chart.value) {
            try {
                chart.value.destroy();
            } catch {
                // Ignore
            }
            chart.value = null;
        }
    });
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

        &__actions {
            display: flex;
            align-items: center;
            gap: vars.$spacing-sm;
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

    .chart-container {
        height: 300px;
        position: relative;
        display: flex;
        flex-direction: column;

        @include mix.responsive(mobile) {
            height: 240px;
        }

        &--empty {
            display: flex;
            align-items: center;
            justify-content: center;
        }
    }

    .chart-canvas {
        display: block;
        max-width: 100%;
        max-height: 100%;
    }

    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: vars.$spacing-sm;
        color: vars.$text-muted;

        &__icon {
            opacity: 0.3;
        }

        &__text {
            font-size: vars.$font-size-sm;
            margin: 0;
        }
    }
</style>
