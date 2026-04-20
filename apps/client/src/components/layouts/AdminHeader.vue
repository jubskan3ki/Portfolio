<template>
    <header class="admin-header">
        <div class="admin-header__inner">
            <BaseButton
                class="admin-header__menu-toggle"
                variant="ghost"
                size="icon"
                aria-label="Ouvrir le menu"
                @click="emit('toggleSidebar')"
            >
                <template #icon-left>
                    <BaseIcon name="menu" :size="20" aria-hidden="true" />
                </template>
            </BaseButton>

            <BaseButton
                class="admin-header__collapse-btn"
                variant="ghost"
                size="icon"
                :aria-label="collapsed ? 'Etendre le menu' : 'Reduire le menu'"
                :title="collapsed ? 'Etendre le menu' : 'Reduire le menu'"
                @click="emit('toggleCollapse')"
            >
                <template #icon-left>
                    <BaseIcon :name="collapseIcon" :size="18" aria-hidden="true" />
                </template>
            </BaseButton>

            <div class="admin-header__spacer"></div>

            <SearchGlobal class="admin-header__search" placeholder="Rechercher..." />

            <div class="admin-header__spacer"></div>

            <div class="admin-header__user">
                <Avatar :src="authStore.user?.avatar" :alt="fullName" :name="fullName" size="sm" />
                <div class="admin-header__user-info">
                    <span class="admin-header__user-name">{{ fullName }}</span>
                    <small class="admin-header__user-role">Administrateur</small>
                </div>
            </div>
        </div>
    </header>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import BaseButton from '@/components/base/BaseButton.vue';
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import Avatar from '@/components/ui/Avatar.vue';
    import SearchGlobal from '@/components/ui/SearchGlobal.vue';
    import { useAuthStore } from '@/stores/auth';

    import type { AdminHeaderProps } from '@/types/components/layouts';

    const props = defineProps<AdminHeaderProps>();

    const emit = defineEmits<{
        toggleSidebar: [];
        toggleCollapse: [];
    }>();

    const authStore = useAuthStore();

    const collapseIcon = computed(() => (props.collapsed ? 'panel-left-open' : 'panel-left-close'));
    const fullName = computed(() => authStore.fullName || 'Admin');
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .admin-header {
        position: fixed;
        top: 0;
        right: 0;
        left: vars.$admin-sidebar-width;
        height: vars.$admin-header-height;
        background: func.color-alpha(vars.$white, 0.85);
        backdrop-filter: blur(12px);
        border-bottom: 1px solid func.color-alpha(vars.$black, 0.06);
        z-index: vars.$z-index-sticky;
        transition: left 0.3s cubic-bezier(0.23, 1, 0.32, 1);

        .admin-layout--collapsed & {
            left: vars.$admin-sidebar-collapsed;
        }

        @include mix.responsive(tablet) {
            left: 0;

            // Override collapsed state on tablet
            .admin-layout--collapsed & {
                left: 0;
            }
        }

        /* Inner */
        &__inner {
            display: flex;
            align-items: center;
            height: 100%;
            padding: 0 vars.$spacing-lg;
            gap: vars.$spacing-md;

            @include mix.responsive(tablet) {
                padding: 0 vars.$spacing-md;
            }
        }

        /* Toggle buttons */
        &__menu-toggle {
            display: none;

            @include mix.responsive(tablet) {
                display: flex;
            }
        }

        &__collapse-btn {
            @include mix.responsive(tablet) {
                display: none;
            }
        }

        /* Spacer */
        &__spacer {
            flex: 1;
        }

        /* Search (centered, visible on mobile via icon) */

        /* User (simple, no dropdown) */
        &__user {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;
        }

        &__user-info {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            gap: 2px;

            @include mix.responsive(mobile) {
                display: none;
            }
        }

        &__user-name {
            color: vars.$text-primary;
            font-weight: vars.$font-weight-medium;
            line-height: 1.2;
        }

        &__user-role {
            color: vars.$text-muted;
            line-height: 1.2;
        }
    }
</style>
