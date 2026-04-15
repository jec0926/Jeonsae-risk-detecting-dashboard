"""Alert logic utilities for JeonSAFE."""

from __future__ import annotations

import numpy as np
import pandas as pd


COUNT_RULE = {"mom_pct": 50.0, "avg_ratio": 1.5, "rank_top_pct": 0.10}
RATIO_RULE = {"mom_pp": 5.0, "avg_ratio": 1.2, "rank_top_pct": 0.10}
ROLLING_AVG = 24
HARD_MIN = 30

RATIO_COLUMNS = ["전세가율", "신규계약비율", "소형주택비중_60이하"]
COUNT_COLUMNS = ["거래건수", "근저당_건수", "임차권_건수", "보증사고_건수"]
STRUCTURAL_COLUMNS = ["거래건수", "근저당_건수", "신규계약비율", "소형주택비중_60이하", "전세가율"]


def _safe_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def add_alert_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add lightweight Warning/Critical alerts to a monthly regional dataset."""

    out = df.copy()
    if "위험알림" in out.columns:
        out["_original_risk_alert"] = out["위험알림"]
    if "사고알림" in out.columns:
        out["_original_incident_alert"] = out["사고알림"]

    out["계약년월"] = out["계약년월"].astype(str).str.replace(r"\D", "", regex=True).str.zfill(6)
    out = out.sort_values(["시도", "시군구", "법정동", "계약년월"]).reset_index(drop=True)

    group_keys = ["시도", "시군구", "법정동"]
    groups = out.groupby(group_keys, sort=False)

    for col in RATIO_COLUMNS + COUNT_COLUMNS:
        if col not in out.columns:
            continue
        values = _safe_numeric(out[col])
        prev = groups[col].shift(1)
        rolling_base = groups[col].shift(1).rolling(ROLLING_AVG, min_periods=6).mean()

        if col in RATIO_COLUMNS:
            out[f"{col}_전월증감"] = values - prev
        else:
            out[f"{col}_전월증감"] = np.where(prev > 0, (values / prev - 1) * 100, np.nan)

        out[f"{col}_24m배수"] = np.where(rolling_base > 0, values / rolling_base, np.nan)

    def is_hit(row: pd.Series, col: str) -> bool:
        if row.get("거래건수", 0) < HARD_MIN:
            return False

        mom = row.get(f"{col}_전월증감")
        avg_multiple = row.get(f"{col}_24m배수")

        if col in RATIO_COLUMNS:
            return (
                pd.notna(mom)
                and mom >= RATIO_RULE["mom_pp"]
            ) or (
                pd.notna(avg_multiple)
                and avg_multiple >= RATIO_RULE["avg_ratio"]
            )

        return (
            pd.notna(mom)
            and mom >= COUNT_RULE["mom_pct"]
        ) or (
            pd.notna(avg_multiple)
            and avg_multiple >= COUNT_RULE["avg_ratio"]
        )

    def alert_level(row: pd.Series) -> str:
        hits = {col: is_hit(row, col) for col in STRUCTURAL_COLUMNS if col in out.columns}
        if hits.get("거래건수", False) and hits.get("근저당_건수", False):
            return "Critical"
        hit_count = sum(hits.values())
        if hit_count >= 3:
            return "Critical"
        if hit_count >= 1:
            return "Warning"
        return "None"

    out["위험알림"] = out.apply(alert_level, axis=1)
    if "_original_risk_alert" in out.columns:
        original_risk_alert = out["_original_risk_alert"]
        has_existing = original_risk_alert.notna() & (original_risk_alert.astype(str) != "None")
        out.loc[has_existing & (out["위험알림"] == "None"), "위험알림"] = original_risk_alert[has_existing]
        out = out.drop(columns=["_original_risk_alert"])

    out["사고발생"] = _safe_numeric(out.get("임차권_건수", 0)).fillna(0) + _safe_numeric(out.get("보증사고_건수", 0)).fillna(0)
    out["사고알림"] = np.where(out["사고발생"] >= HARD_MIN, "Incident", "None")
    if "_original_incident_alert" in out.columns:
        original_incident_alert = out["_original_incident_alert"]
        has_existing = original_incident_alert.notna() & (original_incident_alert.astype(str) != "None")
        out.loc[has_existing & (out["사고알림"] == "None"), "사고알림"] = original_incident_alert[has_existing]
        out = out.drop(columns=["_original_incident_alert"])

    return out
