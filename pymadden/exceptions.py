"""Exception hierarchy for pymadden."""

from __future__ import annotations


class PyMaddenError(Exception):
    """Base exception for all pymadden errors."""


class MaddenAPIError(PyMaddenError):
    """The EA ratings API returned an error response."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class MaddenRateLimitError(MaddenAPIError):
    """The EA ratings API rate-limited the request (HTTP 429)."""

    def __init__(self, message: str = "Rate limited by the EA ratings API"):
        super().__init__(message, status_code=429)


class MaddenConnectionError(PyMaddenError):
    """A network-level error occurred while contacting the EA ratings API."""


class MaddenValidationError(PyMaddenError):
    """The API response could not be parsed into the expected models."""
