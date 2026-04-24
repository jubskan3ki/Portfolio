<template>
    <div v-if="hasTags" class="article-tags">
        <h3 v-if="showTitle" class="article-tags__title">
            <BaseIcon name="hash" :size="16" />
            {{ title }}
        </h3>

        <!-- Simple mode (links) -->
        <div v-if="display === 'simple'" class="article-tags__list">
            <BaseLink v-for="tag in visibleStringTags" :key="tag" :to="`/blog?tag=${tag}`" class="article-tags__link">
                {{ tag }}
            </BaseLink>
        </div>

        <!-- Cloud mode (toggleable buttons) -->
        <div v-else class="article-tags__list">
            <button
                v-for="tag in visibleObjectTags"
                :key="tag.name || tag.id"
                class="article-tags__btn"
                :class="{ 'article-tags__btn--active': isTagActive(tag.name) }"
                type="button"
                @click="toggleTag(tag.name)"
            >
                {{ tag.name }}
                <span v-if="hasCount(tag)" class="article-tags__count">{{ getCount(tag) }}</span>
            </button>
        </div>

        <button v-if="canToggle" class="article-tags__toggle" type="button" @click="showAll = !showAll">
            {{ showAll ? 'Voir moins' : `Voir plus (${hiddenCount})` }}
        </button>
    </div>
</template>

