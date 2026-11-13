"""Tests für home/hooks/check_limits.py. Lauf: python -m pytest tests/ -q"""

import importlib.util
import io
import json
import pathlib
import subprocess

import pytest

HOOKS = pathlib.Path(__file__).resolve().parents[1] / "home" / "hooks"
spec = importlib.util.spec_from_file_location("check_limits", HOOKS / "check_limits.py")
check_limits = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_limits)

CHECKED = ["backend/app/services.py", "frontend/src/app/x.component.ts", "C:\\repo\\src\\styles\\_grid.scss"]
SKIPPED = [
    "README.md",
    "backend/app/tests/test_services.py",
    "frontend/src/app/x.component.spec.ts",
    "backend/app/migrations/0001_initial.py",
    "frontend/node_modules/lib/index.js",
    "static/vendor.min.js",
    "package-lock.json",
]


def function(name: str, body_lines: int, docstring: bool = True) -> str:
    """Return the source of a function with the given number of body statements."""
    doc = ['    """Do the thing."""'] if docstring else []
    return "\n".join([f"def {name}() -> None:", *doc, *["    pass"] * body_lines]) + "\n"


def git(repo: pathlib.Path, *args: str) -> None:
    """Run a git command in the repo with a fixed identity."""
    identity = ["-c", "user.name=t", "-c", "user.email=t@example.com", "-c", "commit.gpgsign=false"]
    subprocess.run(["git", *identity, *args], cwd=repo, check=True, capture_output=True)


@pytest.fixture
def repo(tmp_path: pathlib.Path) -> pathlib.Path:
    """Return an empty git repository with one commit."""
    git(tmp_path, "init", "-q")
    (tmp_path / "seed.txt").write_text("x\n", encoding="utf-8")
    git(tmp_path, "add", "seed.txt")
    git(tmp_path, "commit", "-q", "-m", "seed")
    return tmp_path


def commit(repo: pathlib.Path, name: str, text: str) -> pathlib.Path:
    """Write a file, commit it and return its path."""
    path = repo / name
    path.write_text(text, encoding="utf-8")
    git(repo, "add", name)
    git(repo, "commit", "-q", "-m", name)
    return path


@pytest.mark.parametrize("path", CHECKED)
def test_productive_code_is_checked(path: str) -> None:
    """Code files outside tests and generated folders fall under the limits."""
    assert check_limits.is_checked(path)


@pytest.mark.parametrize("path", SKIPPED)
def test_tests_docs_and_generated_files_are_skipped(path: str) -> None:
    """Tests, migrations, vendored code and non-code files are exempt."""
    assert not check_limits.is_checked(path)


def test_function_at_the_limit_passes() -> None:
    """Twenty lines including the def line are allowed; the docstring does not count."""
    assert check_limits.violations(function("ok", 19), ".py") == {}


def test_function_over_the_limit_is_named_with_its_length() -> None:
    """One line more is reported under the function name."""
    assert check_limits.violations(function("too_long", 20), ".py") == {"too_long": 21}


def test_multiline_docstring_is_not_counted() -> None:
    """A long docstring alone never pushes a function over the limit."""
    doc = '    """Summary.\n\n' + "    More.\n" * 30 + '    """\n'
    source = "def documented() -> None:\n" + doc + "    pass\n"
    assert check_limits.violations(source, ".py") == {}


def test_methods_and_async_functions_are_measured() -> None:
    """Nested and async definitions are found, not only module-level functions."""
    method = "\n".join("    " + line for line in function("run", 25).splitlines())
    source = "class Service:\n" + method + "\n\nasync " + function("fetch", 30)
    assert check_limits.violations(source, ".py") == {"run": 26, "fetch": 31}


def test_file_over_the_limit_is_reported() -> None:
    """The file length limit applies to every checked suffix, not only Python."""
    assert check_limits.violations("a {}\n" * 401, ".scss") == {check_limits.FILE_KEY: 401}
    assert check_limits.violations("a {}\n" * 400, ".scss") == {}


def test_function_length_is_only_measured_for_python() -> None:
    """TypeScript functions are left to ESLint."""
    assert check_limits.violations(function("too_long", 40), ".ts") == {}


def test_unparseable_python_reports_no_functions() -> None:
    """A file that is broken mid-edit does not crash the hook."""
    assert check_limits.function_lengths("def broken(:\n") == {}


def test_new_file_over_the_limit_is_reported(repo: pathlib.Path) -> None:
    """An untracked file has no old state, so every violation is new."""
    path = repo / "services.py"
    path.write_text(function("too_long", 30), encoding="utf-8")
    assert check_limits.check(path) == [
        f"{path}: Funktion too_long hat 31 Zeilen (Grenze 20). Aufteilen."
    ]


def test_legacy_violation_that_did_not_grow_is_silent(repo: pathlib.Path) -> None:
    """Editing elsewhere in a file with an old long function reports nothing."""
    path = commit(repo, "legacy.py", function("old", 30))
    path.write_text(function("old", 30) + "\n\n" + function("new", 3), encoding="utf-8")
    assert check_limits.check(path) == []


def test_legacy_violation_that_grew_is_reported(repo: pathlib.Path) -> None:
    """Making an already long function longer is a new violation."""
    path = commit(repo, "legacy.py", function("old", 30))
    path.write_text(function("old", 31), encoding="utf-8")
    assert check_limits.check(path) == [f"{path}: Funktion old hat 32 Zeilen (Grenze 20). Aufteilen."]


def test_file_crossing_the_limit_is_reported(repo: pathlib.Path) -> None:
    """A file that was under the limit in HEAD and is now over is reported."""
    path = commit(repo, "big.ts", "x;\n" * 400)
    path.write_text("x;\n" * 401, encoding="utf-8")
    assert check_limits.check(path) == [f"{path} hat 401 Zeilen (Grenze 400). Thema teilen."]


def run_main(monkeypatch: pytest.MonkeyPatch, file_path: str) -> int:
    """Call main() with a PostToolUse payload for the given path."""
    payload = {"hook_event_name": "PostToolUse", "tool_name": "Write", "tool_input": {"file_path": file_path}}
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(payload)))
    return check_limits.main()


def test_main_exits_two_and_names_the_rule(
    repo: pathlib.Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Exit 2 puts the reason on stderr, where Claude Code shows it to Claude."""
    path = repo / "services.py"
    path.write_text(function("too_long", 30), encoding="utf-8")
    assert run_main(monkeypatch, str(path)) == 2
    assert "check_limits (Hardrule §11):" in capsys.readouterr().err


def test_main_passes_clean_skipped_and_missing_files(
    repo: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Clean code, exempt files and paths that do not exist all exit 0."""
    clean = repo / "clean.py"
    clean.write_text(function("ok", 5), encoding="utf-8")
    long_test = repo / "test_big.py"
    long_test.write_text(function("too_long", 30), encoding="utf-8")
    for path in (clean, long_test, repo / "gone.py"):
        assert run_main(monkeypatch, str(path)) == 0
