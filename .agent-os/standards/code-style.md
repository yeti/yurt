# Code Style Guide

## Context

Global code style rules for Agent OS projects.

<conditional-block context-check="general-formatting">
IF this General Formatting section already read in current context:
  SKIP: Re-reading this section
  NOTE: "Using General Formatting rules already in context"
ELSE:
  READ: The following formatting rules

## General Formatting

### Indentation

- Use tabs for indendation
- Maintain consistent indentation throughout files
- Align nested structures for readability

### Naming Conventions

- **Methods and Variables**: Use camelCase (e.g., `userProfile`, `calculateTotal`)
- **Database models**: Use PascalCase in prisma schema definition, mapped to
  snake_case (e.g., `user_profile`, `calculate_total`) in underlying database
  names
- **Classes**: Use PascalCase (e.g., `UserProfile`, `PaymentProcessor`)
- **Constants**: Use UPPER_SNAKE_CASE (e.g., `MAX_RETRY_COUNT`)

### String Formatting

- Use single quotes for strings: `'Hello World'`
- Use double quotes only when interpolation is needed
- Use template literals for multi-line strings or complex interpolation

### Code Comments

- Add brief comments above non-obvious business logic
- Document complex algorithms or calculations
- Explain the "why" behind implementation choices
- Never remove existing comments unless removing the associated code
- Update comments when modifying code to maintain accuracy
- Keep comments concise and relevant
- Never use comments as section markers in React trees (TSX or JSX)
  </conditional-block>

<conditional-block task-condition="html-css-tailwind" context-check="html-css-style">
IF current task involves writing or updating HTML or CSS:
  IF css-style.md already in context:
    SKIP: Re-reading this file
    NOTE: "Using CSS style guide already in context"
  ELSE:
    <context_fetcher_strategy>
      IF current agent is Claude Code AND context-fetcher agent exists:
        USE: @agent:context-fetcher
        REQUEST: "Get CSS rules from code-style/css-style.md"
        PROCESS: Returned style rules
      ELSE:
        READ the following style guides (only if not already in context):
        - @.agent-os/standards/code-style/css-style.md (if not in context)
    </context_fetcher_strategy>
ELSE:
  SKIP: CSS style guide not relevant to current task
</conditional-block>

<conditional-block task-condition="javascript" context-check="javascript-style">
IF current task involves writing or updating JavaScript:
  IF javascript-style.md already in context:
    SKIP: Re-reading this file
    NOTE: "Using JavaScript style guide already in context"
  ELSE:
    <context_fetcher_strategy>
      IF current agent is Claude Code AND context-fetcher agent exists:
        USE: @agent:context-fetcher
        REQUEST: "Get JavaScript style rules from code-style/javascript-style.md"
        PROCESS: Returned style rules
      ELSE:
        READ: @.agent-os/standards/code-style/javascript-style.md
    </context_fetcher_strategy>
ELSE:
  SKIP: JavaScript style guide not relevant to current task
</conditional-block>
