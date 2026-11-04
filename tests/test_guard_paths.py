"""Tests für home/hooks/guard_paths.py. Lauf: python -m pytest tests/ -q"""

import importlib.util
import pathlib

import pytest

HOOK = pathlib.Path(__file__).resolve().parents[1] / "home" / "hooks" / "guard_paths.py"
spec = importlib.util.spec_from_file_location("guard_paths", HOOK)
guard_paths = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard_paths)


@pytest.mark.parametrize(
    "path",
    [
        "backend/tests/test_api.py",
        "backend/app/conftest.py",
        "src/app/x.spec.ts",
        "src/app/x.test.tsx",
        "e2e/login.spec.ts",
        "pkg/__tests__/a.js",
        "backend\\tests\\test_win.py",
    ],
)
def test_detects_test_files(path: str) -> None:
    """Test files in Python and TypeScript layouts are recognised."""
    assert guard_paths.is_test_file(path)


@pytest.mark.parametrize("path", ["src/app/service.py", "src/app/x.component.ts", "README.md"])
def test_ignores_source_files(path: str) -> None:
    """Ordinary source files are not test files."""
    assert not guard_paths.is_test_file(path)


@pytest.mark.parametrize(
    "path",
    [
        "/repo/.github/workflows/ci.yml",
        "/repo/docker-compose.yml",
        "/repo/.claude/settings.json",
        "/repo/backend/.env",
        "/repo/.pre-commit-config.yaml",
    ],
)
def test_detects_infra_files(path: str) -> None:
    """CI, container and secret configuration is protected."""
    assert guard_paths.is_infra_file(path)


def test_source_is_not_infra() -> None:
    """A normal source file is not infrastructure."""
    assert not guard_paths.is_infra_file("/repo/src/app/service.py")
