import type { Ref } from 'vue';
import { onMounted, onUnmounted, ref } from 'vue';

import type { TiltCSSOptions } from '@/types/composables/ui';

export function useTiltCSS(elementRef: Ref<HTMLElement | null>, options: TiltCSSOptions = {}) {
    const { maxRotation = 8, perspective = 1000, scale = 1.015, smoothing = 0.08, resetOnLeave = true } = options;

    const isHovering = ref(false);

    const target = { x: 0, y: 0 };
    const current = { x: 0, y: 0 };

    let animationId: number | null = null;
    let rect: DOMRect | null = null;

    const lerp = (start: number, end: number, factor: number): number => {
        return start + (end - start) * factor;
    };

    const animate = () => {
        current.x = lerp(current.x, target.x, smoothing);
        current.y = lerp(current.y, target.y, smoothing);

        const rotateX = Math.round(current.y * 100) / 100;
        const rotateY = Math.round(current.x * 100) / 100;

        if (elementRef.value) {
            const currentScale = isHovering.value ? scale : 1;
            elementRef.value.style.transform = `perspective(${perspective}px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(${currentScale})`;
        }

        const isAtRest = Math.abs(current.x) < 0.01 && Math.abs(current.y) < 0.01;
        if (isHovering.value || !isAtRest) {
            animationId = requestAnimationFrame(animate);
        } else {
            if (elementRef.value) {
                elementRef.value.style.transform = '';
            }
            animationId = null;
        }
    };

    const startAnimation = () => {
        if (animationId === null) {
            animationId = requestAnimationFrame(animate);
        }
    };

    const handleMouseMove = (event: MouseEvent) => {
        if (!elementRef.value || !rect) {
            return;
        }

        const x = (event.clientX - rect.left) / rect.width;
        const y = (event.clientY - rect.top) / rect.height;

        target.x = (x - 0.5) * 2 * maxRotation;
        target.y = (y - 0.5) * -2 * maxRotation;
    };

    const handleMouseEnter = () => {
        isHovering.value = true;
        // Cache rect on enter; avoids getBoundingClientRect on every mousemove (layout thrash).
        if (elementRef.value) {
            rect = elementRef.value.getBoundingClientRect();
        }
        startAnimation();
    };

    const handleMouseLeave = () => {
        isHovering.value = false;
        rect = null;

        if (resetOnLeave) {
            target.x = 0;
            target.y = 0;
        }
        startAnimation();
    };

    const stopAnimation = () => {
        if (animationId !== null) {
            cancelAnimationFrame(animationId);
            animationId = null;
        }
    };

    const bindEvents = () => {
        if (!elementRef.value) {
            return;
        }

        elementRef.value.style.willChange = 'transform';
        elementRef.value.style.transformStyle = 'preserve-3d';

        elementRef.value.addEventListener('mousemove', handleMouseMove, { passive: true });
        elementRef.value.addEventListener('mouseenter', handleMouseEnter, { passive: true });
        elementRef.value.addEventListener('mouseleave', handleMouseLeave, { passive: true });
    };

    const unbindEvents = () => {
        if (!elementRef.value) {
            return;
        }

        elementRef.value.style.willChange = '';
        elementRef.value.style.transformStyle = '';
        elementRef.value.style.transform = '';

        elementRef.value.removeEventListener('mousemove', handleMouseMove);
        elementRef.value.removeEventListener('mouseenter', handleMouseEnter);
        elementRef.value.removeEventListener('mouseleave', handleMouseLeave);

        stopAnimation();
    };

    onMounted(() => {
        if (typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            return;
        }
        bindEvents();
    });

    onUnmounted(() => {
        unbindEvents();
    });

    return {
        isHovering,
        bindEvents,
        unbindEvents,
        stopAnimation,
    };
}
