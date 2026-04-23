from __future__ import annotations

import argparse
import json
import sys

from . import __version__
from .codex_runner import generate_image


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hermes-codex-image",
        description="Generate an image through local Codex CLI and emit structured JSON.",
    )
    parser.add_argument("prompt", help="Image prompt to send to codex exec")
    parser.add_argument(
        "-o",
        "--output",
        dest="output_path",
        help="Final output image path",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="Timeout in seconds (default: 600)",
    )
    parser.add_argument(
        "--metadata-json",
        dest="metadata_path",
        help="Optional JSON sidecar path for saving the same structured result to disk.",
    )
    parser.add_argument(
        "--extra-arg",
        dest="extra_args",
        action="append",
        default=[],
        help="Additional argument passed to `codex exec` before the prompt. Repeatable.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = generate_image(
            args.prompt,
            output_path=args.output_path,
            timeout=args.timeout,
            extra_args=args.extra_args,
            metadata_path=args.metadata_path,
        )
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
        return 0 if result.ok else 1
    except Exception as exc:  # pragma: no cover - final safety net
        print(
            json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2),
            file=sys.stdout,
        )
        return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
