# Hermes Agent Install Guide

This guide is for **two audiences at once**:

1. **A human who is new to AI tools**
2. **A Hermes/OpenClaw agent that receives this repository and needs clear setup steps**

If you only do one thing, follow the **Quick Start for First-Time Users** below.

---

## What this repository does

In simple terms:

- you already have a local `codex` CLI
- you are already logged in there
- this repo gives you a cleaner command that:
  - asks Codex to generate an image
  - finds the generated file
  - copies it to a predictable output path
  - returns JSON metadata that automation can read

So this project is **not** a full image website.
It is a **small automation wrapper** around local Codex image generation.

---

## Before you start

You need these things on your computer:

### Required
- **Python 3.11 or newer**
- **Codex CLI installed**
- **A valid local Codex login**

### Quick checks

Run these commands:

```bash
python3.11 --version
codex --version
codex login status
```

What good looks like:
- Python prints `3.11.x` or newer
- Codex prints a version
- login status says you are logged in

If `codex` is missing or not logged in, this repository cannot complete a real generation yet.
That is a **prerequisite issue**, not a bug in this repo.

---

## Quick Start for First-Time Users

Open a terminal and run this exactly:

```bash
git clone https://github.com/techkwon/hermes-codex-image-skill.git
cd hermes-codex-image-skill
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -e .[dev]
```

Then check that the CLI is installed:

```bash
hermes-codex-image --help
```

If that prints usage text, installation worked.

---

## Your first real run

If `codex login status` is healthy, try:

```bash
hermes-codex-image \
  "Generate a minimal banana icon on a light background" \
  --output /tmp/hermes-codex-image-smoke.png \
  --metadata-json /tmp/hermes-codex-image-smoke.json
```

Expected result:
- an image file appears at `/tmp/hermes-codex-image-smoke.png`
- a JSON file appears at `/tmp/hermes-codex-image-smoke.json`

---

## Easiest explanation of the main command

```bash
hermes-codex-image "your prompt here" --output /path/to/result.png
```

Meaning:
- `hermes-codex-image` → this repo's CLI
- `"your prompt here"` → what image you want
- `--output ...` → where to save the final image

Optional:
- `--metadata-json /path/to/result.json` → also save structured JSON metadata
- `--timeout 300` → wait longer if generation is slow

---

## If you want Hermes Agent to install this for you

You can hand the repository to Hermes and say:

> Install this repository for me like I am a beginner. Check Python first, then check whether Codex exists and is logged in, create the virtualenv, install the package, run lint/tests/build, and tell me exactly what succeeded and what still needs my manual action.

That wording helps the agent avoid skipping prerequisite checks.

---

## Agent checklist

If you are an agent reading this repo, use this exact order:

### 1. Check prerequisites first

```bash
python3.11 --version
codex --version
codex login status
```

### 2. Install the repo

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -e .[dev]
```

### 3. Verify local tooling

```bash
source .venv/bin/activate
hermes-codex-image --version
ruff check .
pytest
python -m build
```

### 4. Optional real smoke test

Only do this if local Codex login is healthy:

```bash
source .venv/bin/activate
hermes-codex-image \
  "Generate a minimal banana icon on a light background" \
  --output /tmp/hermes-codex-image-smoke.png
```

### 5. Report clearly

Agents should report in this format:
- what prerequisites passed
- what was installed
- what validation commands passed
- whether a real Codex generation was tested
- what still requires human action

---

## Common failure cases

### `python3.11: command not found`
Use another Python 3.11+ binary available on the machine.
Examples:

```bash
python3 --version
python3 -m venv .venv
```

### `codex: command not found`
Codex CLI is not installed or not in `PATH`.
Fix Codex first.

### `codex login status` says not logged in
You must log into Codex locally first.
This repo does not do login for you.

### `hermes-codex-image --help` works but real generation fails
Usually one of these is true:
- Codex is logged out
- Codex changed output behavior
- the prompt timed out

If needed, retry with a bigger timeout:

```bash
hermes-codex-image "Generate a minimal banana icon on a light background" --output /tmp/test.png --timeout 300
```

---

## Which file to read next

- `README.md` → overall project overview
- `docs/HERMES_AGENT_INSTALL.md` → detailed install guide
- `docs/README.ko.md` → Korean beginner guide
- `docs/VISUAL_QUICKSTART.md` → visual quickstart flow
- `docs/TROUBLESHOOTING_QUICK.md` → fastest failure triage
- `AGENTS.md` → short agent handoff instructions
- `skill/SKILL.md` → skill-oriented contract
- `docs/KNOWN_LIMITATIONS.md` → what this repo does not claim

## Honest limitation reminder

This repository is useful because it makes a local workflow easier to automate.
It does **not** prove the exact backend model behind Codex image generation.
It also depends on local Codex CLI behavior staying reasonably similar.
