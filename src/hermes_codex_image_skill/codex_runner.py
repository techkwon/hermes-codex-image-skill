from __future__ import annotations

import json
import os
import shutil
import subprocess
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from urllib.parse import unquote, urlparse

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
DEFAULT_TIMEOUT = 600
STDOUT_EXCERPT_LIMIT = 2000


class CodexImageError(RuntimeError):
    """Raised when the Codex image workflow fails."""


@dataclass(slots=True)
class GenerationResult:
    ok: bool
    source_path: str | None
    final_path: str | None
    mode: str
    session_id: str | None = None
    login_status: str | None = None
    model_hint: str | None = None
    started_at: str | None = None
    finished_at: str | None = None
    duration_seconds: float | None = None
    stdout_excerpt: str | None = None
    error: str | None = None

    def to_dict(self) -> dict[str, str | float | bool | None]:
        return {
            "ok": self.ok,
            "source_path": self.source_path,
            "final_path": self.final_path,
            "mode": self.mode,
            "session_id": self.session_id,
            "login_status": self.login_status,
            "model_hint": self.model_hint,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "duration_seconds": self.duration_seconds,
            "stdout_excerpt": self.stdout_excerpt,
            "error": self.error,
        }


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()


def clip_text(text: str, limit: int = STDOUT_EXCERPT_LIMIT) -> str | None:
    stripped = text.strip()
    if not stripped:
        return None
    return stripped[-limit:]


def find_codex_binary() -> str:
    codex = shutil.which("codex")
    if not codex:
        raise CodexImageError("codex command not found in PATH")
    return codex


def check_login_status(codex_bin: str) -> str:
    proc = subprocess.run(
        [codex_bin, "login", "status"],
        capture_output=True,
        text=True,
        check=False,
    )
    combined = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
    if proc.returncode != 0:
        raise CodexImageError(f"failed to check codex login status: {combined}")
    if "Logged in" not in combined:
        raise CodexImageError(f"codex is not logged in: {combined}")
    return combined


def extract_session_id(output: str) -> str | None:
    for line in output.splitlines():
        stripped = line.strip()
        if stripped.startswith("session id:"):
            return stripped.split(":", 1)[1].strip()
    return None


def detect_model_hint(output: str) -> str | None:
    for line in output.splitlines():
        stripped = line.strip()
        if stripped.startswith("model:"):
            return stripped.split(":", 1)[1].strip()
    return None


def normalize_candidate_path(line: str) -> str | None:
    stripped = line.strip().strip("`").strip('"').strip("'")
    if not stripped:
        return None
    if stripped.startswith("file://"):
        parsed = urlparse(stripped)
        stripped = unquote(parsed.path)
    if stripped.startswith("/") and Path(stripped).suffix.lower() in IMAGE_SUFFIXES:
        return stripped
    return None


def extract_final_path(output: str) -> str | None:
    candidates: list[str] = []
    for line in output.splitlines():
        maybe = normalize_candidate_path(line)
        if maybe:
            candidates.append(maybe)
    return candidates[-1] if candidates else None


def generated_images_dir() -> Path:
    base = os.environ.get("CODEX_HOME")
    if base:
        return Path(base).expanduser() / "generated_images"
    return Path.home() / ".codex" / "generated_images"


def iter_images(root: Path) -> Iterable[Path]:
    if not root.exists():
        return []
    return (p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES)


def discover_new_image(root: Path, started_at: float, session_id: str | None = None) -> Path | None:
    candidates: list[Path] = []
    preferred_root = root / session_id if session_id else root
    for search_root in [preferred_root, root]:
        if not search_root.exists():
            continue
        for path in iter_images(search_root):
            try:
                modified = path.stat().st_mtime
            except FileNotFoundError:
                continue
            if modified >= started_at:
                candidates.append(path)
        if candidates:
            break
    if not candidates:
        return None
    candidates.sort(key=lambda p: p.stat().st_mtime_ns)
    return candidates[-1]


def build_prompt(user_prompt: str) -> str:
    prompt = user_prompt.strip()
    if not prompt:
        raise CodexImageError("prompt must not be empty")
    return f"{prompt}\n\nReturn only the final absolute image path when you finish."


def run_codex_exec(
    prompt: str,
    *,
    codex_bin: str,
    timeout: int = DEFAULT_TIMEOUT,
    extra_args: list[str] | None = None,
) -> tuple[subprocess.CompletedProcess[str], float]:
    started_at = datetime.now(UTC).timestamp()
    cmd = [codex_bin, "exec", "--skip-git-repo-check"]
    if extra_args:
        cmd.extend(extra_args)
    cmd.append(build_prompt(prompt))
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout,
    )
    return proc, started_at


def ensure_output_path(output_path: str | None, source_path: Path) -> Path:
    if output_path:
        final_path = Path(output_path).expanduser()
        if final_path.suffix.lower() not in IMAGE_SUFFIXES:
            final_path = final_path.with_suffix(source_path.suffix)
    else:
        output_dir = Path.cwd() / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        final_path = output_dir / source_path.name
    final_path.parent.mkdir(parents=True, exist_ok=True)
    return final_path


