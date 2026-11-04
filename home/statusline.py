"""Statusline mit Kontext-Radar. Zeigt Modell, Balken und Prozent, warnt ab 50 Prozent.

Eintrag in settings.json:
    "statusLine": {"type": "command", "command": "python \"$HOME/.claude/statusline.py\""}

Claude Code reicht nach jeder API-Antwort JSON auf stdin (Doku: code.claude.com/docs/en/statusline).
Zusätzlich schreibt das Skript den Prozentwert in eine Datei je Session, damit der Hook
hooks/context_radar.py ihn lesen und Claude selbst darauf hinweisen kann.
Idee: Session Radar von Andreas Paehge, siehe docs/AUS-DER-COMMUNITY.md.
"""

import json
import pathlib
import sys
import tempfile

WARN_AT = 50


def state_file(session_id: str) -> pathlib.Path:
    """Return the per-session file that carries the current context percentage."""
    return pathlib.Path(tempfile.gettempdir()) / f"claude-context-{session_id}.json"


def render(data: dict) -> str:
    """Build the status line text from the statusline JSON."""
    pct = int((data.get("context_window") or {}).get("used_percentage") or 0)
    model = (data.get("model") or {}).get("display_name", "?")
    filled = min(pct // 10, 10)
    bar = "▓" * filled + "░" * (10 - filled)
    warn = "  ⚠ Übergabe schreiben, dann /clear" if pct >= WARN_AT else ""
    return f"[{model}] {bar} {pct}%{warn}"


def main() -> int:
    """Read statusline JSON, print the line, persist the percentage for the hook."""
    sys.stdout.reconfigure(encoding="utf-8")  # Windows-Konsole ist sonst cp1252, Balken bricht
    data = json.load(sys.stdin)
    print(render(data))
    session_id = str(data.get("session_id", ""))
    if session_id:
        pct = int((data.get("context_window") or {}).get("used_percentage") or 0)
        state_file(session_id).write_text(json.dumps({"pct": pct}), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
