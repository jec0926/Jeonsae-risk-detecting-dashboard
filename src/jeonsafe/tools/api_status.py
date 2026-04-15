"""API configuration status helpers."""

from __future__ import annotations

from jeonsafe.config import get_api_config


def get_api_status() -> dict[str, str]:
    config = get_api_config()
    return {
        "HUG guarantee accident API": "configured" if config.hug_enabled else "not configured",
        "IROS mortgage registration API": "configured" if config.iros_mortgage_enabled else "not configured",
        "IROS lease-right registration API": "configured" if config.iros_lease_right_enabled else "not configured",
        "Local dashboard cache": "active",
    }
