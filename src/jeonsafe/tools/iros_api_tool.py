"""IROS registration API connector.

This module provides configured connectors for:
- 근저당권 설정 등기 현황: Open API id 0000000070
- 임차권등기 설정 등기 현황: Open API id 0000000078

The project uses building-level search where supported by the issued service
specification. Exact parameter names can vary by the IROS API guide, so the
fetch method accepts arbitrary keyword parameters and injects the configured
API key.
"""

from __future__ import annotations

from typing import Any, Literal

from jeonsafe.config import get_api_config

from .base import ApiNotConfiguredError, ApiResponse, get_text


RegistrationApiKind = Literal["mortgage", "lease_right"]


class IrosRegistrationApiTool:
    """Thin REST connector for IROS registration-count Open APIs."""

    BASE_URL = "https://data.iros.go.kr/openapi/cr/rs/selectCrRsRgsCsOpenApi.rest"
    API_IDS = {
        "mortgage": "0000000070",
        "lease_right": "0000000078",
    }

    def __init__(self, kind: RegistrationApiKind, api_key: str | None = None) -> None:
        if kind not in self.API_IDS:
            raise ValueError(f"Unsupported IROS API kind: {kind}")

        config = get_api_config()
        default_key = {
            "mortgage": config.iros_mortgage_api_key,
            "lease_right": config.iros_lease_right_api_key,
        }[kind]
        self.kind = kind
        self.api_key = api_key or default_key
        self.api_id = self.API_IDS[kind]

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def build_params(self, **params: Any) -> dict[str, Any]:
        if not self.api_key:
            env_name = "IROS_MORTGAGE_API_KEY" if self.kind == "mortgage" else "IROS_LEASE_RIGHT_API_KEY"
            raise ApiNotConfiguredError(f"{env_name} is not configured.")

        # id is part of the documented endpoint. The key parameter name should
        # be adjusted if the issued API guide specifies a different name.
        return {
            "id": self.api_id,
            "key": self.api_key,
            **params,
        }

    def fetch(self, **params: Any) -> ApiResponse:
        return get_text(self.BASE_URL, self.build_params(**params))

