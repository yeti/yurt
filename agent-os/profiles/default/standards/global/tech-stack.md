## Tech stack

Global tech stack defaults for Agent OS projects, overridable in
project-specific configuration.

### Framework & Runtime

- **Application Framework:** React, GraphQL (Apollo Client + Apollo Server),
  Node.js, Express
- **Language/Runtime:** TypeScript, Node.js 24 LTS
- **Package Manager:** pnpm
- **Import Strategy:** Node.js modules

### Frontend

- **JavaScript Framework:** React (latest stable)
- **Build Tool:** Vite
- **CSS Framework:** MUI v6 + @emotion/styled + @emotion/react
- **UI Components:** MUI v6
- **Icons:** MUI icons or custom from design
- **Font Provider:** Google Fonts
- **Font Loading:** Self-hosted for performance when possible

### Database & Storage

- **Primary Database:** PostgreSQL 17+
- **ORM/Query Builder:** Prisma
- **Database Hosting:** Render Managed PostgreSQL
- **Database Backups:** Daily automated
- **Asset Storage:** Amazon S3
- **CDN:** Cloudinary
- **Asset Access:** Private with signed URLs

### Deployment & Infrastructure

- **Application Hosting:** Render.com
- **Hosting Region:** Primary region based on user base
- **CI/CD Platform:** GitHub Actions
- **CI/CD Trigger:** Push to main/develop branches
- **Tests:** Run before deployment
- **Production Environment:** main branch
- **Staging Environment:** develop branch
