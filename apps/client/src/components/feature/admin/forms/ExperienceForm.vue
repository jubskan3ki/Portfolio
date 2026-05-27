<template>
    <AdminFormLayout
        :title="isEditMode ? 'Modifier l\'expérience' : 'Nouvelle expérience'"
        :subtitle="isEditMode ? 'Modifiez les informations' : 'Ajoutez une expérience'"
        :loading="isLoading"
        loading-text="Chargement de l'expérience..."
        :error="pageError"
        error-title="Erreur de chargement"
        :back-url="ADMIN_ROUTES.EXPERIENCES.path"
        cancel-text="Annuler"
        :submit-text="isEditMode ? 'Enregistrer' : 'Créer l\'expérience'"
        :submitting-text="isEditMode ? 'Enregistrement...' : 'Création...'"
        :submitting="isSubmitting"
        @submit="onSubmit"
        @retry="fetchData"
    >
        <BaseSelect
            id="type"
            v-model="form.type"
            label="Type d'expérience"
            placeholder="Sélectionner un type"
            :options="typeOptions"
            :initial-value="entity?.type"
            required
            :error="errors.type"
            allow-create
            create-label="Créer un type"
            create-placeholder="Nom du type (ex: Freelance)"
            @create="handleCreateType"
        />

        <BaseInput
            id="title"
            v-model="form.title"
            label="Titre du poste / Diplôme"
            placeholder="Ex: Développeur Full Stack, Master Informatique..."
            required
            :error="errors.title"
        />

        <BaseInput
            id="company"
            v-model="form.company"
            :label="isEducationType ? 'Établissement' : 'Entreprise'"
            :placeholder="isEducationType ? 'Ex: Université Paris-Saclay' : 'Ex: Google, Startup XYZ'"
            required
            :error="errors.company"
        />

        <BaseInput
            id="location"
            v-model="form.location"
            label="Localisation"
            placeholder="Ex: Paris, France"
            required
            :error="errors.location"
        />

        <div class="admin-form__row">
            <BaseInput
                id="start_date"
                v-model="form.start_date"
                label="Date de début"
                type="date"
                required
                :error="errors.start_date"
            />

            <BaseInput
                id="end_date"
                v-model="form.end_date"
                label="Date de fin"
                type="date"
                :disabled="form.is_current"
                :hint="form.is_current ? 'Non applicable (poste actuel)' : ''"
            />
        </div>

        <BaseSwitch
            v-model="form.is_current"
            label="Poste actuel / En cours"
            @update:model-value="handleCurrentChange"
        />

        <BaseTextarea
            id="description"
            v-model="form.description"
            label="Description"
            placeholder="Décrivez vos responsabilités, missions, réalisations..."
            :rows="5"
            required
            :error="errors.description"
        />

        <BaseMultiSelect
            v-model="form.technologies"
            label="Stacks utilisées"
            placeholder="Rechercher une technologie..."
            :options="stackOptions"
            :initial-value="entity?.technologies"
            show-images
            hint="Sélectionnez les technologies utilisées"
        />

        <BaseFileUpload
            v-model="form.logo"
            :preview="previewImage"
            label="Logo de l'entreprise / établissement"
            accept="image/*,.svg"
            :max-size="2"
            placeholder-text="Cliquez pour uploader un logo"
            hint="PNG, JPG, SVG recommandé"
            @update:preview="setPreviewImage"
        />
    </AdminFormLayout>
</template>

