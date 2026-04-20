<template>
    <nav class="admin-breadcrumb" aria-label="Fil d'ariane">
        <ol class="admin-breadcrumb__list">
            <li v-for="(crumb, index) in breadcrumbs" :key="crumb.path" class="admin-breadcrumb__item">
                <NuxtLink v-if="index < breadcrumbs.length - 1" :to="crumb.path" class="admin-breadcrumb__link">
                    <BaseIcon v-if="crumb.icon" :name="crumb.icon" :size="14" aria-hidden="true" />
                    {{ crumb.label }}
                </NuxtLink>
                <span v-else class="admin-breadcrumb__current" aria-current="page">
                    <BaseIcon v-if="crumb.icon" :name="crumb.icon" :size="14" aria-hidden="true" />
                    {{ crumb.label }}
                </span>
                <BaseIcon
                    v-if="index < breadcrumbs.length - 1"
                    :name="separatorIcon"
                    :size="14"
                    class="admin-breadcrumb__separator"
                    aria-hidden="true"
                />
            </li>
        </ol>
    </nav>
</template>

<script setup lang="ts">
    import { computed } from 'vue';
    import { useRoute } from 'vue-router';

    import BaseIcon from '@/components/base/BaseIcon.vue';
    import { getBreadcrumbLabel } from '@/config/adminNav';
    import { ADMIN_ROUTES } from '@/config/routes';

    import type { AdminBreadcrumbProps, AdminBreadcrumb } from '@/types/components/layouts';

    const props = withDefaults(defineProps<AdminBreadcrumbProps>(), {
        items: undefined,
        separator: 'chevron-right',
    });

    const route = useRoute();

    const separatorIcon = computed(() => props.separator || 'chevron-right');

    const breadcrumbs = computed<AdminBreadcrumb[]>(() => {
        // Use provided items if available
        if (props.items?.length) {
            return props.items;
        }

        // Generate from route
        const pathSegments = route.path.split('/').filter(Boolean);
        const crumbs: AdminBreadcrumb[] = [];
        let currentPath = '';

        pathSegments.forEach((segment, index) => {
            currentPath += `/${segment}`;

            // Replace 'admin' with Dashboard as first breadcrumb
            if (index === 0 && segment === 'admin') {
                crumbs.push({
                    label: 'Dashboard',
                    path: ADMIN_ROUTES.DASHBOARD.path,
                    icon: 'home',
                });
                return;
            }

            // Handle dynamic route segments (IDs, slugs)
            if (isDynamicSegment(segment)) {
                const label = getRouteTitle() || 'Details';
                crumbs.push({ label, path: currentPath });
                return;
            }

            // Get label from config or capitalize
            const label = getBreadcrumbLabel(segment);
            crumbs.push({ label, path: currentPath });
        });

        return crumbs;
    });

    const isDynamicSegment = (segment: string): boolean => {
        return /^\d+$/.test(segment) || segment === '[id]' || segment === '[slug]' || /^[a-f0-9-]{36}$/i.test(segment);
    };

    const getRouteTitle = (): string | null => {
        return (route.meta.title as string) || null;
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;

    .admin-breadcrumb {
        margin-bottom: vars.$spacing-md;

        &__list {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: vars.$spacing-xxs;
            list-style: none;
            padding: 0;
            margin: 0;
        }

        &__item {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xxs;
        }

        &__link {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xxs;
            color: vars.$text-muted;
            text-decoration: none;
            transition: color vars.$transition-fast;
            border-radius: vars.$border-radius-sm;

            &:hover {
                color: vars.$primary-color;
            }

            &:focus-visible {
                outline: 2px solid vars.$primary-color;
                outline-offset: 2px;
            }
        }

        &__current {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xxs;
            color: vars.$text-primary;
            font-weight: vars.$font-weight-medium;
        }

        &__separator {
            color: vars.$text-muted;
            opacity: 0.6;
        }
    }
</style>
