"""Tests for update checking and git update helpers."""

from pathlib import Path
from typing import Any

from utils import update_checker


class _CompletedProcess:
    """Small stand-in for subprocess.CompletedProcess in command assertions."""

    def __init__(self, returncode: int = 0, stdout: str = "", stderr: str = "") -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def test_perform_git_pull_uses_fast_forward_only(
    monkeypatch: Any,
    tmp_path: Path,
) -> None:
    """The GUI updater must not create merge commits while updating."""
    (tmp_path / ".git").mkdir()
    commands: list[list[str]] = []

    def fake_run(command: list[str], **_: Any) -> _CompletedProcess:
        commands.append(command)
        if command[:3] == ["git", "stash", "push"]:
            return _CompletedProcess(stdout="No local changes to save")
        return _CompletedProcess()

    monkeypatch.setattr(update_checker, "get_project_root", lambda: tmp_path)
    monkeypatch.setattr(update_checker.subprocess, "run", fake_run)

    success, message = update_checker.perform_git_pull()

    assert success is True
    assert message == "update.pull_ok"
    assert ["git", "pull", "--ff-only"] in commands
    assert ["git", "pull", "--no-edit"] not in commands
