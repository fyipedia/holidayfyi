# holidayfyi

Pure Python holiday engine — Easter dates, public holidays, nth weekday finder. Zero dependencies core.

## Install

```bash
pip install holidayfyi              # Core (zero deps)
pip install "holidayfyi[holidays]"  # + python-holidays integration
pip install "holidayfyi[cli]"       # + CLI (typer, rich)
pip install "holidayfyi[mcp]"       # + MCP server
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

### With python-holidays (optional)

```python
from holidayfyi import get_upcoming_holidays, holidays_on_date
from datetime import date

# Upcoming US holidays
get_upcoming_holidays("US", n=5)
# [{"name": "...", "date": "2026-...", "is_public": True}, ...]

# What holidays are on Dec 25 across countries?
holidays_on_date(date(2026, 12, 25), ["US", "KR", "JP"])
# {"US": ["Christmas Day"], "KR": ["Christmas Day"], ...}
```

## Features

- **Easter dates** — Western (Gregorian) and Orthodox Easter calculation
- **Nth weekday** — find 1st Monday, 3rd Thursday, last Friday of any month
- **Days until** — count days to any target date
- **Next occurrence** — next occurrence of a fixed month/day
- **Weekend check** — is a date Saturday or Sunday
- **Weekday name** — English name of the day of the week
- **Upcoming holidays** — next n public holidays for any country (requires `[holidays]`)
- **Holidays on date** — check what holidays fall on a date across countries (requires `[holidays]`)

## CLI

```bash
holidayfyi easter 2026
holidayfyi easter 2026 --orthodox
holidayfyi upcoming US --count 5
holidayfyi on-date 2026-12-25 US KR JP
holidayfyi nth-weekday 2026 1 0 3
```

## MCP Server

Add to your Claude Desktop config:

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

Tools: `upcoming_holidays`, `check_holidays_on_date`, `easter_date`, `nth_weekday`, `count_days_until`

## API Client

```python
from holidayfyi.api import HolidayFYI

with HolidayFYI() as client:
    result = client.holidays("US")
```

## License

MIT
