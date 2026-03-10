<template>
    <div class="timeline" :class="[customClass]">
        <!-- Header -->
        <header v-if="showHeader && (title || subtitle)" class="timeline__header">
            <h2 v-if="title" class="timeline__title">{{ title }}</h2>
            <p v-if="subtitle" class="timeline__subtitle">{{ subtitle }}</p>
        </header>

        <!-- Filters -->
        <nav v-if="showFilters && filters.length" class="timeline__filters" role="tablist">
            <button
                class="timeline__filter"
                :class="{ 'timeline__filter--active': activeFilter === 'all' }"
                @click="handleFilter('all')"
            >
                {{ allFilterLabel }}
            </button>
            <button
                v-for="filter in filters"
                :key="filter.value"
                class="timeline__filter"
                :class="{ 'timeline__filter--active': activeFilter === filter.value }"
                @click="handleFilter(filter.value)"
            >
                {{ filter.label }}
            </button>
        </nav>

        <!-- List -->
        <TransitionGroup v-if="sortedExperiences.length" name="timeline-item" tag="div" class="timeline__list">
            <div
                v-for="(exp, idx) in sortedExperiences"
                :key="exp.id ?? idx"
                class="timeline__item"
                :style="{ '--item-index': idx }"
            >
                <div class="timeline__marker">
                    <span class="timeline__dot" :class="{ 'timeline__dot--current': !exp.endDate }">
                        <span v-if="!exp.endDate" class="timeline__dot-pulse"></span>
                    </span>
                    <span v-if="idx < sortedExperiences.length - 1" class="timeline__line"></span>
                </div>
                <div class="timeline__content">
                    <slot name="experience-item" :experience="exp" :index="idx">
                        <ExperienceCard
                            :title="exp.title"
                            :company="exp.company"
                            :logo="exp.logo"
                            :location="exp.location"
                            :start-date="exp.startDate"
                            :end-date="exp.endDate"
                            :description="exp.description"
                            :skills="exp.technologies?.length ? exp.technologies : exp.skills"
                            :achievements="exp.achievements"
                            :date-format="dateFormat"
                            :current-text="currentText"
                        />
                    </slot>
                </div>
            </div>
        </TransitionGroup>

        <!-- Empty -->
        <EmptyState v-else-if="!loading" :title="emptyTitle" :description="emptyDescription" icon="inbox" />

        <!-- Loading -->
        <div v-if="loading" class="timeline__loading">
            <Spinner size="lg" :label="loadingText" />
        </div>

        <!-- Footer -->
        <footer v-if="$slots.footer" class="timeline__footer">
            <slot name="footer"></slot>
        </footer>
    </div>
</template>

