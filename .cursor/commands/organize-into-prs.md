# Organize into PRs

This command helps you split a large branch into smaller, logical Pull Requests that are easier to review and merge.

## Triggering

Type `@organize-into-prs` to start. You can optionally specify a base branch, for example: `@organize-into-prs against main`.

## Analysis Process

1.  **Identify the Base Branch:**
    - Determine the base branch to compare against. Use `develop` by default unless a different branch is mentioned in the user's request.
2.  **Evaluate Changes:**
    - Analyze all changes in the current branch compared to the base branch.
    - If the GitHub MCP is enabled and PR numbers were provided, use a tool to view the PRs/comments to understand the full scope of changes. Otherwise, run `git diff [base-branch]...HEAD`.
3.  **Logical Grouping:**
    - Decide how to split these changes into smaller, manageable PRs.
    - PRs should be organized by **feature**, or find a **logical breakpoint** per PR (e.g., core logic first, then UI, or by specific sub-features).
4.  **Information Gathering:**
    - Ask the user for any **ticket numbers** (Jira, Linear, etc.) associated with these changes if they haven't been provided.
5.  **Drafting PR Details:**
    - For each proposed PR, use the format defined in `@.github/pull_request_template.md`.

## Output

Output a clear plan containing:

- **Proposed PRs:** For each PR:
  - Proposed branch name.
  - Proposed PR title.
  - Summary of changes included.
  - List of files that will be moved to this PR.
- **Sequence:** The recommended order in which these PRs should be created and merged.

## Final Confirmation

End the response with the following question:

> "Would you like me to go ahead with this plan and use the GitHub MCP (assuming it's enabled) to create the branches and PRs for you?"

## Requirements

- Always reference `@.github/pull_request_template.md` when planning the PR descriptions.
- Ensure PRs are small enough to be "manageable" for reviewers.
