<template>
    <article
        class="stack-card"
        :class="[levelColorClass, { 'stack-card--flat': flat, 'stack-card--compact': compact }, customClass]"
        tabindex="0"
        role="button"
        :aria-label="`Voir ${stack.name}`"
        v-bind="prefetchHandlers"
        @click="$emit('click')"
        @keydown.enter="$emit('click')"
        @keydown.space.prevent="$emit('click')"
    >
        <div class="stack-card__accent" aria-hidden="true"></div>

        <header class="stack-card__header">
            <div class="stack-card__logo" :style="logoTransitionStyle">
                <BaseImage
                    v-if="stack.logo"
                    :src="stack.logo"
                    :alt="`Logo ${stack.name}`"
                    :width="40"
                    :height="40"
                    object-fit="contain"
                    :show-placeholder="false"
                    class="stack-card__logo-img"
                />
                <span v-else class="stack-card__logo-letter">{{ stack.name.charAt(0) }}</span>
            </div>

            <div class="stack-card__title-group">
                <h3 class="stack-card__name" :style="titleTransitionStyle">{{ stack.name }}</h3>
                <span v-if="stack.category" class="stack-card__category">{{ stack.category }}</span>
            </div>

            <div v-if="stack.level" class="stack-card__level-badge" :class="levelClass">
                {{ levelLabel }}
            </div>
        </header>

        <p v-if="stack.description && !compact" class="stack-card__description">
            {{ truncatedDescription }}
        </p>

        <div v-if="displayedTags.length > 0" class="stack-card__tags">
            <span v-for="tag in displayedTags" :key="tag" class="stack-card__tag">
                {{ tag }}
            </span>
            <span v-if="remainingTagsCount > 0" class="stack-card__tag stack-card__tag--more">
                +{{ remainingTagsCount }}
            </span>
        </div>

        <footer class="stack-card__footer">
            <span v-if="experienceDisplay" class="stack-card__experience">
                <BaseIcon name="clock" :size="12" />
                {{ experienceDisplay }}
            </span>
            <span class="stack-card__action">
                Voir détails
                <BaseIcon name="arrow-right" :size="14" class="stack-card__arrow" />
            </span>
        </footer>
    </article>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import { useCardPrefetch } from '@/composables/performance/usePrefetch';
    import { TEXT_LIMITS } from '@/config/constants';
    import { stackKeys, stacksApi } from '@/services/api/modules/stacks';
    import { sliceTags, truncateText } from '@/services/utils/helpers';

    import type { StackCardProps } from '@/types/feature/stacks';

    const props = withDefaults(defineProps<StackCardProps>(), {
        hoverable: true,
        flat: false,
        compact: false,
        descriptionLength: TEXT_LIMITS.STACK_DESCRIPTION,
        customClass: '',
    });

    defineEmits<{
        click: [];
    }>();

    const truncatedDescription = computed(() => truncateText(props.stack.description ?? '', props.descriptionLength));

    // Tags
    const tagInfo = computed(() => sliceTags(props.stack.tags, 3));
    const displayedTags = computed(() => tagInfo.value.displayed);
    const remainingTagsCount = computed(() => tagInfo.value.remaining);

    // Level configuration | single source of truth
    const LEVEL_CONFIG = [
        { min: 5, label: 'Expert', badge: 'stack-card__level-badge--expert', color: 'level-expert' },
        { min: 4, label: 'Avancé', badge: 'stack-card__level-badge--advanced', color: 'level-advanced' },
        { min: 3, label: 'Confirmé', badge: 'stack-card__level-badge--confirmed', color: 'level-confirmed' },
        { min: 2, label: 'Intermédiaire', badge: 'stack-card__level-badge--beginner', color: 'level-beginner' },
        { min: 0, label: 'Débutant', badge: 'stack-card__level-badge--beginner', color: 'level-beginner' },
    ] as const;

    const levelInfo = computed(() => {
        const level = Number(props.stack.level) || 0;
        return LEVEL_CONFIG.find((c) => level >= c.min) ?? LEVEL_CONFIG[4];
    });

    const levelLabel = computed(() => levelInfo.value.label);
    const levelClass = computed(() => levelInfo.value.badge);
    const levelColorClass = computed(() => levelInfo.value.color);

    // Experience display (experience is in months from API)
    const experienceDisplay = computed(() => {
        const months = Number(props.stack.experience) || 0;
        if (months === 0) {
            return '';
        }
        if (months < 12) {
            return `${months} mois`;
        }
        const years = Math.floor(months / 12);
        const remaining = months % 12;
        const yearLabel = years === 1 ? '1 an' : `${years} ans`;
        return remaining === 0 ? yearLabel : `${yearLabel} ${remaining} mois`;
    });

    // Prefetch on hover
    const prefetchHandlers = useCardPrefetch(
        () => props.stack.slug,
        (s) => stackKeys.detail(s),
        (s) => stacksApi.getBySlug(s),
    );

    const logoTransitionStyle = computed(() =>
        props.stack.slug ? { viewTransitionName: `hero-media-${props.stack.slug}` } : undefined,
    );
    const titleTransitionStyle = computed(() =>
        props.stack.slug ? { viewTransitionName: `hero-title-${props.stack.slug}` } : undefined,
    );
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;

    // Level color CSS custom properties
    .level-expert {
        --level-color: #{vars.$success-color};
        --level-color-light: #{fn.color-alpha(vars.$success-color, 0.1)};
        --level-color-medium: #{fn.color-alpha(vars.$success-color, 0.15)};
    }

    .level-advanced {
        --level-color: #{vars.$primary-color};
        --level-color-light: #{fn.color-alpha(vars.$primary-color, 0.1)};
        --level-color-medium: #{fn.color-alpha(vars.$primary-color, 0.15)};
    }

    .level-confirmed {
        --level-color: #{vars.$secondary-color};
        --level-color-light: #{fn.color-alpha(vars.$secondary-color, 0.1)};
        --level-color-medium: #{fn.color-alpha(vars.$secondary-color, 0.15)};
    }

    .level-beginner {
        --level-color: #{vars.$gray};
        --level-color-light: #{fn.color-alpha(vars.$gray, 0.1)};
        --level-color-medium: #{fn.color-alpha(vars.$gray, 0.15)};
    }

    .stack-card {
        --card-padding: #{vars.$spacing-lg};

        position: relative;
        display: flex;
        flex-direction: column;
        padding: var(--card-padding);
        background: vars.$white;
        border: 1px solid fn.color-alpha(vars.$border-color, 0.5);
        border-radius: vars.$border-radius-xl;
        cursor: pointer;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 8px fn.color-alpha(vars.$black, 0.04);

        &:hover {
            border-color: var(--level-color);
            box-shadow:
                0 12px 32px fn.color-alpha(vars.$black, 0.08),
                0 4px 12px fn.color-alpha(var(--level-color), 0.12);
            transform: translateY(-4px);

            .stack-card__accent {
                transform: scaleX(1);
            }

            .stack-card__logo {
                transform: scale(1.05);
                box-shadow: 0 4px 16px var(--level-color-medium);
            }

            .stack-card__name {
                color: var(--level-color);
            }

            .stack-card__arrow {
                transform: translateX(4px);
                opacity: 1;
            }

            .stack-card__action {
                color: var(--level-color);
            }
        }

        &:focus-visible {
            outline: 2px solid var(--level-color);
            outline-offset: 2px;
        }

        &--flat {
            box-shadow: none;
            border-color: transparent;
            background: vars.$bg-secondary;

            &:hover {
                background: vars.$white;
            }
        }

        &--compact {
            --card-padding: #{vars.$spacing-md};
        }
    }

    // Accent line at top
    .stack-card__accent {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--level-color), fn.color-alpha(var(--level-color), 0.5));
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    // Header
    .stack-card__header {
        display: flex;
        align-items: flex-start;
        gap: vars.$spacing-md;
        margin-bottom: vars.$spacing-md;
    }

    .stack-card__logo {
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 48px;
        height: 48px;
        background: var(--level-color-light);
        border-radius: vars.$border-radius-lg;
        transition: all 0.3s ease;
    }

    .stack-card__logo-img {
        width: 32px;
        height: 32px;
        object-fit: contain;
    }

    .stack-card__logo-letter {
        font-size: vars.$font-size-xl;
        font-weight: vars.$font-weight-bold;
        color: var(--level-color);
    }

    .stack-card__title-group {
        flex: 1;
        min-width: 0;
    }

    .stack-card__name {
        margin: 0 0 vars.$spacing-xxxxs;
        font-size: vars.$font-size-lg;
        font-weight: vars.$font-weight-bold;
        color: vars.$text-primary;
        line-height: 1.3;
        transition: color 0.2s ease;

        @include mix.truncate(1);
    }

    .stack-card__category {
        font-size: vars.$font-size-xs;
        font-weight: vars.$font-weight-medium;
        color: vars.$text-muted;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }

    // Level badge
    .stack-card__level-badge {
        flex-shrink: 0;
        padding: vars.$spacing-xxs vars.$spacing-sm;
        font-size: vars.$font-size-xs;
        font-weight: vars.$font-weight-bold;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border-radius: vars.$border-radius-full;
        white-space: nowrap;

        &--expert {
            background: fn.color-alpha(vars.$success-color, 0.12);
            color: vars.$success-color;
        }

        &--advanced {
            background: fn.color-alpha(vars.$primary-color, 0.12);
            color: vars.$primary-color;
        }

        &--confirmed {
            background: fn.color-alpha(vars.$secondary-color, 0.12);
            color: vars.$secondary-color;
        }

        &--beginner {
            background: fn.color-alpha(vars.$gray, 0.12);
            color: vars.$gray;
        }
    }

    // Description
    .stack-card__description {
        margin: 0 0 vars.$spacing-md;
        font-size: vars.$font-size-sm;
        color: vars.$text-secondary;
        line-height: vars.$line-height-relaxed;

        @include mix.truncate(3);
    }

    // Tags
    .stack-card__tags {
        display: flex;
        flex-wrap: wrap;
        gap: vars.$spacing-xxs;
        margin-bottom: vars.$spacing-md;
    }

    .stack-card__tag {
        padding: vars.$spacing-xxxs vars.$spacing-xs;
        font-size: vars.$font-size-xs;
        font-weight: vars.$font-weight-medium;
        color: vars.$text-secondary;
        background: vars.$bg-secondary;
        border-radius: vars.$border-radius-sm;
        transition: all 0.2s ease;

        &--more {
            color: var(--level-color);
            background: var(--level-color-light);
            font-weight: vars.$font-weight-semibold;
        }
    }

    // Footer
    .stack-card__footer {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: auto;
        padding-top: vars.$spacing-sm;
        border-top: 1px solid fn.color-alpha(vars.$border-color, 0.5);
    }

    .stack-card__experience {
        display: inline-flex;
        align-items: center;
        gap: vars.$spacing-xxxs;
        font-size: vars.$font-size-xs;
        font-weight: vars.$font-weight-medium;
        color: vars.$text-muted;
    }

    .stack-card__action {
        display: inline-flex;
        align-items: center;
        gap: vars.$spacing-xxs;
        font-size: vars.$font-size-sm;
        font-weight: vars.$font-weight-medium;
        color: vars.$text-muted;
        transition: color 0.2s ease;
    }

    .stack-card__arrow {
        opacity: 0.5;
        transition: all 0.2s ease;
    }

    // Reduced motion
    @media (prefers-reduced-motion: reduce) {
        .stack-card {
            transition: none;

            &:hover {
                transform: none;
            }
        }

        .stack-card__accent,
        .stack-card__logo {
            transition: none;
        }
    }

    // Responsive
    @include mix.responsive(mobile) {
        .stack-card {
            --card-padding: #{vars.$spacing-md};
        }

        .stack-card__header {
            gap: vars.$spacing-sm;
        }

        .stack-card__logo {
            width: 44px;
            height: 44px;
        }

        .stack-card__logo-img {
            width: 28px;
            height: 28px;
        }

        .stack-card__name {
            font-size: vars.$font-size-base;
        }

        .stack-card__level-badge {
            padding: 3px vars.$spacing-xs;
            font-size: vars.$font-size-xs;
        }
    }
</style>
