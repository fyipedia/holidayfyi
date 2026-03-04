"""Tests for the holidayfyi MCP server."""

from holidayfyi.mcp_server import (
    check_holidays_on_date,
    count_days_until,
    easter_date,
    nth_weekday,
    upcoming_holidays,
)


def test_upcoming_holidays_us() -> None:
    result = upcoming_holidays("US", n=5)
    assert "Upcoming Holidays" in result
    assert "US" in result


def test_upcoming_holidays_invalid() -> None:
    result = upcoming_holidays("ZZ")
    assert "No holidays found" in result


def test_check_holidays_on_date_christmas() -> None:
    result = check_holidays_on_date("2026-12-25", "US")
    assert "2026-12-25" in result
    assert "US" in result


def test_easter_date_western() -> None:
    result = easter_date(2026)
    assert "2026-04-05" in result
    assert "Western" in result


def test_easter_date_orthodox() -> None:
    result = easter_date(2026, orthodox=True)
    assert "2026-04-12" in result
    assert "Orthodox" in result


def test_nth_weekday_tool() -> None:
    result = nth_weekday(2026, 1, 0, 3)
    assert "2026-01-19" in result
    assert "Monday" in result


def test_nth_weekday_last() -> None:
    result = nth_weekday(2026, 1, 4, -1)
    assert "2026-01-30" in result
    assert "Friday" in result


def test_count_days_until_future() -> None:
    result = count_days_until("2026-12-25", "2026-12-20")
    assert "5 days until" in result


def test_count_days_until_past() -> None:
    result = count_days_until("2026-01-01", "2026-01-10")
    assert "9 days ago" in result


def test_count_days_until_today() -> None:
    result = count_days_until("2026-06-15", "2026-06-15")
    assert "today" in result
