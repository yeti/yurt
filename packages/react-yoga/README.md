# React Yoga

A React frontend template built with Vite, TypeScript, MUI, and Apollo Client — designed to pair with the `backend` package.

## Tech Stack

- [React](https://react.dev/) with TypeScript
- [Vite](https://vitejs.dev/) (SWC) for bundling and dev server
- [Apollo Client](https://www.apollographql.com/docs/react/) for GraphQL data fetching
- [GraphQL Code Generator](https://the-guild.dev/graphql/codegen) for typed GraphQL operations
- [MUI](https://mui.com/) for UI components
- [React Router](https://reactrouter.com/) for routing
- [React Hook Form](https://react-hook-form.com/) + [Zod](https://zod.dev/) for forms and validation
- [Vitest](https://vitest.dev/) + [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/) for testing
- [Sentry](https://sentry.io/) for error monitoring

## Getting Started

1. Make sure you have `pnpm` version 8+ installed. You can find installation instructions [here](https://pnpm.io/installation).
2. Make sure the `backend` package is running (see `packages/backend/README.md`).
3. From `packages/react-yoga` run `pnpm install`.
4. Copy `.env.example` to `.env` and fill in the required values.
5. From `packages/react-yoga` run `pnpm dev` to start the local dev server.

## Available Scripts

| Command              | Description                                      |
| -------------------- | ------------------------------------------------ |
| `pnpm dev`           | Start the Vite dev server                        |
| `pnpm dev:host`      | Start the Vite dev server exposed on the network |
| `pnpm build`         | Type-check and build for production              |
| `pnpm lint`          | Run ESLint                                       |
| `pnpm type`          | Run `tsc` type-checking in watch mode            |
| `pnpm type:watch`    | Run `tsc` type-checking in watch mode            |
| `pnpm test`          | Run tests with Vitest                            |
| `pnpm preview`       | Preview the production build locally             |
| `pnpm codegen`       | Generate typed GraphQL hooks and types           |
| `pnpm codegen:watch` | Run codegen in watch mode                        |

## GraphQL Codegen

This package uses [GraphQL Code Generator](https://the-guild.dev/graphql/codegen) to produce typed hooks and types from the backend schema. GraphQL operations are defined in `src/graphql/` and generated output is written to `src/graphql/gen/graphql.ts`.

To regenerate after updating queries or mutations:

```sh
pnpm codegen
```

Or run in watch mode during development:

```sh
pnpm codegen:watch
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```
VITE_AUTH0_DOMAIN=""
VITE_AUTH0_CLIENT_ID=""
VITE_AUTH0_AUDIENCE=""
VITE_GRAPHQL_URL="http://localhost:8080/api/graphql"
```

## Deploying to Render

When deploying to Render, you'll need to add some environment variables to the Render service:

- `HUSKY="0"` to disable Husky
- `SKIP_INSTALL_DEPS="true"` to prevent Render from using `npm` to install dependencies. This is necessary because Render uses `npm` by default, but this project uses `pnpm`.
