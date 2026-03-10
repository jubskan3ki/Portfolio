<template>
    <article ref="cardRef" class="exp-card" :class="{ 'exp-card--current': isCurrent }">
        <header class="exp-card__header">
            <!-- Logo -->
            <figure class="exp-card__logo">
                <BaseImage
                    v-if="logo"
                    :src="resolvedLogo"
                    :alt="`Logo ${company}`"
                    :width="48"
                    :height="48"
                    object-fit="contain"
                    :show-placeholder="false"
                    class="exp-card__logo-img"
                />
                <BaseIcon v-else name="building-2" :size="22" />
            </figure>

            <!-- Info -->
            <div class="exp-card__info">
                <h4 class="exp-card__title">{{ title }}</h4>
                <p class="exp-card__company">
                    <span>{{ company }}</span>
                    <span v-if="location" class="exp-card__location">
                        <BaseIcon name="map-pin" :size="12" />
                        {{ location }}
                    </span>
                </p>
            </div>

            <!-- Date Badge -->
            <time class="exp-card__date" :class="{ 'exp-card__date--current': isCurrent }" :datetime="startDate">
                <span v-if="isCurrent" class="exp-card__pulse"></span>
                <span class="exp-card__date-text">{{ formattedPeriod }}</span>
            </time>
        </header>

        <!-- Description -->
        <p v-if="description" class="exp-card__desc">{{ truncatedDescription }}</p>

        <!-- Skills -->
        <ul v-if="displayedSkills.length" class="exp-card__skills">
            <li v-for="skill in displayedSkills" :key="skill" class="exp-card__skill">
                {{ skill }}
            </li>
            <li v-if="hiddenSkillsCount > 0" class="exp-card__skill exp-card__skill--more">+{{ hiddenSkillsCount }}</li>
        </ul>

        <!-- Achievements -->
        <ul v-if="displayedAchievements.length" class="exp-card__achievements">
            <li v-for="(item, i) in displayedAchievements" :key="i">
                <BaseIcon name="check-circle" :size="14" />
                <span>{{ item }}</span>
            </li>
        </ul>

        <!-- Footer slot -->
        <footer v-if="$slots.footer" class="exp-card__footer">
            <slot name="footer"></slot>
        </footer>
    </article>
</template>