def copy_output(source_path: Path, output_path: str | None) -> Path:
    final_path = ensure_output_path(output_path, source_path)
    if source_path.resolve() != final_path.resolve():
        shutil.copy2(source_path, final_path)
    return final_path


def write_metadata(metadata_path: str | None, result: GenerationResult) -> str | None:
    if not metadata_path:
        return None
    path = Path(metadata_path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(result.to_dict(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return str(path)


def generate_image(
    prompt: str,
    *,
    output_path: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
    extra_args: list[str] | None = None,
    metadata_path: str | None = None,
) -> GenerationResult:
    started_at_iso = utc_now_iso()
    wall_started = perf_counter()
    try:
        codex_bin = find_codex_binary()
        login_status = check_login_status(codex_bin)
    except CodexImageError as exc:
        result = GenerationResult(
            ok=False,
            source_path=None,
            final_path=None,
            mode="preflight_failed",
            started_at=started_at_iso,
            finished_at=utc_now_iso(),
            duration_seconds=round(perf_counter() - wall_started, 3),
            error=str(exc),
        )
        write_metadata(metadata_path, result)
        return result

    try:
        proc, discovery_started_at = run_codex_exec(
            prompt,
            codex_bin=codex_bin,
            timeout=timeout,
            extra_args=extra_args,
        )
    except subprocess.TimeoutExpired as exc:
        combined = ((exc.stdout or "") + "\n" + (exc.stderr or "")).strip()
        result = GenerationResult(
            ok=False,
            source_path=None,
            final_path=None,
            mode="timeout",
            login_status=login_status,
            started_at=started_at_iso,
            finished_at=utc_now_iso(),
            duration_seconds=round(perf_counter() - wall_started, 3),
            stdout_excerpt=clip_text(combined),
            error=f"codex exec timed out after {timeout} seconds",
        )
        write_metadata(metadata_path, result)
        return result

    combined = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
    session_id = extract_session_id(combined)
    model_hint = detect_model_hint(combined)
    source = extract_final_path(combined)

    if proc.returncode != 0:
        result = GenerationResult(
            ok=False,
            source_path=source,
            final_path=None,
            mode="failed",
            session_id=session_id,
            login_status=login_status,
            model_hint=model_hint,
            started_at=started_at_iso,
            finished_at=utc_now_iso(),
            duration_seconds=round(perf_counter() - wall_started, 3),
            stdout_excerpt=clip_text(combined),
            error=f"codex exec failed with exit code {proc.returncode}",
        )
        write_metadata(metadata_path, result)
        return result

    if source:
        source_path = Path(source).expanduser()
        if not source_path.is_file():
            result = GenerationResult(
                ok=False,
                source_path=str(source_path),
                final_path=None,
                mode="not_found",
                session_id=session_id,
                login_status=login_status,
                model_hint=model_hint,
                started_at=started_at_iso,
                finished_at=utc_now_iso(),
                duration_seconds=round(perf_counter() - wall_started, 3),
                stdout_excerpt=clip_text(combined),
                error="image path reported by codex does not exist on disk",
            )
            write_metadata(metadata_path, result)
            return result
    else:
        discovered = discover_new_image(
            generated_images_dir(),
            discovery_started_at,
            session_id=session_id,
        )
        if not discovered:
            result = GenerationResult(
                ok=False,
                source_path=None,
                final_path=None,
                mode="not_found",
                session_id=session_id,
                login_status=login_status,
                model_hint=model_hint,
                started_at=started_at_iso,
                finished_at=utc_now_iso(),
                duration_seconds=round(perf_counter() - wall_started, 3),
                stdout_excerpt=clip_text(combined),
                error="no generated image path found in codex output or generated_images directory",
            )
            write_metadata(metadata_path, result)
            return result
        source_path = discovered

    final_path = copy_output(source_path, output_path)
    result = GenerationResult(
        ok=True,
        source_path=str(source_path),
        final_path=str(final_path),
        mode="copied" if source_path.resolve() != final_path.resolve() else "original",
        session_id=session_id,
        login_status=login_status,
        model_hint=model_hint,
        started_at=started_at_iso,
        finished_at=utc_now_iso(),
        duration_seconds=round(perf_counter() - wall_started, 3),
        stdout_excerpt=clip_text(combined),
        error=None,
    )
    write_metadata(metadata_path, result)
    return result


def generate_image_json(
    prompt: str,
    *,
    output_path: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
    extra_args: list[str] | None = None,
    metadata_path: str | None = None,
) -> str:
    return json.dumps(
        generate_image(
            prompt,
            output_path=output_path,
            timeout=timeout,
            extra_args=extra_args,
            metadata_path=metadata_path,
        ).to_dict(),
        ensure_ascii=False,
        indent=2,
    )
