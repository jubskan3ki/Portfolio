<template>
    <div class="admin-page">
        <div class="admin-page__header">
            <div>
                <h1 class="admin-page__title">Parametres</h1>
                <p class="admin-page__subtitle">Gerez votre profil et vos preferences</p>
            </div>
            <BaseButton variant="outline" :loading="isLoggingOut" custom-class="btn-logout" @click="handleLogout">
                <template #icon-left>
                    <BaseIcon name="log-out" :size="16" />
                </template>
                {{ isLoggingOut ? 'Deconnexion...' : 'Se deconnecter' }}
            </BaseButton>
        </div>

        <div class="settings-grid">
            <div class="admin-card admin-card--full">
                <div class="admin-card__header">
                    <h2 class="admin-card__title">Profil</h2>
                </div>
                <form @submit.prevent="updateProfile">
                    <div class="profile-header">
                        <div
                            class="profile-avatar"
                            role="button"
                            tabindex="0"
                            @click="triggerAvatarUpload"
                            @keydown.enter="triggerAvatarUpload"
                            @keydown.space.prevent="triggerAvatarUpload"
                        >
                            <Avatar
                                :src="authStore.user?.avatar"
                                :name="authStore.fullName || 'Admin'"
                                size="xl"
                                shape="square"
                            />
                            <div class="profile-avatar__overlay">
                                <BaseIcon name="camera" :size="20" />
                            </div>
                            <input
                                ref="avatarInput"
                                type="file"
                                accept="image/*"
                                class="profile-avatar__input"
                                aria-label="Changer l'avatar"
                                @change="handleAvatarChange"
                            />
                        </div>
                        <div class="profile-info">
                            <h3>{{ authStore.fullName || 'Admin' }}</h3>
                            <p>{{ authStore.user?.email }}</p>
                            <small v-if="authStore.user?.dateJoined" class="profile-info__date">
                                Membre depuis {{ formatDate(authStore.user.dateJoined, 'MMMM YYYY') }}
                            </small>
                        </div>
                    </div>

                    <BaseDivider label="Identite" spacing="lg" />
                    <div class="form-grid">
                        <BaseInput v-model="profileForm.firstName" label="Prenom" placeholder="Votre prenom" />
                        <BaseInput v-model="profileForm.lastName" label="Nom" placeholder="Votre nom" />
                    </div>
                    <BaseInput v-model="profileForm.position" label="Poste" placeholder="Ex: Developpeur Full-Stack" />
                    <BaseTextarea v-model="profileForm.bio" label="Bio" placeholder="Courte description..." :rows="3" />

                    <BaseDivider label="Contact" spacing="lg" />
                    <div class="form-grid">
                        <BaseInput
                            :model-value="authStore.user?.email"
                            label="Email (compte)"
                            type="email"
                            disabled
                            hint="L'email du compte ne peut pas etre modifie"
                        />
                        <BaseInput
                            v-model="profileForm.publicEmail"
                            label="Email public"
                            type="email"
                            placeholder="contact@exemple.com"
                        />
                    </div>
                    <BaseInput
                        v-model="profileForm.phoneNumber"
                        label="Telephone"
                        type="tel"
                        placeholder="+33 6 00 00 00 00"
                    />

                    <BaseDivider label="Reseaux sociaux" spacing="lg" />
                    <BaseInput
                        v-model="profileForm.linkedin"
                        label="LinkedIn"
                        type="url"
                        placeholder="https://linkedin.com/in/..."
                    >
                        <template #icon-left>
                            <BaseIcon name="linkedin" :size="16" />
                        </template>
                    </BaseInput>
                    <BaseInput
                        v-model="profileForm.github"
                        label="GitHub"
                        type="url"
                        placeholder="https://github.com/..."
                    >
                        <template #icon-left>
                            <BaseIcon name="github" :size="16" />
                        </template>
                    </BaseInput>
                    <BaseInput
                        v-model="profileForm.twitter"
                        label="Twitter / X"
                        type="url"
                        placeholder="https://twitter.com/..."
                    >
                        <template #icon-left>
                            <BaseIcon name="twitter" :size="16" />
                        </template>
                    </BaseInput>

                    <div class="form-actions">
                        <BaseButton type="submit" variant="primary" :loading="isUpdatingProfile">
                            <template #icon-left>
                                <BaseIcon name="save" :size="16" />
                            </template>
                            {{ isUpdatingProfile ? 'Enregistrement...' : 'Enregistrer' }}
                        </BaseButton>
                        <Transition name="fade">
                            <Badge
                                v-if="profileMessage"
                                :variant="profileMessage.type === 'success' ? 'success' : 'danger'"
                                :icon="profileMessage.type === 'success' ? 'check' : 'x'"
                            >
                                {{ profileMessage.text }}
                            </Badge>
                        </Transition>
                    </div>
                </form>
            </div>

            <div class="admin-card">
                <div class="admin-card__header">
                    <h2 class="admin-card__title">Securite</h2>
                </div>
                <form @submit.prevent="changePassword">
                    <BaseInput
                        v-model="passwordForm.currentPassword"
                        label="Mot de passe actuel"
                        :type="showCurrentPassword ? 'text' : 'password'"
                        autocomplete="current-password"
                    >
                        <template #icon-right>
                            <button
                                type="button"
                                class="password-toggle"
                                :aria-label="showCurrentPassword ? 'Masquer' : 'Afficher'"
                                @click="showCurrentPassword = !showCurrentPassword"
                            >
                                <BaseIcon :name="showCurrentPassword ? 'eye-off' : 'eye'" :size="18" />
                            </button>
                        </template>
                    </BaseInput>

                    <BaseInput
                        v-model="passwordForm.newPassword"
                        label="Nouveau mot de passe"
                        :type="showNewPassword ? 'text' : 'password'"
                        autocomplete="new-password"
                    >
                        <template #icon-right>
                            <button
                                type="button"
                                class="password-toggle"
                                :aria-label="showNewPassword ? 'Masquer' : 'Afficher'"
                                @click="showNewPassword = !showNewPassword"
                            >
                                <BaseIcon :name="showNewPassword ? 'eye-off' : 'eye'" :size="18" />
                            </button>
                        </template>
                    </BaseInput>

                    <ProgressBar
                        v-if="passwordForm.newPassword"
                        :value="passwordStrengthValue"
                        :variant="passwordStrengthVariant"
                        :label="'Force: ' + passwordStrengthText"
                        size="sm"
                        custom-class="password-strength-bar"
                    />

                    <BaseInput
                        v-model="passwordForm.confirmPassword"
                        label="Confirmer"
                        type="password"
                        autocomplete="new-password"
                        :error="passwordMismatchError"
                    />

                    <div class="form-actions">
                        <BaseButton
                            type="submit"
                            variant="primary"
                            :disabled="!canChangePassword"
                            :loading="isChangingPassword"
                        >
                            <template #icon-left>
                                <BaseIcon name="lock" :size="16" />
                            </template>
                            {{ isChangingPassword ? 'Modification...' : 'Modifier' }}
                        </BaseButton>
                        <Transition name="fade">
                            <Badge
                                v-if="passwordMessage"
                                :variant="passwordMessage.type === 'success' ? 'success' : 'danger'"
                                :icon="passwordMessage.type === 'success' ? 'check' : 'x'"
                            >
                                {{ passwordMessage.text }}
                            </Badge>
                        </Transition>
                    </div>
                </form>
            </div>

            <div class="admin-card admin-card--full">
                <div class="admin-card__header">
                    <h2 class="admin-card__title">Contact public &amp; disponibilite</h2>
                    <small>Ces informations s'affichent dans le footer du site public.</small>
                </div>
                <form @submit.prevent="saveSiteSettings">
                    <div class="form-grid">
                        <BaseInput
                            v-model="siteForm.email"
                            label="Email public"
                            type="email"
                            placeholder="contact@exemple.com"
                            required
                        />
                        <BaseInput
                            v-model="siteForm.phone"
                            label="Telephone public"
                            type="tel"
                            placeholder="+33 6 00 00 00 00"
                        />
                    </div>

                    <BaseDivider label="Adresse" spacing="lg" />
                    <div class="form-grid">
                        <BaseInput v-model="siteForm.city" label="Ville" placeholder="Paris" />
                        <BaseInput v-model="siteForm.country" label="Pays" placeholder="France" />
                    </div>

                    <BaseDivider label="Disponibilite" spacing="lg" />
                    <div class="availability-row">
                        <BaseSwitch v-model="siteForm.isAvailable" label="Disponible pour de nouveaux projets" />
                    </div>
                    <BaseInput
                        v-model="siteForm.availabilityMessage"
                        label="Texte affiche dans le footer"
                        placeholder="Disponible pour de nouveaux projets"
                        hint="Laisser vide pour utiliser le texte par defaut selon le statut."
                    />

                    <div class="form-actions">
                        <BaseButton type="submit" variant="primary" :loading="isSavingSite">
                            <template #icon-left>
                                <BaseIcon name="save" :size="16" />
                            </template>
                            {{ isSavingSite ? 'Enregistrement...' : 'Enregistrer' }}
                        </BaseButton>
                        <Transition name="fade">
                            <Badge
                                v-if="siteMessage"
                                :variant="siteMessage.type === 'success' ? 'success' : 'danger'"
                                :icon="siteMessage.type === 'success' ? 'check' : 'x'"
                            >
                                {{ siteMessage.text }}
                            </Badge>
                        </Transition>
                    </div>
                </form>
            </div>

            <div class="admin-card">
                <SessionList />

                <div class="fingerprint-lock">
                    <div class="fingerprint-lock__icon">
                        <BaseIcon name="shield" :size="18" />
                    </div>
                    <div class="fingerprint-lock__body">
                        <div class="fingerprint-lock__title">Verrouillage par fingerprint</div>
                        <p class="fingerprint-lock__text">
                            Chaque session est liee a l'empreinte de votre navigateur. Un token utilise depuis un
                            autre appareil est automatiquement rejete.
                        </p>
                    </div>
                    <Badge variant="success" icon="check">Actif</Badge>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref, reactive, computed, onMounted, watch } from 'vue';

    import BaseButton from '@/components/base/BaseButton.vue';
    import BaseDivider from '@/components/base/BaseDivider.vue';
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import BaseInput from '@/components/base/BaseInput.vue';
    import BaseSwitch from '@/components/base/BaseSwitch.vue';
    import BaseTextarea from '@/components/base/BaseTextarea.vue';
    import { SessionList } from '@/components/feature/admin';
    import Avatar from '@/components/ui/Avatar.vue';
    import Badge from '@/components/ui/Badge.vue';
    import ProgressBar from '@/components/ui/ProgressBar.vue';
    import { useSeo } from '@/composables/seo/useSeo';
    import { authApi, useUpdateProfile, useUploadProfileAvatar, useLogout } from '@/services/api/modules/auth';
    import { useContactInfo, useContactInfoUpsert } from '@/services/api/modules/contact';
    import { formatDate } from '@/services/utils/date';
    import { useAuthStore } from '@/stores/auth';

    definePageMeta({ layout: 'admin', title: 'Parametres' });

    useSeo({
        title: 'Parametres',
        description: 'Configuration du profil et des preferences',
        noindex: true,
    });

    const authStore = useAuthStore();
    const updateProfileMutation = useUpdateProfile();
    const uploadAvatarMutation = useUploadProfileAvatar();
    const logoutMutation = useLogout();

    const avatarInput = ref<HTMLInputElement | null>(null);
    const isUpdatingProfile = updateProfileMutation.isPending;
    const isChangingPassword = ref(false);
    const isLoggingOut = logoutMutation.isPending;
    const showCurrentPassword = ref(false);
    const showNewPassword = ref(false);

    // Messages
    const profileMessage = ref<{ type: 'success' | 'error'; text: string } | null>(null);
    const passwordMessage = ref<{ type: 'success' | 'error'; text: string } | null>(null);
    const siteMessage = ref<{ type: 'success' | 'error'; text: string } | null>(null);

    // Forms
    const profileForm = reactive({
        firstName: '',
        lastName: '',
        position: '',
        bio: '',
        phoneNumber: '',
        publicEmail: '',
        linkedin: '',
        github: '',
        twitter: '',
    });

    const passwordForm = reactive({
        currentPassword: '',
        newPassword: '',
        confirmPassword: '',
    });

    const siteForm = reactive({
        id: undefined as number | undefined,
        email: '',
        phone: '',
        city: '',
        country: '',
        isAvailable: true,
        availabilityMessage: '',
    });

    // Contact info query + upsert mutation
    const { data: contactInfo } = useContactInfo();
    const contactInfoMutation = useContactInfoUpsert();
    const isSavingSite = contactInfoMutation.isPending;

    const passwordStrengthValue = computed(() => {
        const password = passwordForm.newPassword;
        if (!password) {
            return 0;
        }
        if (password.length < 6) {
            return 25;
        }
        if (password.length < 8) {
            return 50;
        }
        if (/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(password)) {
            return 100;
        }
        return 66;
    });

    const passwordStrengthVariant = computed(() => {
        if (passwordStrengthValue.value <= 25) {
            return 'danger';
        }
        if (passwordStrengthValue.value <= 50) {
            return 'warning';
        }
        return 'success';
    });

    const passwordStrengthText = computed(() => {
        if (passwordStrengthValue.value <= 25) {
            return 'Faible';
        }
        if (passwordStrengthValue.value <= 50) {
            return 'Moyen';
        }
        return 'Fort';
    });

    const passwordMismatchError = computed(() => {
        if (passwordForm.confirmPassword && passwordForm.newPassword !== passwordForm.confirmPassword) {
            return 'Les mots de passe ne correspondent pas';
        }
        return '';
    });

    const canChangePassword = computed(() => {
        return (
            passwordForm.currentPassword
            && passwordForm.newPassword
            && passwordForm.newPassword === passwordForm.confirmPassword
            && passwordForm.newPassword.length >= 6
        );
    });

    const triggerAvatarUpload = () => avatarInput.value?.click();

    const showMessage = (
        msgRef: typeof profileMessage | typeof passwordMessage,
        type: 'success' | 'error',
        text: string,
    ) => {
        msgRef.value = { type, text };
        setTimeout(() => {
            msgRef.value = null;
        }, 3000);
    };

    const handleAvatarChange = (event: Event) => {
        const file = (event.target as HTMLInputElement).files?.[0];
        if (!file) {
            return;
        }

        const formData = new FormData();
        formData.append('avatar', file);

        uploadAvatarMutation.mutate(formData, {
            onSuccess: () => showMessage(profileMessage, 'success', 'Avatar mis a jour'),
            onError: () => showMessage(profileMessage, 'error', 'Erreur lors du telechargement'),
        });
    };

    const updateProfile = () => {
        updateProfileMutation.mutate(
            {
                firstName: profileForm.firstName,
                lastName: profileForm.lastName,
                position: profileForm.position,
                bio: profileForm.bio,
                phoneNumber: profileForm.phoneNumber,
                publicEmail: profileForm.publicEmail,
                linkedin: profileForm.linkedin,
                github: profileForm.github,
                twitter: profileForm.twitter,
            },
            {
                onSuccess: () => showMessage(profileMessage, 'success', 'Profil mis a jour'),
                onError: () => showMessage(profileMessage, 'error', 'Erreur lors de la mise a jour'),
            },
        );
    };

    const changePassword = async () => {
        if (!canChangePassword.value) {
            return;
        }
        isChangingPassword.value = true;

        try {
            await authApi.changePassword({
                old_password: passwordForm.currentPassword,
                new_password: passwordForm.newPassword,
            });

            passwordForm.currentPassword = '';
            passwordForm.newPassword = '';
            passwordForm.confirmPassword = '';
            showMessage(passwordMessage, 'success', 'Mot de passe modifie');
        } catch {
            showMessage(passwordMessage, 'error', 'Mot de passe incorrect');
        } finally {
            isChangingPassword.value = false;
        }
    };

    const handleLogout = () => {
        logoutMutation.mutate(undefined, {
            onSettled: () => {
                navigateTo('/admin/login', { replace: true });
            },
        });
    };

    const initForm = () => {
        if (authStore.user) {
            profileForm.firstName = authStore.user.firstName || '';
            profileForm.lastName = authStore.user.lastName || '';
            profileForm.position = authStore.user.position || '';
            profileForm.bio = authStore.user.bio || '';
            profileForm.phoneNumber = authStore.user.phoneNumber || '';
            profileForm.publicEmail = authStore.user.publicEmail || '';
            profileForm.linkedin = authStore.user.linkedin || '';
            profileForm.github = authStore.user.github || '';
            profileForm.twitter = authStore.user.twitter || '';
        }
    };

    const initSiteForm = () => {
        const info = contactInfo.value;
        if (!info) {
            return;
        }
        siteForm.id = info.id;
        siteForm.email = info.email || '';
        siteForm.phone = info.phone || '';
        siteForm.city = info.address?.city || '';
        siteForm.country = info.address?.country || '';
        siteForm.isAvailable = info.availability?.status === 'available';
        siteForm.availabilityMessage = info.availability?.message || '';
    };

    watch(contactInfo, () => initSiteForm(), { immediate: true });

    const saveSiteSettings = () => {
        contactInfoMutation.mutate(
            {
                id: siteForm.id,
                email: siteForm.email,
                phone: siteForm.phone,
                address: {
                    city: siteForm.city,
                    country: siteForm.country,
                },
                availability: {
                    status: siteForm.isAvailable ? 'available' : 'unavailable',
                    message: siteForm.availabilityMessage,
                },
            },
            {
                onSuccess: (updated) => {
                    siteForm.id = updated.id;
                    showMessage(siteMessage, 'success', 'Informations enregistrees');
                },
                onError: () => showMessage(siteMessage, 'error', 'Erreur lors de l\'enregistrement'),
            },
        );
    };

    onMounted(() => {
        initForm();
        initSiteForm();
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/functions' as func;

    .admin-page {
        &__header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: vars.$spacing-lg;
            gap: vars.$spacing-md;

            @include mix.responsive(mobile) {
                flex-direction: column;
            }
        }

        &__title {
            font-weight: vars.$font-weight-bold;
            margin-bottom: 4px;
            letter-spacing: -0.02em;
        }

        &__subtitle {
            color: vars.$text-muted;
        }
    }

    .settings-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: vars.$spacing-lg;

        @include mix.responsive(tablet) {
            grid-template-columns: 1fr;
        }
    }

    .admin-card {
        background: vars.$white;
        border-radius: 16px;
        border: 1px solid vars.$admin-border;
        padding: vars.$spacing-lg;
        box-shadow:
            0 1px 3px func.color-alpha(vars.$black, 0.02),
            0 4px 12px func.color-alpha(vars.$black, 0.02);

        &--full {
            grid-column: 1 / -1;
        }

        &__header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: vars.$spacing-lg;
            padding-bottom: vars.$spacing-md;
            border-bottom: 1px solid vars.$admin-border;
        }

        &__title {
            font-weight: vars.$font-weight-semibold;
        }

        form {
            display: flex;
            flex-direction: column;
        }
    }

    /* Profile Header */
    .profile-header {
        display: flex;
        align-items: center;
        gap: vars.$spacing-lg;
        margin-bottom: vars.$spacing-md;
    }

    .profile-avatar {
        position: relative;
        cursor: pointer;
        border-radius: vars.$border-radius-lg;
        overflow: hidden;
        flex-shrink: 0;

        &:hover .profile-avatar__overlay {
            opacity: 1;
        }

        &__overlay {
            position: absolute;
            inset: 0;
            background: func.color-alpha(vars.$black, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            color: vars.$white;
            opacity: 0;
            transition: opacity 0.2s ease;
        }

        &__input {
            display: none;
        }
    }

    .profile-info {
        h3 {
            font-weight: vars.$font-weight-semibold;
            margin-bottom: vars.$spacing-xxxs;
        }

        p {
            color: vars.$text-muted;
            margin-bottom: vars.$spacing-xxxs;
        }

        &__date {
            color: vars.$text-muted;
        }
    }

    /* Availability row */
    .availability-row {
        margin-bottom: vars.$spacing-sm;
    }

    /* Form Layout */
    .form-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: vars.$spacing-md;

        @include mix.responsive(mobile) {
            grid-template-columns: 1fr;
        }
    }

    .form-actions {
        display: flex;
        align-items: center;
        gap: vars.$spacing-md;
    }

    /* Password Toggle */
    .password-toggle {
        background: none;
        border: none;
        padding: 0;
        cursor: pointer;
        color: vars.$text-muted;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: color 0.2s ease;

        &:hover {
            color: vars.$text-primary;
        }
    }

    // Password Strength Bar override
    :deep(.password-strength-bar) {
        margin-top: calc(-1 * vars.$spacing-xs);
        margin-bottom: vars.$spacing-xs;
    }

    /* Fingerprint lock info */
    .fingerprint-lock {
        display: flex;
        align-items: flex-start;
        gap: vars.$spacing-sm;
        margin-top: vars.$spacing-lg;
        padding: vars.$spacing-md;
        background-color: func.color-alpha(vars.$primary-color, 0.04);
        border: 1px solid func.color-alpha(vars.$primary-color, 0.12);
        border-radius: vars.$border-radius-md;

        &__icon {
            color: vars.$primary-color;
            flex-shrink: 0;
            margin-top: 2px;
        }

        &__body {
            flex: 1;
            min-width: 0;
        }

        &__title {
            font-weight: vars.$font-weight-semibold;
            margin-bottom: 2px;
        }

        &__text {
            color: vars.$text-muted;
            font-size: 13px;
            margin: 0;
        }
    }

    /* Transitions */
    .fade-enter-active,
    .fade-leave-active {
        transition: opacity 0.2s ease;
    }

    .fade-enter-from,
    .fade-leave-to {
        opacity: 0;
    }
</style>
