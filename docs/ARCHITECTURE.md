# Architecture Notes

## Core workflow

1. **Preflight**
   - resolve `codex` from `PATH`
   - verify login state with `codex login status`
2. **Execution**
   - run `codex exec --skip-git-repo-check <prompt>`
3. **Result discovery**
   - prefer an absolute image path printed in stdout
   - otherwise scan `~/.codex/generated_images` (or `$CODEX_HOME/generated_images`) for new files
4. **Stabilization**
   - copy the chosen image into a caller-controlled output path
   - emit structured JSON to stdout
   - optionally persist the same metadata to a sidecar JSON file

## Why this shape

This wrapper deliberately stays small and stdlib-first.

### Advantages
- easy to audit
- no network/API credential handling inside the wrapper itself
- simple to embed in Hermes/OpenClaw skills
- easy to adapt to shell scripts, cron jobs, or larger pipelines

### Trade-offs
- depends on current Codex CLI behavior
- output discovery is partly heuristic
- exact backend model identity is not guaranteed by this wrapper

## Module layout

- `src/hermes_codex_image_skill/codex_runner.py`
  - core workflow and result object
- `src/hermes_codex_image_skill/cli.py`
  - argparse entrypoint
- `skill/scripts/generate_with_codex.py`
  - repo-friendly Hermes/OpenClaw script wrapper
- `tests/test_cli_smoke.py`
  - parser, fallback, timeout, and preflight tests

## Stability strategy

The repo avoids coupling to internal undocumented JSON protocols from Codex. Instead it uses:

- human-visible login status checks
- stdout path extraction when present
- generated-image directory fallback when stdout is incomplete

That approach is less elegant than a formal API, but more resilient for current local workflows.
