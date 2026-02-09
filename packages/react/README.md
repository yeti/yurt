# React

A standalone React frontend template built with Vite, TypeScript, and MUI.

## Tech Stack

- [React](https://react.dev/) with TypeScript
- [Vite](https://vitejs.dev/) (SWC) for bundling and dev server
- [MUI](https://mui.com/) for UI components
- [React Router](https://reactrouter.com/) for routing
- [React Hook Form](https://react-hook-form.com/) + [Zod](https://zod.dev/) for forms and validation
- [Axios](https://axios-http.com/) for HTTP requests
- [Vitest](https://vitest.dev/) + [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/) for testing
- [Sentry](https://sentry.io/) for error monitoring

## Getting Started

1. Make sure you have `pnpm` version 8+ installed. You can find installation instructions [here](https://pnpm.io/installation).
2. From `packages/react` run `pnpm install`.
3. From `packages/react` run `pnpm dev` to start the local dev server.

## Available Scripts

| Command           | Description                                      |
| ----------------- | ------------------------------------------------ |
| `pnpm dev`        | Start the Vite dev server                        |
| `pnpm dev:host`   | Start the Vite dev server exposed on the network |
| `pnpm build`      | Type-check and build for production              |
| `pnpm lint`       | Run ESLint                                       |
| `pnpm type`       | Run `tsc` type-checking in watch mode            |
| `pnpm type:watch` | Run `tsc` type-checking in watch mode            |
| `pnpm test`       | Run tests with Vitest                            |
| `pnpm preview`    | Preview the production build locally             |

## Environment Variables

This template uses Zod to validate required environment variables at runtime. Create a `.env` file in the package root with the following:

```
VITE_AUTH0_DOMAIN=""
VITE_AUTH0_CLIENT_ID=""
VITE_AUTH0_AUDIENCE=""
```

## Deploying to Render

When deploying to Render, you'll need to add some environment variables to the Render service:

- `HUSKY="0"` to disable Husky
- `SKIP_INSTALL_DEPS="true"` to prevent Render from using `npm` to install dependencies. This is necessary because Render uses `npm` by default, but this project uses `pnpm`.
