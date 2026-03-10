<template>
    <AdminFormLayout
        :title="isEditMode ? 'Modifier le projet' : 'Nouveau projet'"
        :subtitle="isEditMode && entity ? entity.title : 'Ajoutez un nouveau projet à votre portfolio'"
        :loading="isLoading"
        loading-text="Chargement du projet..."
        :error="pageError"
        error-title="Erreur de chargement"
        :back-url="ADMIN_ROUTES.PROJECTS.path"
        cancel-text="Annuler"
        :submit-text="isEditMode ? 'Enregistrer' : 'Créer le projet'"
        :submitting-text="isEditMode ? 'Enregistrement...' : 'Création...'"
        :submitting="isSubmitting"
        @submit="onSubmit"
        @retry="fetchData"
    >
        <template #header-actions>
            <BaseButton v-if="isEditMode && entity" :to="`/projects/${entity.slug}`" target="_blank" variant="outline">
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
            placeholder="Nom du projet"
            required
            :error="errors.title"
            @input="onTitleChange"
        />

        <BaseInput
            id="slug"
            v-model="form.slug"
            label="Slug"
            placeholder="nom-du-projet"
            required
            :error="errors.slug"
            :hint="`URL: /projects/${form.slug || 'slug'}`"
        />

        <BaseTextarea
            id="description"
            v-model="form.description"
            label="Description courte"
            placeholder="Décrivez brièvement votre projet..."
            :rows="3"
            required
            :error="errors.description"
        />

        <BaseTextarea
            id="long_description"
            v-model="form.long_description"
            label="Description détaillée"
            placeholder="Description complète du projet (Markdown supporté)..."
            :rows="8"
        />

        <div class="admin-form__row">
            <BaseSelect
                id="category"
                v-model="form.category"
                label="Catégorie"
                placeholder="Sélectionner une catégorie"
                :options="categoryOptions"
                required
                :error="errors.category"
                allow-create
                create-label="Créer une catégorie"
                create-placeholder="Nom de la catégorie"
                @create="handleCreateCategory"
            />

            <BaseSelect id="status" v-model="form.status" label="Statut" :options="statusOptions" />
        </div>

        <BaseMultiSelect
            v-model="form.technologies"
            label="Stacks utilisées"
            placeholder="Rechercher une technologie..."
            :options="stackOptions"
            show-images
            hint="Sélectionnez les technologies utilisées dans ce projet"
        />

        <div class="admin-form__row">
            <BaseInput
                id="demo_url"
                v-model="form.demo_url"
                label="URL Démo"
                type="url"
                placeholder="https://demo.example.com"
            />

            <BaseInput
                id="github_url"
                v-model="form.github_url"
                label="URL GitHub"
                type="url"
                placeholder="https://github.com/user/repo"
            />
        </div>

        <BaseInput
            id="documentation_url"
            v-model="form.documentation_url"
            label="URL Documentation"
            type="url"
            placeholder="https://docs.example.com"
        />

        <BaseFileUpload
            v-model="form.image"
            :preview="previewImage"
            label="Image du projet"
            accept="image/*"
            :max-size="5"
            placeholder-text="Cliquez pour uploader une image"
            hint="PNG, JPG jusqu'à 5MB"
            @update:preview="setPreviewImage"
        />

        <BaseSwitch v-model="form.is_featured" label="Projet vedette (affiché en priorité)" />
    </AdminFormLayout>
</template>

