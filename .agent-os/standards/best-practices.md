# Development Best Practices

## Context

Global development guidelines for Agent OS projects.

<conditional-block context-check="core-principles">
IF this Core Principles section already read in current context:
  SKIP: Re-reading this section
  NOTE: "Using Core Principles already in context"
ELSE:
  READ: The following principles

## Core Principles

### Keep It Simple

- Implement code in the fewest lines possible
- Avoid over-engineering solutions
- Choose straightforward approaches over clever ones
- Avoid redundant layers of abstraction

### Optimize for Readability

- Prioritize code clarity over micro-optimizations
- Write self-documenting code with clear, descriptive variable names. Avoid
  single-letter abbreviations (e.g., x, y, i) unless they are conventional in
  context (such as loop counters or mathematical formulas).
- Add comments for "why" not "what"

### DRY (Don't Repeat Yourself)

- Extract repeated business logic to private methods
- Extract repeated UI markup to reusable components
- Create utility functions for common operations

### File Structure

- Keep files focused on a single responsibility
- Group related functionality together
- Use consistent naming conventions

#### Frontend File Structure

Root Level:

- Standard React/Vite configuration files (package.json, tsconfig.json, vite.config.ts)
- Entry points: src/index.tsx, src/App.tsx
- MSW setup: public/mockServiceWorker.js for API mocking

src/
├── apollo/ # Apollo Client configuration and setup
├── modules/ # Feature-based modules (auth, home, profile)
├── shared/ # Reusable cross-module code
│ ├── components/ # Common UI components (Layout, ErrorPage, NotFound)
│ ├── hooks/ # Custom hooks organized by category (storage/)
│ ├── styles/ # Theme system with component-specific styling
│ ├── types/ # TypeScript definitions
│ ├── queries/ # Shared GraphQL queries
│ ├── mutations/ # Shared GraphQL mutations
│ ├── constants.ts # App-wide constants
│ └── config.ts # Configuration settings
├── services/ # API and external service integrations
├── stores/ # State management
├── tests/ # Test configuration and setup
│ └── mocks/ # MSW API mocking setup
├── assets/ # Static assets
└── static/ # Static resources (icons)

#### Backend File Structure

Root Level:

- GraphQL server configuration (schema.ts, server.ts, serverSetup.ts)
- Database setup: Prisma schema and migrations in prisma/
- Entry point: src/server.ts
- Dev tooling: nodemon.json, .eslintrc.js

GraphQL API Architecture:
src/
├── schemaModules/ # Feature-based GraphQL schema modules
│ └── user/ # Domain-specific modules (user, etc.)
│ ├── index.ts # Module exports
│ ├── objectTypes._.ts # GraphQL object type definitions
│ ├── queries._.ts # GraphQL query resolvers
│ ├── mutations.\*.ts # GraphQL mutation resolvers
│ └── tests/ # Module-specific tests
├── apolloPlugins/ # Apollo Server plugins (sentry, logger)
├── services/ # Service classes (external APIs, internal domains, etc.)
│ └── Http/ # HTTP service with tests
├── shared/ # Cross-module utilities
│ ├── types/ # Shared TypeScript definitions
│ ├── utils.ts # Utility functions
│ └── constants.ts # App-wide constants
├── tests/ # Global test setup and helpers
├── context.ts # GraphQL context setup
├── permissions.ts # GraphQL Shield permissions
├── prismaClient.ts # Prisma database client
├── config.ts # Environment configuration
└── loggers.ts # Logging setup

prisma/
├── migrations/ # Database migration files
├── schema.prisma # Database schema definition
└── seed.ts # Database seeding script

Key Backend Patterns:

- GraphQL-first: Nexus-based type-safe GraphQL schema with code generation
- Domain modules: Schema organized by business domain (user/, etc.)
- Type safety: Nexus + Prisma for end-to-end type safety
- Prisma ORM-driven: Prisma ORM with migrations and seeding
- Plugin architecture: Modular Apollo Server plugins (Sentry, logging)
- Testing: Jest with Docker Compose for isolated database testing
- Security: GraphQL Shield for permissions, Helmet for HTTP server security headers

Tech Stack:

- GraphQL: Apollo Server 4 + Nexus code-first approach
- Database: Prisma ORM with PostgreSQL
- Runtime: Node.js with Express
- Testing: Jest with Supertest and Docker-based test databases
- Monitoring: Sentry integration and Pino logging

  </conditional-block>

<conditional-block context-check="dependencies" task-condition="choosing-external-library">
IF current task involves choosing an external library:
  IF Dependencies section already read in current context:
    SKIP: Re-reading this section
    NOTE: "Using Dependencies guidelines already in context"
  ELSE:
    READ: The following guidelines
ELSE:
  SKIP: Dependencies section not relevant to current task

## Dependencies

### Choose Libraries Wisely

When adding third-party dependencies:

- Select the most popular and actively maintained option
- Check the library's GitHub repository for:
  - Recent commits (within last 6 months)
  - Active issue resolution
  - Number of stars/downloads
  - Clear documentation
- Make sure the library provides TypeScript type definitions either within the package or within a `@types/*` package on `npm`

  </conditional-block>
