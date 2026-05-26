import type { Ref } from 'vue';
import { onBeforeUnmount, onMounted, ref } from 'vue';
import { useReducedMotion } from '@/composables/accessibility/useReducedMotion';
import type { UseDragScrollOptions } from '@/types/composables/ui';

export function useDragScroll(elRef: Readonly<Ref<HTMLElement | null>>, options: UseDragScrollOptions = {}) {
    const { inertia = true, dragThreshold = 5 } = options;
    const { prefersReducedMotion } = useReducedMotion();

    const isDragging = ref(false);
    const hasDragged = ref(false);

    let startX = 0;
    let startScrollLeft = 0;
    let lastX = 0;
    let lastTime = 0;
    let velocity = 0;
    let pointerId: number | null = null;
    let inertiaRaf: number | null = null;

    const cancelInertia = () => {
        if (inertiaRaf !== null) {
            cancelAnimationFrame(inertiaRaf);
            inertiaRaf = null;
        }
    };

    const onPointerDown = (e: PointerEvent) => {
        if (e.pointerType === 'mouse' && e.button !== 0) {
            return;
        }

        const el = elRef.value;
        if (!el) {
            return;
        }

        if (el.scrollWidth <= el.clientWidth) {
            return;
        }

        cancelInertia();

        isDragging.value = true;
        hasDragged.value = false;
        startX = e.pageX;
        startScrollLeft = el.scrollLeft;
        lastX = e.pageX;
        lastTime = performance.now();
        velocity = 0;
        pointerId = e.pointerId;

        // setPointerCapture est reporté à onPointerMove (seulement quand drag réel détecté).
        // Sinon un simple click sur un child button est redirigé vers le root capturer.
        el.classList.add('is-dragging');
    };

    const onPointerMove = (e: PointerEvent) => {
        if (!isDragging.value || e.pointerId !== pointerId) {
            return;
        }

        const el = elRef.value;
        if (!el) {
            return;
        }

        const dx = e.pageX - startX;
        if (!hasDragged.value && Math.abs(dx) > dragThreshold) {
            hasDragged.value = true;
            // Capture uniquement quand on sait qu'on drague (pas sur simple tap/click).
            try {
                el.setPointerCapture(e.pointerId);
            } catch {
                /* noop */
            }
        }

        if (!hasDragged.value) {
            return;
        }

        el.scrollLeft = startScrollLeft - dx;

        const now = performance.now();
        const dt = now - lastTime;
        if (dt > 0) {
            velocity = (e.pageX - lastX) / dt;
        }
        lastX = e.pageX;
        lastTime = now;
    };

    const startInertia = (el: HTMLElement) => {
        const friction = 0.94;
        let v = velocity * 16;
        const step = () => {
            if (Math.abs(v) < 0.4) {
                inertiaRaf = null;
                return;
            }
            el.scrollLeft -= v;
            v *= friction;
            inertiaRaf = requestAnimationFrame(step);
        };
        inertiaRaf = requestAnimationFrame(step);
    };

    const endDrag = (e: PointerEvent) => {
        if (!isDragging.value || e.pointerId !== pointerId) {
            return;
        }
        const el = elRef.value;
        isDragging.value = false;
        pointerId = null;

        if (!el) {
            return;
        }

        el.classList.remove('is-dragging');
        if (hasDragged.value) {
            try {
                el.releasePointerCapture(e.pointerId);
            } catch {
                /* noop */
            }
        }

        if (inertia && !prefersReducedMotion.value && hasDragged.value && Math.abs(velocity) > 0.1) {
            startInertia(el);
        }
    };

    const onClickCapture = (e: MouseEvent) => {
        if (hasDragged.value) {
            e.preventDefault();
            e.stopPropagation();
            hasDragged.value = false;
        }
    };

    const attach = () => {
        const el = elRef.value;
        if (!el) {
            return;
        }
        el.addEventListener('pointerdown', onPointerDown);
        el.addEventListener('pointermove', onPointerMove);
        el.addEventListener('pointerup', endDrag);
        el.addEventListener('pointercancel', endDrag);
        el.addEventListener('click', onClickCapture, { capture: true });
    };

    const detach = () => {
        const el = elRef.value;
        if (!el) {
            return;
        }
        el.removeEventListener('pointerdown', onPointerDown);
        el.removeEventListener('pointermove', onPointerMove);
        el.removeEventListener('pointerup', endDrag);
        el.removeEventListener('pointercancel', endDrag);
        el.removeEventListener('click', onClickCapture, { capture: true });
    };

    onMounted(attach);

    onBeforeUnmount(() => {
        cancelInertia();
        detach();
    });

    return { isDragging, hasDragged };
}
