"""Tests für die ausgelieferten Konfigurationsdateien: gültiges JSON, Hook-Skripte vorhanden."""

import json
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
JSON_FILES = ["home/settings.json", "project/.claude/settings.json", "project/.mcp.json.example"]


def commands(settings: dict) -> list[str]:
    """Return every command string configured as a hook or status line."""
    found = [settings["statusLine"]["command"]] if "statusLine" in settings else []
    for groups in settings.get("hooks", {}).values():
        for group in groups:
            found += [hook["command"] for hook in group["hooks"] if hook.get("type") == "command"]
    return found


@pytest.mark.parametrize("relative", JSON_FILES)
def test_json_files_parse(relative: str) -> None:
    """Shipped JSON has no comments or trailing commas."""
    json.loads((ROOT / relative).read_text(encoding="utf-8"))


def test_home_commands_point_at_shipped_scripts() -> None:
    """Every script named in home/settings.json exists under home/."""
    settings = json.loads((ROOT / "home/settings.json").read_text(encoding="utf-8"))
    scripts = [re.search(r"\.claude/([\w/]+\.py)", command) for command in commands(settings)]
    assert scripts and all(scripts)
    missing = [m.group(1) for m in scripts if not (ROOT / "home" / m.group(1)).is_file()]
    assert missing == []


def test_home_registers_all_four_hook_events() -> None:
    """Shell guard, limit check, context radar and reinject are all wired up."""
    hooks = json.loads((ROOT / "home/settings.json").read_text(encoding="utf-8"))["hooks"]
    assert set(hooks) == {"PreToolUse", "PostToolUse", "UserPromptSubmit", "SessionStart"}
    assert hooks["PostToolUse"][0]["matcher"] == "Edit|Write"
    assert hooks["SessionStart"][0]["matcher"] == "compact"


def test_explained_settings_name_the_same_hook_scripts() -> None:
    """settings.erklaert.jsonc documents every script that settings.json runs."""
    settings = json.loads((ROOT / "home/settings.json").read_text(encoding="utf-8"))
    explained = (ROOT / "home/settings.erklaert.jsonc").read_text(encoding="utf-8")
    scripts = [re.search(r"[\w/]+\.py", command).group(0) for command in commands(settings)]
    assert [script for script in scripts if script not in explained] == []
