---
name: plan-feature
description: Use at the start of every new feature, before any code is written. Triggers when the user is planning, scoping, designing, or kicking off a new feature, page, route, model, form, endpoint, or user-facing capability — e.g. "let's build X", "add a Y feature", "I want to add", "start on", "scope out", "plan the", "design the", or any request for new functionality that hasn't yet been broken into files. Enters Plan Mode, produces a short technical plan grounded in /docs conventions, waits for explicit approval, then writes the approved plan to ./plans/<current-branch>.md before any code is written.
---

# plan-feature

Run this skill at the **start** of every new feature, before touching any code. Its job is to force a short, doc-grounded plan and get explicit approval before implementation.

## When to use

Auto-trigger whenever the user is starting a new feature — a new page, route, model, form, endpoint, flow, or user-facing capability that hasn't yet been broken into files. Signals include "let's build", "add a ... feature", "start on", "scope out", "plan the", "design the", "I want to add", or any new-functionality request without an existing plan file for the current branch.

Do **not** run for: bug fixes to existing code, small tweaks, doc-only edits, or when a plan file for the current branch already exists and the user is continuing that work.

## Steps

1. **Enter Plan Mode.** Call `ExitPlanMode` only after the user approves — first switch into plan mode via `EnterPlanMode`. No file edits, writes, or code changes may happen before approval.

2. **Read the relevant /docs.** Always read `docs/architecture.md` and `docs/database.md`. Then read the docs matching the feature area — e.g.:
   - New route or page → `docs/routing.md`, `docs/data-fetching.md`
   - Form or Server Action → `docs/errors-and-validation.md`, `docs/coding-standards.md`
   - Auth / session / access control → `docs/auth.md`, `docs/security.md`
   - UI component → `docs/ui.md`, `docs/design-system.md`
   - Tests → `docs/testing.md`
   - Commits / branches → `docs/git-conventions.md`

3. **Draft the plan** in the exact structure below. Keep it short — bullets, not prose. Every design choice must cite the doc it comes from (e.g. "per `docs/database.md`, user-scope with `userId`").

4. **Present the plan and wait for explicit approval.** Use `ExitPlanMode` to surface it. Do not write any code or files (including the plan file itself) until the user approves.

5. **On approval, persist the plan.** Determine the current branch with `git branch --show-current`, then write the approved plan to `./plans/<current-branch>.md`. Create the `plans/` directory if it doesn't exist. Only then hand off to implementation.

## Plan format

```markdown
# <Feature name>

## Summary
One or two sentences: what this feature does and why.

## Docs consulted
- `docs/architecture.md` — <what it constrained>
- `docs/<area>.md` — <what it constrained>
- ...

## Files to create
- `src/app/<path>/page.tsx` — <one-line purpose>
- `src/lib/<...>.ts` — <one-line purpose>
- ...

## Files to change
- `src/<path>` — <what changes and why>
- ...

## Data model / validation
- Mongoose schema changes, Zod schemas, indexes, user-scoping. Cite the doc.

## Open questions
- Anything the user needs to decide before implementation. Leave empty if none.

## QA Scenarios
Cover happy path, auth boundary, validation, and edge cases. 3–6 scenarios.

1. **Happy path** — User does X → expect Y.
2. **Auth boundary** — Unauthenticated user tries X → expect Y.
3. **Validation** — User submits invalid X → expect Y.
4. **Edge case** — <specific edge> → expect Y.
5. ...
```

## Rules

- No code, no file writes, no schema changes before approval.
- Every non-trivial choice cites a `/docs` file. If a doc is silent on something, say so explicitly rather than inventing convention.
- QA Scenarios are concrete: name the actor, the action, and the expected observable result. Not "form validation works" — "user submits a link with empty URL → inline field error 'URL is required', no network request".
- The plan file path is exactly `./plans/<current-branch>.md`, using the output of `git branch --show-current` verbatim (slashes in branch names create subdirectories — that's fine, `mkdir -p` the parent).
- If a plan file for the current branch already exists, ask whether to overwrite, append, or start a new branch before writing.
