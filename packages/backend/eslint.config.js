import typescriptEslint from '@typescript-eslint/eslint-plugin';
import unicorn from 'eslint-plugin-unicorn';
import tsParser from '@typescript-eslint/parser';

export default [
  {
    ignores: ['**/gen/**', '**/generated/**'],
  },
  {
    files: ['**/*.ts', '**/*.tsx'],
    plugins: {
      '@typescript-eslint': typescriptEslint,
      unicorn: unicorn,
    },
    languageOptions: {
      parser: tsParser,
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: {
        node: true,
        es2024: true,
      },
    },
    rules: {
      ...typescriptEslint.configs.recommended.rules,
      '@typescript-eslint/ban-ts-comment': 'off',
      curly: 'error',
      'unicorn/switch-case-braces': 'error',
      'no-nested-ternary': 'error',
      radix: 'error',
    },
  },
  {
    files: ['.eslintrc.{js,cjs}'],
    languageOptions: {
      sourceType: 'script',
      globals: {
        node: true,
      },
    },
  },
];
