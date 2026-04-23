# AGENTS.md

This file is for **Hermes/OpenClaw or other coding agents** that receive this repository with little or no extra context.

## Mission

Set up this repository so the user can generate images through a **locally logged-in Codex CLI**.

Do **not** present this project as:
- a hosted image API
- proof of the exact backend image model
- a GUI product

## Fastest safe install path

From the repository root:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -e .[dev]
```

If `python3.11` is unavailable, use another Python 3.11+ interpreter.

Alternative:

```bash
make PYTHON=python3.11 install
```

## Required prerequisites

Before claiming success, verify all 3:

```bash
python3.11 --version
codex --version
codex login status
```

Expected outcome:
- Python is **3.11+**
- `codex` exists in `PATH`
- `codex login status` reports a valid local login

If Codex is missing or logged out, **stop and report that clearly**. Do not pretend the repository is broken if the real issue is missing local Codex setup.

## Post-install verification

Run these in order:

```bash
source .venv/bin/activate
hermes-codex-image --version
ruff check .
pytest
python -m build
```

If the user wants a real end-to-end check and local Codex is logged in:

```bash
source .venv/bin/activate
hermes-codex-image \
  "Generate a minimal banana icon on a light background" \
  --output /tmp/hermes-codex-image-smoke.png
```

## Beginner-friendly explanation to give the user

Explain the repo in one sentence like this:

> This repository is a small Python wrapper that lets Hermes/OpenClaw reuse your already logged-in Codex CLI, generate an image, and save the result to a predictable file path with JSON metadata.

## Files worth reading first

1. `README.md` — human overview
2. `docs/HERMES_AGENT_INSTALL.md` — beginner + agent install guide
3. `docs/README.ko.md` — Korean beginner-friendly guide
4. `docs/VISUAL_QUICKSTART.md` — visual quickstart flow
5. `docs/TROUBLESHOOTING_QUICK.md` — fastest error triage
6. `docs/FAQ.md` — beginner questions answered quickly
7. `skill/SKILL.md` — skill-facing usage contract
8. `src/hermes_codex_image_skill/cli.py` — CLI entrypoint
9. `src/hermes_codex_image_skill/codex_runner.py` — actual runtime logic

## What to tell a first-time user to run

Use this exact minimal sequence:

```bash
git clone https://github.com/techkwon/hermes-codex-image-skill.git
cd hermes-codex-image-skill
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -e .[dev]
codex login status
hermes-codex-image --help
```

## Suggested handoff prompt for Hermes Agent

If the user pastes this repository to Hermes and wants the agent to do setup, a good prompt is:

> Open this repository and install it for me like I am a first-time user. Check Python, check whether Codex is installed and logged in, set up the virtualenv, install the package, run lint/tests/build, then summarize exactly what worked and what still needs my action.

## Guardrails

- Prefer small, auditable changes.
- Do not add hidden network services.
- Do not claim official OpenAI API equivalence.
- Keep docs honest when prerequisites are external to this repo.
