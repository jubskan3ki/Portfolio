<template>
    <div ref="cardRef" class="stats-card" :class="{ 'stats-card--loading': loading }">
        <!-- Icon -->
        <div class="stats-card__icon" :style="{ backgroundColor: iconBgColor, color }">
            <BaseIcon :name="icon" :size="22" />
        </div>

        <!-- Content -->
        <div class="stats-card__content">
            <span class="stats-card__label">{{ label }}</span>
            <div class="stats-card__value-row">
                <span v-if="loading" class="stats-card__skeleton"></span>
                <span v-else class="stats-card__value">{{ value }}</span>
                <span v-if="trend && !loading" class="stats-card__trend" :class="trendClass">
                    <BaseIcon :name="trendIcon" :size="14" />
                    {{ trend }}
                </span>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { computed, ref } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import { useTiltCSS } from '@/composables/ui/useTilt';

    import type { StatsCardProps } from '@/types/components/admin';

    const props = withDefaults(defineProps<StatsCardProps>(), {
        color: '#3b82f6',
    });

    // Parallax tilt effect (manipulates DOM directly)
    const cardRef = ref<HTMLElement | null>(null);
    useTiltCSS(cardRef, {
        maxRotation: 8,
        perspective: 800,
        scale: 1.02,
    });

    const iconBgColor = computed(() => `${props.color}15`);

    const trendClass = computed(() => {
        if (!props.trend) {
            return '';
        }
        if (props.trend.startsWith('+') && props.trend !== '+0%') {
            return 'stats-card__trend--up';
        }
        if (props.trend.startsWith('-')) {
            return 'stats-card__trend--down';
        }
        return '';
    });

    const trendIcon = computed(() => {
        if (!props.trend) {
            return 'minus';
        }
        if (props.trend.startsWith('+') && props.trend !== '+0%') {
            return 'trending-up';
        }
        if (props.trend.startsWith('-')) {
            return 'trending-down';
        }
        return 'minus';
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as func;

    .stats-card {
        background: vars.$white;
        border: 1px solid func.color-alpha(vars.$black, 0.06);
        border-radius: vars.$border-radius-xl;
        padding: vars.$spacing-lg;
        display: flex;
        align-items: flex-start;
        gap: vars.$spacing-md;
        transition: all 0.2s ease;

        &:hover {
            border-color: func.color-alpha(vars.$black, 0.1);
            box-shadow: 0 4px 12px func.color-alpha(vars.$black, 0.06);
        }

        &__icon {
            width: 48px;
            height: 48px;
            border-radius: vars.$border-radius-lg;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }

        &__content {
            flex: 1;
            min-width: 0;
        }

        &__label {
            display: block;
            color: vars.$text-secondary;
            margin-bottom: vars.$spacing-xxs;
            font-weight: vars.$font-weight-medium;
        }

        &__value-row {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;
            flex-wrap: wrap;
        }

        &__value {
            font-weight: vars.$font-weight-bold;
            color: vars.$text-primary;
            line-height: 1;
        }

        &__trend {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 4px 8px;
            border-radius: vars.$border-radius-full;
            font-weight: vars.$font-weight-medium;
            background: vars.$bg-secondary;
            color: vars.$text-secondary;

            &--up {
                background: func.color-alpha(#10b981, 0.1);
                color: #059669;
            }

            &--down {
                background: func.color-alpha(#ef4444, 0.1);
                color: #dc2626;
            }
        }

        &__skeleton {
            display: block;
            width: 60px;
            height: 32px;
            background: vars.$bg-secondary;
            animation: pulse 1.5s infinite;
            border-radius: vars.$border-radius-sm;
        }

        &--loading {
            pointer-events: none;
        }
    }

    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
        }

        50% {
            opacity: 0.5;
        }
    }
</style>
