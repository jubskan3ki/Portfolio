import { onBeforeUnmount, ref, type Ref } from 'vue';

interface UseProgressTimerOptions {
    duration: number;
    onComplete?: () => void;
    autoStart?: boolean;
    stepTime?: number;
}

interface UseProgressTimerReturn {
    progress: Ref<number>;
    isRunning: Ref<boolean>;
    remainingTime: Ref<number>;
    start: () => void;
    pause: () => void;
    resume: () => void;
    reset: () => void;
    stop: () => void;
}

/**
 * Composable for managing progress-based timers with pause/resume functionality
 * Used by Toast, AlertItem, and other auto-closing components
 */
export function useProgressTimer(options: UseProgressTimerOptions): UseProgressTimerReturn {
    const { duration, onComplete, autoStart = false, stepTime = 10 } = options;

    const progress = ref(100);
    const isRunning = ref(false);
    const remainingTime = ref(duration);

    let timer: ReturnType<typeof setTimeout> | null = null;
    let progressInterval: ReturnType<typeof setInterval> | null = null;
    let startTime = 0;

    const clearTimers = () => {
        if (timer) {
            clearTimeout(timer);
            timer = null;
        }
        if (progressInterval) {
            clearInterval(progressInterval);
            progressInterval = null;
        }
    };

    const start = () => {
        if (isRunning.value) {
            return;
        }

        isRunning.value = true;
        startTime = Date.now();

        timer = setTimeout(() => {
            stop();
            onComplete?.();
        }, remainingTime.value);

        const decrement = (100 / duration) * stepTime;
        progressInterval = setInterval(() => {
            progress.value = Math.max(0, progress.value - decrement);
        }, stepTime);
    };

    const pause = () => {
        if (!isRunning.value) {
            return;
        }

        clearTimers();
        isRunning.value = false;

        const elapsed = Date.now() - startTime;
        remainingTime.value = Math.max(0, remainingTime.value - elapsed);
    };

    const resume = () => {
        if (isRunning.value || remainingTime.value <= 0) {
            return;
        }

        isRunning.value = true;
        startTime = Date.now();

        timer = setTimeout(() => {
            stop();
            onComplete?.();
        }, remainingTime.value);

        const decrement = (progress.value / remainingTime.value) * stepTime;
        progressInterval = setInterval(() => {
            progress.value = Math.max(0, progress.value - decrement);
        }, stepTime);
    };

    const reset = () => {
        clearTimers();
        isRunning.value = false;
        progress.value = 100;
        remainingTime.value = duration;
    };

    const stop = () => {
        clearTimers();
        isRunning.value = false;
    };

    if (autoStart) {
        start();
    }

    onBeforeUnmount(() => {
        clearTimers();
    });

    return {
        progress,
        isRunning,
        remainingTime,
        start,
        pause,
        resume,
        reset,
        stop,
    };
}
