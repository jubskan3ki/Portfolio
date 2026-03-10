<template>
    <footer class="search-footer">
        <span><kbd>↑↓</kbd> Naviguer</span>
        <span><kbd>↵</kbd> Ouvrir</span>
        <span><kbd>Esc</kbd> Fermer</span>
    </footer>
</template>

<style lang="scss" scoped>
    @use '@/styles/abstracts/variables' as v;

    .search-footer {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: v.$spacing-lg;
        padding: v.$spacing-xs v.$spacing-sm;
        background: v.$bg-secondary;
        border-top: 1px solid v.$border-color;
        color: v.$text-muted;

        kbd {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 18px;
            height: 18px;
            padding: 0 v.$spacing-xxs;
            margin-right: v.$spacing-xxs;
            border: 1px solid v.$border-color;
            border-radius: v.$border-radius-sm;
            background: v.$white;
            font-weight: v.$font-weight-medium;
            font-family: inherit;
        }
    }
</style>
