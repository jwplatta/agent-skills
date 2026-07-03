---
name: explain-diff
description: Explain the current git diff or a selected patch in a way a human can quickly understand. Use when a user wants the changes summarized, needs background and intuition before code details, wants a guided walkthrough of the key hunks instead of raw diff order, wants the explanation written to the terminal or a markdown note, or wants a short quiz about the change.
---

# Explain Diff

Read the current git diff or the user-selected diff first. Explain the change from context to mechanics, not from file order.

## Workflow

1. Establish scope.
- Determine whether to inspect `git diff`, `git diff --cached`, a commit, or a specific file.
- Prefer the smallest diff that answers the user's request.

2. Explain the background first.
- State the problem, limitation, bug, or maintenance goal the diff appears to address.
- If the motivation is not explicit in the diff, say that you are inferring it.
- Connect the change to the surrounding subsystem so the reader understands why the code exists.

3. Explain the intuition second.
- Describe the design idea in plain language before discussing implementation.
- Answer questions like: why this approach, what the new data flow is, what the safety or performance tradeoff is, and what changed conceptually.
- If a diagram would help, generate or suggest a simple image or ASCII diagram showing before/after flow, data shape, or control flow.

4. Walk through the important code changes.
- Group related hunks by purpose, not alphabetically and not just by file order.
- For each group, explain what the old code did, what the new code does, and why that difference matters.
- Highlight the few key lines or branches that carry most of the meaning.
  - Use codeblocks in the markdown
- Avoid narrating every changed line unless the user asks for hunk-by-hunk detail.

5. Close with trade-offs.
- Explain the main trade-offs in the chosen approach: complexity, performance, safety, flexibility, compatibility, or operational cost.
- Note likely edge cases, migration concerns, or behavior changes when they affect those trade-offs.
- Be explicit when something is a refactor versus a behavior change.

## Output Formats

Choose the output target the user asked for:
- Terminal: concise explanation with clear sections.
- Repo markdown note: write a markdown file inside the current repository when requested.
- Obsidian note: when the user wants Obsidian output, use the Obsidian MCP server to read or write markdown notes in the `Notes` folder of the `my_ken` vault. If the MCP server or vault access is unavailable, say so and fall back to a repo markdown note.
- Pull request: use the output to write the pull request summary.

When writing a note, include these sections in order:
1. Background
2. Intuition
3. Guided Walkthrough
4. Trade-offs
5. Questions

## Style

- Optimize for human readability over diff completeness.
- Use short paragraphs and group changes by intent.
- Use explanations concise and focused.
- Prefer concrete explanations like "this moves validation earlier" or "this changes the stored type from string to date".
- Clearly label inference versus direct evidence from the diff.

## Images

Use images only when they would materially improve understanding.
Good cases:
- before/after architecture
- request/response flow
- table/schema changes
- state machine or control-flow changes

Keep visuals simple. Prefer ASCII or markdown diagrams unless the user explicitly wants an actual image.

## Quiz

When useful, generate 3 to 5 short questions about the diff and write them to a markdown note.
- Write the quiz to either a markdown file inside the repo or, for Obsidian output, use the Obsidian MCP server to create a markdown note in the `Notes` folder of the `my_ken` vault.
- Focus on what changed, why it changed, and what trade-offs remain.
- Prefer questions that test understanding, not memorization.
- Include brief answer keys only when the user asks for them.

## Avoid

- Do not just restate the raw diff in file order.
- Do not lead with implementation details before giving context.
- Do not claim a motivation unless the diff or surrounding context supports it; otherwise mark it as inference.
- Do not overwhelm the user with every touched line when a grouped explanation is clearer.
