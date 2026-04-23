---
name: codex-image-generation-oauth
description: Generate images through local Codex CLI using existing ChatGPT/Codex login, then copy the result into a stable workspace path.
version: 0.1.0
author: techkwon
license: MIT
metadata:
  hermes:
    tags: [Codex, Image-Generation, Hermes, OAuth, ChatGPT]
---

# Codex Image Generation via OAuth

Use this skill when you want Hermes/OpenClaw to generate an image through a **locally logged-in Codex CLI** instead of calling the OpenAI Images API directly.

## What this skill does

- checks whether `codex` exists in `PATH`
- verifies current login state via `codex login status`
- runs `codex exec --skip-git-repo-check`
- extracts the generated image path from stdout **or** from `~/.codex/generated_images`
- copies the result to a stable output path
- prints JSON so higher-level automation can parse it safely

## Important limits

- This skill depends on **local Codex CLI behavior** and existing login state.
- It proves that image generation works through Codex, but it does **not** by itself prove the exact backend image model identity.
- If Codex changes its output format or storage path, this wrapper may need updating.

## Usage

```bash
python3 skill/scripts/generate_with_codex.py \
  "Generate a premium SaaS hero image of a banana turning into academic charts" \
  --output /tmp/paper-banana-hero.png
```

## JSON contract

Successful run:

```json
{
  "ok": true,
  "source_path": "/Users/.../.codex/generated_images/.../ig_xxx.png",
  "final_path": "/tmp/paper-banana-hero.png",
  "mode": "copied"
}
```

Failure example:

```json
{
  "ok": false,
  "error": "codex command not found in PATH"
}
```

## Recommended workflow

1. Confirm `codex login status` is healthy.
2. Start with a concise prompt.
3. Save to an explicit output path.
4. Visually inspect the result before downstream use.
5. For public demos, avoid claims about exact backend model identity unless separately verified.
