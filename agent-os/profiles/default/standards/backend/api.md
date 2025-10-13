## API standards and conventions

### GraphQL API Architecture

This project uses GraphQL with Apollo Server. Follow these patterns for consistency.

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

#### Key Backend Patterns

- **GraphQL-first**: Nexus-based type-safe GraphQL schema with code generation
- **Domain modules**: Schema organized by business domain (user/, etc.)
- **Type safety**: Nexus + Prisma for end-to-end type safety
- **Prisma ORM-driven**: Prisma ORM with migrations and seeding
- **Plugin architecture**: Modular Apollo Server plugins (Sentry, logging)
- **Testing**: Jest with Docker Compose for isolated database testing
- **Security**: GraphQL Shield for permissions, Helmet for HTTP server security headers

#### Tech Stack

- GraphQL: Apollo Server 4 + Nexus code-first approach
- Database: Prisma ORM with PostgreSQL
- Runtime: Node.js with Express
- Testing: Jest with Supertest and Docker-based test databases
- Monitoring: Sentry integration and Pino logging

### GraphQL Best Practices

- **Schema Organization**: Organize schema by business domain, not by technical layers
- **Type Safety**: Use Nexus for type-safe schema definition with automatic TypeScript type generation
- **Resolver Patterns**: Keep resolvers thin; move business logic to service classes
- **Error Handling**: Use consistent error handling patterns across resolvers
- **Authorization**: Implement authorization using GraphQL Shield at the schema level
- **N+1 Prevention**: Use DataLoader or similar patterns to prevent N+1 query problems
- **Testing**: Write integration tests for resolvers using test databases
