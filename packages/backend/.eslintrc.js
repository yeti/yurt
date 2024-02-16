module.exports = {
  plugins: ['@typescript-eslint', 'unicorn'],
  env: {
    es2024: true,
  },
  extends: ['eslint:recommended', 'plugin:@typescript-eslint/recommended'],
  overrides: [
    {
      env: {
        node: true,
      },
      files: ['.eslintrc.{js,cjs}'],
      parserOptions: {
        sourceType: 'script',
      },
    },
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
  },
  rules: {
    '@typescript-eslint/ban-ts-comment': 'off',
    curly: 'error',
    'unicorn/switch-case-braces': 'error',
    'no-nested-ternary': 'error',
    radix: 'error',
  },
};
