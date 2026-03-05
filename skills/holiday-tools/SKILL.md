---
name: holiday-tools
description: Calculate Easter dates, find upcoming holidays, check holidays on specific dates.
---

# Holiday Tools

Holiday date calculations powered by [holidayfyi](https://holidayfyi.com/) -- a pure Python holiday engine with zero dependencies.

## Setup

Install the MCP server:

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

## Available Tools

| Tool | Description |
|------|-------------|
| `upcoming_holidays` | Find upcoming holidays for a country |
| `check_holidays_on_date` | Check if a specific date has any holidays |
| `easter_date` | Calculate Easter Sunday for any year (Western and Orthodox) |
| `nth_weekday` | Find the nth occurrence of a weekday in a month (e.g., 3rd Monday) |
| `count_days_until` | Count the number of days until a specific holiday |

## When to Use

- Finding upcoming public holidays in any country
- Checking if a date falls on a holiday before scheduling
- Calculating Easter and other moveable feast dates
- Finding specific weekday occurrences (like Thanksgiving)
- Counting days until the next holiday

## Demo

![HolidayFYI CLI Demo](https://raw.githubusercontent.com/fyipedia/holidayfyi/main/demo.gif)

## Links

- [Holiday Calendar](https://holidayfyi.com/) -- Holidays for every country
- [API Documentation](https://holidayfyi.com/developers/) -- Free REST API
- [PyPI Package](https://pypi.org/project/holidayfyi/)
