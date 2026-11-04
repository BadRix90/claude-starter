"""UserPromptSubmit-Hook: sagt Claude, wie voll der Kontext ist, sobald es eng wird.

Liest den Prozentwert, den statusline.py je Session ablegt, und gibt ab WARN_AT einen
Hinweis als additionalContext zurück. Blockt nie (Exit 0). Ohne Statusline-Eintrag
findet der Hook keine Datei und bleibt still.

Eintrag in settings.json:
    "UserPromptSubmit": [{"hooks": [{"type": "command",
        "command": "python \"$HOME/.claude/hooks/context_radar.py\""}]}]
Test: tests/test_context_radar.py
"""

import json
import pathlib
import sys
import tempfile

WARN_AT = 50
URGENT_AT = 75


def read_pct(session_id: str) -> int | None:
    """Return the stored context percentage for the session, or None if unknown."""
    path = pathlib.Path(tempfile.gettempdir()) / f"claude-context-{session_id}.json"
    if not path.exists():
        return None
    try:
        return int(json.loads(path.read_text(encoding="utf-8")).get("pct", 0))
    except (ValueError, OSError):
        return None


def message_for(pct: int | None) -> str | None:
    """Return the hint for Claude, or None below the warning threshold."""
    if pct is None or pct < WARN_AT:
        return None
    if pct >= URGENT_AT:
        return (
            f"Kontextfenster zu {pct} % belegt. Vor der nächsten Aufgabe eine Übergabe "
            "schreiben (Stand, offene Punkte, geänderte Dateien) und /clear vorschlagen."
        )
    return f"Kontextfenster zu {pct} % belegt. Bei der nächsten Gelegenheit Übergabe und /clear anbieten."


def main() -> int:
    """Emit additionalContext when the stored percentage crosses a threshold."""
    payload = json.load(sys.stdin)
    hint = message_for(read_pct(str(payload.get("session_id", ""))))
    if hint:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": hint}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
