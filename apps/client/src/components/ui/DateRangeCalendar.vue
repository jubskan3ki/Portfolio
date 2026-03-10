<template>
    <div class="date-range-calendar">
        <!-- Calendar Header -->
        <div class="calendar-header">
            <button type="button" class="calendar-header__nav" @click="$emit('previousMonth')">
                <BaseIcon name="chevron-left" :size="16" />
            </button>
            <div class="calendar-header__title">{{ currentMonthYear }}</div>
            <button type="button" class="calendar-header__nav" @click="$emit('nextMonth')">
                <BaseIcon name="chevron-right" :size="16" />
            </button>
        </div>

        <!-- Weekday labels -->
        <div class="calendar-weekdays">
            <div v-for="day in weekDays" :key="day" class="calendar-weekdays__item">{{ day }}</div>
        </div>

        <!-- Calendar grid -->
        <div class="calendar-grid">
            <button
                v-for="day in calendarDays"
                :key="`${day.date}-${day.isCurrentMonth}`"
                type="button"
                class="calendar-day"
                :class="{
                    'calendar-day--other-month': !day.isCurrentMonth,
                    'calendar-day--disabled': !day.isAvailable || day.isDisabled,
                    'calendar-day--selected': day.isSelected,
                    'calendar-day--in-range': day.isInRange,
                    'calendar-day--range-start': day.isRangeStart,
                    'calendar-day--range-end': day.isRangeEnd,
                    'calendar-day--today': day.isToday,
                }"
                :disabled="!day.isCurrentMonth || !day.isAvailable || day.isDisabled"
                @click="$emit('selectDate', day.date)"
                @mouseenter="$emit('mouseEnterDate', day.date)"
            >
                {{ day.day }}
            </button>
        </div>

        <!-- Action buttons -->
        <div class="calendar-actions">
            <button
                type="button"
                class="calendar-actions__btn calendar-actions__btn--secondary"
                @click="$emit('cancel')"
            >
                Annuler
            </button>
            <button
                type="button"
                class="calendar-actions__btn calendar-actions__btn--primary"
                :disabled="!isValidSelection"
                @click="$emit('apply')"
            >
                Appliquer
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
    import BaseIcon from '@/components/base/BaseIcon.vue';

    import type { DateRangeCalendarProps } from '@/types/components/ui';

    defineProps<DateRangeCalendarProps>();

    defineEmits<{
        previousMonth: [];
        nextMonth: [];
        selectDate: [date: string];
        mouseEnterDate: [date: string];
        cancel: [];
        apply: [];
    }>();
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as func;
    @use '@/styles/abstracts/mixins' as mix;

    .calendar-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: vars.$spacing-md;
        padding-bottom: vars.$spacing-sm;
        border-bottom: 1px solid func.color-alpha(vars.$black, 0.06);

        @include mix.responsive(mobile) {
            margin-bottom: vars.$spacing-sm;
        }

        &__nav {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 32px;
            height: 32px;
            border: 1px solid func.color-alpha(vars.$black, 0.08);
            background: vars.$white;
            padding: vars.$spacing-xxs;
            border-radius: vars.$border-radius-sm;
            color: vars.$text-primary;
            cursor: pointer;
            transition:
                background-color vars.$transition-fast,
                border-color vars.$transition-fast,
                color vars.$transition-fast;

            &:hover {
                background-color: vars.$primary-color;
                border-color: vars.$primary-color;
                color: vars.$white;
            }
        }

        &__title {
            font-weight: vars.$font-weight-semibold;
            color: vars.$text-primary;
            text-transform: capitalize;
        }
    }

    .calendar-weekdays {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: vars.$spacing-xxxs;
        margin-bottom: vars.$spacing-xs;
        padding: vars.$spacing-xxs 0;
        background: func.color-alpha(vars.$black, 0.02);
        border-radius: vars.$border-radius-sm;

        &__item {
            text-align: center;
            font-weight: vars.$font-weight-bold;
            color: vars.$text-secondary;
        }
    }

    .calendar-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: vars.$spacing-xxxs;
        margin-bottom: vars.$spacing-md;

        @include mix.responsive(mobile) {
            margin-bottom: vars.$spacing-sm;
        }
    }

    .calendar-day {
        aspect-ratio: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid transparent;
        background: transparent;
        border-radius: vars.$border-radius-sm;
        font-weight: vars.$font-weight-medium;
        color: vars.$text-primary;
        cursor: pointer;
        transition:
            background-color vars.$transition-fast,
            color vars.$transition-fast,
            border-color vars.$transition-fast;
        position: relative;
        padding: vars.$spacing-xxxs vars.$spacing-xxs;

        &:hover:not(&--disabled) {
            background-color: func.color-alpha(vars.$primary-color, 0.1);
            border-color: vars.$primary-color;
            color: vars.$primary-color;
        }

        &--other-month {
            color: vars.$text-muted;
            opacity: 0.2;
        }

        &--disabled {
            color: vars.$text-muted;
            opacity: 0.4;
            cursor: not-allowed;
            text-decoration: line-through;
            background: func.color-alpha(vars.$black, 0.02);

            &:hover {
                background: func.color-alpha(vars.$black, 0.02);
                border-color: transparent;
            }
        }

        &--today {
            font-weight: vars.$font-weight-bold;
            border-color: vars.$primary-color;

            &::after {
                content: '';
                position: absolute;
                bottom: vars.$spacing-xxxs;
                left: 50%;
                transform: translateX(-50%);
                width: vars.$spacing-xxxs;
                height: vars.$spacing-xxxs;
                border-radius: 50%;
                background: vars.$primary-color;
            }
        }

        &--selected {
            background: vars.$primary-color;
            border-color: vars.$primary-color;
            color: vars.$white;
            font-weight: vars.$font-weight-semibold;

            &:hover {
                background: vars.$primary-dark;
                border-color: vars.$primary-dark;
                color: vars.$white;
            }
        }

        &--in-range {
            background: func.color-alpha(vars.$primary-color, 0.12);
            border-color: func.color-alpha(vars.$primary-color, 0.2);
            color: vars.$primary-color;
        }

        &--range-start,
        &--range-end {
            background: vars.$primary-color;
            border-color: vars.$primary-color;
            color: vars.$white;
            font-weight: vars.$font-weight-semibold;

            &:hover {
                background: vars.$primary-dark;
                border-color: vars.$primary-dark;
            }
        }
    }

    .calendar-actions {
        display: flex;
        gap: vars.$spacing-xs;
        padding-top: vars.$spacing-sm;
        border-top: 1px solid func.color-alpha(vars.$black, 0.06);

        &__btn {
            flex: 1;
            padding: vars.$spacing-xs vars.$spacing-sm;
            border: none;
            border-radius: vars.$border-radius-md;
            font-weight: vars.$font-weight-medium;
            cursor: pointer;
            transition:
                background-color vars.$transition-fast,
                opacity vars.$transition-fast;

            @include mix.responsive(mobile) {
                padding: vars.$spacing-xxs vars.$spacing-xs;
            }

            &--secondary {
                background: vars.$bg-secondary;
                color: vars.$text-primary;

                &:hover {
                    background: func.color-alpha(vars.$black, 0.1);
                }
            }

            &--primary {
                background: vars.$primary-color;
                color: vars.$white;

                &:hover:not(:disabled) {
                    background: vars.$primary-dark;
                }

                &:disabled {
                    opacity: 0.5;
                    cursor: not-allowed;
                }
            }
        }
    }
</style>
