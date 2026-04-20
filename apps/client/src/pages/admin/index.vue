<template>
    <div class="login-page" @mousemove="handleMouseMove">
        <div class="login-page__bg" aria-hidden="true">
            <div class="login-page__gradient"></div>
            <div class="login-page__dots"></div>

            <div class="login-page__shapes">
                <div class="deco-shape deco-shape--1"></div>
                <div class="deco-shape deco-shape--2"></div>
                <div class="deco-shape deco-shape--3"></div>
            </div>

            <div class="login-page__glow"></div>
        </div>

        <main
            ref="cardRef"
            class="login-card"
            :style="cardStyle"
            role="main"
            aria-labelledby="login-title"
            @mouseenter="isCardHovered = true"
            @mouseleave="handleCardLeave"
        >
            <div class="login-card__shine" :style="shineStyle" aria-hidden="true"></div>

            <header class="login-card__header">
                <AppLogo size="lg" class="login-card__logo" />
                <h1 id="login-title" class="login-card__title">Administration</h1>
                <p class="login-card__subtitle">Connectez-vous pour accéder au panel</p>
            </header>

            <div class="login-card__divider"></div>

            <form class="login-card__form" @submit.prevent="handleSubmit">
                <BaseInput
                    id="email"
                    v-model="form.email"
                    type="email"
                    label="Email"
                    placeholder="admin@example.com"
                    autocomplete="email"
                    required
                    :error="errors.email"
                    custom-class="login-input"
                >
                    <template #icon-left>
                        <BaseIcon name="mail" :size="18" aria-hidden="true" />
                    </template>
                </BaseInput>

                <BaseInput
                    id="password"
                    v-model="form.password"
                    :type="showPassword ? 'text' : 'password'"
                    label="Mot de passe"
                    placeholder="••••••••"
                    autocomplete="current-password"
                    required
                    :error="errors.password"
                    custom-class="login-input"
                >
                    <template #icon-left>
                        <BaseIcon name="lock" :size="18" aria-hidden="true" />
                    </template>
                    <template #icon-right>
                        <button
                            type="button"
                            class="password-toggle"
                            :aria-label="showPassword ? 'Masquer le mot de passe' : 'Afficher le mot de passe'"
                            :aria-pressed="showPassword"
                            @click="showPassword = !showPassword"
                        >
                            <BaseIcon :name="showPassword ? 'eye-off' : 'eye'" :size="18" aria-hidden="true" />
                        </button>
                    </template>
                </BaseInput>

                <div class="login-card__options">
                    <BaseCheckbox v-model="form.rememberMe" label="Se souvenir de moi" />
                </div>

                <Transition name="fade-slide">
                    <div v-if="loginError" class="login-card__alert" role="alert" aria-live="polite">
                        <BaseIcon name="alert-circle" :size="18" aria-hidden="true" />
                        <span>{{ loginError }}</span>
                    </div>
                </Transition>

                <BaseButton
                    type="submit"
                    variant="primary"
                    :disabled="loginMutation.isPending.value"
                    custom-class="login-card__btn"
                >
                    <template v-if="loginMutation.isPending.value" #icon-left>
                        <span class="login-card__loader" role="status" aria-label="Chargement en cours"></span>
                    </template>
                    <template v-if="!loginMutation.isPending.value" #icon-right>
                        <BaseIcon name="arrow-right" :size="18" aria-hidden="true" />
                    </template>
                    {{ loginMutation.isPending.value ? 'Connexion...' : 'Se connecter' }}
                </BaseButton>
            </form>

            <footer class="login-card__footer">
                <BaseLink to="/" variant="subtle" custom-class="login-card__back" aria-label="Retour au site principal">
                    <template #icon-left>
                        <BaseIcon name="arrow-left" :size="16" aria-hidden="true" />
                    </template>
                    Retour au site
                </BaseLink>
            </footer>
        </main>

        <small class="login-page__version" aria-hidden="true">v1.0.0</small>
    </div>
</template>

