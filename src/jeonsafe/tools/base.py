"""Shared API helper functions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests


@dataclass(frozen=True)
class ApiResponse:
    url: str
    params: dict[str, Any]
    status_code: int
    text: str


class ApiNotConfiguredError(RuntimeError):
    """Raised when a connector is used without a required API key."""


def get_text(url: str, params: dict[str, Any], timeout: int = 20) -> ApiResponse:
    response = requests.get(url, params=params, timeout=timeout)
    response.raise_for_status()
    return ApiResponse(
        url=response.url,
        params=params,
        status_code=response.status_code,
        text=response.text,
    )

