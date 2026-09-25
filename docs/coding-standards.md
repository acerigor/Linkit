# Coding Standards

> Read before writing or reviewing any TypeScript in this project.

## Language & Tooling

- **TypeScript** with `strict: true` — no implicit any, no unchecked index access.
- **Prettier** formats all code — do not override its style choices.
- **ESLint** with the Next.js config (`core-web-vitals` + `typescript`) catches issues Prettier doesn't.

## Imports

Order imports in three groups, separated by a blank line:

1. External packages (`react`, `next/link`, `mongoose`, …)
2. Internal aliases (`@/lib/…`, `@/components/…`, `@/actions/…`)
3. Relative imports (`./`, `../`)

```ts
import { useState } from "react";
import Link from "next/link";

import { connectDb } from "@/lib/db";
import { Button } from "@/components/ui/button";

import { formatDate } from "./utils";
```

## Components

- Use **function declarations**, not arrow functions assigned to variables.
- Type props with an inline type or a named `Props` type — never `any`.
- **No default exports** except for Next.js route files (`page.tsx`, `layout.tsx`, `route.ts`, etc.) where the framework requires them.

```ts
// ✅ Named export with typed props
type Props = {
  title: string;
  count: number;
};

export function StatCard({ title, count }: Props) {
  return (
    <div>
      <h3>{title}</h3>
      <p>{count}</p>
    </div>
  );
}
```

## Async

- Use `async`/`await` — never `.then()` chains.
- Throw real `Error` objects, never strings.

```ts
// ✅
const user = await getUser(id);
if (!user) throw new Error("User not found");

// ❌
getUser(id).then((u) => { … });
throw "User not found";
```

## Type Safety

- **No `any`**. Use `unknown` and narrow, or type the value properly.
- **No `@ts-ignore`** without a comment explaining why the suppression is necessary.

```ts
// ✅ If suppression is truly unavoidable
// @ts-ignore — third-party type is missing the `onDismiss` callback
```
