"""PreToolUse-Hook für Write und Edit in Subagenten: begrenzt, welche Pfade ein Agent anfasst.

Aufruf im Frontmatter eines Agenten (siehe extras/agents/implementer.md):
    python "$HOME/.claude/hooks/guard_paths.py" [--only-tests | --no-tests]

Ohne Flag: nur Infrastruktur geschützt (CI, Container, Settings, .env).
--only-tests  erlaubt ausschließlich Testdateien (Test-Writer).
--no-tests    verbietet Testdateien (Implementer, Doc-Writer).
Test: tests/test_guard_paths.py
"""

import json
import re
import sys

TEST_PATTERN = re.compile(
    r"([\\/]tests?[\\/]|[\\/]test_[^\\/]+\.py$|_test\.py$|[\\/]conftest\.py$"
    r"|\.(spec|test)\.[cm]?[jt]sx?$|[\\/]e2e[\\/]|[\\/]__tests__[\\/])",
    flags=re.IGNORECASE,
)

INFRA_PATTERN = re.compile(
    r"([\/]\.github[\/]|[\/]docker[^\/]*|[\/]settings[^\/]*\.json$|[\/]\.env|\.pre-commit-config\.yaml$)",
    flags=re.IGNORECASE,
)


def is_infra_file(path: str) -> bool:
    """Return True if the path is CI, container or secret configuration."""
    return bool(INFRA_PATTERN.search(path.replace("\\", "/")))


def is_test_file(path: str) -> bool:
    """Return True if the path looks like a test file."""
    return bool(TEST_PATTERN.search(path.replace("\\", "/")))


def main() -> int:
    """Exit 2 when the edited path violates the agent's mode."""
    sys.stderr.reconfigure(encoding="utf-8")  # Windows-Konsole ist sonst cp1252
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    payload = json.load(sys.stdin)
    path = str(payload.get("tool_input", {}).get("file_path", ""))
    if is_infra_file(path):
        print(f"Blockiert: CI/Infrastruktur fasst kein Subagent an ({path}).", file=sys.stderr)
        return 2
    if mode == "--only-tests" and not is_test_file(path):
        print(f"Blockiert: dieser Agent darf nur Testdateien schreiben ({path}).", file=sys.stderr)
        return 2
    if mode == "--no-tests" and is_test_file(path):
        print(f"Blockiert: dieser Agent darf keine Testdateien ändern ({path}).", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
