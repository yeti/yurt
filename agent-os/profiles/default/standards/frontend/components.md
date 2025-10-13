## UI component best practices

### Component Design Principles

- **Single Responsibility**: Each component should have one clear purpose and
  do it well
- **Reusability**: Design components to be reused across different contexts
  with configurable props
- **Composability**: Build complex UIs by combining smaller, simpler components
  rather than monolithic structures
- **Clear Interface**: Define explicit, well-documented props with sensible
  defaults for ease of use
- **Encapsulation**: Keep internal implementation details private and expose
  only necessary APIs
- **Consistent Naming**: Use clear, descriptive names that indicate the
  component's purpose and follow team conventions
- **State Management**: Keep state as local as possible; lift it up only when
  needed by multiple components
- **Minimal Props**: Keep the number of props manageable; if a component needs
  many props, consider composition or splitting it
- **Documentation**: Document component usage, props, and provide examples for
  easier adoption by team members

### Frontend File Structure

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
