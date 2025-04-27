import tsPlugin from '@typescript-eslint/eslint-plugin';
import tsParser from '@typescript-eslint/parser';
import importPlugin from 'eslint-plugin-import';
import prettierPlugin from 'eslint-plugin-prettier';
import vuePlugin from 'eslint-plugin-vue';
import vueA11yPlugin from 'eslint-plugin-vuejs-accessibility';
import vueParser from 'vue-eslint-parser';

const parserOptionsWithTypes = {
	project: './tsconfig.eslint.json',
	tsconfigRootDir: process.cwd(),
	ecmaVersion: 'latest',
	sourceType: 'module',
};

export default [
	{
		ignores: ['.nuxt/**/*', '.output/**/*', 'dist/**/*', 'node_modules/**/*', '**/*.config.ts'],
	},
	{
		files: ['**/*.vue'],
		languageOptions: {
			parser: vueParser,
			parserOptions: {
				...parserOptionsWithTypes,
				parser: tsParser,
				extraFileExtensions: ['.vue'],
			},
		},
		plugins: {
			vue: vuePlugin,
			prettier: prettierPlugin,
			'vuejs-accessibility': vueA11yPlugin,
		},
		rules: {
			'prettier/prettier': 'error',

			'vue/component-tags-order': ['error', { order: ['template', 'script', 'style'] }],
			'vue/define-macros-order': ['error', { order: ['defineProps', 'defineEmits'] }],
			'vue/html-indent': ['error', 'tab', { baseIndent: 1 }],
			'vue/attribute-hyphenation': ['error', 'always'],
			'vue/component-api-style': ['error', ['script-setup', 'composition']],
			'vue/no-unused-components': 'warn',
			'vue/no-v-html': 'off',
			'vue/multi-word-component-names': 'off',

			'vue/require-default-prop': 'off',
			'vue/no-v-text-v-html-on-component': 'warn',
			'vue/no-useless-template-attributes': 'error',
			'vue/no-static-inline-styles': 'warn',
			'vue/no-duplicate-attributes': 'error',
			'vue/no-unused-properties': [
				'warn',
				{
					groups: ['props', 'data', 'computed', 'methods'],
					deepData: true,
				},
			],
			'vue/block-order': [
				'error',
				{
					order: ['template', 'script', 'style'],
				},
			],
			'vue/attributes-order': 'warn',
			'vue/order-in-components': 'warn',

			'vuejs-accessibility/click-events-have-key-events': 'warn',
		},
	},

	{
		files: ['**/*.ts'],
		languageOptions: {
			parser: tsParser,
			parserOptions: parserOptionsWithTypes,
			globals: {
				window: 'readonly',
				document: 'readonly',
				console: 'readonly',
				NodeJS: 'readonly',
			},
		},
		plugins: {
			'@typescript-eslint': tsPlugin,
			prettier: prettierPlugin,
			import: importPlugin,
		},
		rules: {
			'prettier/prettier': 'error',

			'@typescript-eslint/no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
			'@typescript-eslint/ban-ts-comment': 'warn',
			'@typescript-eslint/consistent-type-imports': 'error',
			'@typescript-eslint/consistent-type-definitions': ['error', 'interface'],
			'@typescript-eslint/no-inferrable-types': 'warn',
			'@typescript-eslint/prefer-optional-chain': 'warn',

			'@typescript-eslint/prefer-ts-expect-error': 'error',
			'@typescript-eslint/switch-exhaustiveness-check': 'warn',
			'@typescript-eslint/no-misused-promises': ['warn', { checksVoidReturn: false }],

			'import/order': [
				'warn',
				{
					groups: ['builtin', 'external', 'internal', ['parent', 'sibling'], 'index'],
					pathGroups: [
						{
							pattern: '@/**',
							group: 'internal',
							position: 'after',
						},
						{
							pattern: '~/**',
							group: 'internal',
							position: 'after',
						},
						{
							pattern: './*.{css,scss,sass,less}',
							group: 'index',
							position: 'after',
						},
					],
					pathGroupsExcludedImportTypes: ['builtin'],
					'newlines-between': 'always',
					alphabetize: {
						order: 'asc',
						caseInsensitive: true,
					},
				},
			],
			'import/extensions': [
				'error',
				'ignorePackages',
				{ js: 'never', ts: 'never', vue: 'always', scss: 'always' },
			],
			'import/no-unresolved': 'error',
			'import/no-relative-packages': 'error',
		},
		settings: {
			'import/resolver': {
				typescript: {
					alwaysTryTypes: true,
					project: './tsconfig.json',
				},
				alias: {
					map: [['@', './src']],
					extensions: ['.ts', '.js', '.vue', '.json'],
				},
			},
		},
	},
];
