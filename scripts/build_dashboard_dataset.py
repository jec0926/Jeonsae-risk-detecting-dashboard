from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parents[1]
SOURCE = PROJECT_ROOT / "DAB" / "Data" / "Result" / "risk_parts" / "이상치 탐지 결과(법정동 병합).csv"
TARGET = ROOT / "data" / "jeonsafe_dashboard.csv.gz"

DASHBOARD_COLUMNS = [
    "계약년월",
    "시도",
    "시군구",
    "법정동",
    "위험알림",
    "사고알림",
    "사고집계범위",
    "사고발생",
    "임차권등기",
    "보증사고",
    "구조적위험점수",
    "발생경보점수",
    "종합점수",
    "요약설명",
    "사후검증",
    "임차권_건수",
    "보증사고_건수",
    "레벨",
    "거래건수",
    "근저당_건수",
    "신규계약비율",
    "소형주택비중_60이하",
    "전세가율",
    "구조적위험총점",
    "발생경보총점",
    "종합총점",
    "신규계약비율_전월증감(단위%p)",
    "신규계약비율_24m배수",
    "소형주택비중_60이하_전월증감(단위%p)",
    "소형주택비중_60이하_24m배수",
    "전세가율_전월증감(단위%p)",
    "전세가율_24m배수",
    "거래건수_전월증감(%)",
    "거래건수_24m배수",
    "근저당_건수_전월증감(%)",
    "근저당_건수_24m배수",
    "임차권_건수_전월증감(%)",
    "임차권_건수_24m배수",
    "보증사고_건수_전월증감(%)",
    "보증사고_건수_24m배수",
    "사고발생_전월증감(%)",
    "사고발생_24m배수",
    "거래건수_순위(상위%)",
    "근저당_건수_순위(상위%)",
    "신규계약비율_순위(상위%)",
    "소형주택비중_60이하_순위(상위%)",
    "전세가율_순위(상위%)",
    "사고발생_순위(상위%)",
    "_gate_skip",
    "_acc_gate_skip",
]


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Source result file not found: {SOURCE}")

    header = pd.read_csv(SOURCE, nrows=0).columns
    usecols = [col for col in DASHBOARD_COLUMNS if col in header]
    df = pd.read_csv(SOURCE, usecols=usecols)

    for col in ["시도", "시군구", "법정동"]:
        if col in df.columns:
            df[col] = df[col].fillna("(전체)").astype(str).str.strip()

    if "계약년월" in df.columns:
        df["계약년월"] = (
            df["계약년월"].astype(str)
            .str.replace(r"\D", "", regex=True)
            .str.zfill(6)
        )

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(TARGET, index=False, encoding="utf-8-sig", compression="gzip")
    print(f"saved: {TARGET}")
    print(f"rows={len(df):,}, cols={len(df.columns):,}")


if __name__ == "__main__":
    main()

