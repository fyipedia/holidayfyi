# holidayfyi

[![PyPI](https://img.shields.io/pypi/v/holidayfyi)](https://pypi.org/project/holidayfyi/)
[![Python](https://img.shields.io/pypi/pyversions/holidayfyi)](https://pypi.org/project/holidayfyi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Pure Python holiday engine for developers. Compute [Easter dates](https://holidayfyi.com/) for both Western and Orthodox traditions, find nth weekday occurrences (e.g., "3rd Monday of January"), count days until any date, look up public holidays by country, and check what holidays fall on a given date -- zero dependencies core with optional [python-holidays](https://pypi.org/project/holidays/) integration.

> **Browse holidays by country at [holidayfyi.com](https://holidayfyi.com/)** -- holiday calendars, upcoming dates, and traditions for countries worldwide.

<p align="center">
  <img src="demo.gif" alt="holidayfyi CLI demo" width="800">
</p>

## Table of Contents

- [Install](#install)
- [Quick Start](#quick-start)
- [How Easter is Calculated](#how-easter-is-calculated)
- [Fixed vs Moveable Holidays](#fixed-vs-moveable-holidays)
- [Country Holidays](#country-holidays-optional)
- [Command-Line Interface](#command-line-interface)
- [MCP Server (Claude, Cursor, Windsurf)](#mcp-server-claude-cursor-windsurf)
- [REST API Client](#rest-api-client)
- [API Reference](#api-reference)
  - [Easter Dates](#easter-dates)
  - [Date Utilities](#date-utilities)
  - [Weekend & Weekday](#weekend--weekday)
  - [Country Holidays](#country-holidays-requires-holidays)
- [Features](#features)
- [Learn More About Holidays](#learn-more-about-holidays)
- [FYIPedia Developer Tools](#fyipedia-developer-tools)
- [License](#license)

## Install

```bash
pip install holidayfyi              # Core engine (zero deps)
pip install "holidayfyi[holidays]"  # + python-holidays integration
pip install "holidayfyi[cli]"       # + Command-line interface
pip install "holidayfyi[mcp]"       # + MCP server for AI assistants
pip install "holidayfyi[api]"       # + HTTP client for holidayfyi.com API
pip install "holidayfyi[all]"       # Everything
```

## Quick Start

```python
from holidayfyi import easter_western, easter_orthodox, nth_weekday_of_month

# Easter dates
easter_western(2026)    # datetime.date(2026, 4, 5)
easter_orthodox(2026)   # datetime.date(2026, 4, 19)

# 3rd Monday of January 2026 (MLK Day)
nth_weekday_of_month(2026, 1, 0, 3)  # datetime.date(2026, 1, 19)

# Days until Christmas
from holidayfyi import days_until
from datetime import date
days_until(date(2026, 12, 25), from_date=date(2026, 1, 1))  # 358

# Next occurrence of a fixed date
from holidayfyi import next_occurrence
next_occurrence(7, 4, from_date=date(2026, 1, 1))  # datetime.date(2026, 7, 4)

# Weekend check
from holidayfyi import is_weekend, get_weekday_name
is_weekend(date(2026, 3, 7))      # True (Saturday)
get_weekday_name(date(2026, 3, 2)) # "Monday"
```

## How Easter is Calculated

Easter is the most computationally interesting holiday because its date depends on a combination of solar and lunar cycles. The rule established at the Council of Nicaea (325 AD) states: Easter falls on the first Sunday after the first full moon on or after the spring equinox (March 21).

The algorithm to compute this is called the **Computus**. The `holidayfyi` package implements two variants:

**Western Easter (Gregorian)** uses the Anonymous Gregorian algorithm (also known as the Meeus/Jones/Butcher algorithm). It accounts for the Gregorian calendar's leap year corrections and the 19-year Metonic cycle of lunar phases. Western Easter can fall between March 22 and April 25.

**Orthodox Easter (Julian)** uses Meeus's Julian algorithm. The Orthodox churches still compute Easter based on the Julian calendar, then map the result to the Gregorian date. Orthodox Easter can fall between April 4 and May 8 (Gregorian). In some years, Western and Orthodox Easter coincide; in others, they are up to 5 weeks apart.

```python
from holidayfyi import easter_western, easter_orthodox

# Compare Western and Orthodox Easter for several years
for year in range(2025, 2031):
    w = easter_western(year)
    o = easter_orthodox(year)
    gap = (o - w).days
    print(f"{year}: Western {w}, Orthodox {o}, gap {gap} days")

# 2025: Western 2025-04-20, Orthodox 2025-04-20, gap 0 days
# 2026: Western 2026-04-05, Orthodox 2026-04-19, gap 14 days
# 2027: Western 2027-03-28, Orthodox 2027-05-02, gap 35 days
```

Many other Christian holidays are defined relative to Easter: Ash Wednesday is 46 days before, Good Friday is 2 days before, Ascension is 39 days after, and Pentecost is 49 days after. Once you have the Easter date, all of these follow by simple arithmetic.

## Fixed vs Moveable Holidays

Most public holidays follow one of two simple patterns:

**Fixed-date holidays** fall on the same calendar date every year: Christmas (December 25), Independence Day (July 4), New Year's Day (January 1). When these fall on a weekend, many countries observe them on the nearest weekday.

**Nth-weekday holidays** are defined as a specific weekday occurrence within a month: Martin Luther King Jr. Day (3rd Monday of January), Thanksgiving (4th Thursday of November in the US, 2nd Monday of October in Canada), Labor Day (1st Monday of September).

```python
from holidayfyi import nth_weekday_of_month, next_occurrence

# Nth-weekday pattern: weekday 0=Monday, 1=Tuesday, ..., 6=Sunday
# MLK Day: 3rd Monday of January
nth_weekday_of_month(2026, 1, 0, 3)    # date(2026, 1, 19)

# Thanksgiving US: 4th Thursday of November
nth_weekday_of_month(2026, 11, 3, 4)   # date(2026, 11, 26)

# Thanksgiving Canada: 2nd Monday of October
nth_weekday_of_month(2026, 10, 0, 2)   # date(2026, 10, 12)

# Fixed-date: next July 4th
next_occurrence(7, 4, from_date=date(2026, 1, 1))  # date(2026, 7, 4)
```

Easter and its dependent holidays are the notable exceptions -- they are moveable but follow the lunar-solar Computus algorithm rather than a simple weekday rule.

## Country Holidays (optional)

```python
# Requires: pip install "holidayfyi[holidays]"
from holidayfyi import get_upcoming_holidays, holidays_on_date
from datetime import date

# Upcoming US holidays
get_upcoming_holidays("US", n=5)
# [{"name": "...", "date": "2026-...", "is_public": True}, ...]

# What holidays are on Dec 25 across countries?
holidays_on_date(date(2026, 12, 25), ["US", "KR", "JP"])
# {"US": ["Christmas Day"], "KR": ["Christmas Day"], ...}
```

## Command-Line Interface

```bash
pip install "holidayfyi[cli]"

holidayfyi easter 2026
holidayfyi easter 2026 --orthodox
holidayfyi upcoming US --count 5
holidayfyi on-date 2026-12-25 US KR JP
holidayfyi nth-weekday 2026 1 0 3
```

## MCP Server (Claude, Cursor, Windsurf)

Add holiday tools to any AI assistant that supports [Model Context Protocol](https://modelcontextprotocol.io/).

```bash
pip install "holidayfyi[mcp]"
```

Add to your `claude_desktop_config.json`:

```json
{
    "mcpServers": {
        "holidayfyi": {
            "command": "python",
            "args": ["-m", "holidayfyi.mcp_server"]
        }
    }
}
```

**Available tools**: `upcoming_holidays`, `check_holidays_on_date`, `easter_date`, `nth_weekday`, `count_days_until`

## REST API Client

```python
pip install "holidayfyi[api]"
```

```python
from holidayfyi.api import HolidayFYI

with HolidayFYI() as client:
    result = client.holidays("US")
```

Full [API documentation](https://holidayfyi.com/developers/) at holidayfyi.com.

## API Reference

### Easter Dates

| Function | Description |
|----------|-------------|
| `easter_western(year) -> date` | Western (Gregorian) Easter date |
| `easter_orthodox(year) -> date` | Orthodox Easter date (Gregorian calendar) |

### Date Utilities

| Function | Description |
|----------|-------------|
| `nth_weekday_of_month(year, month, weekday, n) -> date` | Find nth weekday (e.g., 3rd Monday) |
| `days_until(target, from_date) -> int` | Count days until a target date |
| `next_occurrence(month, day, from_date) -> date` | Next occurrence of a fixed month/day |

### Weekend & Weekday

| Function | Description |
|----------|-------------|
| `is_weekend(d) -> bool` | Check if a date is Saturday or Sunday |
| `get_weekday_name(d) -> str` | English name of the day of the week |

### Country Holidays (requires `[holidays]`)

| Function | Description |
|----------|-------------|
| `get_upcoming_holidays(country, n) -> list[dict]` | Next n public holidays for a country |
| `holidays_on_date(d, countries) -> dict` | Check what holidays fall on a date across countries |

## Features

- **Easter dates** -- Western (Gregorian) and Orthodox Easter calculation
- **Nth weekday** -- find 1st Monday, 3rd Thursday, last Friday of any month
- **Days until** -- count days to any target date
- **Next occurrence** -- next occurrence of a fixed month/day
- **Weekend check** -- is a date Saturday or Sunday
- **Weekday name** -- English name of the day of the week
- **Upcoming holidays** -- next n public holidays for any country (requires `[holidays]`)
- **Holidays on date** -- check what holidays fall on a date across countries (requires `[holidays]`)
- **CLI** -- Rich terminal output with holiday tables
- **MCP server** -- 5 tools for AI assistants (Claude, Cursor, Windsurf)
- **REST API client** -- httpx-based client for [holidayfyi.com API](https://holidayfyi.com/developers/)
- **Zero dependencies** -- core engine uses only `datetime` from stdlib
- **Type-safe** -- full type annotations, `py.typed` marker (PEP 561)

## Learn More About Holidays

- **Browse**: [Holiday Calendar](https://holidayfyi.com/) · [Countries](https://holidayfyi.com/country/) · [Today's Holidays](https://holidayfyi.com/today/)
- **Tools**: [Date Calculator](https://holidayfyi.com/tools/date-calculator/) · [Easter Calculator](https://holidayfyi.com/tools/easter/)
- **Guides**: [Glossary](https://holidayfyi.com/glossary/) · [Blog](https://holidayfyi.com/blog/)
- **API**: [REST API Docs](https://holidayfyi.com/developers/) · [OpenAPI Spec](https://holidayfyi.com/api/openapi.json)

## FYIPedia Developer Tools

Part of the [FYIPedia](https://fyipedia.com) open-source developer tools ecosystem.

| Package | PyPI | npm | Description |
|---------|------|-----|-------------|
| colorfyi | [PyPI](https://pypi.org/project/colorfyi/) | [npm](https://www.npmjs.com/package/@fyipedia/colorfyi) | Color conversion, WCAG contrast, harmonies -- [colorfyi.com](https://colorfyi.com/) |
| emojifyi | [PyPI](https://pypi.org/project/emojifyi/) | [npm](https://www.npmjs.com/package/emojifyi) | Emoji encoding & metadata for 3,781 emojis -- [emojifyi.com](https://emojifyi.com/) |
| symbolfyi | [PyPI](https://pypi.org/project/symbolfyi/) | [npm](https://www.npmjs.com/package/symbolfyi) | Symbol encoding in 11 formats -- [symbolfyi.com](https://symbolfyi.com/) |
| unicodefyi | [PyPI](https://pypi.org/project/unicodefyi/) | [npm](https://www.npmjs.com/package/unicodefyi) | Unicode lookup with 17 encodings -- [unicodefyi.com](https://unicodefyi.com/) |
| fontfyi | [PyPI](https://pypi.org/project/fontfyi/) | [npm](https://www.npmjs.com/package/fontfyi) | Google Fonts metadata & CSS -- [fontfyi.com](https://fontfyi.com/) |
| distancefyi | [PyPI](https://pypi.org/project/distancefyi/) | [npm](https://www.npmjs.com/package/distancefyi) | Haversine distance & travel times -- [distancefyi.com](https://distancefyi.com/) |
| timefyi | [PyPI](https://pypi.org/project/timefyi/) | [npm](https://www.npmjs.com/package/timefyi) | Timezone ops & business hours -- [timefyi.com](https://timefyi.com/) |
| namefyi | [PyPI](https://pypi.org/project/namefyi/) | [npm](https://www.npmjs.com/package/namefyi) | Korean romanization & Five Elements -- [namefyi.com](https://namefyi.com/) |
| unitfyi | [PyPI](https://pypi.org/project/unitfyi/) | [npm](https://www.npmjs.com/package/unitfyi) | Unit conversion, 220 units -- [unitfyi.com](https://unitfyi.com/) |
| **holidayfyi** | [PyPI](https://pypi.org/project/holidayfyi/) | [npm](https://www.npmjs.com/package/holidayfyi) | Holiday dates & Easter calculation -- [holidayfyi.com](https://holidayfyi.com/) |
| cocktailfyi | [PyPI](https://pypi.org/project/cocktailfyi/) | -- | Cocktail ABV, calories, flavor -- [cocktailfyi.com](https://cocktailfyi.com/) |
| fyipedia | [PyPI](https://pypi.org/project/fyipedia/) | -- | Unified CLI: `fyi color info FF6B35` -- [fyipedia.com](https://fyipedia.com/) |
| fyipedia-mcp | [PyPI](https://pypi.org/project/fyipedia-mcp/) | -- | Unified MCP hub for AI assistants -- [fyipedia.com](https://fyipedia.com/) |

## License

MIT
