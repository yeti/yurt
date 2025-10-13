## General development conventions

### Project Organization

- **Consistent Project Structure**: Organize files and directories in a
  predictable, logical structure that team members can navigate easily
- **Clear Documentation**: Maintain up-to-date README files with setup
  instructions, architecture overview, and contribution guidelines

### Version Control

- **Version Control Best Practices**: Use clear commit messages, feature
  branches, and meaningful pull/merge requests with descriptions
- **Code Review Process**: Establish a consistent code review process with
  clear expectations for reviewers and authors

### Configuration & Security

- **Environment Configuration**: Use environment variables for configuration;
  never commit secrets or API keys to version control

### Dependencies

- **Dependency Management**: Keep dependencies up-to-date and minimal; document
  why major dependencies are used
- **Choose Libraries Wisely**: When adding third-party dependencies:
  - Select the most popular and actively maintained option
  - Check the library's GitHub repository for:
    - Recent commits (within last 6 months)
    - Active issue resolution
    - Number of stars/downloads
    - Clear documentation
  - Make sure the library provides TypeScript type definitions either within
    the package or within a `@types/*` package on npm

### Development Process

- **Testing Requirements**: Define what level of testing is required before
  merging (unit tests, integration tests, etc.)
- **Feature Flags**: Use feature flags for incomplete features rather than
  long-lived feature branches
- **Changelog Maintenance**: Keep a changelog or release notes to track
  significant changes and improvements
