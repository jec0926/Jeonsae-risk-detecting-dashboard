"""Runtime configuration for JeonSAFE.

Secrets are read from environment variables only. Do not hardcode issued
service keys in source files.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None


if load_dotenv:
    load_dotenv()


@dataclass(frozen=True)
class ApiConfig:
    hug_guarantee_accident_api_key: str | None = os.getenv("HUG_GUARANTEE_ACCIDENT_API_KEY")
    hug_guarantee_accident_key_param: str = os.getenv("HUG_GUARANTEE_ACCIDENT_KEY_PARAM", "serviceKey")
    iros_mortgage_api_key: str | None = os.getenv("IROS_MORTGAGE_API_KEY")
    iros_lease_right_api_key: str | None = os.getenv("IROS_LEASE_RIGHT_API_KEY")

    @property
    def hug_enabled(self) -> bool:
        return bool(self.hug_guarantee_accident_api_key)

    @property
    def iros_mortgage_enabled(self) -> bool:
        return bool(self.iros_mortgage_api_key)

    @property
    def iros_lease_right_enabled(self) -> bool:
        return bool(self.iros_lease_right_api_key)

def get_api_config() -> ApiConfig:
    return ApiConfig()
