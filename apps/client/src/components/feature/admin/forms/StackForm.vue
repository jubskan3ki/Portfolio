<template>
    <AdminFormLayout
        :title="isEditMode ? 'Modifier la stack' : 'Nouvelle stack'"
        :subtitle="isEditMode && entity ? entity.name : 'Ajoutez une nouvelle technologie à votre portfolio'"
        :loading="isLoading"
        loading-text="Chargement de la stack..."
        :error="pageError"
        error-title="Erreur de chargement"
        :back-url="ADMIN_ROUTES.STACKS.path"
        cancel-text="Annuler"
        :submit-text="isEditMode ? 'Enregistrer' : 'Créer la stack'"
        :submitting-text="isEditMode ? 'Enregistrement...' : 'Création...'"
        :submitting="isSubmitting"
        @submit="onSubmit"
        @retry="fetchData"
    >
        <template #header-actions>
            <BaseButton v-if="isEditMode && entity" :to="`/stacks/${entity.slug}`" target="_blank" variant="outline">
                <template #icon-left>
                    <BaseIcon name="external-link" :size="16" />
                </template>
                Voir
            </BaseButton>
        </template>

        <BaseInput
            id="name"
            v-model="form.name"
            label="Nom de la technologie"
            placeholder="Ex: Vue.js, Python, Docker..."
            required
            :error="errors.name"
            @input="onNameChange"
        />

        <BaseInput
            id="slug"
            v-model="form.slug"
            label="Slug"
            placeholder="nom-de-la-techno"
            :hint="`URL: /stacks/${form.slug || 'slug'}`"
        />

        <div class="admin-form__row">
            <BaseSelect
                id="category"
                v-model="form.category"
                label="Catégorie"
                placeholder="Sélectionner une catégorie"
                :options="categoryOptions"
                :initial-value="entity?.category"
                required
                :error="errors.category"
                allow-create
                create-label="Créer une catégorie"
                create-placeholder="Nom de la catégorie"
                @create="handleCreateCategory"
            />

            <BaseInput
                id="proficiency"
                v-model.number="form.proficiency"
                label="Niveau de maîtrise (%)"
                type="number"
                :min="0"
                :max="100"
                placeholder="80"
                required
                :error="errors.proficiency"
            />
        </div>

        <div class="admin-form__row">
            <BaseInput
                id="started_date"
                v-model="form.started_date"
                label="Date de début d'utilisation"
                type="date"
                hint="Depuis quand utilisez-vous cette technologie ?"
            />

            <BaseInput
                id="first_release"
                v-model="form.first_release"
                label="Première version"
                placeholder="Ex: 2014"
            />
        </div>

        <div class="admin-form__row">
            <BaseInput
                id="website"
                v-model="form.website"
                label="Site officiel"
                type="url"
                placeholder="https://vuejs.org"
                :error="errors.website"
            />

            <BaseInput
                id="website_label"
                v-model="form.website_label"
                label="Libellé du site"
                placeholder="Ex: Documentation"
                :maxlength="50"
            />
        </div>

        <div class="admin-form__row">
            <BaseInput
                id="github"
                v-model="form.github"
                label="Dépôt GitHub"
                type="url"
                placeholder="https://github.com/vuejs/core"
                :error="errors.github"
            />

            <BaseInput
                id="github_label"
                v-model="form.github_label"
                label="Libellé GitHub"
                placeholder="Ex: Code source"
                :maxlength="50"
            />
        </div>

        <BaseInput id="license" v-model="form.license" label="Licence" placeholder="Ex: MIT, Apache 2.0" />

        <BaseTextarea
            id="description"
            v-model="form.description"
            label="Description"
            placeholder="Décrivez brièvement votre expérience avec cette technologie..."
            :rows="3"
        />

        <BaseTextarea
            id="tags"
            v-model="form.tags"
            label="Tags"
            placeholder="Un tag par ligne..."
            :rows="4"
            hint="Un tag par ligne"
        />

        <BaseTextarea
            id="content"
            v-model="form.content"
            label="Détails techniques"
            placeholder="Contenu détaillé (Markdown supporté)..."
            :rows="10"
            hint="Markdown supporté (titres, listes, tableaux, code, blockquotes...)"
        />

        <BaseFileUpload
            v-model="form.logo"
            :preview="previewImage"
            label="Icône / Logo"
            accept="image/*,.svg"
            :max-size="2"
            placeholder-text="Cliquez pour uploader une icône"
            hint="PNG, SVG recommandé (64x64 ou plus)"
            @update:preview="setPreviewImage"
        />

        <BaseSwitch v-model="form.is_featured" label="Technologie mise en avant" />

        <details class="admin-form__seo">
            <summary class="admin-form__seo-summary">
                <BaseIcon name="search" :size="16" />
                Référencement (SEO)
            </summary>
            <div class="admin-form__seo-content">
                <BaseInput
                    id="seo_title"
                    v-model="form.seo_title"
                    label="Titre SEO"
                    placeholder="Titre optimisé pour les moteurs de recherche"
                    :maxlength="70"
                    :hint="`${form.seo_title.length}/70 caractères | utilise le nom si vide`"
                />

                <BaseTextarea
                    id="meta_description"
                    v-model="form.meta_description"
                    label="Meta description"
                    placeholder="Résumé affiché dans les résultats de recherche..."
                    :rows="3"
                    :maxlength="160"
                    :hint="`${form.meta_description.length}/160 caractères | utilise la description si vide`"
                />
            </div>
        </details>
    </AdminFormLayout>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    import BaseButton from '@/components/base/BaseButton.vue';
    import BaseFileUpload from '@/components/base/BaseFileUpload.vue';
    import BaseIcon from '@/components/base/BaseIcon.vue';
    import BaseInput from '@/components/base/BaseInput.vue';
    import BaseSelect from '@/components/base/BaseSelect.vue';
    import BaseSwitch from '@/components/base/BaseSwitch.vue';
    import BaseTextarea from '@/components/base/BaseTextarea.vue';
    import AdminFormLayout from '@/components/feature/admin/AdminFormLayout.vue';
    import { useDeferredMatch } from '@/composables/data/useDeferredMatch';
    import { useForm } from '@/composables/forms/useForm';
    import {
        toSelectOptions,
        findItemByIdOrName,
        linesToArray,
        arrayToLines,
        isValidHttpUrl,
    } from '@/composables/forms/useFormUtils';
    import { generateSlug } from '@/composables/forms/useSlugGenerator';
    import { useAlert } from '@/composables/ui/useAlert';
    import { ERROR_MESSAGES, SUCCESS_MESSAGES } from '@/config/errorMessages';
    import { ADMIN_ROUTES } from '@/config/routes';
    import { stacksApi, stackKeys, useStackCategories, useCreateStackCategory } from '@/services/api/modules/stacks';
    import { createFormData } from '@/services/utils/formDataBuilder';
    import { usePaginatedData } from '@/services/utils/pagination';

    import type { StackFormProps } from '@/types/components/admin';
    import type { StackCategory, StackDetail } from '@/types/feature/stacks';

    const props = defineProps<StackFormProps>();
    const { success: showSuccess, error: showError } = useAlert();

    const {
        isEditMode,
        isLoading,
        isSubmitting,
        pageError,
        entity,
        form,
        errors,
        setFieldValue,
        previewImage,
        setPreviewImage,
        getRawValue,
        onSubmit,
        fetchData,
    } = useForm<
        {
            name: string;
            slug: string;
            category: string | number;
            proficiency: number;
            started_date: string;
            first_release: string;
            description: string;
            website: string;
            website_label: string;
            github: string;
            github_label: string;
            license: string;
            tags: string;
            content: string;
            logo: File | null;
            is_featured: boolean;
            seo_title: string;
            meta_description: string;
        },
        StackDetail
    >({
        id: computed(() => props.id),
        initialValues: {
            name: '',
            slug: '',
            category: '' as string | number,
            proficiency: 80,
            started_date: '',
            first_release: '',
            description: '',
            website: '',
            website_label: '',
            github: '',
            github_label: '',
            license: '',
            tags: '',
            content: '',
            logo: null as File | null,
            is_featured: false,
            seo_title: '',
            meta_description: '',
        },
        validate: (values) => {
            const errs: Partial<Record<string, string>> = {};
            if (!values.name?.trim()) {
                errs.name = 'Le nom est requis';
            }
            if (!values.category) {
                errs.category = 'La catégorie est requise';
            }
            if (!Number.isFinite(values.proficiency)) {
                errs.proficiency = 'La maîtrise est requise (0 à 100)';
            } else if (values.proficiency < 0 || values.proficiency > 100) {
                errs.proficiency = 'La maîtrise doit être entre 0 et 100';
            }
            if (!isValidHttpUrl(values.website)) {
                errs.website = 'URL invalide (http:// ou https:// attendu)';
            }
            if (!isValidHttpUrl(values.github)) {
                errs.github = 'URL invalide (http:// ou https:// attendu)';
            }
            return errs;
        },
        api: {
            create: (payload) => stacksApi.createWithForm(payload as FormData),
            update: (id, payload) => stacksApi.updateWithForm(id, payload as FormData),
            fetch: (id) => stacksApi.getBySlug(id),
        },
        queryKeys: [stackKeys.all],
        onSuccess: {
            route: ADMIN_ROUTES.STACKS.path,
            messages: { create: SUCCESS_MESSAGES.STACK.CREATED, update: SUCCESS_MESSAGES.STACK.UPDATED },
        },
        mapEntityToForm: (data, ctx) => {
            ctx.setFieldValue('name', data.name);
            ctx.setFieldValue('slug', data.slug ?? '');
            ctx.setFieldValue('description', data.description ?? '');
            ctx.setFieldValue('website', data.website ?? '');
            ctx.setFieldValue('website_label', data.websiteLabel ?? '');
            ctx.setFieldValue('github', data.github ?? '');
            ctx.setFieldValue('github_label', data.githubLabel ?? '');
            ctx.setFieldValue('first_release', data.firstRelease ?? '');
            ctx.setFieldValue('license', data.license ?? '');
            ctx.setFieldValue('tags', arrayToLines(data.tags));
            ctx.setFieldValue('content', data.content ?? '');
            ctx.setFieldValue('is_featured', data.isFeatured ?? false);
            ctx.setFieldValue('proficiency', Math.round((data.level || 2.5) * 20));
            ctx.setFieldValue('started_date', data.startedDate ?? '');
            ctx.setFieldValue('seo_title', data.seoTitle ?? '');
            ctx.setFieldValue('meta_description', data.metaDescription ?? '');

            if (data.category) {
                ctx.setRawValue('category', data.category);
            }
            if (data.logo) {
                ctx.setPreviewImage(data.logo);
            }
        },
        buildPayload: (formValues) => {
            const level = Math.max(0.5, Math.min(5.0, formValues.proficiency / 20));

            return createFormData()
                .append('name', formValues.name)
                .append('category', String(formValues.category))
                .append('level', level.toFixed(1))
                .append('seo_title', formValues.seo_title)
                .append('meta_description', formValues.meta_description)
                .appendBoolean('is_featured', formValues.is_featured)
                .appendIfPresent('slug', formValues.slug)
                .appendIfPresent('started_date', formValues.started_date)
                .appendIfPresent('first_release', formValues.first_release)
                .appendIfPresent('description', formValues.description)
                .appendIfPresent('website', formValues.website)
                .appendIfPresent('website_label', formValues.website_label)
                .appendIfPresent('github', formValues.github)
                .appendIfPresent('github_label', formValues.github_label)
                .appendIfPresent('license', formValues.license)
                .appendIfPresent('content', formValues.content)
                .appendArray('tags', linesToArray(formValues.tags))
                .appendFile('logo', formValues.logo)
                .build();
        },
        notFoundMessage: `La stack "${props.id}" n'existe pas ou a été supprimée.`,
        loadErrorMessage: 'Impossible de charger la stack. Veuillez réessayer.',
    });

    const { data: categoriesData, refetch: refetchCategories } = useStackCategories();
    const createCategoryMutation = useCreateStackCategory();

    const categories = usePaginatedData<StackCategory>(categoriesData);
    const categoryOptions = computed(() => toSelectOptions(categories.value));

    const onNameChange = () => {
        if (!isEditMode.value) {
            setFieldValue('slug', generateSlug(form.name));
        }
    };

    const handleCreateCategory = async (name: string) => {
        try {
            const newCategory = await createCategoryMutation.mutateAsync({ name });
            setFieldValue('category', newCategory.id);
            refetchCategories();
            showSuccess(SUCCESS_MESSAGES.CATEGORY.CREATED, 'Catégorie');
        } catch {
            showError(ERROR_MESSAGES.CATEGORY.CREATE_FAILED, 'Erreur');
        }
    };

    useDeferredMatch({
        source: categories,
        getRawValue: () => getRawValue<string>('category'),
        isUnmatched: () => !form.category,
        match: (items, raw) => findItemByIdOrName(items, raw)?.id,
        setFieldValue: (val) => setFieldValue('category', val as string | number),
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/mixins' as mix;
    @use '@/styles/abstracts/variables' as vars;

    .admin-form__row {
        @include mix.admin-form-row;
    }

    .admin-form__seo {
        margin-top: vars.$spacing-md;
        border: 1px solid vars.$border-color;
        border-radius: vars.$border-radius-md;
        background-color: vars.$bg-primary;
    }

    .admin-form__seo-summary {
        display: flex;
        align-items: center;
        gap: vars.$spacing-xs;
        padding: vars.$spacing-sm vars.$spacing-md;
        cursor: pointer;
        font-weight: vars.$font-weight-medium;
        color: vars.$text-primary;
        list-style: none;
        user-select: none;

        &::-webkit-details-marker {
            display: none;
        }

        &::after {
            content: '+';
            margin-left: auto;
            font-size: 1.25rem;
            line-height: 1;
            color: vars.$text-muted;
        }
    }

    details[open] .admin-form__seo-summary::after {
        content: '−';
    }

    .admin-form__seo-content {
        padding: vars.$spacing-sm vars.$spacing-md vars.$spacing-md;
        border-top: 1px solid vars.$border-color;
    }
</style>
