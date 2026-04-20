<template>
    <div v-if="message || $slots.default" class="error-message" :class="[customClass]">
        <div v-if="showIcon" class="error-message__icon">
            <BaseIcon name="error" :size="16" />
        </div>
        <div class="error-message__content">
            <slot>{{ message }}</slot>
        </div>
    </div>
</template>

<script setup lang="ts">
    import BaseIcon from '@/components/base/BaseIcon.vue';

    import type { ErrorMessageProps } from '@/types/components/feedback';

    withDefaults(defineProps<ErrorMessageProps>(), {
        message: '',
        showIcon: true,
        customClass: '',
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
    }
</style>
