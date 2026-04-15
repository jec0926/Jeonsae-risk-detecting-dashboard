"""HUG guarantee accident API connector.

The endpoint currently used by the portfolio is the HUG 분양보증사고현황
API. The public service appears to provide region-level accident status, and
the available granularity should be checked after key issuance.
"""

from __future__ import annotations

from typing import Any

from jeonsafe.config import get_api_config

from .base import ApiNotConfiguredError, ApiResponse, get_text


class HugGuaranteeAccidentApiTool:
    """Thin REST connector for HUG guarantee accident status."""

    DEFAULT_URL = "https://www.khug.or.kr/accidentDistributionGuaranteeStatus.do"

    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:
        config = get_api_config()
        self.api_key = api_key or config.hug_guarantee_accident_api_key
        self.key_param = config.hug_guarantee_accident_key_param
        self.base_url = base_url or self.DEFAULT_URL

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def build_params(self, **params: Any) -> dict[str, Any]:
        if not self.api_key:
            raise ApiNotConfiguredError("HUG_GUARANTEE_ACCIDENT_API_KEY is not configured.")

        # HUG parameter names can differ by issued Open API specification.
        # Configure HUG_GUARANTEE_ACCIDENT_KEY_PARAM after checking the guide.
        return {self.key_param: self.api_key, **params}

    def fetch(self, **params: Any) -> ApiResponse:
        return get_text(self.base_url, self.build_params(**params))
