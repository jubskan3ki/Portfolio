<template>
    <div class="offline-page">
        <div class="container offline-page__inner">
            <div class="offline-page__icon">
                <BaseIcon name="wifi-off" :size="48" />
            </div>
            <h1 class="offline-page__title">Hors ligne</h1>
            <p class="offline-page__text">
                Vous n'êtes pas connecté à internet. Les articles déjà consultés restent accessibles depuis le cache du
                service worker.
            </p>
            <div class="offline-page__actions">
                <button type="button" class="offline-page__btn" @click="retry">
                    <BaseIcon name="refresh" :size="16" />
                    Réessayer
                </button>
                <NuxtLink to="/blog" class="offline-page__btn offline-page__btn--secondary">
                    Articles en cache
                </NuxtLink>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import BaseIcon from '@/components/base/BaseIcon.vue';

    useSeoMeta({
        title: 'Hors ligne',
        description: 'Vous êtes hors ligne. Les articles déjà consultés restent disponibles.',
        robots: 'noindex, nofollow',
    });

    function retry() {
        if (typeof window !== 'undefined') {
            window.location.reload();
        }
    }
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/functions' as fn;

    .offline-page {
        min-height: calc(100vh - vars.$navbar-height);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: vars.$spacing-xl 0;

        &__inner {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: vars.$spacing-lg;
            text-align: center;
            max-width: 560px;
        }

        &__icon {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 96px;
            height: 96px;
            border-radius: 50%;
            background: fn.color-alpha(vars.$primary-color, 0.08);
            color: vars.$primary-color;
        }

        &__title {
            margin: 0;
            color: vars.$text-primary;
        }

        &__text {
            margin: 0;
            color: vars.$text-secondary;
            line-height: 1.7;
        }

        &__actions {
            display: flex;
            gap: vars.$spacing-sm;
            flex-wrap: wrap;
            justify-content: center;
        }

        &__btn {
            display: inline-flex;
            align-items: center;
            gap: vars.$spacing-xs;
            padding: vars.$spacing-sm vars.$spacing-lg;
            font-weight: vars.$font-weight-semibold;
            border-radius: vars.$border-radius-full;
            border: 1px solid vars.$primary-color;
            background: vars.$primary-color;
            color: vars.$white;
            cursor: pointer;
            text-decoration: none;
            transition:
                background 0.2s ease,
                color 0.2s ease;

            &:hover,
            &:focus-visible {
                background: fn.color-alpha(vars.$primary-color, 0.85);
            }

            &--secondary {
                background: transparent;
                color: vars.$primary-color;

                &:hover,
                &:focus-visible {
                    background: fn.color-alpha(vars.$primary-color, 0.08);
                    color: vars.$primary-color;
                }
            }
        }
    }
</style>