<script setup lang="ts">
    import { ref, reactive, computed, onMounted } from 'vue';
    import { useRoute } from 'vue-router';

    import BaseButton from '@/components/base/BaseButton.vue';
    import BaseCheckbox from '@/components/base/BaseCheckbox.vue';
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import BaseInput from '@/components/base/BaseInput.vue';
    import BaseLink from '@/components/base/BaseLink.vue';
    import AppLogo from '@/components/ui/AppLogo.vue';
    import { useSeo } from '@/composables/seo/useSeo';
    import { refreshTokenManager } from '@/services/api/core/token';
    import { authApi, useLogin } from '@/services/api/modules/auth';
    import { parseError } from '@/services/utils/errors';
    import { useAuthStore } from '@/stores/auth';

    definePageMeta({
        layout: false,
        prefetch: false,
    });

    // SEO - noindex for admin pages
    useSeo({
        title: 'Connexion Admin',
        description: 'Connexion au panneau d\'administration',
        noindex: true,
        url: '/admin',
    });

    const route = useRoute();
    const authStore = useAuthStore();
    const loginMutation = useLogin();

    const loginError = computed(() => {
        if (!loginMutation.error.value) {
            return null;
        }
        return parseError(loginMutation.error.value).message;
    });

    // Whitelist of allowed redirect paths (security: prevent open redirect)
    const ALLOWED_REDIRECTS = [
        '/admin/dashboard',
        '/admin/articles',
        '/admin/projects',
        '/admin/stacks',
        '/admin/experiences',
        '/admin/messages',
        '/admin/settings',
        '/admin/history',
        '/admin/import-export',
    ] as const;

    // Get redirect URL from query param with validation
    const redirectUrl = computed(() => {
        const redirect = route.query.redirect as string;
        if (!redirect) {
            return '/admin/dashboard';
        }

        // Only allow internal admin paths
        if (!redirect.startsWith('/admin/')) {
            return '/admin/dashboard';
        }

        // Check against whitelist or allow any /admin/* subpath
        const isAllowed = ALLOWED_REDIRECTS.some((path) => redirect === path || redirect.startsWith(`${path}/`));
        return isAllowed ? redirect : '/admin/dashboard';
    });

    // Form
    const form = reactive({ email: '', password: '', rememberMe: false });
    const errors = reactive({ email: '', password: '' });
    const showPassword = ref(false);

    // Card parallax
    const cardRef = ref<HTMLElement | null>(null);
    const isCardHovered = ref(false);
    const rotation = reactive({ x: 0, y: 0 });

    const handleMouseMove = (e: MouseEvent) => {
        if (!isCardHovered.value || !cardRef.value) {
            return;
        }
        const rect = cardRef.value.getBoundingClientRect();
        const x = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
        const y = ((e.clientY - rect.top) / rect.height - 0.5) * 2;
        rotation.x = y * -4;
        rotation.y = x * 4;
    };

    const handleCardLeave = () => {
        isCardHovered.value = false;
        rotation.x = 0;
        rotation.y = 0;
    };

    const cardStyle = computed(() => ({
        transform: isCardHovered.value
            ? `perspective(800px) rotateX(${rotation.x}deg) rotateY(${rotation.y}deg) scale(1.01)`
            : 'perspective(800px) rotateX(0deg) rotateY(0deg) scale(1)',
    }));

    const shineStyle = computed(() => {
        if (!isCardHovered.value) {
            return { opacity: 0 };
        }
        const x = ((rotation.y / 4 + 1) / 2) * 100;
        const y = ((-rotation.x / 4 + 1) / 2) * 100;
        return {
            opacity: 1,
            background: `radial-gradient(circle at ${x}% ${y}%, rgba(255,255,255,0.08) 0%, transparent 50%)`,
        };
    });

    // Validation
    const validate = (): boolean => {
        errors.email = '';
        errors.password = '';
        let valid = true;

        if (!form.email) {
            errors.email = 'L\'email est requis';
            valid = false;
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
            errors.email = 'Email invalide';
            valid = false;
        }

        if (!form.password) {
            errors.password = 'Le mot de passe est requis';
            valid = false;
        } else if (form.password.length < 6) {
            errors.password = 'Minimum 6 caractères';
            valid = false;
        }

        return valid;
    };

    const handleSubmit = () => {
        if (!validate()) {
            return;
        }
        loginMutation.mutate(
            {
                email: form.email,
                password: form.password,
                rememberMe: form.rememberMe,
            },
            {
                onSuccess: () => {
                    navigateTo(redirectUrl.value, { replace: true });
                },
            },
        );
    };

    // Check if already authenticated on mount
    onMounted(async () => {
        if (!import.meta.client) {
            return;
        }

        // If already authenticated in memory, redirect
        if (authStore.isAuthenticated) {
            await navigateTo(redirectUrl.value, { replace: true });
            return;
        }

        // Verify with backend
        try {
            const refreshed = await refreshTokenManager.refresh();
            if (!refreshed) {
                return;
            }
            const profile = await authApi.getProfile();
            authStore.setUser(profile);
            await navigateTo(redirectUrl.value, { replace: true });
        } catch {
            // Not authenticated — stay on login page
        }
    });
</script>

