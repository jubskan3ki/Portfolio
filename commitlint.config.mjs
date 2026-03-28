/** @type {import('@commitlint/types').UserConfig} */
export default {
    extends: ['@commitlint/config-conventional'],
    rules: {
        'type-enum': [
            2,
            'always',
            ['feat', 'fix', 'docs', 'style', 'refactor', 'perf', 'test', 'chore', 'ci', 'revert', 'build'],
        ],
        'scope-enum': [
            1,
            'always',
            ['frontend', 'backend', 'docker', 'ci', 'deps', 'nginx', 'monitoring', 'auth', 'api'],
        ],
        'subject-max-length': [2, 'always', 100],
        'header-max-length': [2, 'always', 120],
        'body-max-line-length': [1, 'always', 200],
    },
};
