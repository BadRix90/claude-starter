"""Tests für home/hooks/guard_shell.py. Lauf: python -m pytest tests/ -q"""

import importlib.util
import pathlib

import pytest

HOOK = pathlib.Path(__file__).resolve().parents[1] / "home" / "hooks" / "guard_shell.py"
spec = importlib.util.spec_from_file_location("guard_shell", HOOK)
guard_shell = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard_shell)

BLOCKED = [
    "git commit --no-" + "verify -m x",
    "git add .",
    "git add -A",
    "git add --all && git commit -m x",
    "git commit -am 'x'",
    "git commit -a -m 'x'",
    "git push --force origin main",
    "git push -f",
    "git push --force-with-lease",
    "git worktree add ../x",
    "git reset --hard HEAD~1",
    "git clean -fd",
    "psql -c 'DELETE FROM users'",
    "echo SECRET=1 >> .env",
    "echo SECRET=1 > backend/.env",
    "sed -i 's/a/b/' .env",
    "cp .env.example .env",
]

ALLOWED = [
    "git add src/app.py tests/test_app.py",
    "git commit -m 'feat(x): y' -- src/app.py",
    "git push origin main",
    "git status",
    "git diff --stat",
    "cat .env.example",
    "psql -c 'SELECT 1'",
    "python -m pytest -q",
    "echo hello > out.txt",
    "git log --oneline -5",
]


@pytest.mark.parametrize("command", BLOCKED)
def test_blocks_forbidden_commands(command: str) -> None:
    """Every forbidden command yields a reason."""
    assert guard_shell.check(command) is not None, command


@pytest.mark.parametrize("command", ALLOWED)
def test_allows_normal_commands(command: str) -> None:
    """Normal commands pass without a reason."""
    assert guard_shell.check(command) is None, command
