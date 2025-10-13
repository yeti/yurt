## Coding style best practices

### Core Principles

#### Keep It Simple

- Implement code in the fewest lines possible
- Avoid over-engineering solutions
- Choose straightforward approaches over clever ones

#### Optimize for Readability

- Prioritize code clarity over micro-optimizations
- Write self-documenting code with clear variable names
- Add comments for "why" not "what"

#### DRY (Don't Repeat Yourself)

- Extract repeated business logic to private methods
- Extract repeated UI markup to reusable components
- Create utility functions for common operations

### File Structure

Keep files focused on a single responsibility. Group related functionality
together. Use consistent naming conventions.

#### Frontend File Structure

Root Level:

- Standard React/Vite configuration files (package.json, tsconfig.json,
  vite.config.ts)
- Entry points: src/index.tsx, src/App.tsx
- MSW setup: public/mockServiceWorker.js for API mocking

```
src/
├── apollo/              # Apollo Client configuration and setup
├── modules/             # Feature-based modules (auth, home, profile)
├── shared/              # Reusable cross-module code
│   ├── components/      # Common UI components (Layout, ErrorPage, NotFound)
│   ├── hooks/           # Custom hooks organized by category (storage/)
│   ├── styles/          # Theme system with component-specific styling
│   ├── types/           # TypeScript definitions
│   ├── queries/         # Shared GraphQL queries
│   ├── mutations/       # Shared GraphQL mutations
│   ├── constants.ts     # App-wide constants
│   └── config.ts        # Configuration settings
├── services/            # API and external service integrations
├── stores/              # State management
├── tests/               # Test configuration and setup
│   └── mocks/           # MSW API mocking setup
├── assets/              # Static assets
└── static/              # Static resources (icons)
```

#### Backend File Structure

Root Level:

- GraphQL server configuration (schema.ts, server.ts, serverSetup.ts)
- Database setup: Prisma schema and migrations in prisma/
- Entry point: src/server.ts
- Dev tooling: nodemon.json, .eslintrc.js

GraphQL API Architecture:

```
src/
├── schemaModules/       # Feature-based GraphQL schema modules
│   └── user/            # Domain-specific modules (user, etc.)
│       ├── index.ts     # Module exports
│       ├── objectTypes.*.ts  # GraphQL object type definitions
│       ├── queries.*.ts      # GraphQL query resolvers
│       ├── mutations.*.ts    # GraphQL mutation resolvers
│       └── tests/            # Module-specific tests
├── apolloPlugins/       # Apollo Server plugins (sentry, logger)
├── services/            # Service classes (external APIs, internal domains, etc.)
│   └── Http/            # HTTP service with tests
├── shared/              # Cross-module utilities
│   ├── types/           # Shared TypeScript definitions
│   ├── utils.ts         # Utility functions
│   └── constants.ts     # App-wide constants
├── tests/               # Global test setup and helpers
├── context.ts           # GraphQL context setup
├── permissions.ts       # GraphQL Shield permissions
├── prismaClient.ts      # Prisma database client
├── config.ts            # Environment configuration
└── loggers.ts           # Logging setup

prisma/
├── migrations/          # Database migration files
├── schema.prisma        # Database schema definition
└── seed.ts              # Database seeding script
```

Key Backend Patterns:

- GraphQL-first: Nexus-based type-safe GraphQL schema with code generation
- Domain modules: Schema organized by business domain (user/, etc.)
- Type safety: Nexus + Prisma for end-to-end type safety
- Prisma ORM-driven: Prisma ORM with migrations and seeding
- Plugin architecture: Modular Apollo Server plugins (Sentry, logging)
- Testing: Jest with Docker Compose for isolated database testing
- Security: GraphQL Shield for permissions, Helmet for HTTP server security
  headers

Tech Stack:

- GraphQL: Apollo Server 4 + Nexus code-first approach
- Database: Prisma ORM with PostgreSQL
- Runtime: Node.js with Express
- Testing: Jest with Supertest and Docker-based test databases
- Monitoring: Sentry integration and Pino logging

### General Formatting

#### Indentation

- Use tabs for indentation
- Maintain consistent indentation throughout files
- Align nested structures for readability

#### Naming Conventions

- **Methods and Variables**: Use camelCase (e.g., `userProfile`,
  `calculateTotal`)
- **Database models**: Use PascalCase in prisma schema definition, mapped to
  snake_case (e.g., `user_profile`, `calculate_total`) in underlying database
  names
- **Classes**: Use PascalCase (e.g., `UserProfile`, `PaymentProcessor`)
- **Constants**: Use UPPER_SNAKE_CASE (e.g., `MAX_RETRY_COUNT`)

#### String Formatting

- Use single quotes for strings: `'Hello World'`
- Use double quotes only when interpolation is needed
- Use template literals for multi-line strings or complex interpolation

### TypeScript/JavaScript

#### Type Safety

- Use Prettier config file, TypeScript config, and eslint rules as guidelines
  for specific JavaScript and TypeScript conventions
- All code should be auto-formatted using a husky pre-commit hook
- **Never** use the `any` type to bypass the TypeScript compiler
- If you are unable to determine the correct type for a value, stop and prompt
  the developer for help
- Make sure all libraries provide TypeScript type definitions either within the
  package or within a `@types/*` package on npm

### Style Guidelines

- **Consistent Naming Conventions**: Establish and follow naming conventions
  for variables, functions, classes, and files across the codebase
- **Automated Formatting**: Maintain consistent code style (indenting, line
  breaks, etc.)
- **Meaningful Names**: Choose descriptive names that reveal intent; avoid
  abbreviations and single-letter variables except in narrow contexts
- **Small, Focused Functions**: Keep functions small and focused on a single
  task for better readability and testability
- **Consistent Indentation**: Use consistent indentation (tabs) and configure
  your editor/linter to enforce it
- **Remove Dead Code**: Delete unused code, commented-out blocks, and imports
  rather than leaving them as clutter
- **Backward compatibility only when required**: Unless specifically instructed
  otherwise, assume you do not need to write additional code logic to handle
  backward compatibility
- **DRY Principle**: Avoid duplication by extracting common logic into reusable
  functions or modules

### Dependencies

When adding third-party dependencies:

- Select the most popular and actively maintained option
- Check the library's GitHub repository for:
  - Recent commits (within last 6 months)
  - Active issue resolution
  - Number of stars/downloads
  - Clear documentation
- Make sure the library provides TypeScript type definitions either within the
  package or within a `@types/*` package on npm
