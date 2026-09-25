# Auth

> Read before touching sign-in, sessions, route protection, or ownership checks.

## Stack

- **NextAuth (Auth.js)** — handles sign-in, sessions, and security following industry best practices.

## Route Protection

All routes under `app/(dashboard)/*` are protected by default and require an authenticated session. Middleware enforces access before the page renders — unauthenticated requests are redirected to sign-in.

The public profile at `/user/[handle]` stays open to everyone.

## Ownership & Data Access

Users can only read and write their own links. Identity is enforced on the server in every Server Action and at the database level through ownership checks on `userId`.

### Rules

1. **Never trust the client.** Always resolve the current user from the session on the server — never accept a `userId` from the request body or query string.
2. **Scope every query.** Every read and write query must include the session user's `userId` in the filter so one user can never access another's data.
3. **Fail closed.** If the session is missing or invalid, reject the request — do not fall back to anonymous access.

## File Layout

```
src/lib/auth/             # Auth config, session helpers
src/app/api/auth/[...nextauth]/  # NextAuth route handler
middleware.ts             # Protects (dashboard) routes
```
