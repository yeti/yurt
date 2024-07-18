# Backend

## Getting Started

1. Make sure you have `pnpm` version 8+ installed. You can find installation instructions [here](https://pnpm.io/installation).
2. Make sure you've started your dev database by running `docker compose up` from the project's root.
3. From `packages/backend` run `pnpm install`
4. From `packages/backend` run `pnpm generate` to generate the Prisma and Nexus schemas.
5. From `packages/backend` run `pnpm dev` to start the local dev server. You should be able to visit the Apollo Server sandbox at `localhost:8080/api/graphql`.

## Updating Models

After updating the schema in `packages/backend/prisma/schema.prisma`, you'll need to run the following commands from `packages/backend` to update the Prisma and Nexus schemas:

1. `pnpm generate:prisma`
2. `pnpm migrate:create`
3. `pnpm migrate`
4. `pnpm generate:nexus`

## Tests

[Jest](https://jestjs.io/) is used for unit and integration testing.
In order to run integration tests, you'll need to run the following commands from `packages/backend`:

1. `pnpm db:test:start`
2. `pnpm test`

## Deploying to Render

When deploying the backend to Render, you will first need to create a PostgreSQL database for your backend to connnect to.

Upon creation of the database, you will then create a web service for the backend. The prompts should be filled in as follows:

Branch: `develop` or `main` depending on whether this is for staging or production,

Root Directory: `packages/backend`

Build Command: `pnpm build;`

Start Command: `node dist/src/server.js`

Generally speaking we can select the `Starter` plan unless otherwise specified by the projects needs.

Add any required env variables including the `DATABASE_URL` from the database you created earlier.
