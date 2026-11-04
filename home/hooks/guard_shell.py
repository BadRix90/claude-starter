"""PreToolUse-Hook für Bash und PowerShell: blockt verbotene Befehle mit Exit 2.

Registriert in settings.json unter hooks.PreToolUse mit matcher "Bash|PowerShell".
Claude Code reicht den Tool-Aufruf als JSON auf stdin. Exit 2 blockt den Befehl,
stderr wird Claude als Grund gezeigt. Exit 0 lässt ihn durch.

Regeln ergänzen: ein Tupel (Regex, Begründung) in RULES. Test: tests/test_guard_shell.py
"""

import json
import re
import sys

_NO_VERIFY = "--no-" + "verify"  # getrennt, damit dieser Text selbst den Hook passiert

RULES: list[tuple[str, str]] = [
    (_NO_VERIFY + r"\b", f"{_NO_VERIFY} ist verboten: Git-Hooks werden nie umgangen."),
    (r"\bgit\s+add\s+(\.|-A|--all)(\s|$|;|&)", "git add . / -A ist verboten: Pfade explizit angeben."),
    (r"\bgit\s+commit\b[^|;&]*\s-a(m?)(\s|$)", "git commit -a ist verboten: Pfade explizit angeben."),
    (r"\bgit\s+push\b.*(\s--force\b|\s-f\b|--force-with-lease)", "Force-Push ist verboten."),
    (r"\bgit\s+worktree\s+add\b", "Worktrees sind verboten (Hardrule §4)."),
    (r"\bgit\s+(reset\s+--hard|clean\s+-[a-z]*f)", "git reset --hard / git clean -f nur mit ausdrücklicher Freigabe."),
    (r"\bpsql\b.*\b(UPDATE|DELETE|INSERT|DROP|TRUNCATE|ALTER)\b", "psql mit schreibendem SQL ist verboten."),
    (
        r"(>>?|\btee\b(\s+-a)?|\bsed\s+-i\S*.*|\b(cp|mv|Set-Content|Add-Content|Out-File)\b.*)\s*\S*\.env(\s|$|\.|\"|')",
        "Schreibzugriff auf .env ist verboten.",
    ),
]


def check(command: str) -> str | None:
    """Return the block reason for a command, or None if it is allowed."""
    for pattern, reason in RULES:
        if re.search(pattern, command, flags=re.IGNORECASE):
            return reason
    return None


def main() -> int:
    """Read the hook payload from stdin and exit 2 on a forbidden command."""
    sys.stderr.reconfigure(encoding="utf-8")  # Windows-Konsole ist sonst cp1252
    payload = json.load(sys.stdin)
    command = str(payload.get("tool_input", {}).get("command", ""))
    reason = check(command)
    if reason:
        print(f"Blockiert durch guard_shell: {reason}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
