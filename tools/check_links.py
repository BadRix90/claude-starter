"""Prüft relative Markdown-Links im Repo. Lauf: python tools/check_links.py

Findet [text](pfad) und [text](pfad#anker) in allen .md-Dateien und meldet Ziele,
die nicht existieren. HTTP-Links und reine Anker werden übersprungen.
Exit 1 bei mindestens einem toten Link.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules"}


def md_files() -> list[pathlib.Path]:
    """Return all markdown files below ROOT, skipping tool and cache folders."""
    return [p for p in ROOT.rglob("*.md") if not SKIP_DIRS & set(p.relative_to(ROOT).parts)]


def dead_links(path: pathlib.Path) -> list[str]:
    """Return the relative link targets in one file that do not resolve."""
    dead: list[str] = []
    for target in LINK.findall(path.read_text(encoding="utf-8")):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        clean = target.split("#", 1)[0]
        if not (path.parent / clean).exists():
            dead.append(target)
    return dead


def main() -> int:
    """Print every dead link as file: target and return 1 if any exist."""
    failures = 0
    for path in md_files():
        for target in dead_links(path):
            print(f"{path.relative_to(ROOT)}: {target}")
            failures += 1
    print(f"{failures} tote Links" if failures else "Alle relativen Links erreichbar.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
