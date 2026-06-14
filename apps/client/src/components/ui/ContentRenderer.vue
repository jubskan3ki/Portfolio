<template>
    <div class="article-blocks">
        <template v-for="(block, index) in blocks" :key="`block-${index}`">
            <p v-if="block.type === 'paragraph'" class="article-blocks__paragraph">
                <InlineMarkdown :text="block.content" />
            </p>

            <h2
                v-else-if="block.type === 'heading' && block.level === 2"
                :id="slugify(block.content)"
                class="article-blocks__heading article-blocks__heading--h2"
            >
                <InlineMarkdown :text="block.content" />
            </h2>
            <h3
                v-else-if="block.type === 'heading' && block.level === 3"
                :id="slugify(block.content)"
                class="article-blocks__heading article-blocks__heading--h3"
            >
                <InlineMarkdown :text="block.content" />
            </h3>
            <h4
                v-else-if="block.type === 'heading' && block.level === 4"
                :id="slugify(block.content)"
                class="article-blocks__heading article-blocks__heading--h4"
            >
                <InlineMarkdown :text="block.content" />
            </h4>

            <blockquote v-else-if="block.type === 'blockquote'" class="article-blocks__quote">
                <p>
                    <InlineMarkdown :text="block.content" />
                </p>
                <cite v-if="block.cite" class="article-blocks__quote-cite"> | {{ block.cite }} </cite>
            </blockquote>

            <figure v-else-if="block.type === 'image'" class="article-blocks__figure">
                <BaseImage :src="block.src" :alt="block.alt" object-fit="cover" class="article-blocks__figure-img" />
                <figcaption v-if="block.caption" class="article-blocks__figure-caption">
                    {{ block.caption }}
                </figcaption>
            </figure>

            <pre v-else-if="block.type === 'code'" class="article-blocks__code"><code>{{ block.content }}</code></pre>

            <ol v-else-if="block.type === 'list' && block.ordered" class="article-blocks__list">
                <li v-for="(item, liIndex) in block.items" :key="`li-${index}-${liIndex}`">
                    <InlineMarkdown :text="item" />
                </li>
            </ol>
            <ul v-else-if="block.type === 'list'" class="article-blocks__list">
                <li v-for="(item, liIndex) in block.items" :key="`li-${index}-${liIndex}`">
                    <InlineMarkdown :text="item" />
                </li>
            </ul>

            <div v-else-if="block.type === 'table'" class="article-blocks__table-wrapper">
                <table class="article-blocks__table">
                    <thead>
                        <tr>
                            <th v-for="(header, hIdx) in block.headers" :key="`th-${index}-${hIdx}`">
                                <InlineMarkdown :text="header" />
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(row, rIdx) in block.rows" :key="`tr-${index}-${rIdx}`">
                            <td v-for="(cell, cIdx) in row" :key="`td-${index}-${rIdx}-${cIdx}`">
                                <InlineMarkdown :text="cell" />
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </template>
    </div>
</template>

