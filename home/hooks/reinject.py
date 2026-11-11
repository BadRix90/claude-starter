"""SessionStart-Hook (Matcher "compact"): spielt nach einer Kompaktierung den Arbeitsstand zurück.

Nach /compact liest Claude Code die CLAUDE.md im Projekt-Root selbst neu. Was verloren
geht, ist der Stand der Arbeit. Dieser Hook liest ihn frisch aus dem Repo: Branch,
letzte Commits, offene Änderungen und laufende Slices aus der Tracking-Datei.
Claude Code nimmt den Klartext auf stdout eines SessionStart-Hooks in den Kontext
(höchstens 10.000 Zeichen). Der Hook blockt nie und ändert nichts.

Eintrag in settings.json:
    "SessionStart": [{"matcher": "compact", "hooks": [{"type": "command",
        "command": "python \"$HOME/.claude/hooks/reinject.py\""}]}]
Test: tests/test_reinject.py
"""

import json
import pathlib
import subprocess
import sys

TRACKING_FILE = "SLICES.md"
ACTIVE = ("IN_PROGRESS", "CODE_READY", "PARTIAL", "BLOCKED")
MAX_LINES = 15


def git(cwd: str, *args: str) -> list[str]:
    """Return the output lines of a read-only git command, or [] on any failure."""
    try:
        out = subprocess.run(
            ["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8", timeout=5
        )
    except (OSError, subprocess.SubprocessError):
        return []
    return out.stdout.splitlines() if out.returncode == 0 else []


def active_slices(text: str) -> list[str]:
    """Return the table rows of the tracking file whose state is still in flight."""
    rows = []
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.split("|")]
        if any(state in cells for state in ACTIVE):
            rows.append(line.strip())
    return rows


def section(title: str, lines: list[str]) -> list[str]:
    """Return a titled, indented block, or nothing when there are no lines."""
    if not lines:
        return []
    return [title, *[f"  {line}" for line in lines[:MAX_LINES]]]


def build(cwd: str) -> str:
    """Assemble the state summary for a working directory; empty if nothing is known."""
    parts = section("Branch:", git(cwd, "branch", "--show-current"))
    parts += section("Letzte Commits:", git(cwd, "log", "--oneline", "-5"))
    parts += section("Uncommittete Änderungen:", git(cwd, "status", "--short"))
    tracking = pathlib.Path(cwd) / TRACKING_FILE
    if tracking.is_file():
        rows = active_slices(tracking.read_text(encoding="utf-8"))
        parts += section(f"Laufende Slices ({TRACKING_FILE}):", rows)
    if not parts:
        return ""
    return "\n".join(["Arbeitsstand nach Kompaktierung, frisch aus dem Repo gelesen:", *parts])


def main() -> int:
    """Print the state summary for the session's working directory."""
    sys.stdout.reconfigure(encoding="utf-8")  # Windows-Konsole ist sonst cp1252
    payload = json.load(sys.stdin)
    summary = build(str(payload.get("cwd") or "."))
    if summary:
        print(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
