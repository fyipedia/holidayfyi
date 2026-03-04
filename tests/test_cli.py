"""Tests for the holidayfyi CLI."""

from typer.testing import CliRunner

from holidayfyi.cli import app

runner = CliRunner()


def test_easter_command() -> None:
    result = runner.invoke(app, ["easter", "2026"])
    assert result.exit_code == 0
    assert "2026-04-05" in result.output


def test_easter_orthodox_command() -> None:
    result = runner.invoke(app, ["easter", "2026", "--orthodox"])
    assert result.exit_code == 0
    assert "2026-04-12" in result.output


def test_upcoming_command() -> None:
    result = runner.invoke(app, ["upcoming", "US"])
    assert result.exit_code == 0
    assert "Upcoming Holidays" in result.output


def test_on_date_command() -> None:
    result = runner.invoke(app, ["on-date", "2026-12-25", "US"])
    assert result.exit_code == 0
    assert "2026-12-25" in result.output


def test_nth_weekday_command() -> None:
    result = runner.invoke(app, ["nth-weekday", "2026", "1", "0", "3"])
    assert result.exit_code == 0
    assert "2026-01-19" in result.output


def test_nth_weekday_invalid() -> None:
    result = runner.invoke(app, ["nth-weekday", "2026", "2", "0", "5"])
    assert result.exit_code == 1
