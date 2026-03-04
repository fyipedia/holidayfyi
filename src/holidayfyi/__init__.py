"""holidayfyi — Pure Python holiday engine for developers.

Compute Easter dates, find nth weekday occurrences, count days until
holidays, and look up public holidays by country. Zero dependencies core.

Basic usage::

    >>> from holidayfyi import easter_western, easter_orthodox, nth_weekday_of_month
    >>> easter_western(2026)
    datetime.date(2026, 4, 5)
    >>> easter_orthodox(2026)
    datetime.date(2026, 4, 19)
    >>> nth_weekday_of_month(2026, 1, 0, 3)  # 3rd Monday of Jan 2026
    datetime.date(2026, 1, 19)
"""

from holidayfyi.engine import (
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

__version__ = "0.1.0"

__all__ = [
    # Easter dates
    "easter_western",
    "easter_orthodox",
    # Nth weekday
    "nth_weekday_of_month",
    # Days until & next occurrence
    "days_until",
    "next_occurrence",
    # Upcoming & on-date (requires python-holidays)
    "get_upcoming_holidays",
    "holidays_on_date",
    # Weekend & weekday
    "is_weekend",
    "get_weekday_name",
]
