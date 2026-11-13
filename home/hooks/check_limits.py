"""PostToolUse-Hook für Edit und Write: meldet Dateien über 400 und Funktionen über 20 Zeilen.

Setzt Hardrule §11 durch. Das Werkzeug ist schon gelaufen, der Hook kann nichts
verhindern: Exit 2 zeigt Claude stderr, und Claude teilt die Datei oder Funktion sofort.
Gemeldet wird nur, was durch die Änderung neu über die Grenze kam oder weiter gewachsen
ist. Der Vergleich ist der Stand in HEAD. Altlasten lösen so keinen ungefragten Umbau aus.

Dateilänge: alle Endungen in CODE_SUFFIXES. Funktionslänge: nur Python, gezählt von der
def-Zeile bis zum Ende, ohne Docstring. Für TypeScript die ESLint-Regeln max-lines und
max-lines-per-function nutzen. Testdateien, Migrationen und Build-Ausgaben sind ausgenommen.

Eintrag in settings.json:
    "PostToolUse": [{"matcher": "Edit|Write", "hooks": [{"type": "command",
        "command": "python \"$HOME/.claude/hooks/check_limits.py\""}]}]
Test: tests/test_check_limits.py
"""

import ast
import json
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from guard_paths import is_test_file  # noqa: E402  eine Quelle für "was ist ein Test"

MAX_FILE_LINES = 400
MAX_FUNCTION_LINES = 20
CODE_SUFFIXES = {".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".scss", ".html", ".astro"}
EXEMPT = re.compile(r"/(migrations|node_modules|dist|build|\.venv|venv)/|\.min\.[a-z]+$")
FILE_KEY = "<Datei>"


def is_checked(path: str) -> bool:
    """Return True for productive code files the limits apply to."""
    normal = path.replace("\\", "/")
    suffix = pathlib.PurePosixPath(normal).suffix.lower()
    return suffix in CODE_SUFFIXES and not EXEMPT.search(normal) and not is_test_file(path)


def span(node: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
    """Return the line count of a function from its def line, without the docstring."""
    total = (node.end_lineno or node.lineno) - node.lineno + 1
    first = node.body[0]
    if isinstance(first, ast.Expr) and isinstance(getattr(first, "value", None), ast.Constant):
        if isinstance(first.value.value, str):
            total -= (first.end_lineno or first.lineno) - first.lineno + 1
    return total


def function_lengths(source: str) -> dict[str, int]:
    """Return name -> longest span for every function; empty if the source does not parse."""
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError):
        return {}
    lengths: dict[str, int] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            lengths[node.name] = max(lengths.get(node.name, 0), span(node))
    return lengths


def violations(source: str, suffix: str) -> dict[str, int]:
    """Return everything over a limit: FILE_KEY -> lines, function name -> lines."""
    found: dict[str, int] = {}
    lines = len(source.splitlines())
    if lines > MAX_FILE_LINES:
        found[FILE_KEY] = lines
    if suffix == ".py":
        long = {name: n for name, n in function_lengths(source).items() if n > MAX_FUNCTION_LINES}
        found.update(long)
    return found


def head_text(path: pathlib.Path) -> str:
    """Return the committed version of the file, or "" if untracked or outside git."""
    try:
        out = subprocess.run(
            ["git", "show", f"HEAD:./{path.name}"],
            cwd=path.parent, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return out.stdout if out.returncode == 0 else ""


def new_violations(now: dict[str, int], before: dict[str, int]) -> dict[str, int]:
    """Return the violations that are new or have grown compared to the old state."""
    return {key: n for key, n in now.items() if n > before.get(key, 0)}


def report(path: str, found: dict[str, int]) -> list[str]:
    """Return one line per violation, worded as an instruction to split."""
    lines = []
    for key, count in sorted(found.items()):
        if key == FILE_KEY:
            lines.append(f"{path} hat {count} Zeilen (Grenze {MAX_FILE_LINES}). Thema teilen.")
        else:
            lines.append(f"{path}: Funktion {key} hat {count} Zeilen (Grenze {MAX_FUNCTION_LINES}). Aufteilen.")
    return lines


def check(path: pathlib.Path) -> list[str]:
    """Return the report lines for one file on disk; empty if nothing new is over a limit."""
    if not path.is_file():
        return []
    suffix = path.suffix.lower()
    now = violations(path.read_text(encoding="utf-8", errors="replace"), suffix)
    if not now:
        return []
    return report(str(path), new_violations(now, violations(head_text(path), suffix)))


def main() -> int:
    """Read the hook payload from stdin and exit 2 when the edit crossed a limit."""
    sys.stderr.reconfigure(encoding="utf-8")  # Windows-Konsole ist sonst cp1252
    payload = json.load(sys.stdin)
    path = str(payload.get("tool_input", {}).get("file_path", ""))
    lines = check(pathlib.Path(path)) if path and is_checked(path) else []
    if not lines:
        return 0
    print("check_limits (Hardrule §11):", *lines, sep="\n", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
