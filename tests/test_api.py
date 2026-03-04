"""Tests for the holidayfyi API client."""

from holidayfyi.api import HolidayFYI


def test_client_init() -> None:
    """Client initializes with default URL."""
    client = HolidayFYI()
    assert str(client._client.base_url).rstrip("/") == "https://holidayfyi.com/api"
    client.close()


def test_client_custom_url() -> None:
    """Client accepts custom base URL."""
    client = HolidayFYI(base_url="https://custom.example.com/api")
    assert str(client._client.base_url).rstrip("/") == "https://custom.example.com/api"
    client.close()


def test_client_context_manager() -> None:
    """Client works as context manager."""
    with HolidayFYI() as client:
        assert client._client is not None
