# Troubleshooting Quick Reference

This page is for the **5 problems most people hit first**.

---

## 1. `python3.11: command not found`

Meaning:
- your machine does not have a `python3.11` command in `PATH`

What to try:

```bash
python3 --version
python3 -m venv .venv
```

Use any Python **3.11+** binary.

---

## 2. `codex: command not found`

Meaning:
- Codex CLI is not installed, or it is not available in `PATH`

What to try:

```bash
codex --version
which codex
```

If those fail, fix your local Codex install first.
This repository cannot generate real images without it.

---

## 3. `codex login status` says you are not logged in

Meaning:
- Codex exists, but your local login is not active

What to try:

```bash
codex login status
```

If login is not healthy, log into Codex first.
This repository does **not** perform login for you.

---

## 4. `hermes-codex-image --help` works, but real generation fails

Meaning:
- the Python package installed correctly
- but a real end-to-end Codex generation still failed

Most common causes:
- Codex login is not healthy
- Codex changed output behavior
- the request timed out

What to try:

```bash
codex login status
hermes-codex-image "Generate a minimal banana icon on a light background" --output /tmp/test.png --timeout 300
```

---

## 5. Install succeeded, but you want to know if the repo itself is healthy

Run the built-in quality checks:

```bash
source .venv/bin/activate
ruff check .
pytest
python -m build
```

Or use the shortcut:

```bash
make doctor
```

If these pass, the repository itself is in good shape.
If a real image still fails, the remaining problem is usually in **Codex installation/login/runtime**, not the Python package structure.

---

## Good escalation path

If you are still stuck, check in this order:

1. Python version
2. Codex installed
3. Codex login healthy
4. package installed
5. repo quality checks pass
6. real smoke test

---

## Related guides

- [README.md](../README.md)
- [HERMES_AGENT_INSTALL.md](HERMES_AGENT_INSTALL.md)
- [README.ko.md](README.ko.md)
- [VISUAL_QUICKSTART.md](VISUAL_QUICKSTART.md)
- [../AGENTS.md](../AGENTS.md)
