import { onBeforeUnmount, onMounted, ref } from 'vue';

import type { Ref } from 'vue';

interface UseTypingEffectOptions {
    typeSpeed?: number;
    deleteSpeed?: number;
    pauseMs?: number;
    startDelay?: number;
}

interface UseTypingEffectReturn {
    currentText: Ref<string>;
    isPaused: Ref<boolean>;
}

export function useTypingEffect(texts: string[], options: UseTypingEffectOptions = {}): UseTypingEffectReturn {
    const { typeSpeed = 150, deleteSpeed = 50, pauseMs = 2000, startDelay = 300 } = options;

    const currentText = ref('');
    const isPaused = ref(false);

    let currentIndex = 0;
    let isDeleting = false;
    let timer: ReturnType<typeof setTimeout> | null = null;

    const tick = () => {
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

    onMounted(() => {
        if ('requestIdleCallback' in window) {
            requestIdleCallback(() => tick());
        } else {
            setTimeout(() => tick(), startDelay);
        }
    });

    onBeforeUnmount(() => {
        if (timer) {
            clearTimeout(timer);
        }
    });

    return { currentText, isPaused };
}