<script setup lang="ts">
    import { computed, ref } from 'vue';

    import ExperienceCard from '@/components/feature/experience/ExperienceCard.vue';
    import EmptyState from '@/components/feedback/EmptyState.vue';
    import Spinner from '@/components/loaders/Spinner.vue';

    import type { Experience, ExperienceTimelineProps } from '@/types/feature/experience';

    const props = withDefaults(defineProps<ExperienceTimelineProps>(), {
        experiences: () => [],
        limit: undefined,
        title: '',
        subtitle: '',
        showHeader: true,
        showFilters: false,
        filters: () => [],
        filterLabel: 'Filtrer',
        allFilterLabel: 'Tout',
        defaultFilter: 'all',
        dateFormat: 'MMM yyyy',
        currentText: 'Présent',
        emptyTitle: 'Aucune expérience',
        emptyDescription: 'Aucune expérience trouvée.',
        loading: false,
        loadingText: 'Chargement...',
        customClass: '',
    });

    const emit = defineEmits<{
        filterChange: [filter: string];
    }>();

    const activeFilter = ref(props.defaultFilter);

    const handleFilter = (value: string) => {
        activeFilter.value = value;
        emit('filterChange', value);
    };

    const sortedExperiences = computed(() => {
        let list: Experience[] = Array.isArray(props.experiences) ? [...props.experiences] : [];

        if (activeFilter.value !== 'all') {
            list = list.filter((e) => e.type === activeFilter.value);
        }

        list.sort((a, b) => new Date(b.startDate).getTime() - new Date(a.startDate).getTime());

        if (props.limit && props.limit > 0) {
            list = list.slice(0, props.limit);
        }

        return list;
    });

    defineExpose({ handleFilter });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;

    .timeline {
        width: 100%;

        &__header {
            text-align: center;
            margin-bottom: vars.$spacing-xl;
        }

        &__title {
            font-weight: vars.$font-weight-bold;
            color: vars.$text-primary;
            margin: 0 0 vars.$spacing-xxs;
        }

        &__subtitle {
            color: vars.$text-secondary;
            max-width: 480px;
            margin: 0 auto;
        }

        &__filters {
            @include mix.flex(row, center, center, vars.$spacing-xxs);
            flex-wrap: wrap;
            margin-bottom: vars.$spacing-xl;
        }

        &__filter {
            padding: vars.$spacing-xxs vars.$spacing-sm;
            font-weight: vars.$font-weight-medium;
            color: vars.$text-secondary;
            background: fn.color-alpha(vars.$white, 0.9);
            backdrop-filter: blur(8px);
            border: 1px solid fn.color-alpha(vars.$border-color, 0.5);
            border-radius: vars.$border-radius-full;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

            &:hover:not(&--active) {
                color: vars.$primary-color;
                border-color: fn.color-alpha(vars.$primary-color, 0.3);
                background: fn.color-alpha(vars.$primary-color, 0.05);
            }

            &--active {
                color: vars.$white;
                background: linear-gradient(135deg, vars.$primary-color, vars.$primary-dark);
                border-color: vars.$primary-color;
                box-shadow: 0 4px 12px fn.color-alpha(vars.$primary-color, 0.3);
            }
        }

        &__list {
            position: relative;
            padding-left: vars.$spacing-xl;

            @include mix.responsive(mobile) {
                padding-left: vars.$spacing-lg;
            }
        }

        &__item {
            position: relative;
            padding-bottom: vars.$spacing-xl;
            animation: timeline-fade-in 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
            animation-delay: calc(var(--item-index, 0) * 0.1s);
            opacity: 0;

            &:last-child {
                padding-bottom: 0;
            }
        }

        &__marker {
            position: absolute;
            left: calc(-1 * vars.$spacing-xl);
            top: 0;
            height: 100%;
            @include mix.flex(column, flex-start, center);

            @include mix.responsive(mobile) {
                left: calc(-1 * vars.$spacing-lg);
            }
        }

        &__dot {
            position: relative;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: vars.$bg-secondary;
            z-index: 2;
            flex-shrink: 0;
            transition: all 0.3s ease;

            &::before {
                content: '';
                position: absolute;
                inset: 3px;
                background: vars.$gray-light;
                border-radius: 50%;
                transition: all 0.3s ease;
            }

            &--current {
                background: fn.color-alpha(vars.$primary-color, 0.15);

                &::before {
                    background: vars.$primary-color;
                }
            }
        }

        &__dot-pulse {
            position: absolute;
            inset: -6px;
            border-radius: 50%;
            border: 2px solid vars.$primary-color;
            opacity: 0;
            animation: marker-pulse 2s ease-out infinite;
        }

        &__line {
            width: 2px;
            flex: 1;
            margin-top: vars.$spacing-xs;
            background: linear-gradient(180deg, vars.$border-color 0%, fn.color-alpha(vars.$border-color, 0.3) 100%);
            border-radius: 1px;
        }

        &__content {
            width: 100%;
        }

        &__loading {
            @include mix.flex-center;
            padding: vars.$spacing-xxl 0;
        }

        &__footer {
            margin-top: vars.$spacing-xl;
            text-align: center;
        }
    }

    /* Item animations */
    @keyframes timeline-fade-in {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }

        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    /* Marker pulse */
    @keyframes marker-pulse {
        0% {
            transform: scale(1);
            opacity: 0.8;
        }

        100% {
            transform: scale(2);
            opacity: 0;
        }
    }

    /* TransitionGroup animations */
    .timeline-item-enter-active {
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .timeline-item-leave-active {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .timeline-item-enter-from {
        opacity: 0;
        transform: translateX(-20px);
    }

    .timeline-item-leave-to {
        opacity: 0;
        transform: translateX(20px);
    }

    .timeline-item-move {
        transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Reduced motion */
    @media (prefers-reduced-motion: reduce) {
        .timeline__item {
            animation: none;
            opacity: 1;
        }

        .timeline__dot-pulse {
            animation: none;
        }
    }
</style>
