# Testing

How this project is tested: unit tests with Vitest, end-to-end QA with Playwright MCP.
Read before writing tests, adding test tooling, or setting up QA.

---

## Two Layers

| Layer         | Tool                        | Covers                                      |
| ------------- | --------------------------- | ------------------------------------------- |
| Unit          | Vitest                      | Pure functions and Zod schemas              |
| End-to-end QA | Playwright MCP (`run-qa-suite` skill) | Full user flows, including Server Actions   |

## Unit Tests

- Use **Vitest** for pure functions and Zod schemas.
- Test files live **next to the file they test**, named `*.test.ts`.

```
src/lib/slug.ts
src/lib/slug.test.ts
```

- Keep units pure: test input → output. No database, no network, no rendering.

## End-to-End QA

- Driven by the **`run-qa-suite` skill** on top of **Playwright MCP**.
- There is **no `/e2e` folder**, **no `playwright.config.ts`**, and **no committed `.spec.ts` files** — QA is MCP-driven, not a checked-in Playwright project.
- **Server Actions are tested through MCP-driven QA**, exercised via real flows — not mocked.

## Test Database

- QA runs against a **separate test database**: `MONGODB_URI_TEST` in `.env.test`.
- **Never** run QA against the dev or prod database.

## Independence

- Every test is **independent** — no shared state, no test-order dependencies.
- A test sets up and tears down whatever it needs, and passes in isolation or in any order.
