"""Holiday computation engine — pure Python, zero dependencies, <1ms.

Provides Easter date calculation, nth weekday finder, days-until counting,
next occurrence lookup, and weekend/weekday helpers. All functions are
stateless and thread-safe.

Functions requiring python-holidays (get_upcoming_holidays, holidays_on_date)
use lazy imports — install with: pip install holidayfyi[holidays]
"""

from __future__ import annotations

import calendar
from datetime import date, timedelta

# ── Easter Dates ──────────────────────────────────────────────────


def easter_western(year: int) -> date:
    """Calculate Western (Gregorian) Easter date using the Anonymous Gregorian algorithm.

    Reference: https://en.wikipedia.org/wiki/Date_of_Easter#Anonymous_Gregorian_algorithm

    Args:
        year: Calendar year.

    Returns:
        The date of Western Easter Sunday.
    """
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    el = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * el) // 451
    month, day = divmod(h + el - 7 * m + 114, 31)
    return date(year, month, day + 1)


def easter_orthodox(year: int) -> date:
    """Calculate Orthodox Easter date (Julian Easter + 13-day offset).

    Uses the Meeus Julian algorithm, then adds 13 days to convert
    from Julian to Gregorian calendar.

    Args:
        year: Calendar year.

    Returns:
        The date of Orthodox Easter Sunday (Gregorian calendar).
    """
    a = year % 4
    b = year % 7
    c = year % 19
    d = (19 * c + 15) % 30
    e = (2 * a + 4 * b - d + 34) % 7
    month, day = divmod(d + e + 114, 31)
    # Julian to Gregorian: add 13 days
    julian_date = date(year, month, day + 1)
    return julian_date + timedelta(days=13)


# ── Nth Weekday ───────────────────────────────────────────────────


def nth_weekday_of_month(year: int, month: int, weekday: int, n: int) -> date:
    """Find the nth occurrence of a weekday in a given month.

    Args:
        year: Calendar year.
        month: Month (1-12).
        weekday: Day of week (0=Monday, 6=Sunday).
        n: 1-indexed occurrence (1=first, 2=second, ...) or -1 for last.

    Returns:
        The date of the nth weekday in the given month.

    Raises:
        ValueError: If the requested occurrence does not exist.
    """
    if n == -1:
        # Last occurrence: start from last day of month, go backwards
        last_day = calendar.monthrange(year, month)[1]
        d = date(year, month, last_day)
        while d.weekday() != weekday:
            d -= timedelta(days=1)
        return d

    if n < 1:
        msg = f"n must be >= 1 or -1 for last, got {n}"
        raise ValueError(msg)

    # Find the first occurrence of the weekday in the month
    first_day = date(year, month, 1)
    days_ahead = weekday - first_day.weekday()
    if days_ahead < 0:
        days_ahead += 7
    first_occurrence = first_day + timedelta(days=days_ahead)

    # Add (n-1) weeks
    result = first_occurrence + timedelta(weeks=n - 1)
    if result.month != month:
        msg = f"No {n}th occurrence of weekday {weekday} in {year}-{month:02d}"
        raise ValueError(msg)
    return result


# ── Days Until & Next Occurrence ──────────────────────────────────


def days_until(target_date: date, from_date: date | None = None) -> int:
    """Calculate the number of days until a target date.

    Args:
        target_date: The future date to count towards.
        from_date: The starting date (defaults to today).

    Returns:
        Number of days (negative if target_date is in the past).
    """
    if from_date is None:
        from_date = date.today()
    return (target_date - from_date).days


def next_occurrence(fixed_month: int, fixed_day: int, from_date: date | None = None) -> date:
    """Find the next occurrence of a fixed-date holiday.

    Args:
        fixed_month: Month of the holiday (1-12).
        fixed_day: Day of the holiday (1-31).
        from_date: Reference date (defaults to today).

    Returns:
        The next occurrence of the given month/day (this year or next).
    """
    if from_date is None:
        from_date = date.today()
    this_year = date(from_date.year, fixed_month, fixed_day)
    if this_year >= from_date:
        return this_year
    return date(from_date.year + 1, fixed_month, fixed_day)


# ── Upcoming & On-Date (requires python-holidays) ────────────────


def get_upcoming_holidays(country_iso: str, n: int = 10) -> list[dict[str, str | bool]]:
    """Get the next n upcoming holidays for a country using python-holidays.

    Requires: pip install holidayfyi[holidays]

    Args:
        country_iso: ISO 3166-1 alpha-2 country code (e.g. "US", "KR").
        n: Number of upcoming holidays to return.

    Returns:
        List of dicts with keys: name, date, is_public.
        Returns empty list if country is not supported.
    """
    try:
        import holidays as holidays_lib
    except ImportError:
        msg = (
            "python-holidays is required for get_upcoming_holidays(). "
            "Install with: pip install holidayfyi[holidays]"
        )
        raise ImportError(msg) from None

    try:
        country_holidays = holidays_lib.country_holidays(country_iso)
    except NotImplementedError:
        return []

    today = date.today()
    current_year = today.year
    # Gather holidays for current year and next year to ensure enough results
    all_dates: list[tuple[date, str]] = []
    for yr in (current_year, current_year + 1):
        yearly = holidays_lib.country_holidays(country_iso, years=yr)
        for d, name in sorted(yearly.items()):
            if d >= today:
                all_dates.append((d, name))

    # Deduplicate and sort
    seen: set[tuple[date, str]] = set()
    unique: list[tuple[date, str]] = []
    for d, name in sorted(all_dates):
        if (d, name) not in seen:
            seen.add((d, name))
            unique.append((d, name))

    results: list[dict[str, str | bool]] = []
    for d, name in unique[:n]:
        results.append(
            {
                "name": name,
                "date": d.isoformat(),
                "is_public": d in country_holidays,
            }
        )
    return results


def holidays_on_date(target_date: date, countries: list[str]) -> dict[str, list[str]]:
    """Find which holidays fall on a given date across multiple countries.

    Requires: pip install holidayfyi[holidays]

    Args:
        target_date: The date to check.
        countries: List of ISO 3166-1 alpha-2 country codes.

    Returns:
        Dict mapping country code to list of holiday names on that date.
        Countries with no holidays on that date are omitted.
    """
    try:
        import holidays as holidays_lib
    except ImportError:
        msg = (
            "python-holidays is required for holidays_on_date(). "
            "Install with: pip install holidayfyi[holidays]"
        )
        raise ImportError(msg) from None

    result: dict[str, list[str]] = {}
    for code in countries:
        try:
            country_holidays = holidays_lib.country_holidays(code, years=target_date.year)
        except NotImplementedError:
            continue
        if target_date in country_holidays:
            names = country_holidays.get_list(target_date)
            if names:
                result[code] = names
    return result


# ── Weekend & Weekday ─────────────────────────────────────────────


def is_weekend(d: date) -> bool:
    """Check if a date falls on a weekend (Saturday or Sunday).

    Args:
        d: The date to check.

    Returns:
        True if Saturday or Sunday.
    """
    return d.weekday() >= 5


def get_weekday_name(d: date) -> str:
    """Get the English name of the day of the week.

    Args:
        d: The date to get the weekday name for.

    Returns:
        English weekday name (e.g., "Monday", "Friday").
    """
    return calendar.day_name[d.weekday()]
