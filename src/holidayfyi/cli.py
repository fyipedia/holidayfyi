"""Command-line interface for holidayfyi.

Requires: pip install holidayfyi[cli]

Usage::

    holidayfyi upcoming US
    holidayfyi easter 2026
    holidayfyi easter 2026 --orthodox
    holidayfyi on-date 2026-12-25 US KR JP
    holidayfyi nth-weekday 2026 1 0 3
"""

from __future__ import annotations

from datetime import date

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    name="holidayfyi",
    help="Holiday calculations and lookups.",
    no_args_is_help=True,
)
console = Console()


@app.command()
def upcoming(
    country: str = typer.Argument(help="ISO 3166-1 alpha-2 country code (e.g., US, KR)"),
    n: int = typer.Option(10, "--count", "-n", help="Number of holidays to show"),
) -> None:
    """Show upcoming holidays for a country (requires [holidays])."""
    from holidayfyi import get_upcoming_holidays

    holidays = get_upcoming_holidays(country.upper(), n=n)
    if not holidays:
        console.print(f"[yellow]No holidays found for country: {country}[/]")
        raise typer.Exit(1)

    table = Table(title=f"Upcoming Holidays — {country.upper()}")
    table.add_column("Date", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Public", style="yellow")

    for h in holidays:
        table.add_row(
            str(h["date"]),
            str(h["name"]),
            "Yes" if h["is_public"] else "No",
        )

    console.print(table)


@app.command()
def easter(
    year: int = typer.Argument(help="Calendar year"),
    orthodox: bool = typer.Option(False, "--orthodox", help="Calculate Orthodox Easter instead"),
) -> None:
    """Calculate Easter date for a given year."""
    from holidayfyi import easter_orthodox, easter_western

    if orthodox:
        d = easter_orthodox(year)
        label = "Orthodox Easter"
    else:
        d = easter_western(year)
        label = "Western Easter"

    console.print(f"[cyan]{label} {year}:[/] [green]{d.isoformat()}[/]")


@app.command("on-date")
def on_date_cmd(
    date_str: str = typer.Argument(help="Date in ISO format (YYYY-MM-DD)"),
    countries: list[str] = typer.Argument(help="Country codes (e.g., US KR JP)"),
) -> None:
    """Show holidays on a specific date across countries (requires [holidays])."""
    from holidayfyi import holidays_on_date

    target = date.fromisoformat(date_str)
    upper_countries = [c.upper() for c in countries]
    result = holidays_on_date(target, upper_countries)

    if not result:
        joined = ", ".join(upper_countries)
        console.print(f"[yellow]No holidays found on {date_str} for: {joined}[/]")
        raise typer.Exit(1)

    table = Table(title=f"Holidays on {date_str}")
    table.add_column("Country", style="cyan")
    table.add_column("Holidays", style="green")

    for code, names in sorted(result.items()):
        table.add_row(code, ", ".join(names))

    console.print(table)


@app.command("nth-weekday")
def nth_weekday_cmd(
    year: int = typer.Argument(help="Calendar year"),
    month: int = typer.Argument(help="Month (1-12)"),
    weekday: int = typer.Argument(help="Day of week (0=Monday, 6=Sunday)"),
    n: int = typer.Argument(help="Occurrence (1=first, 2=second, -1=last)"),
) -> None:
    """Find nth occurrence of a weekday in a month."""
    from holidayfyi import nth_weekday_of_month

    try:
        d = nth_weekday_of_month(year, month, weekday, n)
    except ValueError as e:
        console.print(f"[red]{e}[/]")
        raise typer.Exit(1) from None

    console.print(f"[cyan]Result:[/] [green]{d.isoformat()}[/]")
