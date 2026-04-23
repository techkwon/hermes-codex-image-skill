# Known Limitations

## 1. Depends on local Codex CLI behavior
This project works because local Codex CLI can generate images and place them under a generated images directory. If Codex changes its CLI output format, session format, or storage layout, this wrapper may need updates.

## 2. Requires an already valid login state
This tool does not perform login for the user. It checks `codex login status` and fails if the local Codex session is unavailable.

## 3. Does not prove exact backend image model identity
This repository demonstrates a practical image-generation workflow through Codex CLI. It does **not** by itself prove whether the underlying image model is a specific public model version.

## 4. Output parsing is heuristic
The wrapper tries two strategies:
- parse a final image path directly from Codex stdout
- detect newly created files under the generated images directory

This is robust enough for current testing, but still heuristic.

## 5. Quality depends on Codex and prompt quality
The wrapper stabilizes the workflow, not the artistic result. Final image quality still depends on:
- current Codex capability
- prompt clarity
- text rendering difficulty
- composition complexity

## 6. Local path assumptions
Default fallback output uses the current working directory `output/` folder. Users running from automation environments should usually pass an explicit `--output` path.
