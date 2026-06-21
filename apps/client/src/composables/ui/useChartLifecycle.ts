import type { Chart, ChartConfiguration, ChartData, ChartOptions, ChartType } from 'chart.js';
import type { Ref } from 'vue';
import { nextTick, onUnmounted, ref, shallowRef } from 'vue';
import type { UseChartLifecycleOptions, UseChartLifecycleReturn } from '@/types/composables/ui';

const waitForCanvas = (
    canvasRef: Ref<HTMLCanvasElement | null>,
    isCancelled: () => boolean,
    maxAttempts = 10,
    delay = 50,
): Promise<HTMLCanvasElement | null> => {
    const poll = (attempt: number): Promise<HTMLCanvasElement | null> =>
        nextTick().then(() => {
            if (isCancelled() || canvasRef.value?.isConnected) {
                return canvasRef.value;
            }
            if (attempt >= maxAttempts) {
                return canvasRef.value;
            }
            // La chaîne s'arrête au prochain tour via le garde isCancelled() en
            // tête de poll : au plus un setTimeout résiduel après destruction.
            return new Promise<HTMLCanvasElement | null>((resolve) => {
                setTimeout(() => resolve(poll(attempt + 1)), delay);
            });
        });
    return poll(0);
};

export function useChartLifecycle<T extends ChartType = ChartType>(
    options: UseChartLifecycleOptions<T>,
): UseChartLifecycleReturn<T> {
    const { type, defaultOptions = {} } = options;

    const chart = shallowRef<Chart<T> | null>(null) as Ref<Chart<T> | null>;
    const canvasRef = ref<HTMLCanvasElement | null>(null);
    const isUpdating = ref(false);
    const isInitialized = ref(false);
    let isDestroyed = false;
    let isInitializing = false;

    const destroyChart = () => {
        isDestroyed = true;
        if (chart.value) {
            try {
                chart.value.destroy();
            } catch {
                /* noop */
            }
            chart.value = null;
        }
        isInitialized.value = false;
    };

    const initChart = async (data: ChartData<T>, chartOptions?: ChartOptions<T>): Promise<boolean> => {
        if (isDestroyed || isInitializing) {
            return false;
        }

        isInitializing = true;

        try {
            if (chart.value) {
                try {
                    chart.value.destroy();
                } catch {
                    /* noop */
                }
                chart.value = null;
                isInitialized.value = false;
            }

            const canvas = await waitForCanvas(canvasRef, () => isDestroyed);

            if (!canvas || isDestroyed) {
                return false;
            }

            const ctx = canvas.getContext('2d');
            if (!ctx) {
                return false;
            }

            const {
                Chart: ChartJS,
                LineController,
                LineElement,
                PointElement,
                DoughnutController,
                ArcElement,
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
                DoughnutController,
                ArcElement,
                CategoryScale,
                LinearScale,
                Tooltip,
                Legend,
                Filler,
            );

            if (isDestroyed || !canvasRef.value?.isConnected) {
                return false;
            }

            const existingChart = ChartJS.getChart(canvas);
            if (existingChart) {
                existingChart.destroy();
            }

            const config: ChartConfiguration<T> = {
                type,
                data,
                options: {
                    ...defaultOptions,
                    ...chartOptions,
                } as ChartOptions<T>,
            };

            chart.value = new ChartJS(ctx, config) as Chart<T>;
            isInitialized.value = true;
            return true;
        } catch (error) {
            if (import.meta.dev) {
                console.error('[useChartLifecycle] Failed to initialize chart:', error);
            }
            return false;
        } finally {
            isInitializing = false;
        }
    };

    const updateData = (data: ChartData<T>) => {
        if (!chart.value || !isInitialized.value || isUpdating.value || isDestroyed) {
            return;
        }

        if (!canvasRef.value?.isConnected) {
            return;
        }

        try {
            isUpdating.value = true;
            chart.value.data = data;
            chart.value.update('none');
        } catch (error) {
            if (import.meta.dev) {
                console.warn('[useChartLifecycle] Update failed:', error);
            }
        } finally {
            isUpdating.value = false;
        }
    };

    const updateOptions = (newOptions: ChartOptions<T>) => {
        if (!chart.value || !isInitialized.value || isDestroyed) {
            return;
        }

        try {
            chart.value.options = {
                ...chart.value.options,
                ...newOptions,
            };
            chart.value.update('none');
        } catch {
            /* noop */
        }
    };

    onUnmounted(() => {
        destroyChart();
    });

    return {
        chart,
        canvasRef,
        initChart,
        updateData,
        updateOptions,
        destroyChart,
        isInitialized,
    };
}
