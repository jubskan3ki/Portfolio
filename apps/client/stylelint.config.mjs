/** @type {import('stylelint').Config} */
export default {
	extends: ['stylelint-config-standard-scss', 'stylelint-config-recommended-vue/scss'],

	rules: {
		// === Désactiver les règles de commentaires ===
		'comment-empty-line-before': null,
		'comment-whitespace-inside': null,
		'scss/double-slash-comment-empty-line-before': null,
		'scss/double-slash-comment-whitespace-inside': null,
		'scss/comment-no-empty': null,

		// === Désactiver les règles de lignes vides ===
		'scss/dollar-variable-empty-line-before': null,
		'declaration-empty-line-before': null,
		'rule-empty-line-before': null,
		'at-rule-empty-line-before': null,
		'custom-property-empty-line-before': null,

		// === Naming - Flexibilité pour BEM ===
		'selector-class-pattern': null,
		'scss/at-mixin-pattern': null,
		'scss/dollar-variable-pattern': null,
		'scss/percent-placeholder-pattern': null,
		'keyframes-name-pattern': null,

		// === Structure ===
		'no-empty-source': null,
		'no-descending-specificity': null,
		'declaration-block-no-redundant-longhand-properties': null,

		// === SCSS specifics ===
		'scss/no-global-function-names': null,
		'scss/at-rule-no-unknown': [
			true,
			{
				ignoreAtRules: [
					'tailwind',
					'apply',
					'variants',
					'responsive',
					'screen',
					'use',
					'forward',
					'mixin',
					'include',
					'function',
					'return',
					'if',
					'else',
					'each',
					'for',
					'while',
					'extend',
					'at-root',
					'debug',
					'warn',
					'error',
				],
			},
		],

		// === Values ===
		'color-function-notation': null,
		'color-function-alias-notation': null,
		'alpha-value-notation': null,
		'number-max-precision': 4,

		// === Modern CSS ===
		'media-feature-range-notation': null,
		'import-notation': null,

		'property-no-deprecated': null,
		'declaration-property-value-keyword-no-deprecated': null,

		// === Autres ===
		'property-no-vendor-prefix': null,
		'value-no-vendor-prefix': null,
		'selector-no-vendor-prefix': null,
		'max-nesting-depth': [4, { ignoreAtRules: ['media', 'supports', 'include'] }],
	},

	overrides: [
		{
			files: ['**/*.vue'],
			customSyntax: 'postcss-html',
		},
		{
			files: ['**/*.scss'],
			customSyntax: 'postcss-scss',
		},
	],

	ignoreFiles: ['dist/**', '.output/**', '.nuxt/**', 'node_modules/**', 'public/**'],
};
