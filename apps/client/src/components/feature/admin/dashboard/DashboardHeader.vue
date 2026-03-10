<template>
    <header class="dashboard-header">
        <div class="dashboard-header__content">
            <div class="dashboard-header__greeting">
                <span class="dashboard-header__icon">
                    <BaseIcon :name="greetingIcon" :size="24" />
                </span>
                <div>
                    <h4 class="dashboard-header__title">{{ greetingText }}</h4>
                    <p class="dashboard-header__subtitle">{{ userName }}</p>
                </div>
            </div>
            <small class="dashboard-header__date">{{ formattedDate }}</small>
        </div>
        <div class="dashboard-header__actions">
            <button class="dashboard-header__btn" :disabled="isRefreshing" @click="$emit('refresh')">
                <BaseIcon name="refresh-cw" :size="16" :class="{ 'dashboard-header__spinning': isRefreshing }" />
                <span>Actualiser</span>
            </button>
        </div>
    </header>
</template>

<script setup lang="ts">
    import { ref, computed, onMounted } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';

    interface Props {
        userName?: string;
        isRefreshing?: boolean;
    }

    withDefaults(defineProps<Props>(), {
        userName: 'Admin',
        isRefreshing: false,
    });

    defineEmits<{
        refresh: [];
    }>();

    // Greeting based on time of day
    const getInitialHour = () => {
        if (import.meta.server) {
            return 12;
        }
        return new Date().getHours();
    };

    const currentHour = ref(getInitialHour());

    const greetingText = computed(() => {
        if (currentHour.value < 12) {
            return 'Bonjour';
        }
        if (currentHour.value < 18) {
            return 'Bon après-midi';
        }
        return 'Bonsoir';
    });

    const greetingIcon = computed(() => {
        if (currentHour.value < 12) {
            return 'sunrise';
        }
        if (currentHour.value < 18) {
            return 'sun';
        }
        return 'moon';
    });

    const formattedDate = computed(() => {
        if (import.meta.server) {
            return '';
        }
        return new Date().toLocaleDateString('fr-FR', {
            weekday: 'long',
            day: 'numeric',
            month: 'long',
            year: 'numeric',
        });
    });

    onMounted(() => {
        currentHour.value = new Date().getHours();
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .dashboard-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: vars.$spacing-xl;
        gap: vars.$spacing-lg;
        flex-wrap: wrap;

        &__content {
            flex: 1;
            min-width: 200px;
        }

        &__greeting {
            display: flex;
            align-items: center;
            gap: vars.$spacing-md;
        }

        &__icon {
            width: 48px;
            height: 48px;
            background: func.color-alpha(vars.$primary-color, 0.1);
            border-radius: vars.$border-radius-lg;
            display: flex;
            align-items: center;
            justify-content: center;
            color: vars.$primary-color;
            flex-shrink: 0;
        }

        &__title {
            font-weight: vars.$font-weight-bold;
            color: vars.$text-primary;
            margin: 0;
        }

        &__subtitle {
            color: vars.$text-secondary;
            margin: 0;
        }

        &__date {
            display: block;
            color: vars.$text-muted;
            margin-top: vars.$spacing-xs;
            text-transform: capitalize;
        }

        &__btn {
            display: inline-flex;
            align-items: center;
            gap: vars.$spacing-xs;
            padding: vars.$spacing-xs vars.$spacing-md;
            border-radius: vars.$border-radius-lg;
            font-weight: vars.$font-weight-medium;
            cursor: pointer;
            transition: all 0.15s;
            background: vars.$white;
            border: 1px solid func.color-alpha(vars.$black, 0.1);
            color: vars.$text-primary;

            &:hover:not(:disabled) {
                border-color: vars.$primary-color;
                color: vars.$primary-color;
            }

            &:disabled {
                opacity: 0.6;
                cursor: not-allowed;
            }
        }

        &__spinning {
            animation: spin 1s linear infinite;
        }
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }
</style>
