<template>
    <article ref="cardRef" class="exp-card" :class="{ 'exp-card--current': isCurrent }">
        <header class="exp-card__header">
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

            <time class="exp-card__date" :class="{ 'exp-card__date--current': isCurrent }" :datetime="startDate">
                <span v-if="isCurrent" class="exp-card__pulse"></span>
                <span class="exp-card__date-text">{{ formattedPeriod }}</span>
            </time>
        </header>

        <div v-if="descriptionParagraphs.length" class="exp-card__desc">
            <SafeHtml v-for="(para, i) in descriptionParagraphs" :key="i" tag="p" :html="para" />
        </div>

        <ul v-if="displayedSkills.length" class="exp-card__skills">
            <li v-for="skill in displayedSkills" :key="skill" class="exp-card__skill">
                {{ skill }}
            </li>
            <li v-if="hiddenSkillsCount > 0" class="exp-card__skill exp-card__skill--more">+{{ hiddenSkillsCount }}</li>
        </ul>

        <ul v-if="displayedAchievements.length" class="exp-card__achievements">
            <li v-for="(item, i) in displayedAchievements" :key="i">
                <BaseIcon name="check-circle" :size="14" />
                <span>{{ item }}</span>
            </li>
        </ul>

        <footer v-if="$slots.footer" class="exp-card__footer">
            <slot name="footer"></slot>
        </footer>
    </article>
</template>

<script setup lang="ts">
    import { computed, ref } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import SafeHtml from '@/components/base/SafeHtml.vue';
    import { useTiltCSS } from '@/composables/ui/useTilt';
    import { renderInlineMarkdown } from '@/services/utils/contentParser';
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

    const MAX_SKILLS = 5;
    const MAX_ACHIEVEMENTS = 3;

    const cardRef = ref<HTMLElement | null>(null);

    useTiltCSS(cardRef, {
        maxRotation: 3,
        scale: 1,
        smoothing: 0.06,
    });

    const resolvedLogo = computed(() => resolveMediaUrl(props.logo));

    const isCurrent = computed(() => !props.endDate);

    const formatDate = (date: string): string => {
        if (!date) {
            return '';
        }
        const d = new Date(date);
        return d.toLocaleDateString('fr-FR', { month: 'short', year: 'numeric' });
    };

    const formattedPeriod = computed(() => {
        if (props.period) {
            return props.period;
        }
        const start = formatDate(props.startDate);
        const end = props.endDate ? formatDate(props.endDate) : props.currentText;
        return `${start} — ${end}`;
    });

    // Blank lines split paragraphs; single newlines become <br>. Inline markdown rendered per paragraph.
    const descriptionParagraphs = computed(() => {
        if (!props.description) {
            return [];
        }
        return props.description
            .split(/\n\s*\n/)
            .map((p) => p.trim())
            .filter(Boolean)
            .map((p) => renderInlineMarkdown(p).replace(/\n/g, '<br>'));
    });

    const skillsList = computed((): string[] => {
        if (Array.isArray(props.skills)) {
            return props.skills.map(String);
        }
        if (typeof props.skills === 'string' && props.skills.trim()) {
            return props.skills.split(',').map((s) => s.trim());
        }
        return [];
    });

    const displayedSkills = computed(() => skillsList.value.slice(0, MAX_SKILLS));

    const hiddenSkillsCount = computed(() => Math.max(0, skillsList.value.length - MAX_SKILLS));

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

    const displayedAchievements = computed(() => achievementsList.value.slice(0, MAX_ACHIEVEMENTS));
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;

    .exp-card {
        position: relative;
        display: flex;
        flex-direction: column;
        align-self: flex-start;
        height: auto;
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

        &__desc {
            display: flex;
            flex-direction: column;
            gap: vars.$spacing-xs;
            margin: 0 0 vars.$spacing-md;
            color: vars.$text-secondary;
            line-height: 1.6;
            overflow-wrap: break-word;

            p {
                margin: 0;
            }

            :deep(strong) {
                font-weight: vars.$font-weight-semibold;
                color: vars.$text-primary;
            }

            :deep(em) {
                font-style: italic;
            }

            :deep(code) {
                padding: 2px 6px;
                font-size: 0.88em;
                font-family: vars.$font-family-mono;
                color: vars.$primary-color;
                background: fn.color-alpha(vars.$primary-color, 0.08);
                border-radius: vars.$border-radius-sm;
            }

            :deep(a) {
                color: vars.$primary-color;
                text-decoration: underline;
                text-underline-offset: 2px;
                transition: color 0.2s ease;

                &:hover {
                    color: vars.$primary-dark;
                }
            }
        }

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

        &__footer {
            margin-top: vars.$spacing-md;
            padding-top: vars.$spacing-md;
            border-top: 1px solid fn.color-alpha(vars.$border-color, 0.3);
        }
    }

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

    @media (prefers-reduced-motion: reduce) {
        .exp-card {
            transition: none;

            &__pulse {
                animation: none;
            }
        }
    }
</style>
