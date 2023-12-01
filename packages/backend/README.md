# Backend

## Getting Started

1. Make sure you have `pnpm` version 8+ installed. You can find installation instructions [here](https://pnpm.io/installation).
2. Make sure you've started your dev database by running `docker compose up` from the project's root.
3. From `packages/backend` run `pnpm install`
4. From `packages/backend` run `pnpm generate` to generate the Prisma and Nexus schemas.
5. From `packages/backend` run `pnpm dev` to start the local dev server. You should be able to visit the Apollo Server sandbox at `localhost:8080/api/graphql`.
