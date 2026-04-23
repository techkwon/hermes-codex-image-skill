# Release Checklist

- [ ] README install steps verified on a clean Python 3.11 environment
- [ ] `pip install -e .[dev]` succeeds
- [ ] `ruff check .` succeeds
- [ ] `pytest` succeeds
- [ ] `python -m build` succeeds
- [ ] real Codex smoke test succeeds locally
- [ ] example images are visually reviewed
- [ ] no secrets or private tokens in repo
- [ ] no unverifiable claims about exact backend image model
- [ ] docs mention the dependency on local Codex login
- [ ] repo description and topics prepared
- [ ] initial release tag planned
