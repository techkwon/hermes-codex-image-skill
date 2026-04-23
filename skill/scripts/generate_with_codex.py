#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# Ruff: import must stay below the path bootstrap above.
from hermes_codex_image_skill.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
