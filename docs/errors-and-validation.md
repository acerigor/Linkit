# Errors & Validation

> Read before writing Server Actions, form handling, or error boundaries.

## Validation

- **Zod** validates all input at the Server Action boundary, before any database call.
- Shared schemas live in `src/lib/validation/` — co-locate with the domain, not the route.

```
src/lib/validation/
├── link.ts       # linkSchema, createLinkSchema, …
├── user.ts       # profileSchema, handleSchema, …
└── ...
```

### Validation errors are returned, not thrown

Server Actions return a typed result object so the form can render errors inline next to each field.

```ts
type ActionResult<T = void> =
  | { success: true; data: T }
  | { success: false; errors: Record<string, string[]> };
```

```ts
export async function createLink(formData: FormData): Promise<ActionResult> {
  const parsed = createLinkSchema.safeParse(Object.fromEntries(formData));
  if (!parsed.success) {
    return {
      success: false,
      errors: parsed.error.flatten().fieldErrors,
    };
  }
  // … proceed with validated data
}
```

## Unexpected Errors

- **Throw real `Error` objects** — never strings, never Zod errors.
- The nearest `error.tsx` boundary catches them and shows a user-safe message.
- Log with enough context to debug (action name, user id, input shape) but **never expose raw error messages or stack traces to the client**.

```ts
try {
  await db.link.create(data);
} catch (err) {
  console.error("[createLink]", { userId, url: data.url }, err);
  throw new Error("Failed to create link");
}
```

## Rules

1. **Validate first.** No database call runs on unvalidated input.
2. **Return field errors.** Validation failures produce a result object the UI can map to individual fields — never throw them.
3. **Throw the rest.** Unexpected failures (database down, network errors) are thrown and caught by `error.tsx`.
4. **Log for debugging, sanitise for the client.** Server logs get full context; the user sees a generic message.
