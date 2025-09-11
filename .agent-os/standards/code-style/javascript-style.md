# Javascript Style Guide

Use Prettier config file, TypeScript config, and eslint rules as guidelines for
specific JavaScript and TypeScript conventions.

All code should be auto-formatted using a husky pre-commit hook, which should
already be installed in the repository:

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npx lint-staged
```

**Never** use the `any` type to bypass the TypeScript compiler. If you are
unable to determine the correct type for a value, stop and prompt the developer
for help.

**Never** nest ternary functions.
