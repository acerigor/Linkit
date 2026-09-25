# Routing

> Read before adding routes, layouts, or API endpoints.

## Route Map

### Public Routes

| Path | Description |
| --- | --- |
| `/` | Landing page |
| `/user/[handle]` | Public profile — visible to everyone, no session required |

### Authenticated Routes — `(dashboard)` group

All routes in this group require an authenticated session. Middleware redirects unauthenticated users to sign-in.

| Path | Description |
| --- | --- |
| `/dashboard` | User's main dashboard |
| `/add-links` | Create and manage links |

### Auth Routes — `(auth)` group

| Path | Description |
| --- | --- |
| `/sign-in` | Sign-in page |
| `/sign-up` | Sign-up page |

## Directory Structure

```
src/app/
├── page.tsx                  # Landing page (/)
├── layout.tsx                # Root layout
├── user/
│   └── [handle]/
│       └── page.tsx          # Public profile
├── (dashboard)/
│   ├── layout.tsx            # Shared dashboard layout (auth-gated)
│   ├── dashboard/
│   │   └── page.tsx
│   └── add-links/
│       └── page.tsx
├── (auth)/
│   ├── layout.tsx            # Auth pages layout
│   ├── sign-in/
│   │   └── page.tsx
│   └── sign-up/
│       └── page.tsx
└── api/                      # Webhooks & third-party callbacks only
    └── auth/
        └── [...nextauth]/
            └── route.ts
```

## Rules

1. **Each route owns its boundaries.** Add `layout.tsx`, `loading.tsx`, and `error.tsx` at the route level where needed — don't rely on parent boundaries for route-specific UI.
2. **Route Handlers are for external callers only.** `/app/api` is reserved for webhooks and third-party callbacks (e.g. NextAuth, payment providers). All internal data mutations and fetches go through Server Actions.
3. **Route groups don't affect URLs.** `(dashboard)` and `(auth)` are organisational — they share layouts and middleware rules without adding a URL segment.
4. **Middleware enforces access.** The `(dashboard)` group is protected at the middleware level. See `docs/auth.md` for ownership and session rules.
