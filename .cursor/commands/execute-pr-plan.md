# Execute PR Plan

## Triggering

@execute-pr-plan

## Preconditions

- A PR plan has already been approved in the current conversation.

## Actions

0. Create a backup branch with all of the changes committed together than can be reverted to later.
1. Create branches from the base branch in the specified order.
2. Move files/commits into each branch.
3. Push branches to origin.
4. Create GitHub PRs using the GitHub MCP.
5. Populate PR descriptions using `@.github/pull_request_template.md`. If the user hasn't provided ticket #s, leave that step of the template as "N/A."

## Safety

- Do not proceed unless the user has explicitly confirmed execution.
- Ask for confirmation if there is ambiguity.
