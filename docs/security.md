# Security

Rules for secrets, headers, rate limiting, and user-generated content.
Read before handling environment variables, configuring headers, adding rate limits, or rendering user input.

---

## Secrets

- All secrets live in **environment variables**, never in code or the repo.
- `.env.local` is gitignored — use it for local development secrets.
- `.env.example` is checked in as a template with placeholder values (no real secrets).
- Never log, serialize, or expose secret values to the client.

## Security Headers

Set the following in `next.config.js`:

| Header              | Value / Purpose                                    |
| ------------------- | -------------------------------------------------- |
| `Content-Security-Policy` | Restrict script/style/frame sources to trusted origins. |
| `X-Frame-Options`   | `DENY` — prevent clickjacking.                     |
| `Referrer-Policy`   | `strict-origin-when-cross-origin` — limit referrer leakage. |

## Rate Limiting

- **Sign-in attempts** — rate limit per IP to prevent brute-force attacks.
- **Link creation** — rate limit per authenticated user to stop abuse.
- Implement at the Server Action or Route Handler boundary, not in middleware.

## User-Generated Content

- **Link URLs and titles** are escaped on render (React's default JSX escaping handles most cases — never use `dangerouslySetInnerHTML` with user input).
- **Outbound links** always include `rel="noopener noreferrer"` and `target="_blank"`.
- Validate URL schemes on input — allow only `https://` and `http://`.
