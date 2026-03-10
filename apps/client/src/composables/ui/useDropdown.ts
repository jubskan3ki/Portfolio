import { ref, computed, nextTick, type Ref } from 'vue';

import { useClickOutside } from './useClickOutside';

import type { UseDropdownOptions, UseDropdownReturn } from '@/types/composables/ui';

export function useDropdown(
    containerRef: Ref<HTMLElement | null>,
    options: UseDropdownOptions = {},
): UseDropdownReturn {
    const { onOpen, onClose, closeOnSelect = true, disabled = false } = options;

    const isOpen = ref(false);
    const highlightedIndex = ref(0);

    const isDisabled = computed(() => (typeof disabled === 'boolean' ? disabled : disabled.value));

    const open = () => {
        if (isDisabled.value) {
            return;
        }
        if (isOpen.value) {
            return;
        }

        isOpen.value = true;
        onOpen?.();
    };

    const close = () => {
        if (!isOpen.value) {
            return;
        }

        isOpen.value = false;
        highlightedIndex.value = 0;
        onClose?.();
    };

    const toggle = () => {
        if (isDisabled.value) {
            return;
        }
        isOpen.value ? close() : open();
    };

    const navigate = (direction: 1 | -1, optionsLength: number) => {
        if (!isOpen.value || optionsLength === 0) {
            return;
        }

        const newIndex = highlightedIndex.value + direction;

        if (newIndex >= 0 && newIndex < optionsLength) {
            highlightedIndex.value = newIndex;
        } else if (direction === 1 && newIndex >= optionsLength) {
            highlightedIndex.value = 0;
        } else if (direction === -1 && newIndex < 0) {
            highlightedIndex.value = optionsLength - 1;
        }
    };

    const setHighlighted = (index: number) => {
        highlightedIndex.value = index;
    };

    const resetHighlighted = () => {
        highlightedIndex.value = 0;
    };

    const handleKeydown = (event: KeyboardEvent, optionsLength: number, onSelect?: () => void) => {
        const actions: Record<string, () => void> = {
            ArrowDown: () => {
                event.preventDefault();
                if (!isOpen.value) {
                    open();
                } else {
                    navigate(1, optionsLength);
                }
            },
            ArrowUp: () => {
                event.preventDefault();
                if (isOpen.value) {
                    navigate(-1, optionsLength);
                }
            },
            Enter: () => {
                event.preventDefault();
                if (isOpen.value && onSelect) {
                    onSelect();
                    if (closeOnSelect) {
                        close();
                    }
                } else if (!isOpen.value) {
                    open();
                }
            },
            Escape: () => {
                event.preventDefault();
                close();
            },
            Tab: () => {
                close();
            },
        };

        actions[event.key]?.();
    };

    const scrollToHighlighted = (optionsRef: Ref<HTMLElement | null>, optionClass: string) => {
        nextTick(() => {
            const container = optionsRef.value;
            if (!container) {
                return;
            }

            const highlighted = container.querySelector(`.${optionClass}--highlighted`);
            highlighted?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
        });
    };

    const getActiveDescendant = (baseId: string): string | undefined => {
        if (!isOpen.value || highlightedIndex.value < 0) {
            return undefined;
        }
        return `${baseId}-option-${highlightedIndex.value}`;
    };

    useClickOutside(containerRef, () => close(), { enabled: isOpen });

    return {
        isOpen,
        highlightedIndex,
        open,
        close,
        toggle,
        navigate,
        setHighlighted,
        resetHighlighted,
        handleKeydown,
        scrollToHighlighted,
        getActiveDescendant,
    };
}
