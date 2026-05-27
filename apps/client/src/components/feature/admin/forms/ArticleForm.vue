<template>
    <AdminFormLayout
        :title="isEditMode ? 'Modifier l\'article' : 'Nouvel article'"
        :subtitle="isEditMode && entity ? entity.title : 'Créez un nouvel article de blog'"
        :loading="isLoading"
        loading-text="Chargement de l'article..."
        :error="pageError"
        error-title="Erreur de chargement"
        :back-url="ADMIN_ROUTES.ARTICLES.path"
        cancel-text="Annuler"
        :submit-text="isEditMode ? 'Enregistrer' : 'Créer l\'article'"
        :submitting-text="isEditMode ? 'Enregistrement...' : 'Création...'"
        :submitting="isSubmitting"
        @submit="onSubmit"
        @retry="fetchData"
    >
        <template #header-actions>
            <BaseButton v-if="isEditMode && entity" :to="`/blog/${entity.slug}`" target="_blank" variant="outline">
                <template #icon-left>
                    <BaseIcon name="external-link" :size="16" />
                </template>
                Voir
            </BaseButton>
        </template>

        <BaseInput
            id="title"
            v-model="form.title"
            label="Titre"
            placeholder="Titre de l'article"
            required
            :error="errors.title"
            @input="onTitleChange"
        />

        <BaseInput
            id="slug"
            v-model="form.slug"
            label="Slug"
            placeholder="titre-de-larticle"
            required
            :error="errors.slug"
            :hint="`URL: /blog/${form.slug || 'slug'}`"
        />

        <BaseTextarea
            id="excerpt"
            v-model="form.excerpt"
            label="Extrait"
            placeholder="Résumé court de l'article..."
            :rows="3"
        />

        <BaseTextarea
            id="content"
            v-model="form.content"
            label="Contenu"
            placeholder="Contenu de l'article en Markdown..."
            required
            :error="errors.content"
            :rows="12"
        />

        <div class="admin-form__row">
            <BaseSelect
                id="category"
                v-model="form.category"
                label="Catégorie"
                placeholder="Sélectionner une catégorie"
                :options="categoryOptions"
                :initial-value="entity?.category"
                allow-create
                create-label="Créer une catégorie"
                create-placeholder="Nom de la catégorie"
                @create="handleCreateCategory"
            />

            <BaseMultiSelect
                v-model="form.tags"
                label="Tags"
                placeholder="Rechercher ou créer un tag..."
                :options="tagOptions"
                :initial-value="entity?.tags"
                allow-create
                @create="handleCreateTag"
            />
        </div>

        <BaseFileUpload
            v-model="form.cover_image"
            :preview="previewImage"
            label="Image de couverture"
            accept="image/*"
            :max-size="5"
            placeholder-text="Cliquez pour uploader une image"
            hint="PNG, JPG jusqu'à 5MB"
            @update:preview="setPreviewImage"
        />

        <BaseSwitch v-model="form.is_published" :label="form.is_published ? 'Publié' : 'Brouillon'" />

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
                    :hint="`${form.seo_title.length}/70 caractères | utilise le titre si vide`"
                />

                <BaseTextarea
                    id="meta_description"
                    v-model="form.meta_description"
                    label="Meta description"
                    placeholder="Résumé affiché dans les résultats de recherche..."
                    :rows="3"
                    :maxlength="160"
                    :hint="`${form.meta_description.length}/160 caractères | utilise l'extrait si vide`"
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
    import BaseMultiSelect from '@/components/base/BaseMultiSelect.vue';
    import BaseSelect from '@/components/base/BaseSelect.vue';
    import BaseSwitch from '@/components/base/BaseSwitch.vue';
    import BaseTextarea from '@/components/base/BaseTextarea.vue';
    import AdminFormLayout from '@/components/feature/admin/AdminFormLayout.vue';
    import { useDeferredMatch } from '@/composables/data/useDeferredMatch';
    import { useForm } from '@/composables/forms/useForm';
    import { toSelectOptions, findItemByIdOrName } from '@/composables/forms/useFormUtils';
    import { generateSlug } from '@/composables/forms/useSlugGenerator';
    import { useAlert } from '@/composables/ui/useAlert';
    import { ERROR_MESSAGES, SUCCESS_MESSAGES } from '@/config/errorMessages';
    import { ADMIN_ROUTES } from '@/config/routes';
    import {
        articlesApi,
        articleKeys,
        useArticleCategories,
        useArticleTags,
        useCreateArticleCategory,
        useCreateArticleTag,
    } from '@/services/api/modules/articles';
    import { formatContentForApi, parseJsonContent } from '@/services/utils/contentParser';
    import { usePaginatedData } from '@/services/utils/pagination';

    import type { ArticleFormProps } from '@/types/components/admin';
    import type { MultiSelectOption } from '@/types/components/base';
    import type { ArticleDetail, Category, Tag } from '@/types/feature/blog';

    const props = defineProps<ArticleFormProps>();
    const { success: showSuccess, error: showError } = useAlert();

    // Form (useForm orchestre useFormState + useFormMutation + fetch + lifecycle)
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
            title: string;
            slug: string;
            excerpt: string;
            content: string;
            category: string | number;
            tags: Array<string | number>;
            cover_image: File | null;
            is_published: boolean;
            seo_title: string;
            meta_description: string;
        },
        ArticleDetail
    >({
        id: computed(() => props.id),
        initialValues: {
            title: '',
            slug: '',
            excerpt: '',
            content: '',
            category: '' as string | number,
            tags: [] as Array<string | number>,
            cover_image: null as File | null,
            is_published: false,
            seo_title: '',
            meta_description: '',
        },
        validate: (values) => {
            const errs: Partial<Record<string, string>> = {};
            if (!values.title?.trim()) {
                errs.title = 'Le titre est requis';
            }
            if (!values.slug?.trim()) {
                errs.slug = 'Le slug est requis';
            }
            if (!values.content?.trim()) {
                errs.content = 'Le contenu est requis';
            }
            return errs;
        },
        api: {
            create: (payload) => articlesApi.createWithForm(payload as FormData),
            update: (id, payload) => articlesApi.updateWithForm(id, payload as FormData),
            fetch: (id) => articlesApi.getBySlug(id),
        },
        queryKeys: [articleKeys.all],
        onSuccess: {
            route: ADMIN_ROUTES.ARTICLES.path,
            messages: { create: SUCCESS_MESSAGES.ARTICLE.CREATED, update: SUCCESS_MESSAGES.ARTICLE.UPDATED },
        },
        mapEntityToForm: (data, ctx) => {
            ctx.setFieldValue('title', data.title);
            ctx.setFieldValue('slug', data.slug);
            ctx.setFieldValue('excerpt', data.excerpt || '');
            ctx.setFieldValue('content', parseJsonContent(data.content));
            ctx.setFieldValue('is_published', data.isPublished ?? false);
            ctx.setFieldValue('seo_title', data.seoTitle ?? '');
            ctx.setFieldValue('meta_description', data.metaDescription ?? '');

            if (data.category) {
                ctx.setRawValue('category', data.category);
            }
            if (Array.isArray(data.tags)) {
                ctx.setRawValue('tags', data.tags);
            }
            if (data.image) {
                ctx.setPreviewImage(data.image);
            }
        },
        buildPayload: (formValues) => {
            const fd = new FormData();
            fd.append('title', formValues.title);
            fd.append('slug', formValues.slug);
            fd.append('excerpt', formValues.excerpt);
            fd.append('content', formatContentForApi(formValues.content));
            fd.append('is_published', String(formValues.is_published));
            fd.append('seo_title', formValues.seo_title);
            fd.append('meta_description', formValues.meta_description);

            if (formValues.category) {
                fd.append('category', String(formValues.category));
            }

            formValues.tags.forEach((tagId) => {
                if (!String(tagId).startsWith('new-')) {
                    fd.append('tags', String(tagId));
                }
            });

            if (formValues.cover_image instanceof File) {
                fd.append('image', formValues.cover_image, formValues.cover_image.name);
            }

            return fd;
        },
        notFoundMessage: `L'article "${props.id}" n'existe pas ou a été supprimé.`,
        loadErrorMessage: 'Impossible de charger l\'article. Veuillez réessayer.',
    });

    // Données Externes (Catégories & Tags)

    const { data: categoriesData, refetch: refetchCategories } = useArticleCategories();
    const { data: tagsData, refetch: refetchTags } = useArticleTags();
    const createCategoryMutation = useCreateArticleCategory();
    const createTagMutation = useCreateArticleTag();

    const categories = usePaginatedData<Category>(categoriesData);
    const tags = usePaginatedData<Tag>(tagsData);

    const categoryOptions = computed(() => toSelectOptions(categories.value));
    const tagOptions = computed(() => toSelectOptions(tags.value) as MultiSelectOption[]);

    // Handlers

    const onTitleChange = () => {
        if (!isEditMode.value) {
            setFieldValue('slug', generateSlug(form.title));
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

    const handleCreateTag = async (name: string) => {
        try {
            const newTag = await createTagMutation.mutateAsync({ name });
            form.tags.push(newTag.id);
            refetchTags();
            showSuccess(SUCCESS_MESSAGES.TAG.CREATED, 'Tag');
        } catch {
            showError(ERROR_MESSAGES.TAG.CREATE_FAILED, 'Erreur');
        }
    };

    // Matching Différé

    useDeferredMatch({
        source: categories,
        getRawValue: () => getRawValue<string | number>('category'),
        isUnmatched: () => !form.category,
        match: (items, raw) => findItemByIdOrName(items, raw)?.id,
        setFieldValue: (val) => setFieldValue('category', val as string | number),
    });

    useDeferredMatch({
        source: tags,
        getRawValue: () => getRawValue<Array<string | number>>('tags'),
        isUnmatched: () => form.tags.length === 0,
        match: (items, rawTags) => {
            const ids = rawTags
                .map((tag) => (typeof tag === 'string' ? findItemByIdOrName(items, tag)?.id : tag))
                .filter((id): id is number => typeof id === 'number');
            return ids.length ? ids : undefined;
        },
        setFieldValue: (val) => setFieldValue('tags', val as Array<string | number>),
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
