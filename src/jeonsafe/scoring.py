"""Score aggregation utilities for JeonSAFE."""

from __future__ import annotations

import pandas as pd


STRUCTURAL_SCORE_COLUMNS = [
    "전세가율_점수",
    "거래건수_점수",
    "신규계약_점수",
    "소형주택_점수",
    "근저당권_점수",
]

INCIDENT_SCORE_COLUMNS = [
    "임차권_점수",
    "보증사고_점수",
    "강제경매_점수",
    "사고율_점수",
]


def add_total_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Add structural, incident, and total risk scores.

    Missing score columns are treated as zero so the function can be reused
    with partial datasets during dashboard prototyping.
    """

    out = df.copy()

    for col in STRUCTURAL_SCORE_COLUMNS + INCIDENT_SCORE_COLUMNS:
        if col not in out.columns:
            out[col] = 0
        out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0)

    out["구조적위험총점"] = out[STRUCTURAL_SCORE_COLUMNS].sum(axis=1)
    out["발생경보총점"] = out[INCIDENT_SCORE_COLUMNS].sum(axis=1)
    out["종합총점"] = out["구조적위험총점"] + out["발생경보총점"]

    return out

