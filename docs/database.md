# Database

> Read before writing any database model, query, or Server Action that touches persistence.

## Stack

- **MongoDB** — document store.
- **Mongoose 8** — schema definition, validation, connection management.

## Connection

A single Mongoose connection is created on first use and cached for the lifetime of the process. In development Next.js hot-reloads server files, so the cached promise is stored on `globalThis` to avoid opening a new connection on every reload.

```
src/lib/db/
├── index.ts          # connectDb() — cached connection helper
└── models/
    ├── user.ts       # User model
    ├── link.ts       # Link model
    └── ...           # one file per model
```

### `lib/db/index.ts` pattern

```ts
import mongoose from "mongoose";

const MONGODB_URI = process.env.MONGODB_URI!;

interface CachedConnection {
  conn: typeof mongoose | null;
  promise: Promise<typeof mongoose> | null;
}

declare global {
  // eslint-disable-next-line no-var
  var _mongooseCache: CachedConnection | undefined;
}

const cached: CachedConnection = globalThis._mongooseCache ?? {
  conn: null,
  promise: null,
};
globalThis._mongooseCache = cached;

export async function connectDb() {
  if (cached.conn) return cached.conn;

  if (!cached.promise) {
    cached.promise = mongoose.connect(MONGODB_URI, {
      bufferCommands: false,
    });
  }

  cached.conn = await cached.promise;
  return cached.conn;
}
```

Every Server Action and Route Handler calls `await connectDb()` before any query.

## Schema Conventions

| Rule | Detail |
| --- | --- |
| **Strict mode** | `{ strict: true }` (Mongoose default) — extra fields are silently dropped, never persisted. |
| **Timestamps** | `{ timestamps: true }` on every schema — adds `createdAt` and `updatedAt` automatically. |
| **userId index** | Every document that belongs to a user has a `userId: ObjectId` field with an index. |
| **handle index** | Schemas with a user-facing slug add a compound unique index on `{ userId, handle }`. |

### Model file template

```ts
import { Schema, model, models, type InferSchemaType } from "mongoose";

const linkSchema = new Schema(
  {
    userId: { type: Schema.Types.ObjectId, required: true, index: true },
    handle: { type: String, required: true },
    url:    { type: String, required: true },
    label:  { type: String, default: "" },
  },
  { timestamps: true },
);

linkSchema.index({ userId: 1, handle: 1 }, { unique: true });

export const Link = models.Link ?? model("Link", linkSchema);
export type LinkDocument = InferSchemaType<typeof linkSchema>;
```

Key points:

- **`models.Link ?? model(...)`** prevents the `OverwriteModelError` that occurs when Next.js hot-reloads the file.
- Export the inferred type so Server Actions and components stay in sync without manual interfaces.
- Keep schemas flat. If a sub-document grows beyond three fields, promote it to its own collection.

## User Scoping

Every query **must** include `userId` in the filter so a user can only read, update, or delete their own data. This is the primary authorization boundary.

```ts
// correct
const links = await Link.find({ userId: session.user.id });

// wrong — returns data across all users
const links = await Link.find({ handle: "my-link" });
```

Server Actions should obtain `userId` from the server-side session (e.g. `auth()` or `getSession()`), never from client-supplied input.

## Environment

| Variable | Purpose |
| --- | --- |
| `MONGODB_URI` | Full connection string including database name (e.g. `mongodb+srv://.../<db>?retryWrites=true`). |

Add `MONGODB_URI` to `.env.local` for development and to the hosting provider's environment for production. Never commit connection strings to the repository.

## Query Rules

1. **Always `await connectDb()`** at the top of any server-side function that queries the database.
2. **Always filter by `userId`** — no exceptions outside admin tooling (which does not exist yet).
3. **Use `lean()`** for read-only queries to skip Mongoose hydration and return plain objects.
4. **Prefer `findOneAndUpdate` with `{ new: true }`** over separate find-then-save for atomic updates.
5. **Validate at the boundary** — let Mongoose schema validation reject bad data; don't duplicate checks in every action.
