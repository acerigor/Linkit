# Data Fetching

> Read before loading data in a page or component.

## Principle

Server Components fetch data by calling the database directly — never by issuing HTTP requests to internal API routes. Client Components never query the database; they receive data as props from a parent Server Component.

## Private Data (Dashboard)

Queries for private data are scoped to the signed-in user's `id`, obtained from the server-side session.

```ts
import { auth } from "@/lib/auth";
import { connectDb } from "@/lib/db";
import { Link } from "@/lib/db/models/link";

export default async function DashboardPage() {
  const session = await auth();
  await connectDb();

  const links = await Link.find({ userId: session!.user.id }).lean();

  return <LinkList links={links} />;
}
```

Key points:

- Resolve the user from `auth()` on the server — never accept a user id from the client.
- Always filter by `userId` so one user cannot see another's data.
- Use `.lean()` for read-only queries.

## Public Data (Profile Pages)

Public profile pages query by `handle` instead of `userId`. No session is required.

```ts
// app/user/[handle]/page.tsx
import { connectDb } from "@/lib/db";
import { Link } from "@/lib/db/models/link";

export default async function ProfilePage({ params }: { params: { handle: string } }) {
  const { handle } = await params;
  await connectDb();

  const links = await Link.find({ handle }).lean();

  return <PublicProfile links={links} />;
}
```

Only expose fields that are safe for public view — never leak `userId`, email, or internal ids in the response.

## Client Components

Client Components do not import database code. They receive already-fetched data as props from a Server Component.

```tsx
// Server Component — fetches data
import { LinkEditor } from "@/components/dashboard/link-editor";

export default async function EditPage() {
  const session = await auth();
  await connectDb();
  const link = await Link.findOne({ userId: session!.user.id, _id: id }).lean();

  return <LinkEditor link={link} />;
}

// Client Component — receives data, handles interactivity
"use client";

export function LinkEditor({ link }: { link: LinkDocument }) {
  // local state, event handlers, Server Action calls — no database imports
}
```

## Caching

Use `unstable_cache` (or the Next.js `fetch` cache for external HTTP calls) to avoid redundant database reads. Tag every cached entry so `revalidateTag` can clear it after mutations.

```ts
import { unstable_cache } from "next/cache";

const getLinks = unstable_cache(
  async (userId: string) => {
    await connectDb();
    return Link.find({ userId }).lean();
  },
  ["user-links"],
  { tags: ["links"] },
);
```

After a mutation in a Server Action, invalidate the relevant tag:

```ts
"use server";

import { revalidateTag } from "next/cache";

export async function createLink(data: CreateLinkInput) {
  // ... validate, write to db
  revalidateTag("links");
}
```

### Tag Naming

| Tag | Scope | Cleared after |
| --- | --- | --- |
| `links` | All link queries for the current user | Link created, updated, or deleted |
| `profile-{handle}` | Public profile data for a handle | Profile or link changes for that handle |

Add new tags as features grow, keeping names short and predictable.

## Rules

1. **Server Components fetch, Client Components receive.** Never import database code in a `"use client"` file.
2. **No internal fetch calls.** Do not `fetch("/api/...")` from a Server Component — call the database directly.
3. **Scope every query.** Private data filters by `userId`; public data filters by `handle`.
4. **Cache with tags.** Wrap repeated reads in `unstable_cache` with a tag so mutations can invalidate them with `revalidateTag`.
5. **Lean reads.** Use `.lean()` on every read-only Mongoose query.