<script setup lang="ts">
    import { computed, ref } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import { useTiltCSS } from '@/composables/ui/useTilt';
    import { resolveMediaUrl } from '@/services/utils/helpers';

    import type { ExperienceCardProps } from '@/types/feature/experience';

    const props = withDefaults(defineProps<ExperienceCardProps>(), {
        logo: '',
        location: '',
        endDate: '',
        period: '',
        description: '',
        skills: () => [],
        achievements: () => [],
        dateFormat: 'MMM yyyy',
        currentText: 'Présent',
    });

    // Constants
    const MAX_SKILLS = 5;
    const MAX_ACHIEVEMENTS = 3;
    const MAX_DESC_LENGTH = 150;

    // Refs
    const cardRef = ref<HTMLElement | null>(null);

    // Tilt effect - subtle et fluide
    useTiltCSS(cardRef, {
        maxRotation: 3,
        scale: 1,
        smoothing: 0.06,
    });

    const resolvedLogo = computed(() => resolveMediaUrl(props.logo));

    // Is current position
    const isCurrent = computed(() => !props.endDate);

    // Format date
    const formatDate = (date: string): string => {
        if (!date) {
            return '';
        }
        const d = new Date(date);
        return d.toLocaleDateString('fr-FR', { month: 'short', year: 'numeric' });
    };

    // Formatted period
    const formattedPeriod = computed(() => {
        if (props.period) {
            return props.period;
        }
        const start = formatDate(props.startDate);
        const end = props.endDate ? formatDate(props.endDate) : props.currentText;
        return `${start} — ${end}`;
    });

    // Truncated description
    const truncatedDescription = computed(() => {
        if (!props.description) {
            return '';
        }
        if (props.description.length <= MAX_DESC_LENGTH) {
            return props.description;
        }
        return `${props.description.slice(0, MAX_DESC_LENGTH).trim()}...`;
    });

    // Skills list
    const skillsList = computed((): string[] => {
        if (Array.isArray(props.skills)) {
            return props.skills.map(String);
        }
        if (typeof props.skills === 'string' && props.skills.trim()) {
            return props.skills.split(',').map((s) => s.trim());
        }
        return [];
    });

    // Displayed skills
    const displayedSkills = computed(() => skillsList.value.slice(0, MAX_SKILLS));

    // Hidden skills count
    const hiddenSkillsCount = computed(() => Math.max(0, skillsList.value.length - MAX_SKILLS));

    // Achievements list
    const achievementsList = computed((): string[] => {
        if (Array.isArray(props.achievements)) {
            return props.achievements.map(String);
        }
        if (typeof props.achievements === 'string' && props.achievements.trim()) {
            return props.achievements
                .split('\n')
                .map((s) => s.trim())
                .filter(Boolean);
        }
        return [];
    });

    // Displayed achievements
    const displayedAchievements = computed(() => achievementsList.value.slice(0, MAX_ACHIEVEMENTS));
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;

    .exp-card {
        position: relative;
        padding: vars.$spacing-lg;
        background: vars.$white;
        border: 1px solid fn.color-alpha(vars.$border-color, 0.5);
        border-radius: vars.$border-radius-lg;
        transition:
            border-color 0.25s ease,
            box-shadow 0.25s ease;

        &:hover {
            border-color: fn.color-alpha(vars.$primary-color, 0.3);
            box-shadow: 0 8px 24px fn.color-alpha(vars.$black, 0.08);
        }

        &--current {
            .exp-card__date {
                background: fn.color-alpha(vars.$primary-color, 0.1);
                color: vars.$primary-color;
            }
        }

        // Header
        &__header {
            display: grid;
            grid-template-columns: auto 1fr auto;
            gap: vars.$spacing-md;
            align-items: start;
            margin-bottom: vars.$spacing-md;

            @include mix.responsive(mobile) {
                grid-template-columns: auto 1fr;
                gap: vars.$spacing-sm;
            }
        }

        // Logo
        &__logo {
            @include mix.flex-center;
            width: 48px;
            height: 48px;
            margin: 0;
            background: vars.$bg-secondary;
            border: 1px solid fn.color-alpha(vars.$border-color, 0.3);
            border-radius: vars.$border-radius-md;
            color: vars.$gray;
            overflow: hidden;
            flex-shrink: 0;
        }

        &__logo-img {
            width: 100%;
            height: 100%;
            object-fit: contain;
            padding: vars.$spacing-xxs;
        }

        // Info
        &__info {
            min-width: 0;
        }

        &__title {
            margin: 0 0 vars.$spacing-xxs;
            font-weight: vars.$font-weight-semibold;
            color: vars.$text-primary;
            line-height: 1.3;
        }

        &__company {
            @include mix.flex(row, flex-start, center, vars.$spacing-sm);
            flex-wrap: wrap;
            margin: 0;
            color: vars.$text-secondary;
        }

        &__location {
            @include mix.flex(row, flex-start, center, vars.$spacing-xxxs);
            color: vars.$text-muted;

            :deep(svg) {
                opacity: 0.6;
            }
        }

        // Date
        &__date {
            @include mix.flex(row, center, center, vars.$spacing-xxs);
            padding: vars.$spacing-xxs vars.$spacing-sm;
            background: vars.$bg-secondary;
            border-radius: vars.$border-radius-sm;
            font-weight: vars.$font-weight-medium;
            color: vars.$text-secondary;
            white-space: nowrap;

            @include mix.responsive(mobile) {
                grid-column: 1 / -1;
                justify-self: start;
                margin-top: vars.$spacing-xs;
            }
        }

        &__pulse {
            width: 6px;
            height: 6px;
            background: vars.$success-color;
            border-radius: 50%;
            animation: pulse 2s ease-in-out infinite;
        }

        &__date-text {
            line-height: 1;
        }

        // Description
        &__desc {
            margin: 0 0 vars.$spacing-md;
            color: vars.$text-secondary;
            line-height: 1.6;
        }

        // Skills
        &__skills {
            display: flex;
            flex-wrap: wrap;
            gap: vars.$spacing-xxs;
            margin: 0 0 vars.$spacing-md;
            padding: 0;
            list-style: none;
        }

        &__skill {
            padding: 2px vars.$spacing-xs;
            background: fn.color-alpha(vars.$primary-color, 0.08);
            border-radius: vars.$border-radius-sm;
            font-weight: vars.$font-weight-medium;
            color: vars.$primary-color;

            &--more {
                background: vars.$bg-secondary;
                color: vars.$text-muted;
            }
        }

        // Achievements
        &__achievements {
            margin: 0;
            padding: 0;
            list-style: none;

            li {
                @include mix.flex(row, flex-start, flex-start, vars.$spacing-xs);
                padding: vars.$spacing-xxs 0;
                color: vars.$text-secondary;

                :deep(svg) {
                    flex-shrink: 0;
                    margin-top: 2px;
                    color: vars.$success-color;
                }

                &:last-child {
                    padding-bottom: 0;
                }
            }
        }

        // Footer
        &__footer {
            margin-top: vars.$spacing-md;
            padding-top: vars.$spacing-md;
            border-top: 1px solid fn.color-alpha(vars.$border-color, 0.3);
        }
    }

    // Pulse animation
    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
            transform: scale(1);
        }

        50% {
            opacity: 0.5;
            transform: scale(1.2);
        }
    }

    // Reduced motion
    @media (prefers-reduced-motion: reduce) {
        .exp-card {
            transition: none;

            &__pulse {
                animation: none;
            }
        }
    }
</style>