<script setup lang="ts">
    import InlineMarkdown from '@/components/base/InlineMarkdown.vue';
    import { slugify } from '@/services/utils/string';

    import type { ContentBlock } from '@/types/feature/blog';

    defineProps<{
        blocks: ContentBlock[];
    }>();
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as fn;

    .article-blocks {
        display: flex;
        flex-direction: column;
        gap: vars.$spacing-md;

        // Paragraph
        &__paragraph {
            font-size: vars.$font-size-lg;
            line-height: 1.8;
            color: vars.$text-secondary;
            max-width: 72ch;
            margin: 0;

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

        // Headings
        &__heading {
            color: vars.$text-primary;
            margin-top: vars.$spacing-xl;
            margin-bottom: vars.$spacing-xs;
            scroll-margin-top: 100px;

            &--h2 {
                font-size: vars.$font-size-xxl;
                font-weight: vars.$font-weight-bold;
                padding-bottom: vars.$spacing-xs;
                border-bottom: 2px solid fn.color-alpha(vars.$primary-color, 0.15);
            }

            &--h3 {
                font-size: vars.$font-size-xl;
                font-weight: vars.$font-weight-semibold;
            }

            &--h4 {
                font-size: vars.$font-size-lg;
                font-weight: vars.$font-weight-semibold;
            }
        }

        // Blockquote
        &__quote {
            position: relative;
            margin: vars.$spacing-lg 0;
            padding: vars.$spacing-lg vars.$spacing-xl;
            background: fn.color-alpha(vars.$primary-color, 0.04);
            border: 1px solid vars.$primary-color;
            border-radius: vars.$border-radius-md;

            p {
                font-size: vars.$font-size-lg;
                font-style: italic;
                line-height: 1.7;
                color: vars.$text-primary;
                margin: 0;
            }

            :deep(strong) {
                font-weight: vars.$font-weight-semibold;
            }
        }

        &__quote-cite {
            display: block;
            margin-top: vars.$spacing-sm;
            font-size: vars.$font-size-sm;
            font-style: normal;
            color: vars.$text-muted;
        }

        // Figure / Image
        &__figure {
            margin: vars.$spacing-lg 0;
            border-radius: vars.$border-radius-lg;
            overflow: hidden;
        }

        &__figure-img {
            width: 100%;
            height: auto;
            display: block;
        }

        &__figure-caption {
            padding: vars.$spacing-sm vars.$spacing-md;
            font-size: vars.$font-size-sm;
            color: vars.$text-muted;
            text-align: center;
            background: fn.color-alpha(vars.$black, 0.02);
        }

        // Code
        &__code {
            margin: vars.$spacing-lg 0;
            padding: vars.$spacing-lg;
            background: #1f2937;
            color: #e5e7eb;
            border-radius: vars.$border-radius-lg;
            overflow-x: auto;
            font-family: vars.$font-family-mono;
            font-size: vars.$font-size-sm;
            line-height: 1.7;

            code {
                background: none;
                padding: 0;
                border-radius: 0;
                color: inherit;
                font-size: inherit;
            }
        }

        // List
        &__list {
            margin: vars.$spacing-sm 0;
            padding-left: vars.$spacing-lg;

            li {
                font-size: vars.$font-size-lg;
                line-height: 1.8;
                color: vars.$text-secondary;
                margin-bottom: vars.$spacing-xs;

                :deep(strong) {
                    font-weight: vars.$font-weight-semibold;
                    color: vars.$text-primary;
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
                }
            }
        }

        // Table
        &__table-wrapper {
            margin: vars.$spacing-lg 0;
            overflow-x: auto;
            border-radius: vars.$border-radius-lg;
            border: 1px solid fn.color-alpha(vars.$border-color, 0.5);
        }

        &__table {
            width: 100%;
            border-collapse: collapse;
            font-size: vars.$font-size-sm;

            thead {
                background: fn.color-alpha(vars.$primary-color, 0.06);
            }

            th {
                padding: vars.$spacing-sm vars.$spacing-md;
                font-weight: vars.$font-weight-semibold;
                color: vars.$text-primary;
                text-align: left;
                border-bottom: 2px solid fn.color-alpha(vars.$primary-color, 0.15);
                white-space: nowrap;
            }

            td {
                padding: vars.$spacing-sm vars.$spacing-md;
                color: vars.$text-secondary;
                border-bottom: 1px solid fn.color-alpha(vars.$border-color, 0.3);
            }

            tbody tr {
                transition: background 0.15s ease;

                &:hover {
                    background: fn.color-alpha(vars.$primary-color, 0.03);
                }

                &:last-child td {
                    border-bottom: none;
                }
            }

            :deep(strong) {
                font-weight: vars.$font-weight-semibold;
                color: vars.$text-primary;
            }
        }
    }

    @include mix.responsive(mobile) {
        .article-blocks {
            &__paragraph,
            &__list li {
                font-size: vars.$font-size-md;
            }

            &__heading--h2 {
                font-size: vars.$font-size-xl;
            }

            &__heading--h3 {
                font-size: vars.$font-size-lg;
            }

            &__quote {
                padding: vars.$spacing-md vars.$spacing-lg;
            }

            &__code {
                padding: vars.$spacing-md;
                font-size: vars.$font-size-xs;
            }

            &__table {
                font-size: vars.$font-size-xs;

                th,
                td {
                    padding: vars.$spacing-xs vars.$spacing-sm;
                }
            }
        }
    }
</style>
