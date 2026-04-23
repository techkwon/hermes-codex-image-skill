# Contributing

Thanks for considering a contribution.

## Principles

Please keep contributions aligned with the repository scope:

- local Codex workflow wrapper
- Hermes/OpenClaw automation friendliness
- honest documentation over hype
- small, auditable Python implementation

## Before opening a PR

1. Create and activate a Python 3.11+ virtual environment.
2. Install dev dependencies.
3. Run lint, tests, and build locally.

```bash
make install
make lint
make test
make build
```

## What we welcome

- better error handling
- improved parsing resilience
- tighter tests and fixtures
- docs clarifications
- clearer examples for Hermes/OpenClaw users

## What to avoid

- unverifiable claims about the exact backend image model
- unrelated GUI/server expansion without a strong reason
- hidden network behavior or secret-handling changes without documentation

## Pull request checklist

- [ ] Scope is still local Codex image automation
- [ ] Tests added or updated for behavior changes
- [ ] README/docs updated if user-visible behavior changed
- [ ] No secrets, local tokens, or private paths leaked
- [ ] No hype claims that exceed what the code actually proves
