<template>
    <div v-if="message || $slots.default" class="error-message" :class="[customClass]" role="alert">
        <div v-if="showIcon" class="error-message__icon">
            <BaseIcon name="error" :size="16" />
        </div>
        <div class="error-message__content">
            <slot>{{ message }}</slot>
            <BaseButton v-if="actionText && to" :to="to" variant="outline" size="sm" class="error-message__action">
                {{ actionText }}
            </BaseButton>
        </div>
    </div>
</template>

<script setup lang="ts">
    import BaseButton from '@/components/base/BaseButton.vue';
    import BaseIcon from '@/components/base/BaseIcon.vue';

    import type { ErrorMessageProps } from '@/types/components/feedback';

    withDefaults(defineProps<ErrorMessageProps>(), {
        message: '',
        showIcon: true,
        customClass: '',
        actionText: '',
        to: '',
    });
</script>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as vars;
    @use '@/styles/abstracts/mixins' as mix;

    .error-message {
        display: flex;
        align-items: flex-start;
        color: vars.$danger-color;

        &__icon {
            flex-shrink: 0;
            margin-right: vars.$spacing-xxs;
            margin-top: 2px;
        }

        &__content {
            flex: 1;
        }

        &__action {
            margin-top: vars.$spacing-xs;
        }
    }
</style>
