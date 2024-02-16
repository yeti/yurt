module.exports = {
  plugins: ['@typescript-eslint', 'react', 'unicorn'],
  env: {
    browser: true,
    es2024: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react/recommended',
  ],
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
    'react/react-in-jsx-scope': 'off',
    'no-console': 'error',
    curly: 'error',
    'unicorn/switch-case-braces': 'error',
    'no-nested-ternary': 'error',
    radix: 'error',
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
};