<script setup lang="ts">
    import { computed, ref } from 'vue';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import BaseLink from '@/components/base/BaseLink.vue';

    import type { ArticleTagsProps, Tag } from '@/types/feature/blog';

    const props = withDefaults(defineProps<ArticleTagsProps & { showTitle?: boolean }>(), {
        title: 'Tags',
        tags: () => [],
        modelValue: () => [],
        display: 'cloud',
        multiSelect: true,
        showTitle: false,
        maxVisible: 0,
    });

    const emit = defineEmits<{
        'update:modelValue': [value: Array<string | number>];
        tagToggle: [tagId: string | number];
        tagSelect: [value: Array<string | number>];
    }>();

    const isTagsObjects = computed(() => {
        if (props.tags.length === 0) {
            return false;
        }
        return typeof props.tags[0] !== 'string';
    });

    // Masque les tags a count=0 (defense-in-depth si le backend en renvoie).
    const filteredTags = computed(() => {
        if (!isTagsObjects.value) {
            return props.tags as string[] | readonly string[];
        }
        return (props.tags as Tag[]).filter((t) => t.count === undefined || t.count > 0);
    });

    const hasTags = computed(() => filteredTags.value.length > 0);

    const stringTags = computed(() => {
        if (!isTagsObjects.value) {
            return filteredTags.value as string[] | readonly string[];
        }

        const hasName = (obj: unknown): obj is { name: string } => {
            return obj !== null && typeof obj === 'object' && 'name' in obj;
        };

        return (filteredTags.value as unknown[]).map((tag) => (hasName(tag) ? tag.name : String(tag)));
    });

    // Tri: count DESC, puis view_count DESC (tags sans count laisses en place).
    const objectTags = computed(() => {
        if (isTagsObjects.value) {
            return [...(filteredTags.value as Tag[])].sort((a, b) => {
                const countDiff = (b.count ?? 0) - (a.count ?? 0);
                if (countDiff !== 0) {
                    return countDiff;
                }
                return (b.view_count ?? 0) - (a.view_count ?? 0);
            });
        }

        return (filteredTags.value as string[] | readonly string[]).map((tag) => ({
            id: tag,
            name: tag,
        }));
    });

    const showAll = ref(false);

    const canToggle = computed(() => props.maxVisible > 0 && filteredTags.value.length > props.maxVisible);

    const hiddenCount = computed(() => Math.max(0, filteredTags.value.length - props.maxVisible));

    const visibleStringTags = computed(() => {
        if (!canToggle.value || showAll.value) {
            return stringTags.value;
        }
        return stringTags.value.slice(0, props.maxVisible);
    });

    const visibleObjectTags = computed(() => {
        if (!canToggle.value || showAll.value) {
            return objectTags.value;
        }
        return objectTags.value.slice(0, props.maxVisible);
    });

    const hasCount = (tag: unknown): tag is { count: number } => {
        return (
            tag !== null
            && typeof tag === 'object'
            && 'count' in tag
            && (tag as { count?: unknown }).count !== undefined
        );
    };

    const getCount = (tag: unknown): number => {
        return hasCount(tag) ? tag.count : 0;
    };

    const isTagActive = (tagId: string | number) => {
        return props.modelValue.includes(tagId);
    };

    const toggleTag = (tagId: string | number) => {
        let newValue;

        if (props.multiSelect) {
            newValue = [...props.modelValue];
            const index = newValue.indexOf(tagId);
            if (index === -1) {
                newValue.push(tagId);
            } else {
                newValue.splice(index, 1);
            }
        } else {
            newValue = isTagActive(tagId) ? [] : [tagId];
        }

        emit('update:modelValue', newValue);
        emit('tagToggle', tagId);
        emit('tagSelect', newValue);
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as fn;

    .article-tags {
        padding: vars.$spacing-lg;

        &__title {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;
            margin: 0 0 vars.$spacing-md;
            padding-bottom: vars.$spacing-sm;
            font-size: vars.$font-size-sm;
            font-weight: vars.$font-weight-semibold;
            color: vars.$text-primary;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            border-bottom: 1px solid fn.color-alpha(vars.$border-color, 0.5);
        }

        &__list {
            display: flex;
            flex-wrap: wrap;
            gap: vars.$spacing-xs;
        }

        &__link {
            display: inline-flex;
            align-items: center;
            padding: vars.$spacing-xxs vars.$spacing-sm;
            font-size: vars.$font-size-xs;
            font-weight: vars.$font-weight-medium;
            color: vars.$text-secondary;
            background: vars.$bg-secondary;
            border: 1px solid transparent;
            border-radius: vars.$border-radius-full;
            text-decoration: none;
            transition:
                background 0.2s ease,
                border-color 0.2s ease,
                color 0.2s ease,
                transform 0.2s ease,
                box-shadow 0.2s ease;

            &:hover {
                color: vars.$primary-color;
                background: fn.color-alpha(vars.$primary-color, 0.1);
                border-color: fn.color-alpha(vars.$primary-color, 0.2);
                transform: translateY(-1px);
                box-shadow: 0 2px 6px fn.color-alpha(vars.$primary-color, 0.08);
                // Override .link:hover { text-decoration: underline } de BaseLink.
                text-decoration: none;
            }

            &:active {
                transform: translateY(0);
            }

            // Retire l'outline focus par défaut du navigateur (remplacé par bordure + :focus-visible).
            &:focus {
                outline: none;
            }

            &:focus-visible {
                outline: 2px solid fn.color-alpha(vars.$primary-color, 0.5);
                outline-offset: 2px;
            }

            @media (prefers-reduced-motion: reduce) {
                transition: none;

                &:hover,
                &:active {
                    transform: none;
                }
            }
        }

        &__btn {
            display: inline-flex;
            align-items: center;
            gap: vars.$spacing-xxs;
            padding: vars.$spacing-xxs vars.$spacing-sm;
            font-size: vars.$font-size-xs;
            font-weight: vars.$font-weight-medium;
            color: vars.$text-secondary;
            background: vars.$bg-secondary;
            border: 1px solid transparent;
            border-radius: vars.$border-radius-full;
            cursor: pointer;
            transition:
                background 0.2s ease,
                border-color 0.2s ease,
                color 0.2s ease,
                transform 0.2s ease,
                box-shadow 0.2s ease;

            &:hover:not(&--active) {
                color: vars.$primary-color;
                border-color: fn.color-alpha(vars.$primary-color, 0.2);
                background: fn.color-alpha(vars.$primary-color, 0.08);
                transform: translateY(-1px);
                box-shadow: 0 2px 6px fn.color-alpha(vars.$primary-color, 0.08);
            }

            &:active {
                transform: translateY(0);
            }

            @media (prefers-reduced-motion: reduce) {
                transition: none;

                &:hover,
                &:active {
                    transform: none;
                }
            }

            &--active {
                color: vars.$primary-color;
                background: fn.color-alpha(vars.$primary-color, 0.1);
                border-color: fn.color-alpha(vars.$primary-color, 0.25);
                font-weight: vars.$font-weight-semibold;

                .article-tags__count {
                    color: vars.$white;
                    background: vars.$primary-color;
                }

                &:hover {
                    color: vars.$white;
                    background: vars.$primary-color;
                    border-color: vars.$primary-color;

                    .article-tags__count {
                        color: vars.$primary-color;
                        background: vars.$white;
                    }
                }
            }
        }

        &__count {
            padding: 1px 6px;
            font-size: 10px;
            font-weight: vars.$font-weight-semibold;
            color: vars.$text-muted;
            background: fn.color-alpha(vars.$black, 0.06);
            border-radius: vars.$border-radius-full;
            transition: all 0.2s ease;
        }

        &__toggle {
            margin-top: vars.$spacing-sm;
            padding: vars.$spacing-xs vars.$spacing-sm;
            font-size: vars.$font-size-xs;
            font-weight: vars.$font-weight-semibold;
            color: vars.$primary-color;
            background: transparent;
            border: none;
            border-radius: vars.$border-radius-full;
            cursor: pointer;
            transition: background 0.2s ease;

            &:hover {
                background: fn.color-alpha(vars.$primary-color, 0.08);
            }
        }
    }
</style>
