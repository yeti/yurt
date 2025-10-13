## CSS best practices

### MUI Framework Standards

We always use version 6 of MUI for all CSS.

All theme tokens (spacing, font-size, colors, etc.) must be defined in the MUI
theme. Never hard-code values without first prompting the user and confirming
whether the color is a one-off or should be added to the theme.

Use project `prettier` settings for formatting style-related code.

### General CSS Practices

- **Consistent Methodology**: Apply and stick to the project's consistent CSS
  methodology (MUI, Tailwind, BEM, utility classes, CSS modules, etc.) across the
  entire project
- **Avoid Overriding Framework Styles**: Work with your framework's patterns
  rather than fighting against them with excessive overrides
- **Maintain Design System**: Establish and document design tokens (colors,
  spacing, typography) for consistency
- **Minimize Custom CSS**: Leverage framework utilities and components to
  reduce custom CSS maintenance burden
- **Performance Considerations**: Optimize for production with CSS
  purging/tree-shaking to remove unused styles
