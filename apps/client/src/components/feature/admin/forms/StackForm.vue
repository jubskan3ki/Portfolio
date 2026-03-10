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
                id="website"
                v-model="form.website"
                label="Site officiel"
                type="url"
                placeholder="https://vuejs.org"
            />
        </div>

        <BaseTextarea
            id="description"
            v-model="form.description"
            label="Description"
            placeholder="Décrivez brièvement votre expérience avec cette technologie..."
            :rows="3"
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
    import { toSelectOptions, findItemByIdOrName, buildImageUrl } from '@/composables/forms/useFormUtils';
    import { useAlert } from '@/composables/ui/useAlert';
    import { ERROR_MESSAGES, SUCCESS_MESSAGES } from '@/config/errorMessages';
    import { ADMIN_ROUTES } from '@/config/routes';
    import { stacksApi, stackKeys, useStackCategories, useCreateStackCategory } from '@/services/api/modules/stacks';
    import { createFormData } from '@/services/utils/formDataBuilder';
    import { usePaginatedData } from '@/services/utils/pagination';

    import type { StackFormProps } from '@/types/components/admin';
    import type { StackCategory, StackDetail } from '@/types/feature/stacks';

    // Props

    const props = defineProps<StackFormProps>();
    const { success: showSuccess, error: showError } = useAlert();

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
            name: string;
            category: string | number;
            proficiency: number;
            started_date: string;
            description: string;
            website: string;
            logo: File | null;
            is_featured: boolean;
        },
        StackDetail
    >({
        id: computed(() => props.id),
        initialValues: {
            name: '',
            category: '' as string | number,
            proficiency: 80,
            started_date: '',
            description: '',
            website: '',
            logo: null as File | null,
            is_featured: false,
        },
        validate: (values) => {
            const errs: Partial<Record<string, string>> = {};
            if (!values.name?.trim()) {
                errs.name = 'Le nom est requis';
            }
            if (!values.category) {
                errs.category = 'La catégorie est requise';
            }
            if (values.proficiency < 0 || values.proficiency > 100) {
                errs.proficiency = 'La maîtrise doit être entre 0 et 100';
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
            ctx.setFieldValue('description', data.description ?? '');
            ctx.setFieldValue('website', data.website ?? '');
            ctx.setFieldValue('is_featured', data.isFeatured ?? false);
            ctx.setFieldValue('proficiency', Math.round((data.level || 2.5) * 20));
            ctx.setFieldValue('started_date', data.startedDate ?? '');

            if (data.category) {
                ctx.setRawValue('category', data.category);
            }
            if (data.logo) {
                ctx.setPreviewImage(buildImageUrl(data.logo));
            }
        },
        buildPayload: (formValues) => {
            const level = Math.max(0.5, Math.min(5.0, formValues.proficiency / 20));

            return createFormData()
                .append('name', formValues.name)
                .append('category', String(formValues.category))
                .append('level', level.toFixed(1))
                .appendBoolean('is_featured', formValues.is_featured)
                .appendIfPresent('started_date', formValues.started_date)
                .appendIfPresent('description', formValues.description)
                .appendIfPresent('website', formValues.website)
                .appendFile('logo', formValues.logo)
                .build();
        },
        notFoundMessage: `La stack "${props.id}" n'existe pas ou a été supprimée.`,
        loadErrorMessage: 'Impossible de charger la stack. Veuillez réessayer.',
    });

    // Données Externes

    const { data: categoriesData, refetch: refetchCategories } = useStackCategories();
    const createCategoryMutation = useCreateStackCategory();

    const categories = usePaginatedData<StackCategory>(categoriesData);
    const categoryOptions = computed(() => toSelectOptions(categories.value));

    // Handlers

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
        getRawValue: () => getRawValue<string>('category'),
        isUnmatched: () => !form.category,
        match: (items, raw) => findItemByIdOrName(items, raw)?.id,
        setFieldValue: (val) => setFieldValue('category', val as string | number),
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/mixins' as mix;

    .admin-form__row {
        @include mix.admin-form-row;
    }
</style>
