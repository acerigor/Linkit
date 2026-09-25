---
name: create-feature
description: Use after a feature plan has been approved (see plan-feature skill) to build the feature in code. Triggers when the user says "build it", "implement the plan", "go ahead and build", "start implementing", "create the feature", "write the code", "let's build this now", or otherwise signals that an approved plan in ./plans/<current-branch>.md should now be turned into code. Reads the plan and the /docs files it cites, pulls live library docs via Context7, then writes only the source code — no tests, no QA, no commits — and hands back with a 2–3 line summary of what was built.
---

# create-feature

Build the feature described in the approved plan file. Code only — no tests, no QA runs, no commits. Stop and hand back when the code is written.

## When to use

Auto-trigger after a plan has been approved (via the `plan-feature` skill) and the user signals it's time to build. Phrases like "build it", "implement the plan", "start implementing", "create the feature", "write the code", "go ahead", or "let's build this now" after a plan exists all count.

Do **not** run:
- Before a plan file exists at `./plans/<current-branch>.md`. If none exists, invoke `plan-feature` first.
- When the user explicitly asks for tests, QA, or a commit — those are separate skills (`write-tests`, `run-qa-suite`, commit skills).

## Steps

1. **Load the plan.** Determine the current branch with `git branch --show-current`, then read `./plans/<current-branch>.md`. If it doesn't exist, stop and tell the user to run `plan-feature` first. Do not invent a plan from memory.

2. **Read every doc the plan cites.** The plan's "Docs consulted" section lists them — read each one in full before writing code. Also read `docs/coding-standards.md` and `docs/architecture.md` if the plan didn't already list them.

3. **Pull live library docs via Context7.** For any third-party library the plan uses — Next.js, Mongoose, NextAuth, Zod, Tailwind, React, etc. — call `mcp__context7__resolve-library-id` then `mcp__context7__query-docs` for the specific APIs you'll touch. Do not rely on training-data recall for API signatures. Per `CLAUDE.md`, also skim `node_modules/next/dist/docs/index.md` before writing Next.js 16 code.

4. **Build the feature.** Create and modify exactly the files listed in the plan's "Files to create" and "Files to change" sections. Follow project conventions:
   - TypeScript strict, Prettier/ESLint clean, import order per `docs/coding-standards.md`.
   - Server/Client Component split per `docs/architecture.md` and `docs/data-fetching.md`.
   - User-scoping and Mongoose conventions per `docs/database.md`.
   - Zod validation at the Server Action boundary per `docs/errors-and-validation.md`.
   - Auth checks per `docs/auth.md`.
   - Tailwind tokens per `docs/design-system.md`; component shape per `docs/ui.md`.
5. **Stay in scope.** Do not add files or refactors not in the plan. If you discover the plan is wrong or incomplete, stop and surface the gap — do not silently expand scope. Ask the user whether to update the plan.

6. **Stop when the code is written.** Do **not**:
   - Write or scaffold tests.
   - Run the QA suite or start the dev server for QA.
   - Stage, commit, or push.
   - Open a PR.
   Report in 2–3 lines: what was built and which files changed. Then hand back and wait — the user will explicitly trigger `write-tests` and `run-qa-suite` when ready.

## Handoff format

```
Built <feature name>.
Created: <file>, <file>, ...
Changed: <file>, <file>, ...
Ready for /write-tests and /run-qa-suite when you are.
```

## Rules

- No tests. No QA. No commits. No PRs. Code only.
- No files outside the approved plan without explicit user approval.
- Every third-party API call is verified against Context7 (or `node_modules/next/dist/docs/` for Next.js 16) before it lands in code.
- If the plan is missing or the branch has no plan file, stop and route the user to `plan-feature`.
