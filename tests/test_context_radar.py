"""Tests für home/statusline.py und home/hooks/context_radar.py."""

import importlib.util
import json
import pathlib

HOME = pathlib.Path(__file__).resolve().parents[1] / "home"


def load(name: str, path: pathlib.Path):
    """Import a script file as a module without needing a package."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


statusline = load("statusline", HOME / "statusline.py")
radar = load("context_radar", HOME / "hooks" / "context_radar.py")


def test_statusline_renders_bar_and_percent() -> None:
    """A normal session shows model, bar and percent without a warning."""
    line = statusline.render({"model": {"display_name": "Opus"}, "context_window": {"used_percentage": 32}})
    assert line == "[Opus] ▓▓▓░░░░░░░ 32%"


def test_statusline_warns_from_fifty() -> None:
    """At the threshold the warning text appears."""
    line = statusline.render({"model": {"display_name": "Opus"}, "context_window": {"used_percentage": 50}})
    assert "Übergabe" in line


def test_statusline_handles_missing_fields() -> None:
    """Early in a session the context fields are null; the line still renders."""
    line = statusline.render({"model": {"display_name": "Opus"}, "context_window": {"used_percentage": None}})
    assert line.endswith("0%")


def test_radar_silent_below_threshold() -> None:
    """No hint below the warning threshold or without a stored value."""
    assert radar.message_for(10) is None
    assert radar.message_for(None) is None


def test_radar_warns_and_escalates() -> None:
    """Warning at 50, urgent wording at 75."""
    assert "Übergabe" in radar.message_for(55)
    assert "/clear vorschlagen" in radar.message_for(80)


def test_roundtrip_through_state_file(tmp_path, monkeypatch) -> None:
    """The percentage written by the statusline is what the hook reads back."""
    monkeypatch.setattr(statusline.tempfile, "gettempdir", lambda: str(tmp_path))
    monkeypatch.setattr(radar.tempfile, "gettempdir", lambda: str(tmp_path))
    statusline.state_file("abc").write_text(json.dumps({"pct": 61}), encoding="utf-8")
    assert radar.read_pct("abc") == 61
