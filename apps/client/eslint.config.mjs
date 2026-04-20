import pluginA11y from 'eslint-plugin-vuejs-accessibility';

import withNuxt from './.nuxt/eslint.config.mjs';

export default withNuxt()
    .prepend({
        ignores: ['dist/', '.output/', '.nuxt/', 'node_modules/', 'public/', '*.min.js', 'coverage/'],
    })

    .override('nuxt/vue/rules', {
        rules: {
            'vue/multi-word-component-names': 'off',
            'vue/require-default-prop': 'off',
            'vue/html-self-closing': ['error', { html: { void: 'always', normal: 'never', component: 'always' } }],
            'vue/no-v-html': 'warn',
            'vue/block-order': ['error', { order: ['template', 'script', 'style'] }],
            'vue/define-macros-order': [
                'error',
                { order: ['defineProps', 'defineEmits', 'defineSlots', 'defineModel'] },
            ],
            'vue/component-api-style': ['error', ['script-setup', 'composition']],

            'vue/component-name-in-template-casing': ['error', 'PascalCase'],
            'vue/custom-event-name-casing': ['error', 'camelCase'],
            'vue/attribute-hyphenation': ['error', 'always'],
            'vue/prop-name-casing': ['error', 'camelCase'],

            'vue/html-indent': ['error', 4],
            'vue/script-indent': ['error', 4, { baseIndent: 1, switchCase: 1 }],
            'vue/max-attributes-per-line': ['warn', { singleline: 4, multiline: 1 }],
            'vue/first-attribute-linebreak': ['error', { singleline: 'ignore', multiline: 'below' }],
            'vue/html-closing-bracket-newline': ['error', { singleline: 'never', multiline: 'always' }],
            'vue/singleline-html-element-content-newline': 'off',

            'vue/no-unused-components': 'error',
            'vue/no-unused-vars': 'error',
            'vue/no-useless-v-bind': 'error',
            'vue/no-useless-mustaches': 'error',
            'vue/v-for-delimiter-style': ['error', 'in'],
            'vue/attributes-order': 'warn',

            'vue/no-undef-components': ['error', { ignorePatterns: ['Nuxt*', 'Client*', 'Lazy*', 'Icon', 'Base*'] }],
            'vue/no-undef-properties': 'error',
            'vue/require-explicit-emits': 'error',
            'vue/no-ref-object-reactivity-loss': 'error',
            'vue/prefer-true-attribute-shorthand': 'warn',
            'vue/no-empty-component-block': 'warn',
            'vue/padding-line-between-blocks': ['error', 'always'],
            'vue/prefer-separate-static-class': 'warn',
            'vue/no-static-inline-styles': ['warn', { allowBinding: true }],
            'vue/prefer-define-options': 'error',
            'vue/require-macro-variable-name': [
                'error',
                { defineProps: 'props', defineEmits: 'emit', defineSlots: 'slots' },
            ],
        },
    })

    .override('nuxt/import/rules', {
        rules: {
            'import/order': [
                'error',
                {
                    groups: ['builtin', 'external', 'internal', 'parent', 'sibling', 'index', 'type'],
                    pathGroups: [
                        { pattern: '#**', group: 'internal', position: 'before' },
                        { pattern: '@/**', group: 'internal', position: 'before' },
                        { pattern: '~/**', group: 'internal', position: 'before' },
                    ],
                    pathGroupsExcludedImportTypes: ['type'],
                    'newlines-between': 'always',
                    alphabetize: { order: 'asc', caseInsensitive: true },
                },
            ],
            'import/first': 'error',
            'import/no-duplicates': 'error',
            'import/newline-after-import': 'error',
        },
    })

    .override('nuxt/stylistic', {
        rules: {
            '@stylistic/max-len': [
                'warn',
                {
                    code: 120,
                    ignoreUrls: true,
                    ignoreStrings: true,
                    ignoreTemplateLiterals: true,
                    ignoreComments: true,
                },
            ],
            '@stylistic/object-curly-spacing': ['error', 'always'],
            '@stylistic/array-bracket-spacing': ['error', 'never'],
            '@stylistic/arrow-parens': ['error', 'always'],
            '@stylistic/no-trailing-spaces': 'error',
            '@stylistic/eol-last': ['error', 'always'],
            '@stylistic/comma-spacing': ['error', { before: false, after: true }],
            '@stylistic/space-infix-ops': 'error',
            '@stylistic/keyword-spacing': ['error', { before: true, after: true }],
            '@stylistic/indent': ['error', 4, { SwitchCase: 1 }],
            '@stylistic/indent-binary-ops': ['error', 4],
        },
    })

    // Vue files use vue/script-indent instead of @stylistic/indent.
    .append({
        files: ['**/*.vue'],
        rules: {
            '@stylistic/indent': 'off',
            '@stylistic/indent-binary-ops': 'off',
        },
    })

    // Config files: Prettier disagrees with these stylistic rules and would loop on save.
    .append({
        files: ['*.config.{ts,mjs,js}', 'nuxt.config.ts', 'eslint.config.mjs'],
        rules: {
            '@stylistic/indent': 'off',
            '@stylistic/indent-binary-ops': 'off',
            '@stylistic/operator-linebreak': 'off',
        },
    })

    // SafeHtml is the single trust boundary for v-html; callers sanitize via renderInlineMarkdown.
    .append({
        files: ['src/components/base/SafeHtml.vue'],
        rules: {
            'vue/no-v-html': 'off',
        },
    })

    .append({
        files: ['src/**/*.vue'],
        plugins: {
            'vuejs-accessibility': pluginA11y,
        },
        rules: {
            'vuejs-accessibility/alt-text': 'error',
            'vuejs-accessibility/anchor-has-content': 'error',
            'vuejs-accessibility/click-events-have-key-events': 'warn',
            'vuejs-accessibility/form-control-has-label': 'warn',
            'vuejs-accessibility/interactive-supports-focus': 'warn',
            'vuejs-accessibility/label-has-for': [
                'warn',
                {
                    required: { some: ['nesting', 'id'] },
                    allowChildren: true,
                },
            ],
            'vuejs-accessibility/no-autofocus': 'warn',
            'vuejs-accessibility/tabindex-no-positive': 'error',
        },
    })

    .override('nuxt/typescript/rules', {
        rules: {
            '@typescript-eslint/no-unused-expressions': ['error', { allowTernary: true, allowShortCircuit: true }],

            '@typescript-eslint/no-explicit-any': 'warn',
            '@typescript-eslint/no-non-null-assertion': 'warn',
            '@typescript-eslint/no-inferrable-types': 'error',
            '@typescript-eslint/consistent-type-imports': [
                'error',
                { prefer: 'type-imports', fixStyle: 'inline-type-imports' },
            ],
            '@typescript-eslint/no-import-type-side-effects': 'error',
            '@typescript-eslint/array-type': ['error', { default: 'array-simple' }],
            '@typescript-eslint/consistent-type-definitions': ['error', 'interface'],
            '@typescript-eslint/prefer-as-const': 'error',
            '@typescript-eslint/no-duplicate-enum-values': 'error',
        },
    })

    .append({
        files: ['src/**/*.{ts,vue,js}'],
        rules: {
            'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
            'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
            'prefer-const': 'error',
            'no-var': 'error',
            'object-shorthand': 'error',
            'prefer-arrow-callback': 'error',

            'no-nested-ternary': 'warn',
            'no-unneeded-ternary': 'error',
            'prefer-template': 'error',
            'no-useless-concat': 'error',
            'no-useless-return': 'error',
            'no-lonely-if': 'error',
            'no-else-return': ['error', { allowElseIf: false }],
            'array-callback-return': 'error',
            'no-await-in-loop': 'warn',
            'require-await': 'warn',
            'no-return-await': 'error',
            eqeqeq: ['error', 'always', { null: 'ignore' }],
            curly: ['error', 'all'],
        },
    });
