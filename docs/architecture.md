# Architecture

> Read before adding folders, files, or new patterns to the codebase.

## Rendering Model

- **Server Components** are the default. Every component is a Server Component unless it needs browser APIs or interactivity.
- **Client Components** are opted-in with `"use client"` only where required (event handlers, hooks, browser APIs).
- Keep Client Components as leaves — push interactivity down and data-fetching up.

## Directory Structure

```
src/
├── app/                  # App Router — routes, layouts, loading/error boundaries
│   ├── (group)/          # Route groups for shared layouts without URL segments
│   ├── api/              # Route Handlers (GET, POST, etc.)
│   └── globals.css       # Tailwind v4 theme tokens
├── components/
│   ├── ui/               # Design-system primitives (Button, Input, Card, …)
│   └── [feature]/        # Feature-scoped components (dashboard/, auth/, …)
├── lib/
│   ├── db/               # Database client & query helpers
│   ├── auth/             # Auth helpers, session utilities
│   └── types/            # Shared TypeScript types & Zod schemas
├── actions/              # Server Actions (co-located or imported by routes)
└── hooks/                # Client-side React hooks
```

## Naming Conventions

| Item              | Convention    | Example                        |
| ----------------- | ------------- | ------------------------------ |
| Files & folders   | kebab-case    | `user-profile.tsx`             |
| Components        | PascalCase    | `UserProfile`                  |
| Server Actions    | verb-first    | `createLink`, `deleteBookmark` |
| Route Handlers    | HTTP verb fn  | `export async function GET()`  |
| Types / Interfaces| PascalCase    | `LinkRecord`, `UserSession`    |
| Hooks             | `use` prefix  | `useLinks`, `useAuth`          |

## Data Flow

1. **Server Components** fetch data directly (database, external APIs) — no client-side fetching for initial loads.
2. **Server Actions** (`"use server"`) handle mutations. They validate input, perform the write, and revalidate the cache.
3. **Route Handlers** (`app/api/`) are reserved for webhooks, external integrations, and endpoints consumed outside of React.
4. **Client Components** call Server Actions for mutations and use hooks/context for local UI state only.

## Shared Code (`/lib`)

- `lib/db/` — single database client instance, exported query helpers. No raw queries outside this folder.
- `lib/auth/` — session helpers, permission checks, auth config. All auth logic funnels through here.
- `lib/types/` — shared TypeScript types and Zod schemas. Collocate the Zod schema next to its TS type.

## Component Guidelines

- **`components/ui/`** — Stateless or minimally-stateful primitives. Accept variants via props, never fetch data.
- **`components/[feature]/`** — Compose UI primitives with feature logic. May be Server or Client Components depending on need.
- A component that grows beyond ~200 lines should be split. Extract sub-components into the same feature folder.

## Path Aliases

`@/*` maps to `./src/*`. Always use the alias for imports:

```ts
import { Button } from "@/components/ui/button";
import { db } from "@/lib/db";
```
