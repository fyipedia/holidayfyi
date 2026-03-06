---
name: holiday-tools
description: Compute Easter dates (Western and Orthodox), find nth weekday occurrences, count days until holidays, and look up public holidays by country. Use when calculating holiday dates, Easter, or scheduling around public holidays.
license: MIT
metadata:
  author: fyipedia
  version: "0.1.1"
  homepage: "https://holidayfyi.com/"
---

# HolidayFYI -- Holiday Tools for AI Agents

Pure Python holiday engine. Compute Easter dates for Western and Orthodox traditions, find nth weekday occurrences, count days until any date, look up public holidays by country -- zero dependencies core with optional `python-holidays` integration.

**Install**: `pip install holidayfyi` -- **Web**: [holidayfyi.com](https://holidayfyi.com/) -- **API**: [REST API](https://holidayfyi.com/developers/) -- **npm**: `npm install holidayfyi`

## When to Use

- User asks when Easter falls in a given year (Western or Orthodox)
- User needs to find a specific weekday occurrence (e.g., "3rd Monday of January")
- User wants to count days until a date or find the next occurrence of a fixed date
- User asks about upcoming public holidays for a country
- User wants to check what holidays fall on a specific date across countries

## Tools

### `easter_western(year) -> date`

Calculate Western (Gregorian) Easter date using the Anonymous Gregorian algorithm.

```python
from holidayfyi import easter_western

easter_western(2026)  # datetime.date(2026, 4, 5)
easter_western(2027)  # datetime.date(2027, 3, 28)
easter_western(2028)  # datetime.date(2028, 4, 16)
```

### `easter_orthodox(year) -> date`

Calculate Orthodox Easter date (Julian algorithm + 13-day Gregorian offset).

```python
from holidayfyi import easter_orthodox

easter_orthodox(2026)  # datetime.date(2026, 4, 19)
easter_orthodox(2027)  # datetime.date(2027, 5, 2)
easter_orthodox(2028)  # datetime.date(2028, 4, 16)  # same as Western in 2028
```

### `nth_weekday_of_month(year, month, weekday, n) -> date`

Find the nth occurrence of a weekday in a given month. Weekday: 0=Monday through 6=Sunday. Use n=-1 for last occurrence.

```python
from holidayfyi import nth_weekday_of_month

# Martin Luther King Jr. Day: 3rd Monday of January
nth_weekday_of_month(2026, 1, 0, 3)   # datetime.date(2026, 1, 19)

# US Thanksgiving: 4th Thursday of November
nth_weekday_of_month(2026, 11, 3, 4)  # datetime.date(2026, 11, 26)

# Last Friday of March
nth_weekday_of_month(2026, 3, 4, -1)  # datetime.date(2026, 3, 27)
```

### `days_until(target_date, from_date) -> int`

Count the number of days until a target date.

```python
from datetime import date
from holidayfyi import days_until

days_until(date(2026, 12, 25), from_date=date(2026, 1, 1))  # 358
```

### `next_occurrence(fixed_month, fixed_day, from_date) -> date`

Find the next occurrence of a fixed month/day (this year or next).

```python
from datetime import date
from holidayfyi import next_occurrence

next_occurrence(7, 4, from_date=date(2026, 8, 1))  # datetime.date(2027, 7, 4)
next_occurrence(7, 4, from_date=date(2026, 1, 1))  # datetime.date(2026, 7, 4)
```

### `is_weekend(d) -> bool`

Check if a date falls on Saturday or Sunday.

```python
from datetime import date
from holidayfyi import is_weekend

is_weekend(date(2026, 3, 7))  # True (Saturday)
is_weekend(date(2026, 3, 9))  # False (Monday)
```

### `get_weekday_name(d) -> str`

Get the English name of the day of the week.

```python
from datetime import date
from holidayfyi import get_weekday_name

get_weekday_name(date(2026, 3, 2))  # 'Monday'
```

### `get_upcoming_holidays(country_iso, n) -> list[dict]`

Get the next n upcoming public holidays for a country. Requires `pip install "holidayfyi[holidays]"`.

```python
from holidayfyi import get_upcoming_holidays

get_upcoming_holidays("US", n=5)
# [{"name": "Memorial Day", "date": "2026-05-25", "is_public": True}, ...]
```

### `holidays_on_date(target_date, countries) -> dict[str, list[str]]`

Find which holidays fall on a given date across multiple countries. Requires `pip install "holidayfyi[holidays]"`.

```python
from datetime import date
from holidayfyi import holidays_on_date

holidays_on_date(date(2026, 12, 25), ["US", "KR", "JP", "DE"])
# {"US": ["Christmas Day"], "KR": ["Christmas Day"], "DE": ["Erster Weihnachtstag"]}
```

## REST API (No Auth Required)

```bash
curl https://holidayfyi.com/api/easter/2026/
curl https://holidayfyi.com/api/holidays/US/
curl https://holidayfyi.com/api/on-date/2026-12-25/
curl https://holidayfyi.com/api/nth-weekday/2026/1/0/3/
```

Full spec: [OpenAPI 3.1.0](https://holidayfyi.com/api/openapi.json)

## Easter Dates Reference (2025-2030)

| Year | Western Easter | Orthodox Easter | Gap |
|------|---------------|----------------|-----|
| 2025 | Apr 20 | Apr 20 | 0 days |
| 2026 | Apr 5 | Apr 19 | 14 days |
| 2027 | Mar 28 | May 2 | 35 days |
| 2028 | Apr 16 | Apr 16 | 0 days |
| 2029 | Apr 1 | Apr 8 | 7 days |
| 2030 | Apr 21 | Apr 28 | 7 days |

## Common US Holidays (Nth Weekday Pattern)

| Holiday | Rule | Weekday | N |
|---------|------|---------|---|
| MLK Day | 3rd Monday of January | 0 | 3 |
| Presidents' Day | 3rd Monday of February | 0 | 3 |
| Memorial Day | Last Monday of May | 0 | -1 |
| Labor Day | 1st Monday of September | 0 | 1 |
| Columbus Day | 2nd Monday of October | 0 | 2 |
| Thanksgiving | 4th Thursday of November | 3 | 4 |

## Demo

![HolidayFYI demo](https://raw.githubusercontent.com/fyipedia/holidayfyi/main/demo.gif)

## Utility FYI Family

Part of the [FYIPedia](https://fyipedia.com) ecosystem: [UnitFYI](https://unitfyi.com), [TimeFYI](https://timefyi.com), [HolidayFYI](https://holidayfyi.com), [NameFYI](https://namefyi.com), [DistanceFYI](https://distancefyi.com).
