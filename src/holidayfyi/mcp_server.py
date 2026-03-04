"""MCP server for holidayfyi — holiday tools for AI assistants.

Requires: pip install holidayfyi[mcp]

Configure in claude_desktop_config.json::

    {
        "mcpServers": {
            "holidayfyi": {
                "command": "python",
                "args": ["-m", "holidayfyi.mcp_server"]
            }
        }
    }
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("holidayfyi")


@mcp.tool()
def upcoming_holidays(country_iso: str, n: int = 10) -> str:
    """Get the next upcoming public holidays for a country.

    Requires python-holidays: pip install holidayfyi[holidays]

    Args:
        country_iso: ISO 3166-1 alpha-2 country code (e.g., "US", "KR", "JP").
        n: Number of upcoming holidays to return (default 10).
    """
    from holidayfyi import get_upcoming_holidays

    holidays = get_upcoming_holidays(country_iso.upper(), n=n)
    if not holidays:
        return f"No holidays found for country: {country_iso}"

    lines = [
        f"## Upcoming Holidays — {country_iso.upper()}",
        "",
        "| Date | Name | Public |",
        "|------|------|--------|",
    ]
    for h in holidays:
        public = "Yes" if h["is_public"] else "No"
        lines.append(f"| {h['date']} | {h['name']} | {public} |")

    return "\n".join(lines)


@mcp.tool()
def check_holidays_on_date(date_str: str, countries: str) -> str:
    """Find which holidays fall on a given date across multiple countries.

    Requires python-holidays: pip install holidayfyi[holidays]

    Args:
        date_str: Date in ISO format (e.g., "2026-12-25").
        countries: Comma-separated ISO country codes (e.g., "US,KR,JP").
    """
    from datetime import date

    from holidayfyi import holidays_on_date

    target = date.fromisoformat(date_str)
    country_list = [c.strip().upper() for c in countries.split(",")]
    result = holidays_on_date(target, country_list)

    if not result:
        return f"No holidays found on {date_str} for: {', '.join(country_list)}"

    lines = [
        f"## Holidays on {date_str}",
        "",
        "| Country | Holidays |",
        "|---------|----------|",
    ]
    for code, names in sorted(result.items()):
        lines.append(f"| {code} | {', '.join(names)} |")

    return "\n".join(lines)


@mcp.tool()
def easter_date(year: int, orthodox: bool = False) -> str:
    """Calculate Easter date for a given year.

    Args:
        year: Calendar year (e.g., 2026).
        orthodox: If True, calculate Orthodox Easter; otherwise Western Easter.
    """
    from holidayfyi import easter_orthodox, easter_western

    if orthodox:
        d = easter_orthodox(year)
        label = "Orthodox Easter"
    else:
        d = easter_western(year)
        label = "Western Easter"

    return f"{label} {year}: {d.isoformat()}"


@mcp.tool()
def nth_weekday(year: int, month: int, weekday: int, n: int) -> str:
    """Find the nth occurrence of a weekday in a given month.

    Args:
        year: Calendar year.
        month: Month (1-12).
        weekday: Day of week (0=Monday, 1=Tuesday, ..., 6=Sunday).
        n: Occurrence number (1=first, 2=second, -1=last).
    """
    from holidayfyi import nth_weekday_of_month

    try:
        d = nth_weekday_of_month(year, month, weekday, n)
    except ValueError as e:
        return f"Error: {e}"

    import calendar

    weekday_name = calendar.day_name[weekday]
    month_name = calendar.month_name[month]
    suffix = {1: "st", 2: "nd", 3: "rd"}.get(n if n > 0 else 0, "th")
    occurrence = "last" if n == -1 else f"{n}{suffix}"

    return f"The {occurrence} {weekday_name} of {month_name} {year}: {d.isoformat()}"


@mcp.tool()
def count_days_until(target_date_str: str, from_date_str: str = "") -> str:
    """Count the number of days until a target date.

    Args:
        target_date_str: Target date in ISO format (e.g., "2026-12-25").
        from_date_str: Starting date in ISO format (defaults to today).
    """
    from datetime import date

    from holidayfyi import days_until

    target = date.fromisoformat(target_date_str)
    from_d = date.fromisoformat(from_date_str) if from_date_str else None
    days = days_until(target, from_d)

    if days > 0:
        return f"{days} days until {target_date_str}"
    elif days == 0:
        return f"{target_date_str} is today!"
    else:
        return f"{target_date_str} was {abs(days)} days ago"


def main() -> None:
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