<script setup lang="ts">
    import { computed, ref } from 'vue';

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
    import { toSelectOptions, findItemByIdOrName, mapToIds, buildImageUrl } from '@/composables/forms/useFormUtils';
    import { generateSlug } from '@/composables/forms/useSlugGenerator';
    import { useAlert } from '@/composables/ui/useAlert';
    import { ERROR_MESSAGES, SUCCESS_MESSAGES } from '@/config/errorMessages';
    import { ADMIN_ROUTES } from '@/config/routes';
    import {
        projectsApi,
        projectKeys,
        useProjectCategories,
        useProjectStatuses,
        useCreateProjectCategory,
    } from '@/services/api/modules/projects';
    import { useStacks } from '@/services/api/modules/stacks';
    import { createFormData } from '@/services/utils/formDataBuilder';
    import { usePaginatedData } from '@/services/utils/pagination';

    import type { ProjectFormProps } from '@/types/components/admin';
    import type { AdminProject, AdminCategory } from '@/types/feature/admin';
    import type { Stack } from '@/types/feature/stacks';

    // Props

    const props = defineProps<ProjectFormProps>();
    const { success: showSuccess, error: showError } = useAlert();
    const slugManuallyEdited = ref(false);

    // Form

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
            description: string;
            long_description: string;
            category: string | number;
            status: string | number;
            technologies: Array<string | number>;
            demo_url: string;
            github_url: string;
            documentation_url: string;
            image: File | null;
            is_featured: boolean;
        },
        AdminProject
    >({
        id: computed(() => props.id),
        initialValues: {
            title: '',
            slug: '',
            description: '',
            long_description: '',
            category: '' as string | number,
            status: '' as string | number,
            technologies: [] as Array<string | number>,
            demo_url: '',
            github_url: '',
            documentation_url: '',
            image: null as File | null,
            is_featured: false,
        },
        validate: (values) => {
            const errs: Partial<Record<string, string>> = {};
            if (!values.title?.trim()) {
                errs.title = 'Le titre est requis';
            }
            if (!values.slug?.trim()) {
                errs.slug = 'Le slug est requis';
            }
            if (!values.description?.trim()) {
                errs.description = 'La description est requise';
            }
            if (!values.category) {
                errs.category = 'La catégorie est requise';
            }
            return errs;
        },
        api: {
            create: (payload) => projectsApi.createWithForm(payload as FormData),
            update: (id, payload) => projectsApi.updateWithForm(id, payload as FormData),
            fetch: (id) => projectsApi.getBySlug(id) as unknown as Promise<AdminProject>,
        },
        queryKeys: [projectKeys.all],
        onSuccess: {
            route: ADMIN_ROUTES.PROJECTS.path,
            messages: { create: SUCCESS_MESSAGES.PROJECT.CREATED, update: SUCCESS_MESSAGES.PROJECT.UPDATED },
        },
        mapEntityToForm: (data, ctx) => {
            ctx.setFieldValue('title', data.title);
            ctx.setFieldValue('slug', data.slug);
            ctx.setFieldValue('description', data.description || '');
            ctx.setFieldValue('long_description', data.longDescription ?? '');
            ctx.setFieldValue('status', data.status || 'completed');
            ctx.setFieldValue('demo_url', data.links?.demo || '');
            ctx.setFieldValue('github_url', data.links?.github || '');
            ctx.setFieldValue('documentation_url', data.links?.documentation || '');
            ctx.setFieldValue('is_featured', data.isFeatured ?? false);

            if (data.category) {
                ctx.setRawValue('category', data.category);
            }
            if (data.technologies) {
                ctx.setRawValue('technologies', data.technologies);
            }

            const thumbnail = data.thumbnail || data.image;
            if (thumbnail && typeof thumbnail === 'string') {
                ctx.setPreviewImage(buildImageUrl(thumbnail));
            }

            slugManuallyEdited.value = true;
        },
        buildPayload: (formValues) => {
            const links: Record<string, string> = {};
            if (formValues.demo_url) {
                links.demo = formValues.demo_url;
            }
            if (formValues.github_url) {
                links.github = formValues.github_url;
            }
            if (formValues.documentation_url) {
                links.documentation = formValues.documentation_url;
            }

            const techNames = formValues.technologies
                .map((techId) => stacks.value.find((s) => s.id === techId)?.name || '')
                .filter(Boolean);

            return createFormData()
                .append('title', formValues.title)
                .append('slug', formValues.slug)
                .append('description', formValues.description)
                .append('category', String(formValues.category))
                .appendBoolean('is_featured', formValues.is_featured)
                .appendIfPresent('longDescription', formValues.long_description)
                .appendIfPresent('status', typeof formValues.status === 'number' ? formValues.status : null)
                .appendArray('technologies', techNames.length > 0 ? techNames : null)
                .appendObject('links', Object.keys(links).length > 0 ? links : null)
                .appendFile('image', formValues.image)
                .build();
        },
        notFoundMessage: `Le projet "${props.id}" n'existe pas ou a été supprimé.`,
        loadErrorMessage: 'Impossible de charger le projet. Veuillez réessayer.',
    });

    // Données Externes

    const { data: categoriesData, refetch: refetchCategories } = useProjectCategories();
    const { data: statusesData } = useProjectStatuses();
    const { data: stacksData } = useStacks();
    const createCategoryMutation = useCreateProjectCategory();

    const categories = usePaginatedData<AdminCategory>(categoriesData);
    const statuses = usePaginatedData<{ id: number; name: string }>(statusesData);
    const stacks = usePaginatedData<Stack>(stacksData);

    const categoryOptions = computed(() => toSelectOptions(categories.value));

    const statusOptions = computed(() => {
        if (statuses.value.length === 0) {
            return [
                { value: 'completed', label: 'Terminé' },
                { value: 'in_progress', label: 'En cours' },
                { value: 'planned', label: 'Planifié' },
            ];
        }
        return toSelectOptions(statuses.value);
    });

    const stackOptions = computed(() =>
        stacks.value.map((stack) => ({
            value: stack.id,
            label: stack.name,
            image: stack.logo,
        })),
    );

    // Handlers

    const onTitleChange = () => {
        if (!slugManuallyEdited.value) {
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

    // Matching Différé

    useDeferredMatch({
        source: categories,
        getRawValue: () => getRawValue<AdminCategory | string>('category'),
        isUnmatched: () => !form.category,
        match: (items, raw) => findItemByIdOrName(items, raw)?.id,
        setFieldValue: (val) => setFieldValue('category', val as string | number),
    });

    useDeferredMatch({
        source: stacks,
        getRawValue: () => getRawValue<Array<{ id: number } | string>>('technologies'),
        isUnmatched: () => form.technologies.length === 0,
        match: (items, raw) => {
            const ids = mapToIds(raw, items);
            return ids.length ? ids : undefined;
        },
        setFieldValue: (val) => setFieldValue('technologies', val as Array<string | number>),
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/mixins' as mix;

    .admin-form__row {
        @include mix.admin-form-row;
    }
</style>