<script setup lang="ts">
    import { ref, computed, watch } from 'vue';

    import BaseFileUpload from '@/components/base/BaseFileUpload.vue';
    import BaseInput from '@/components/base/BaseInput.vue';
    import BaseMultiSelect from '@/components/base/BaseMultiSelect.vue';
    import BaseSelect from '@/components/base/BaseSelect.vue';
    import BaseSwitch from '@/components/base/BaseSwitch.vue';
    import BaseTextarea from '@/components/base/BaseTextarea.vue';
    import AdminFormLayout from '@/components/feature/admin/AdminFormLayout.vue';
    import { useDeferredMatch } from '@/composables/data/useDeferredMatch';
    import { useForm } from '@/composables/forms/useForm';
    import { toSelectOptions, mapToIds } from '@/composables/forms/useFormUtils';
    import { useAlert } from '@/composables/ui/useAlert';
    import { ERROR_MESSAGES, SUCCESS_MESSAGES } from '@/config/errorMessages';
    import { ADMIN_ROUTES } from '@/config/routes';
    import {
        experiencesApi,
        experienceKeys,
        useExperienceTypes,
        useCreateExperienceType,
    } from '@/services/api/modules/experiences';
    import { useStacks } from '@/services/api/modules/stacks';
    import { usePaginatedData } from '@/services/utils/pagination';

    import type { ExperienceFormProps } from '@/types/components/admin';
    import type { Experience, ExperienceType } from '@/types/feature/experience';
    import type { Stack } from '@/types/feature/stacks';

    const props = defineProps<ExperienceFormProps>();
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
            type: string | number;
            title: string;
            company: string;
            location: string;
            start_date: string;
            end_date: string;
            is_current: boolean;
            description: string;
            technologies: Array<string | number>;
            logo: File | null;
        },
        Experience
    >({
        id: computed(() => props.id),
        initialValues: {
            type: '' as string | number,
            title: '',
            company: '',
            location: '',
            start_date: '',
            end_date: '',
            is_current: false,
            description: '',
            technologies: [] as Array<string | number>,
            logo: null as File | null,
        },
        validate: (values) => {
            const errs: Partial<Record<string, string>> = {};
            if (!values.type) {
                errs.type = 'Le type est requis';
            }
            if (!values.title?.trim()) {
                errs.title = 'Le titre est requis';
            }
            if (!values.company?.trim()) {
                errs.company = 'L\'entreprise ou l\'établissement est requis';
            }
            if (!values.location?.trim()) {
                errs.location = 'La localisation est requise';
            }
            if (!values.start_date) {
                errs.start_date = 'La date de début est requise';
            }
            if (!values.description?.trim()) {
                errs.description = 'La description est requise';
            }
            return errs;
        },
        api: {
            create: (payload) => experiencesApi.createWithForm(payload as FormData),
            update: (id, payload) => experiencesApi.updateWithForm(id, payload as FormData),
            fetch: (id) => experiencesApi.getById(id),
        },
        queryKeys: [experienceKeys.all],
        onSuccess: {
            route: ADMIN_ROUTES.EXPERIENCES.path,
            messages: { create: SUCCESS_MESSAGES.EXPERIENCE.CREATED, update: SUCCESS_MESSAGES.EXPERIENCE.UPDATED },
        },
        mapEntityToForm: (data, ctx) => {
            ctx.setFieldValue('title', data.title);
            ctx.setFieldValue('company', data.company);
            ctx.setFieldValue('location', data.location);
            ctx.setFieldValue('description', data.description);
            ctx.setFieldValue('start_date', data.startDate || '');
            ctx.setFieldValue('end_date', data.endDate || '');
            ctx.setFieldValue('is_current', data.isCurrent ?? !data.endDate);

            if (data.type) {
                ctx.setRawValue('type', data.type);
            }
            if (data.technologies) {
                ctx.setRawValue('technologies', data.technologies);
            }
            if (data.logo) {
                ctx.setPreviewImage(data.logo);
            }
        },
        buildPayload: (formValues) => {
            const formData = new FormData();
            formData.append('type', String(formValues.type));
            formData.append('title', formValues.title);
            formData.append('company', formValues.company);
            formData.append('location', formValues.location);
            formData.append('start_date', formValues.start_date);
            formData.append('description', formValues.description);

            if (formValues.end_date && !formValues.is_current) {
                formData.append('end_date', formValues.end_date);
            }

            if (formValues.technologies.length > 0) {
                const techNames = formValues.technologies
                    .map((techId) => stacks.value.find((s) => s.id === techId)?.name || '')
                    .filter(Boolean);
                formData.append('technologies', JSON.stringify(techNames));
            }

            if (formValues.logo instanceof File) {
                formData.append('logo', formValues.logo, formValues.logo.name);
            }

            return formData;
        },
        notFoundMessage: 'Cette expérience n\'existe pas ou a été supprimée.',
        loadErrorMessage: 'Impossible de charger l\'expérience. Veuillez réessayer.',
    });

    // Données Externes

    const { data: typesData, refetch: refetchTypes } = useExperienceTypes();
    const { data: stacksData } = useStacks();
    const createTypeMutation = useCreateExperienceType();

    const stacks = usePaginatedData<Stack>(stacksData);

    const typeOptions = ref<Array<{ value: number | string; label: string }>>([]);

    const isEducationType = computed(() => {
        const selectedType = typeOptions.value.find((t) => t.value === form.type);
        return (
            selectedType?.label?.toLowerCase().includes('formation')
            || selectedType?.label?.toLowerCase().includes('education')
        );
    });

    // Watch pour initialiser les types
    watch(
        typesData,
        (response) => {
            let types: ExperienceType[] = [];
            if (response) {
                if (
                    typeof response === 'object'
                    && 'data' in response
                    && Array.isArray((response as { data: unknown }).data)
                ) {
                    types = (response as { data: ExperienceType[] }).data;
                } else if (Array.isArray(response)) {
                    types = response;
                }
            }

            if (types.length > 0) {
                typeOptions.value = toSelectOptions(types);
            } else {
                typeOptions.value = [
                    { value: 1, label: 'Expérience professionnelle' },
                    { value: 2, label: 'Formation' },
                ];
            }
        },
        { immediate: true },
    );

    const stackOptions = computed(() =>
        stacks.value.map((stack) => ({
            value: stack.id,
            label: stack.name,
            image: stack.logo,
        })),
    );

    // Handlers

    const handleCurrentChange = (value: boolean) => {
        if (value) {
            setFieldValue('end_date', '');
        }
    };

    const handleCreateType = async (name: string) => {
        try {
            const newType = await createTypeMutation.mutateAsync({ name });
            typeOptions.value.push({ value: newType.id, label: newType.name });
            setFieldValue('type', newType.id);
            refetchTypes();
            showSuccess(SUCCESS_MESSAGES.TYPE.CREATED, 'Type');
        } catch {
            showError(ERROR_MESSAGES.TYPE.CREATE_FAILED, 'Erreur');
        }
    };

    // Matching Différé

    useDeferredMatch({
        source: typeOptions,
        getRawValue: () => getRawValue<string | { id: number; name: string }>('type'),
        isUnmatched: () => !form.type,
        match: (options, raw) => {
            if (typeof raw === 'object' && 'id' in raw) {
                return raw.id;
            }
            const match = options.find((t) => t.label === raw);
            return match?.value;
        },
        setFieldValue: (val) => setFieldValue('type', val as string | number),
    });

    useDeferredMatch({
        source: stacks,
        getRawValue: () => getRawValue<string[]>('technologies'),
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