<style lang="scss" scoped>
    @use 'sass:color';
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;

    // PAGE

    .login-page {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: vars.$spacing-xl;
        position: relative;
        overflow: hidden;

        @include mix.responsive(mobile) {
            padding: vars.$spacing-md;
        }

        &__bg {
            position: absolute;
            inset: 0;
            z-index: 0;
        }

        &__gradient {
            position: absolute;
            inset: 0;
            background: vars.$primary-dark;
        }

        &__dots {
            position: absolute;
            inset: -50%;

            @include mix.dots-pattern(rgba(255, 255, 255, 0.025), 2px, 28px);

            animation: drift 100s linear infinite;
            animation-delay: 0.5s;
            will-change: transform;
        }

        &__shapes {
            position: absolute;
            inset: 0;
            pointer-events: none;
        }

        &__glow {
            position: absolute;
            top: -30%;
            right: -20%;
            width: 60%;
            height: 70%;
            background: transparent;
            filter: blur(60px);
        }

        &__version {
            position: fixed;
            bottom: vars.$spacing-lg;
            right: vars.$spacing-lg;
            color: rgba(255, 255, 255, 0.35);
            letter-spacing: 0.5px;
        }
    }

    // DECORATIVE SHAPES

    .deco-shape {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.04);

        &--1 {
            top: 12%;
            left: 8%;
            width: 180px;
            height: 180px;
            animation: float 16s ease-in-out infinite;
        }

        &--2 {
            top: 55%;
            right: 6%;
            width: 120px;
            height: 120px;
            animation: float 20s ease-in-out infinite reverse;
        }

        &--3 {
            bottom: 10%;
            left: 20%;
            width: 80px;
            height: 80px;
            animation: float 14s ease-in-out infinite;
            animation-delay: -4s;
        }
    }

    // LOGIN CARD

    .login-card {
        position: relative;
        z-index: 1;
        width: 100%;
        max-width: 420px;
        min-height: 480px;
        border-radius: 20px;
        background: vars.$white;
        padding: vars.$spacing-xxl;
        box-shadow:
            0 30px 60px -20px rgba(0, 0, 0, 0.25),
            0 0 1px rgba(0, 0, 0, 0.1);
        transform-style: preserve-3d;
        transition:
            transform 0.5s cubic-bezier(0.23, 1, 0.32, 1),
            box-shadow 0.5s ease;
        will-change: transform, opacity;
        animation: card-fade-in 0.4s ease-out forwards;
        contain: layout style paint;

        &:hover {
            box-shadow:
                0 40px 80px -25px rgba(0, 0, 0, 0.3),
                0 0 1px rgba(0, 0, 0, 0.1);
        }

        @include mix.responsive(mobile) {
            padding: vars.$spacing-xl;
            border-radius: 16px;
        }

        &__shine {
            position: absolute;
            inset: 0;
            border-radius: inherit;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.4s ease;
        }

        &__header {
            text-align: center;
            margin-bottom: vars.$spacing-lg;
        }

        &__logo {
            display: flex;
            justify-content: center;
            margin: 0 auto vars.$spacing-md;

            svg {
                display: block;
            }
        }

        &__title {
            font-weight: vars.$font-weight-bold;
            color: vars.$text-primary;
            margin-bottom: 4px;
        }

        &__subtitle {
            color: vars.$text-secondary;
        }

        &__divider {
            height: 1px;
            background: vars.$border-color;
            margin-bottom: vars.$spacing-lg;
        }

        &__form {
            display: flex;
            flex-direction: column;
            gap: vars.$spacing-md;
        }

        &__options {
            display: flex;
            align-items: center;
        }

        &__alert {
            display: flex;
            align-items: center;
            gap: vars.$spacing-xs;
            padding: vars.$spacing-xs vars.$spacing-md;
            background: rgba(vars.$danger-color, 0.06);
            border: 1px solid rgba(vars.$danger-color, 0.12);
            border-radius: vars.$border-radius-lg;
            color: vars.$danger-color;
        }

        &__btn {
            width: 100%;
        }

        &__loader {
            width: 20px;
            height: 20px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-top-color: vars.$white;
            border-radius: 50%;
            animation: spin 0.7s linear infinite;
        }

        &__footer {
            margin-top: vars.$spacing-lg;
            padding-top: vars.$spacing-md;
            border-top: 1px solid vars.$border-color;
            text-align: center;
        }

        &__back {
            margin: 0 auto;
        }
    }

    // LOGIN INPUT OVERRIDES

    .login-input {
        margin-bottom: 0;
    }

    .password-toggle {
        padding: vars.$spacing-xxs;
        background: none;
        border: none;
        color: vars.$text-secondary;
        cursor: pointer;
        border-radius: vars.$border-radius-sm;
        transition: all vars.$transition-fast;

        &:hover,
        &:focus {
            color: vars.$text-inverted;
            background-color: vars.$primary-color;
        }

        &:focus-visible {
            outline: 2px solid vars.$primary-color;
            outline-offset: 2px;
        }
    }

    // ANIMATIONS

    @keyframes drift {
        from {
            transform: translate(0, 0);
        }

        to {
            transform: translate(28px, 28px);
        }
    }

    @keyframes float {
        0%,
        100% {
            transform: translateY(0);
        }

        50% {
            transform: translateY(-12px);
        }
    }

    @keyframes card-fade-in {
        from {
            opacity: 0;
        }

        to {
            opacity: 1;
        }
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }

    // Transitions
    .fade-slide-enter-active,
    .fade-slide-leave-active {
        transition: all 0.25s ease;
    }

    .fade-slide-enter-from,
    .fade-slide-leave-to {
        opacity: 0;
        transform: translateY(-6px);
    }

    .fade-enter-active,
    .fade-leave-active {
        transition: opacity 0.15s ease;
    }

    .fade-enter-from,
    .fade-leave-to {
        opacity: 0;
    }

    @media (prefers-reduced-motion: reduce) {
        .login-card {
            animation: none !important;
            opacity: 1 !important;
        }

        .login-page__dots {
            animation: none;
        }

        .deco-shape {
            animation: none;
        }

        .login-card__loader {
            animation: spin 1.5s linear infinite;
        }
    }
</style>
