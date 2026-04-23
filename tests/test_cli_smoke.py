from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from hermes_codex_image_skill import cli, codex_runner


class DummyProcess:
    def __init__(self, returncode: int = 0, stdout: str = "", stderr: str = "") -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def test_extract_final_path_returns_last_image_path() -> None:
    output = """
noise
/tmp/first.png
more noise
/tmp/second.webp
"""
    assert codex_runner.extract_final_path(output) == "/tmp/second.webp"


def test_extract_final_path_accepts_file_url_and_quotes() -> None:
    output = '"file:///tmp/final.png"'
    assert codex_runner.extract_final_path(output) == "/tmp/final.png"


def test_extract_final_path_decodes_escaped_file_url() -> None:
    output = "file:///tmp/my%20image.png"
    assert codex_runner.extract_final_path(output) == "/tmp/my image.png"


def test_build_prompt_rejects_empty_prompt() -> None:
    with pytest.raises(codex_runner.CodexImageError):
        codex_runner.build_prompt("   ")


def test_discover_new_image_prefers_latest_file(tmp_path: Path) -> None:
    root = tmp_path / "generated_images" / "abc"
    root.mkdir(parents=True)
    a = root / "a.png"
    b = root / "b.png"
    a.write_bytes(b"a")
    b.write_bytes(b"b")
    a.touch()
    b.touch()
    found = codex_runner.discover_new_image(
        tmp_path / "generated_images",
        0,
        session_id="abc",
    )
    assert found == b


def test_find_codex_binary_raises_when_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(codex_runner.shutil, "which", lambda _: None)
    with pytest.raises(codex_runner.CodexImageError):
        codex_runner.find_codex_binary()


def test_check_login_status_rejects_logged_out(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *args, **kwargs: DummyProcess(returncode=0, stdout="Not logged in"),
    )
    with pytest.raises(codex_runner.CodexImageError):
        codex_runner.check_login_status("codex")


def test_generate_image_uses_stdout_path_and_metadata(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    source = tmp_path / "source.png"
    source.write_bytes(b"png")
    dest = tmp_path / "copied.png"
    metadata = tmp_path / "result.json"

    monkeypatch.setattr(codex_runner, "find_codex_binary", lambda: "codex")
    monkeypatch.setattr(
        codex_runner,
        "check_login_status",
        lambda _bin: "Logged in using ChatGPT",
    )
    monkeypatch.setattr(
        codex_runner,
        "run_codex_exec",
        lambda *args, **kwargs: (
            DummyProcess(
                returncode=0,
                stdout=f"session id: abc\nmodel: gpt-5.4\n{source}\n",
                stderr="",
            ),
            0.0,
        ),
    )

    result = codex_runner.generate_image(
        "hello",
        output_path=str(dest),
        metadata_path=str(metadata),
    )
    assert result.ok is True
    assert result.source_path == str(source)
    assert result.final_path == str(dest)
    assert dest.exists()
    assert result.session_id == "abc"
    assert result.model_hint == "gpt-5.4"
    payload = json.loads(metadata.read_text(encoding="utf-8"))
    assert payload["final_path"] == str(dest)


def test_generate_image_handles_missing_stdout_path(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    missing = tmp_path / "does-not-exist.png"
    metadata = tmp_path / "missing.json"

    monkeypatch.setattr(codex_runner, "find_codex_binary", lambda: "codex")
    monkeypatch.setattr(
        codex_runner,
        "check_login_status",
        lambda _bin: "Logged in using ChatGPT",
    )
    monkeypatch.setattr(
        codex_runner,
        "run_codex_exec",
        lambda *args, **kwargs: (
            DummyProcess(returncode=0, stdout=f"{missing}\n", stderr=""),
            0.0,
        ),
    )

    result = codex_runner.generate_image("hello", metadata_path=str(metadata))
    assert result.ok is False
    assert result.mode == "not_found"
    assert result.source_path == str(missing)
    payload = json.loads(metadata.read_text(encoding="utf-8"))
    assert payload["error"] == "image path reported by codex does not exist on disk"


def test_generate_image_falls_back_to_generated_images(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    generated_root = tmp_path / "generated_images"
    generated_root.mkdir()
    image = generated_root / "abc" / "ig_test.png"
    image.parent.mkdir()
    image.write_bytes(b"png")
    dest = tmp_path / "out.png"

    monkeypatch.setattr(codex_runner, "find_codex_binary", lambda: "codex")
    monkeypatch.setattr(
        codex_runner,
        "check_login_status",
        lambda _bin: "Logged in using ChatGPT",
    )
    monkeypatch.setattr(
        codex_runner,
        "run_codex_exec",
        lambda *args, **kwargs: (
            DummyProcess(returncode=0, stdout="session id: abc\n", stderr=""),
            0.0,
        ),
    )
    monkeypatch.setattr(codex_runner, "generated_images_dir", lambda: generated_root)

    result = codex_runner.generate_image("hello", output_path=str(dest))
    assert result.ok is True
    assert result.source_path == str(image)
    assert result.final_path == str(dest)


def test_generate_image_returns_timeout_result(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(codex_runner, "find_codex_binary", lambda: "codex")
    monkeypatch.setattr(
        codex_runner,
        "check_login_status",
        lambda _bin: "Logged in using ChatGPT",
    )

    def _raise_timeout(*args, **kwargs):
        exc = subprocess.TimeoutExpired(cmd="codex", timeout=3, output="partial")
        exc.stderr = "late"
        raise exc

    monkeypatch.setattr(codex_runner, "run_codex_exec", _raise_timeout)
    result = codex_runner.generate_image("hello", timeout=3)
    assert result.ok is False
    assert result.mode == "timeout"
    assert "timed out" in (result.error or "")


def _raise_missing_codex():
    raise codex_runner.CodexImageError("missing codex")


def test_generate_image_returns_preflight_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(codex_runner, "find_codex_binary", _raise_missing_codex)
    result = codex_runner.generate_image("hello")
    assert result.ok is False
    assert result.mode == "preflight_failed"
    assert result.error == "missing codex"


def test_cli_main_returns_nonzero_on_failed_result(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        cli,
        "generate_image",
        lambda *args, **kwargs: codex_runner.GenerationResult(
            ok=False,
            source_path=None,
            final_path=None,
            mode="failed",
            error="boom",
        ),
    )
    exit_code = cli.main(["prompt text"])
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert exit_code == 1
    assert payload["ok"] is False
    assert payload["error"] == "boom"
