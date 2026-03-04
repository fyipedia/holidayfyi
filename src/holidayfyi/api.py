"""HTTP API client for holidayfyi.com REST endpoints.

Requires: pip install holidayfyi[api]

Usage::

    from holidayfyi.api import HolidayFYI

    with HolidayFYI() as client:
        result = client.holidays("US")
        print(result)
"""

from __future__ import annotations

from typing import Any

import httpx


class HolidayFYI:
    """API client for the holidayfyi.com REST API."""

    def __init__(
        self,
        base_url: str = "https://holidayfyi.com/api",
        timeout: float = 10.0,
    ) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def _get(self, path: str, **params: Any) -> dict[str, Any]:
        resp = self._client.get(path, params={k: v for k, v in params.items() if v is not None})
        resp.raise_for_status()
        result: dict[str, Any] = resp.json()
        return result

    def holidays(self, country_code: str) -> dict[str, Any]:
        """Get holidays for a country.

        Args:
            country_code: ISO 3166-1 alpha-2 country code (e.g., "US", "KR").

        Returns:
            Dict with holiday data for the country.
        """
        return self._get(f"/holidays/{country_code}/")

    def upcoming(self, country_code: str, n: int = 10) -> dict[str, Any]:
        """Get upcoming holidays for a country.

        Args:
            country_code: ISO 3166-1 alpha-2 country code.
            n: Number of upcoming holidays to return.

        Returns:
            Dict with upcoming holidays list.
        """
        return self._get(f"/holidays/{country_code}/upcoming/", n=n)

    def on_date(self, date_str: str, countries: list[str] | None = None) -> dict[str, Any]:
        """Get holidays on a specific date across countries.

        Args:
            date_str: Date in ISO format (e.g., "2026-12-25").
            countries: Optional list of country codes to check.

        Returns:
            Dict mapping country codes to holiday names.
        """
        params: dict[str, Any] = {}
        if countries:
            params["countries"] = ",".join(countries)
        return self._get(f"/holidays/on-date/{date_str}/", **params)

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> HolidayFYI:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
