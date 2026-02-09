# Backend

A Node.js GraphQL API built with Express, GraphQL Yoga, Pothos, and Prisma.

## Tech Stack

- [Express](https://expressjs.com/) v5 HTTP server
- [GraphQL Yoga](https://the-guild.dev/graphql/yoga-server) for the GraphQL server
- [Pothos](https://pothos-graphql.dev/) for code-first GraphQL schema building
- [Prisma](https://www.prisma.io/) ORM with PostgreSQL
- [Auth0](https://auth0.com/) via `express-oauth2-jwt-bearer` for authentication
- [Zod](https://zod.dev/) for validation
- [Pino](https://getpino.io/) for logging
- [Sentry](https://sentry.io/) for error monitoring
- [Vitest](https://vitest.dev/) for testing

## Prerequisites

- Node.js >= 24.7.0
- `pnpm` version 8+
- Docker (for the local PostgreSQL database)

## Getting Started

1. Start the dev database by running `docker compose up -d` from the project root.
2. From `packages/backend` run `pnpm install`.
3. From `packages/backend` run `pnpm generate` to generate the Prisma client.
4. From `packages/backend` run `pnpm migrate` to apply database migrations.
5. From `packages/backend` run `pnpm dev` to start the local dev server. The
   GraphQL endpoint will be available at `http://localhost:8080/api/graphql`.

## Available Scripts

| Command               | Description                                                                              |
| --------------------- | ---------------------------------------------------------------------------------------- |
| `pnpm dev`            | Start the dev server with nodemon                                                        |
| `pnpm generate`       | Generate the Prisma client                                                               |
| `pnpm migrate`        | Run Prisma migrations and regenerate the client                                          |
| `pnpm migrate:create` | Create a new migration without applying it                                               |
| `pnpm migrate:deploy` | Deploy migrations (used in production builds)                                            |
| `pnpm build`          | Install deps, generate schemas, compile TypeScript, resolve paths, and deploy migrations |
| `pnpm seed`           | Seed the database                                                                        |
| `pnpm lint`           | Run ESLint                                                                               |
| `pnpm type`           | Run TypeScript type-checking                                                             |
| `pnpm test`           | Run the test database migration and execute tests                                        |
| `pnpm db:test:start`  | Start a fresh test database via Docker                                                   |

## Updating Models

After updating the schema in `packages/backend/prisma/schema.prisma`:

1. `pnpm migrate:create` — create the migration
2. `pnpm migrate` — apply the migration and regenerate the Prisma client

## Tests

[Vitest](https://vitest.dev/) is used for testing. To run integration tests:

1. `pnpm db:test:start` — start a clean test database
2. `pnpm test` — run all tests
