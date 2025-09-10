# Tech Stack

## Context

Global tech stack defaults for Agent OS projects, overridable in project-specific `.agent-os/product/tech-stack.md`.

- App Framework: React, GraphQL (apollo client + server), Node, Express
- Language: TypeScript
- Primary Database: PostgreSQL 17+
- ORM: Prisma
- JavaScript Framework: React latest stable
- Build Tool: Vite
- Dependency Mangement: pnpm
- Import Strategy: Node.js modules
- Package Manager: pnpm
- Node Version: 24 LTS
- CSS Framework: MUI + @emotion/styled + @emotion/react
- UI Components: MUI v6
- Font Provider: Google Fonts
- Font Loading: Self-hosted for performance when possible
- Icons: MUI icons or custom from design
- Application Hosting: Render.com
- Hosting Region: Primary region based on user base
- Database Hosting: Render Managed PostgreSQL
- Database Backups: Daily automated
- Asset Storage: Amazon S3 or Cloudinary for images
- CDN: Cloudinary
- Asset Access: Private with signed URLs
- CI/CD Platform: GitHub Actions
- CI/CD Trigger: Push to main/develop branches
- Tests: Run before deployment
- Production Environment: main branch
- Staging Environment: develop branch
