# Git Conventions

Rules for commits, branches, and pull requests.
Read before committing code, creating branches, or opening PRs.

---

## Commits

Follow [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix     | Use for                              |
| ---------- | ------------------------------------ |
| `feat`     | New feature                          |
| `fix`      | Bug fix                              |
| `docs`     | Documentation only                   |
| `refactor` | Code change that neither fixes nor adds |
| `test`     | Adding or updating tests             |
| `chore`    | Tooling, config, dependencies        |

- Subject line is short, imperative mood (`add link creation`, not `added link creation`).
- No period at the end of the subject.

## Branches

Name branches as `type/short-description`:

- `feat/add-links`
- `fix/session-redirect`
- `docs/security-guide`
- `chore/update-deps`

## Pull Requests

- Every feature is built on its own branch and merged through a pull request.
- Never commit straight to `main`.
- Keep a clean history — squash or rebase before merge when commits are noisy.
- Every PR requires human review before merge.
