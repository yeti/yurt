## Database model best practices

### General Principles

- **Clear Naming**: Use singular names for models and plural for tables
  following your framework's conventions
- **Timestamps**: Include created and updated timestamps on all tables for
  auditing and debugging
- **Data Integrity**: Use database constraints (NOT NULL, UNIQUE, foreign keys)
  to enforce data rules at the database level
- **Appropriate Data Types**: Choose data types that match the data's purpose
  and size requirements
- **Indexes on Foreign Keys**: Index foreign key columns and other frequently
  queried fields for performance
- **Validation at Multiple Layers**: Implement validation at both model and
  database levels for defense in depth
- **Relationship Clarity**: Define relationships clearly with appropriate
  cascade behaviors and naming conventions
- **Avoid Over-Normalization**: Balance normalization with practical query
  performance needs

### Prisma-Specific Standards

#### Naming Conventions

- **Database models**: Use PascalCase in Prisma schema definition, mapped to
  snake_case in underlying database names
- Example: `UserProfile` in schema → `user_profile` in database

#### Schema Organization

- Define all models in `prisma/schema.prisma`
- Use migrations in `prisma/migrations/` for database changes
- Maintain a seed script at `prisma/seed.ts` for development and testing data

#### Type Safety

- Prisma provides end-to-end type safety from database to API
- Use generated Prisma Client types throughout the application
- Leverage Prisma Client's type-safe query builders

#### Best Practices

- Run migrations to update database schema: `npx prisma migrate dev`
- Generate client after schema changes: `npx prisma generate`
- Use Prisma Studio for database inspection: `npx prisma studio`
- Test database operations with isolated test databases using Docker Compose
