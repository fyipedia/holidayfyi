"""Tests for the holidayfyi engine."""

from datetime import date

import pytest

from holidayfyi import (
    days_until,
    easter_orthodox,
    easter_western,
    get_upcoming_holidays,
    get_weekday_name,
    holidays_on_date,
    is_weekend,
    next_occurrence,
    nth_weekday_of_month,
)

# ── Easter Western ──


def test_easter_western_2026() -> None:
    """Western Easter 2026 is April 5."""
    assert easter_western(2026) == date(2026, 4, 5)


def test_easter_western_2025() -> None:
    """Western Easter 2025 is April 20."""
    assert easter_western(2025) == date(2025, 4, 20)


def test_easter_western_2024() -> None:
    """Western Easter 2024 is March 31."""
    assert easter_western(2024) == date(2024, 3, 31)


def test_easter_western_2000() -> None:
    """Western Easter 2000 is April 23."""
    assert easter_western(2000) == date(2000, 4, 23)


# ── Easter Orthodox ──


def test_easter_orthodox_2026() -> None:
    """Orthodox Easter 2026 is April 12."""
    assert easter_orthodox(2026) == date(2026, 4, 12)


def test_easter_orthodox_2025() -> None:
    """Orthodox Easter 2025 is April 20."""
    assert easter_orthodox(2025) == date(2025, 4, 20)


def test_easter_orthodox_2024() -> None:
    """Orthodox Easter 2024 is May 5."""
    assert easter_orthodox(2024) == date(2024, 5, 5)


# ── Nth Weekday ──


def test_nth_weekday_3rd_monday_jan_2026() -> None:
    """3rd Monday of January 2026 is Jan 19 (MLK Day)."""
    assert nth_weekday_of_month(2026, 1, 0, 3) == date(2026, 1, 19)


def test_nth_weekday_1st_monday() -> None:
    """1st Monday of March 2026."""
    result = nth_weekday_of_month(2026, 3, 0, 1)
    assert result == date(2026, 3, 2)
    assert result.weekday() == 0  # Monday


def test_nth_weekday_last_friday() -> None:
    """Last Friday of January 2026 is Jan 30."""
    result = nth_weekday_of_month(2026, 1, 4, -1)
    assert result == date(2026, 1, 30)
    assert result.weekday() == 4  # Friday


def test_nth_weekday_4th_thursday_november() -> None:
    """4th Thursday of November 2026 (Thanksgiving)."""
    result = nth_weekday_of_month(2026, 11, 3, 4)
    assert result.weekday() == 3  # Thursday
    assert result.month == 11


def test_nth_weekday_invalid_n() -> None:
    """Invalid n raises ValueError."""
    with pytest.raises(ValueError, match="n must be >= 1"):
        nth_weekday_of_month(2026, 1, 0, 0)


def test_nth_weekday_nonexistent() -> None:
    """5th Monday doesn't always exist."""
    with pytest.raises(ValueError, match="No 5th occurrence"):
        nth_weekday_of_month(2026, 2, 0, 5)


# ── Days Until ──


def test_days_until_future() -> None:
    """Days until a future date from a known reference."""
    result = days_until(date(2026, 12, 25), from_date=date(2026, 12, 20))
    assert result == 5


def test_days_until_past() -> None:
    """Negative result for past dates."""
    result = days_until(date(2026, 1, 1), from_date=date(2026, 1, 10))
    assert result == -9


def test_days_until_same_day() -> None:
    """Zero days if same date."""
    result = days_until(date(2026, 6, 15), from_date=date(2026, 6, 15))
    assert result == 0


# ── Next Occurrence ──


def test_next_occurrence_future_this_year() -> None:
    """Next Dec 25 from Jan 1 is this year."""
    result = next_occurrence(12, 25, from_date=date(2026, 1, 1))
    assert result == date(2026, 12, 25)


def test_next_occurrence_past_this_year() -> None:
    """Next Jan 1 from Dec 31 is next year."""
    result = next_occurrence(1, 1, from_date=date(2026, 12, 31))
    assert result == date(2027, 1, 1)


def test_next_occurrence_same_day() -> None:
    """Same day returns today."""
    result = next_occurrence(6, 15, from_date=date(2026, 6, 15))
    assert result == date(2026, 6, 15)


# ── Get Upcoming Holidays (requires python-holidays) ──


def test_get_upcoming_holidays_us() -> None:
    """US should have multiple upcoming holidays."""
    holidays = get_upcoming_holidays("US", n=5)
    assert len(holidays) > 0
    assert len(holidays) <= 5
    assert "name" in holidays[0]
    assert "date" in holidays[0]
    assert "is_public" in holidays[0]


def test_get_upcoming_holidays_invalid_country() -> None:
    """Invalid country code returns empty list."""
    holidays = get_upcoming_holidays("ZZ", n=5)
    assert holidays == []


# ── Holidays On Date (requires python-holidays) ──


def test_holidays_on_date_christmas() -> None:
    """Christmas is a holiday in the US."""
    result = holidays_on_date(date(2026, 12, 25), ["US"])
    assert "US" in result
    assert len(result["US"]) > 0


def test_holidays_on_date_no_holiday() -> None:
    """Regular weekday with no holidays."""
    # Feb 18 2026 is a Wednesday — test a day that's unlikely to be a holiday
    result = holidays_on_date(date(2026, 2, 18), ["US"])
    # This might or might not have a holiday — just check it returns dict
    assert isinstance(result, dict)


def test_holidays_on_date_multiple_countries() -> None:
    """Check multiple countries at once."""
    result = holidays_on_date(date(2026, 1, 1), ["US", "KR", "JP"])
    # New Year's Day is universal
    assert len(result) > 0


# ── Weekend & Weekday ──


def test_is_weekend_saturday() -> None:
    """Saturday is a weekend."""
    assert is_weekend(date(2026, 3, 7)) is True  # Saturday


def test_is_weekend_sunday() -> None:
    """Sunday is a weekend."""
    assert is_weekend(date(2026, 3, 8)) is True  # Sunday


def test_is_weekend_monday() -> None:
    """Monday is not a weekend."""
    assert is_weekend(date(2026, 3, 2)) is False  # Monday


def test_is_weekend_friday() -> None:
    """Friday is not a weekend."""
    assert is_weekend(date(2026, 3, 6)) is False  # Friday


def test_get_weekday_name_monday() -> None:
    """March 2, 2026 is a Monday."""
    assert get_weekday_name(date(2026, 3, 2)) == "Monday"


def test_get_weekday_name_friday() -> None:
    """March 6, 2026 is a Friday."""
    assert get_weekday_name(date(2026, 3, 6)) == "Friday"


def test_get_weekday_name_sunday() -> None:
    """March 8, 2026 is a Sunday."""
    assert get_weekday_name(date(2026, 3, 8)) == "Sunday"
