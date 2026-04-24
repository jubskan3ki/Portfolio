import { onBeforeUnmount, onMounted, ref, watch } from 'vue';

import type { UseTypingEffectOptions, UseTypingEffectReturn } from '@/types/composables/ui';

export function useTypingEffect(texts: string[], options: UseTypingEffectOptions = {}): UseTypingEffectReturn {
    const { typeSpeed = 150, deleteSpeed = 50, pauseMs = 2000, startDelay = 300, enabled } = options;

    const currentText = ref('');
    const isPaused = ref(false);

    let currentIndex = 0;
    let isDeleting = false;
    let timer: ReturnType<typeof setTimeout> | null = null;
    let running = false;

    const clear = () => {
        if (timer) {
            clearTimeout(timer);
            timer = null;
        }
    };

    const tick = () => {
        if (enabled && !enabled.value) {
            running = false;
            return;
        }
        const fullText = texts[currentIndex] ?? '';
        let nextDelay: number;

        if (isDeleting) {
            currentText.value = fullText.substring(0, currentText.value.length - 1);
            isPaused.value = false;
            nextDelay = deleteSpeed;
        } else {
            currentText.value = fullText.substring(0, currentText.value.length + 1);
            isPaused.value = false;
            nextDelay = typeSpeed;
        }

        if (!isDeleting && currentText.value === fullText) {
            isDeleting = true;
            isPaused.value = true;
            nextDelay = pauseMs;
        } else if (isDeleting && currentText.value === '') {
            isDeleting = false;
            currentIndex = (currentIndex + 1) % texts.length;
            nextDelay = startDelay;
        }

        timer = setTimeout(tick, nextDelay);
    };

    const start = () => {
        if (running) {
            return;
        }
        running = true;
        tick();
    };

    onMounted(() => {
        const boot = () => {
            if (enabled && !enabled.value) {
                return;
            }
            start();
        };
        if ('requestIdleCallback' in window) {
            requestIdleCallback(() => boot());
        } else {
            setTimeout(boot, startDelay);
        }
    });

    if (enabled) {
        watch(enabled, (active) => {
            if (active) {
                start();
            } else {
                clear();
                running = false;
            }
        });
    }

    onBeforeUnmount(clear);

    return { currentText, isPaused };
}
