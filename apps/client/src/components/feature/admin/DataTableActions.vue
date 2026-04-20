<template>
    <div class="data-table-actions">
        <BaseButton
            v-if="showView"
            variant="ghost"
            size="icon"
            title="Voir"
            aria-label="Voir"
            @click="$emit('view')"
        >
            <template #icon-left>
                <BaseIcon name="eye" :size="16" aria-hidden="true" />
            </template>
        </BaseButton>

        <BaseButton
            v-if="showEdit"
            variant="ghost"
            size="icon"
            title="Modifier"
            aria-label="Modifier"
            @click="$emit('edit')"
        >
            <template #icon-left>
                <BaseIcon name="edit" :size="16" aria-hidden="true" />
            </template>
        </BaseButton>

        <BaseButton
            v-if="showDelete"
            variant="ghost"
            size="icon"
            class="data-table-actions__btn--danger"
            title="Supprimer"
            aria-label="Supprimer"
            @click="handleDelete"
        >
            <template #icon-left>
                <BaseIcon name="trash-2" :size="16" aria-hidden="true" />
            </template>
        </BaseButton>

        <slot></slot>
    </div>
</template>

<script setup lang="ts">
    import BaseButton from '@/components/base/BaseButton.vue';
    import BaseIcon from '@/components/base/BaseIcon.vue';

    withDefaults(
        defineProps<{
            showView?: boolean;
            showEdit?: boolean;
            showDelete?: boolean;
        }>(),
        {
            showView: true,
            showEdit: true,
            showDelete: true,
        },
    );

    const emit = defineEmits<{
        view: [];
        edit: [];
        delete: [];
    }>();

    const handleDelete = () => {
        emit('delete');
    };
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;

    .data-table-actions {
        display: flex;
        align-items: center;
        gap: vars.$spacing-xxxs;
        justify-content: flex-end;

        &__btn--danger {
            &:hover {
                background-color: rgba(vars.$danger-color, 0.1);
                color: vars.$danger-color;
            }
        }
    }
</style>
