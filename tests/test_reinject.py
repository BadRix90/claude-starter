"""Tests für home/hooks/reinject.py."""

import importlib.util
import pathlib
import subprocess

HOOK = pathlib.Path(__file__).resolve().parents[1] / "home" / "hooks" / "reinject.py"
spec = importlib.util.spec_from_file_location("reinject", HOOK)
reinject = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reinject)

SLICES = """# Slices
| ID | Typ | Thema | Zustand | Akzeptanzpunkte | Bericht |
|---|---|---|---|---|---|
| F1 | Feature | Login | IN_PROGRESS | 1. Token | |
| F2 | Feature | Export | OPEN | 1. CSV | |
| B3 | Bug | Rundung | BLOCKED | 1. Test | |
| C4 | Chore | Deps | VERIFIED | | |
"""


def run_git(cwd: pathlib.Path, *args: str) -> None:
    """Run a git command in a throwaway repository and fail loudly."""
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


def test_active_slices_keeps_only_work_in_flight() -> None:
    """Rows in progress or blocked are returned; open and verified rows are not."""
    rows = reinject.active_slices(SLICES)
    assert [row.split("|")[1].strip() for row in rows] == ["F1", "B3"]


def test_active_slices_ignores_state_words_in_prose() -> None:
    """A state name inside a longer cell or sentence does not count as a state."""
    assert reinject.active_slices("Der Slice ist BLOCKED, siehe unten.") == []


def test_build_is_empty_without_git_and_tracking(tmp_path) -> None:
    """Outside a repository and without a tracking file there is nothing to say."""
    assert reinject.build(str(tmp_path)) == ""


def test_build_reads_tracking_file_without_git(tmp_path) -> None:
    """The tracking file alone is enough for a summary."""
    (tmp_path / "SLICES.md").write_text(SLICES, encoding="utf-8")
    summary = reinject.build(str(tmp_path))
    assert "Laufende Slices" in summary and "F1" in summary and "F2" not in summary


def test_build_reads_real_repository(tmp_path) -> None:
    """In a real repository the summary carries the last commit and open changes."""
    run_git(tmp_path, "init", "-q")
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    run_git(tmp_path, "add", "a.txt")
    identity = ["-c", "user.name=t", "-c", "user.email=t@example.invalid", "-c", "commit.gpgsign=false"]
    run_git(tmp_path, *identity, "commit", "-q", "-m", "feat: first commit")
    (tmp_path / "b.txt").write_text("b", encoding="utf-8")
    summary = reinject.build(str(tmp_path))
    assert "feat: first commit" in summary
    assert "b.txt" in summary


def test_section_caps_long_output() -> None:
    """A long list is cut so the hook stays far below the context cap."""
    block = reinject.section("Titel:", [str(n) for n in range(100)])
    assert len(block) == reinject.MAX_LINES + 1
