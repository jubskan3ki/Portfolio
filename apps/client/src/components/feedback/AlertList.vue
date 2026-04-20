<template>
    <Teleport to="body">
        <div :class="alertListClasses">
            <TransitionGroup name="alert-slide">
                <AlertItem v-for="alert in displayedAlerts" :key="alert.id" :alert="alert" @close="removeAlert" />
            </TransitionGroup>
        </div>
    </Teleport>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import { useAlertStore } from '@/stores/alert';

    import AlertItem from './AlertItem.vue';

    import type { AlertListProps } from '@/types/components/feedback';

    const props = withDefaults(defineProps<AlertListProps>(), {
        position: 'top-right',
        maxAlerts: 5,
    });

    const alertStore = useAlertStore();

    const displayedAlerts = computed(() => alertStore.alerts.slice(0, props.maxAlerts));

    const alertListClasses = computed(() => ['alert-list', `alert-list--${props.position}`]);

    const removeAlert = (id: string) => {
        alertStore.remove(id);
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;

    .alert-list {
        position: fixed;
        z-index: vars.$z-index-toast;
        padding: vars.$spacing-md;
        display: flex;
        flex-direction: column;
        gap: vars.$spacing-xs;
        pointer-events: none;
        max-width: 100%;
        max-height: 100vh;
        overflow: hidden;

        > * {
            pointer-events: auto;
        }

        &--top-right {
            top: 0;
            right: 0;
            align-items: flex-end;
        }

        &--top-left {
            top: 0;
            left: 0;
            align-items: flex-start;
        }

        &--top-center {
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            align-items: center;
        }

        &--bottom-right {
            bottom: 0;
            right: 0;
            align-items: flex-end;
            flex-direction: column-reverse;
        }

        &--bottom-left {
            bottom: 0;
            left: 0;
            align-items: flex-start;
            flex-direction: column-reverse;
        }

        &--bottom-center {
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            align-items: center;
            flex-direction: column-reverse;
        }
    }

    .alert-slide-enter-active {
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
    }

    .alert-slide-leave-active {
        transition: all 0.3s cubic-bezier(0.55, 0, 0.1, 1);
        position: absolute;
    }

    .alert-slide-enter-from {
        opacity: 0;
        transform: translateX(100px) scale(0.9);
    }

    .alert-slide-leave-to {
        opacity: 0;
        transform: translateX(100px) scale(0.9);
    }

    .alert-slide-move {
        transition: transform 0.3s ease;
    }
</style>
