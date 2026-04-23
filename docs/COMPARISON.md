# Comparison with Similar Public Projects

This repository was created after confirming that related public projects already exist.

## Similar repos observed

### 1. Akuma-real/codex-canvas
- Focus: local desktop/TUI workflow for Codex image generation
- Strength: visual workflow, interactive UX
- Different from this repo: this repo is **CLI + Hermes skill packaging**, not a TUI app

### 2. starhunt/duct-cli
- Focus: adapter/proxy that exposes Codex image generation through an OpenAI Images-compatible interface
- Strength: useful for proxy/server setups
- Different from this repo: this repo is **Python-first local wrapper**, not an API compatibility layer

### 3. aymenbouferroum/gpt-imagen
- Focus: Claude Code plugin/skill workflows around GPT Image 2 generation and editing
- Strength: polished plugin marketplace presentation
- Different from this repo: this repo is **Hermes/OpenClaw-oriented**, explicitly documenting the local Codex login path

## Positioning for Hermes Codex Image Skill

This project is worth sharing only if it remains crisp about its scope:

- local workflow, not hosted service
- Hermes/OpenClaw skill integration, not generic agent marketplace only
- Python wrapper that users can inspect and extend easily
- explicit operational honesty about limitations and backend uncertainty

## Recommended public angle

If published, present it as:

> A Python-first Hermes/OpenClaw-friendly local Codex image wrapper that stabilizes Codex CLI image generation for automation and skills.

Avoid positioning it as:
- "the first"
- "the official way"
- proof of a specific backend image model
- a replacement for direct OpenAI Images API usage
