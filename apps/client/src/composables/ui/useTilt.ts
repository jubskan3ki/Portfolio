// Effet de tilt subtil avec interpolation fluide (lerp) et requestAnimationFrame
import { onMounted, onUnmounted, ref, type Ref } from 'vue';

import type { TiltCSSOptions } from '@/types/composables/ui';

export function useTiltCSS(elementRef: Ref<HTMLElement | null>, options: TiltCSSOptions = {}) {
    const { maxRotation = 8, perspective = 1000, scale = 1.015, smoothing = 0.08, resetOnLeave = true } = options;

    const isHovering = ref(false);

    // Valeurs cibles (où la souris pointe)
    const target = { x: 0, y: 0 };
    // Valeurs actuelles (interpolées)
    const current = { x: 0, y: 0 };

    let animationId: number | null = null;
    let rect: DOMRect | null = null;

    // Lerp (interpolation linéaire)
    const lerp = (start: number, end: number, factor: number): number => {
        return start + (end - start) * factor;
    };

    // Boucle d'animation avec requestAnimationFrame
    const animate = () => {
        // Interpolation fluide vers la cible
        current.x = lerp(current.x, target.x, smoothing);
        current.y = lerp(current.y, target.y, smoothing);

        // Arrondir pour éviter les micro-mouvements
        const rotateX = Math.round(current.y * 100) / 100;
        const rotateY = Math.round(current.x * 100) / 100;

        if (elementRef.value) {
            const currentScale = isHovering.value ? scale : 1;
            elementRef.value.style.transform = `perspective(${perspective}px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(${currentScale})`;
        }

        // Continuer l'animation si on hover ou si pas encore à la position repos
        const isAtRest = Math.abs(current.x) < 0.01 && Math.abs(current.y) < 0.01;
        if (isHovering.value || !isAtRest) {
            animationId = requestAnimationFrame(animate);
        } else {
            // Reset complet quand au repos
            if (elementRef.value) {
                elementRef.value.style.transform = '';
            }
            animationId = null;
        }
    };

    // Démarrer l'animation si pas déjà en cours
    const startAnimation = () => {
        if (animationId === null) {
            animationId = requestAnimationFrame(animate);
        }
    };

    const handleMouseMove = (event: MouseEvent) => {
        if (!elementRef.value || !rect) {
            return;
        }

        // Calculer la position relative au centre (-1 à 1)
        const x = (event.clientX - rect.left) / rect.width;
        const y = (event.clientY - rect.top) / rect.height;

        // Convertir en rotation (centré sur 0)
        target.x = (x - 0.5) * 2 * maxRotation;
        target.y = (y - 0.5) * -2 * maxRotation;
    };

    const handleMouseEnter = () => {
        isHovering.value = true;
        // Cache le rect au début du hover pour éviter les recalculs
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
        // L'animation continue pour revenir doucement à la position de repos
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

        // Style initial pour will-change
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
        // Ne pas activer si l'utilisateur préfère réduire les animations
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
