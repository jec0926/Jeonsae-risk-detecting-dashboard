from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parents[1] if len(ROOT.parents) >= 2 else ROOT
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.append(str(SRC))

from jeonsafe import add_alert_columns  # noqa: E402


st.set_page_config(
    page_title="전 SAFE | 지역 전세사기 리스크 대시보드",
    page_icon="!",
    layout="wide",
)


CSS = """
<style>
:root {
  --safe-red: #d83a34;
  --safe-orange: #f2a541;
  --safe-teal: #0f8b8d;
  --safe-ink: #202124;
  --safe-muted: #667085;
  --safe-line: #d9dee7;
  --safe-bg: #f6f8fb;
}

.stApp {
  background: var(--safe-bg);
  color: var(--safe-ink);
  font-size: 16px;
}

html, body, [class*="css"] {
  font-size: 16px;
}

[data-testid="stSidebar"] {
  background: #ffffff;
  border-right: 1px solid var(--safe-line);
}

.block-container {
  padding-top: 1.4rem;
  padding-bottom: 3rem;
}

.topbar {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 20px;
  padding: 18px 20px;
  border: 1px solid var(--safe-line);
  border-radius: 8px;
  background: #ffffff;
}

.brand-kicker {
  color: var(--safe-red);
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 0;
  margin-bottom: 6px;
}

.brand-title {
  font-size: 34px;
  line-height: 1.18;
  font-weight: 900;
  margin: 0;
}

.brand-subtitle {
  color: var(--safe-muted);
  font-size: 16px;
  margin-top: 8px;
}

.pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 92px;
  height: 34px;
  padding: 0 14px;
  border-radius: 8px;
  font-weight: 800;
  font-size: 13px;
  border: 1px solid var(--safe-line);
  background: #ffffff;
}

.pill-critical {
  color: #ffffff;
  background: var(--safe-red);
  border-color: var(--safe-red);
}

.pill-warning {
  color: #7a4b00;
  background: #fff1d4;
  border-color: #ffd891;
}

.pill-none {
  color: var(--safe-muted);
  background: #f4f6f8;
}

.metric-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
  margin: 16px 0 10px;
}

.metric-card {
  border: 1px solid var(--safe-line);
  border-radius: 8px;
  background: #ffffff;
  padding: 16px 18px;
  min-height: 112px;
}

.metric-label {
  color: var(--safe-muted);
  font-size: 15px;
  font-weight: 700;
  margin-bottom: 10px;
}

.metric-value {
  color: var(--safe-ink);
  font-size: 34px;
  line-height: 1;
  font-weight: 900;
}

.metric-caption {
  color: var(--safe-muted);
  font-size: 13px;
  margin-top: 10px;
}

.report-box {
  border: 1px solid var(--safe-line);
  border-radius: 8px;
  background: #ffffff;
  padding: 18px 20px;
  margin-top: 12px;
}

.report-title {
  font-size: 20px;
  font-weight: 900;
  margin-bottom: 8px;
}

.report-text {
  color: #344054;
  font-size: 16px;
  line-height: 1.65;
}

.section-note {
  color: var(--safe-muted);
  font-size: 15px;
  margin-top: -4px;
  margin-bottom: 8px;
}

.insight-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
  margin: 10px 0 16px;
}

.insight-card {
  border: 1px solid var(--safe-line);
  border-radius: 8px;
  background: #ffffff;
  padding: 12px 14px;
}

.insight-label {
  color: var(--safe-muted);
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 6px;
}

.insight-value {
  font-size: 26px;
  font-weight: 900;
  color: var(--safe-ink);
}

.insight-help {
  color: var(--safe-muted);
  font-size: 13px;
  margin-top: 4px;
}

[data-testid="stTabs"] button {
  font-size: 16px;
}

[data-testid="stDataFrame"] {
  font-size: 15px;
}

@media (max-width: 900px) {
  .topbar {
    display: block;
  }
  .metric-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .insight-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 560px) {
  .metric-grid {
    grid-template-columns: 1fr;
  }
  .insight-grid {
    grid-template-columns: 1fr;
  }
  .brand-title {
    font-size: 24px;
  }
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


def clean_alert(value: object) -> str:
    if pd.isna(value):
        return "None"
    text = str(value).strip()
    if not text or text.lower() == "nan":
        return "None"
    return text


def alert_class(value: object) -> str:
    text = clean_alert(value)
    if text == "Critical":
        return "pill pill-critical"
    if text == "Warning":
        return "pill pill-warning"
    return "pill pill-none"


def fmt_num(value: object, digits: int = 0, suffix: str = "") -> str:
    if pd.isna(value):
        return "-"
    number = float(value)
    if digits == 0:
        return f"{number:,.0f}{suffix}"
    return f"{number:,.{digits}f}{suffix}"


def fmt_delta(value: object, digits: int = 1, suffix: str = "") -> str:
    if pd.isna(value):
        return "-"
    number = float(value)
    sign = "+" if number > 0 else ""
    return f"{sign}{number:,.{digits}f}{suffix}"


def ensure_month_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Guarantee both raw and display month columns exist."""

    out = df.copy()
    if "계약년월" not in out.columns:
        return out

    out["계약년월"] = (
        out["계약년월"].astype(str)
        .str.replace(r"\D", "", regex=True)
        .str.zfill(6)
    )

    if "기준월" not in out.columns:
        out["기준월"] = pd.to_datetime(out["계약년월"], format="%Y%m", errors="coerce")
    else:
        out["기준월"] = pd.to_datetime(out["기준월"], errors="coerce")

    if "계약년월표시" not in out.columns:
        out["계약년월표시"] = out["기준월"].dt.strftime("%Y-%m")

    out["계약년월표시"] = out["계약년월표시"].fillna(out["계약년월"])
    return out


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = ensure_month_columns(df)

    rename_pairs = {
        "구조적위험점수": "구조적위험총점",
        "발생경보점수": "발생경보총점",
        "종합점수": "종합총점",
    }
    for src, dst in rename_pairs.items():
        if src in out.columns and dst not in out.columns:
            out[dst] = out[src]

    for col in ["위험알림", "사고알림"]:
        if col not in out.columns:
            out[col] = "None"
        out[col] = out[col].apply(clean_alert)

    for col in ["시도", "시군구", "법정동"]:
        out[col] = out[col].fillna("(전체)").astype(str).str.strip()

    numeric_cols = [
        "전세가율",
        "거래건수",
        "근저당_건수",
        "임차권_건수",
        "보증사고_건수",
        "강제경매_건수",
        "사고발생",
        "구조적위험총점",
        "발생경보총점",
        "종합총점",
        "신규계약비율",
        "소형주택비중_60이하",
    ]
    numeric_cols += [c for c in out.columns if "전월증감" in c or "24m배수" in c or "순위(상위%)" in c]
    for col in numeric_cols:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")

    return out


@st.cache_data(show_spinner=False)
def load_data() -> tuple[pd.DataFrame, str]:
    local_result = PROJECT_ROOT / "DAB" / "Data" / "Result" / "risk_parts" / "이상치 탐지 결과(법정동 병합).csv"
    packaged_result = ROOT / "data" / "jeonsafe_dashboard.csv.gz"
    packaged_sample = ROOT / "data" / "sample_risk_result.csv"

    if packaged_result.exists():
        return normalize_columns(pd.read_csv(packaged_result, compression="gzip")), f"packaged result: {packaged_result.name}"
    if local_result.exists():
        return normalize_columns(pd.read_csv(local_result)), f"local result: {local_result.name}"
    return normalize_columns(pd.read_csv(packaged_sample)), f"sample: {packaged_sample.name}"


def render_metric(label: str, value: str, caption: str = "") -> None:
    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-label">{label}</div>
          <div class="metric-value">{value}</div>
          <div class="metric-caption">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_insight(label: str, value: str, help_text: str = "") -> None:
    st.markdown(
        f"""
        <div class="insight-card">
          <div class="insight-label">{label}</div>
          <div class="insight-value">{value}</div>
          <div class="insight-help">{help_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_snapshot(df: pd.DataFrame, metric: str) -> dict[str, object]:
    df = ensure_month_columns(df)
    valid = df[["계약년월표시", metric]].dropna()
    coverage = len(valid) / len(df) if len(df) else 0
    if valid.empty:
        return {"current": None, "previous": None, "delta": None, "month": "-", "coverage": coverage}

    current = valid.iloc[-1]
    previous_value = valid.iloc[-2][metric] if len(valid) >= 2 else None
    delta = current[metric] - previous_value if previous_value is not None else None
    return {
        "current": current[metric],
        "previous": previous_value,
        "delta": delta,
        "month": current["계약년월표시"],
        "coverage": coverage,
    }


def build_line(df: pd.DataFrame, y: str, title: str, color: str = "#0f8b8d") -> go.Figure:
    plot_df = ensure_month_columns(df)
    fig = go.Figure()
    shadow_color = "rgba(216,58,52,0.16)" if color == "#d83a34" else "rgba(15,139,141,0.18)"

    valid_df = plot_df[["기준월", "계약년월표시", y, "위험알림", "사고알림"]].dropna(subset=[y, "기준월"])
    if valid_df.empty:
        fig.add_annotation(
            text=f"{y} 값이 선택 지역 단위에 충분히 없습니다. 법정동을 '(전체)'로 선택하면 시군구 집계 지표를 볼 수 있습니다.",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=14, color="#667085"),
        )
    else:
        fig.add_trace(
            go.Scatter(
                x=valid_df["기준월"],
                y=valid_df[y],
                mode="lines",
                name=f"{y} 추세",
                line=dict(color=shadow_color, width=12),
                hoverinfo="skip",
                showlegend=False,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=valid_df["기준월"],
                y=valid_df[y],
                mode="lines+markers",
                name=y,
                line=dict(color=color, width=4),
                marker=dict(size=8, color="#ffffff", line=dict(color=color, width=2)),
                customdata=valid_df[["계약년월표시"]],
                hovertemplate="월=%{customdata[0]}<br>값=%{y:,.2f}<extra></extra>",
            )
        )

        highlight = valid_df[(valid_df["위험알림"] != "None") | (valid_df["사고알림"] != "None")]
        if not highlight.empty:
            marker_color = highlight["위험알림"].map({"Critical": "#d83a34", "Warning": "#f2a541"}).fillna("#d83a34")
            fig.add_trace(
                go.Scatter(
                    x=highlight["기준월"],
                    y=highlight[y],
                    mode="markers+text",
                    name="경보 발생",
                    marker=dict(size=14, color=marker_color, symbol="diamond", line=dict(color="#ffffff", width=2)),
                    text=highlight["위험알림"].replace({"None": ""}),
                    textposition="top center",
                    textfont=dict(size=12, color="#202124"),
                    customdata=highlight[["계약년월표시", "위험알림", "사고알림"]],
                    hovertemplate="경보월=%{customdata[0]}<br>위험=%{customdata[1]}<br>사고=%{customdata[2]}<br>값=%{y:,.2f}<extra></extra>",
                )
            )

        current = valid_df.iloc[-1]
        fig.add_annotation(
            x=current["기준월"],
            y=current[y],
            text=f"{current[y]:,.1f}",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=color,
            ax=34,
            ay=-34,
            bgcolor="#ffffff",
            bordercolor=color,
            borderwidth=1,
            font=dict(size=14, color="#202124"),
        )

    if y == "전세가율":
        fig.add_hline(y=70, line_dash="dot", line_color="#f2a541", annotation_text="주의 70%", annotation_font_size=13)
        fig.add_hline(y=85, line_dash="dash", line_color="#d83a34", annotation_text="고위험 85%", annotation_font_size=13)

    fig.update_layout(
        title_text=title,
        height=430,
        margin=dict(l=18, r=18, t=64, b=32),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#202124", size=15),
        title=dict(font=dict(size=22, color="#202124"), x=0.02, xanchor="left"),
        xaxis=dict(
            title="계약년월",
            showgrid=False,
            tickformat="%Y-%m",
            dtick="M6",
            tickangle=0,
            tickfont=dict(size=13),
        ),
        yaxis=dict(
            title=dict(text=y, font=dict(size=14)),
            gridcolor="#e8edf3",
            zeroline=False,
            tickfont=dict(size=13),
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=13)),
        showlegend=True,
    )
    return fig


df, data_source = load_data()

with st.sidebar:
    st.markdown("### 전 SAFE")
    st.caption("지역 단위 리스크 점검망")
    include_total = st.toggle("전국/전체 행 포함", value=False)

    filter_df = df.copy()
    if not include_total:
        filter_df = filter_df[(filter_df["시도"] != "(전체)") & (filter_df["시군구"] != "(전체)")]

    sido_options = sorted(filter_df["시도"].dropna().unique())
    default_sido = "서울특별시" if "서울특별시" in sido_options else sido_options[0]
    sido = st.selectbox("시도", sido_options, index=sido_options.index(default_sido))

    sigungu_options = sorted(filter_df.loc[filter_df["시도"] == sido, "시군구"].dropna().unique())
    default_sigungu = "강동구" if "강동구" in sigungu_options else sigungu_options[0]
    sigungu = st.selectbox("시군구", sigungu_options, index=sigungu_options.index(default_sigungu))

    dong_options = sorted(
        filter_df.loc[(filter_df["시도"] == sido) & (filter_df["시군구"] == sigungu), "법정동"].dropna().unique()
    )
    default_dong = "(전체)" if "(전체)" in dong_options else ("길동" if "길동" in dong_options else dong_options[0])
    dong = st.selectbox("법정동", dong_options, index=dong_options.index(default_dong))

    st.divider()
    st.caption(f"Data source: {data_source}")

view = df[(df["시도"] == sido) & (df["시군구"] == sigungu) & (df["법정동"] == dong)].copy()
if view.empty:
    st.warning("선택한 지역의 데이터가 없습니다.")
    st.stop()

if "종합총점" not in view.columns or view["종합총점"].isna().all():
    view = add_alert_columns(view)

view = ensure_month_columns(view)
view = view.sort_values("계약년월").reset_index(drop=True)
latest = view.iloc[-1]

risk_alert = clean_alert(latest.get("위험알림"))
incident_alert = clean_alert(latest.get("사고알림"))

st.markdown(
    f"""
    <div class="topbar">
      <div>
        <div class="brand-kicker">JEON SAFE EARLY WARNING</div>
        <h1 class="brand-title">전 SAFE 지역 리스크 대시보드</h1>
        <div class="brand-subtitle">{sido} {sigungu} {dong} · {latest["계약년월표시"]} 기준</div>
      </div>
      <div>
        <span class="{alert_class(risk_alert)}">위험 {risk_alert}</span>
        <span class="{alert_class(incident_alert)}">사고 {incident_alert}</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="metric-grid">', unsafe_allow_html=True)
metric_cols = st.columns(4)
with metric_cols[0]:
    render_metric("종합점수", fmt_num(latest.get("종합총점")), "구조적 위험과 발생경보 합산")
with metric_cols[1]:
    render_metric("구조적위험", fmt_num(latest.get("구조적위험총점")), "전세가율, 거래, 등기 기반")
with metric_cols[2]:
    render_metric("발생경보", fmt_num(latest.get("발생경보총점")), "임차권등기, 보증사고 기반")
with metric_cols[3]:
    render_metric("사고발생", fmt_num(latest.get("사고발생")), "임차권등기 + 보증사고")
st.markdown("</div>", unsafe_allow_html=True)

tab_overview, tab_trend, tab_rank, tab_report, tab_data = st.tabs(["종합 리포트", "위험 지표 추이", "위험지역 랭킹", "경보 상세", "데이터"])

with tab_overview:
    left, right = st.columns([1.2, 0.8])
    with left:
        st.markdown("#### 종합위험점수 추이")
        score_cols = [c for c in ["구조적위험총점", "발생경보총점", "종합총점"] if c in view.columns]
        score_long = view[["기준월"] + score_cols].dropna(subset=["기준월"]).melt("기준월", var_name="점수", value_name="값")
        fig = px.line(score_long, x="기준월", y="값", color="점수", markers=True)
        fig.update_traces(line=dict(width=4), marker=dict(size=8))
        fig.update_layout(
            height=460,
            margin=dict(l=18, r=18, t=28, b=30),
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(size=15, color="#202124"),
            yaxis=dict(gridcolor="#e8edf3"),
            xaxis=dict(title="계약년월", showgrid=False, tickformat="%Y-%m", dtick="M6", tickfont=dict(size=13)),
            title=dict(font=dict(size=22)),
            legend_title_text="",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("#### 최근 경보")
        alert_rows = view[(view["위험알림"] != "None") | (view["사고알림"] != "None")].tail(8)
        if alert_rows.empty:
            st.info("최근 경보가 없습니다.")
        else:
            alert_display = ensure_month_columns(alert_rows)
            alert_display["계약년월"] = alert_display["계약년월표시"]
            st.dataframe(
                alert_display[["계약년월", "위험알림", "사고알림", "종합총점", "요약설명"]]
                if "요약설명" in alert_display.columns
                else alert_display[["계약년월", "위험알림", "사고알림", "종합총점"]],
                hide_index=True,
                use_container_width=True,
            )

    st.markdown(
        f"""
        <div class="report-box">
          <div class="report-title">지역 기반 전세사기 경보 요약</div>
          <div class="report-text">
            선택 지역의 최신 위험알림은 <b>{risk_alert}</b>, 사고알림은 <b>{incident_alert}</b>입니다.
            구조적 위험 점수와 발생경보 점수를 분리해 보며, 경보가 발생한 월의 지표 상승과 이후 사고 신호를 함께 확인합니다.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab_trend:
    st.markdown("#### 위험 지표별 시계열 분석")
    st.markdown('<div class="section-note">전세가율, 거래량, 등기, 보증사고 흐름을 같은 지역-월 단위로 확인합니다.</div>', unsafe_allow_html=True)

    available_metrics = [
        c
        for c in ["전세가율", "거래건수", "근저당_건수", "임차권_건수", "보증사고_건수", "강제경매_건수"]
        if c in view.columns
    ]
    metric_a, metric_b = st.columns([0.58, 0.42])
    with metric_a:
        selected_metric = st.selectbox("주요 지표", available_metrics, index=0)
    with metric_b:
        compare_default = available_metrics.index("거래건수") if "거래건수" in available_metrics else 0
        compare_metric = st.selectbox("비교 지표", available_metrics, index=compare_default)

    snap = metric_snapshot(view, selected_metric)
    mom_col = f"{selected_metric}_전월증감(%)"
    pp_col = f"{selected_metric}_전월증감(단위%p)"
    ratio_col = f"{selected_metric}_24m배수"
    latest_valid = view.dropna(subset=[selected_metric]).tail(1)
    mom_value = None
    ratio_value = None
    if not latest_valid.empty:
        row = latest_valid.iloc[0]
        mom_value = row.get(mom_col, row.get(pp_col))
        ratio_value = row.get(ratio_col)

    st.markdown('<div class="insight-grid">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_insight("최근 관측월", str(snap["month"]), "결측을 제외한 최신 월")
    with c2:
        digits = 1 if selected_metric in ["전세가율", "신규계약비율", "소형주택비중_60이하"] else 0
        render_insight("최근 값", fmt_num(snap["current"], digits), selected_metric)
    with c3:
        suffix = "%p" if pp_col in view.columns else "%"
        render_insight("전월 변화", fmt_delta(mom_value, 1, suffix), "경보 판단 보조 지표")
    with c4:
        render_insight("24개월 배수", fmt_num(ratio_value, 2, "x"), f"커버리지 {snap['coverage']:.0%}")
    st.markdown("</div>", unsafe_allow_html=True)

    chart_a, chart_b = st.columns(2)
    with chart_a:
        st.plotly_chart(build_line(view, selected_metric, f"{selected_metric} 추이", "#0f8b8d"), use_container_width=True)
    with chart_b:
        st.plotly_chart(build_line(view, compare_metric, f"{compare_metric} 추이", "#d83a34"), use_container_width=True)

    rank_cols = [c for c in view.columns if "순위(상위%)" in c]
    if rank_cols:
        st.markdown("#### 동월 Peer Rank")
        rank_view = ensure_month_columns(view)[["계약년월표시"] + rank_cols].tail(12).rename(columns={"계약년월표시": "계약년월"})
        st.dataframe(rank_view, hide_index=True, use_container_width=True)

with tab_rank:
    st.markdown("#### 최신 월 기준 위험지역 랭킹")
    st.markdown('<div class="section-note">실제 산출물에서 최신 월의 Warning/Critical 또는 종합점수 상위 지역을 보여줍니다.</div>', unsafe_allow_html=True)
    latest_month = df["계약년월"].max()
    rank_base = df[(df["계약년월"] == latest_month) & (df["시도"] != "(전체)") & (df["시군구"] != "(전체)")].copy()
    rank_base["위험등급"] = rank_base["위험알림"].map({"Critical": 2, "Warning": 1}).fillna(0)
    rank_base["사고등급"] = rank_base["사고알림"].map({"Warning": 1, "Incident": 1}).fillna(0)
    rank_base["랭킹점수"] = (
        rank_base["위험등급"] * 100
        + rank_base["사고등급"] * 50
        + pd.to_numeric(rank_base.get("종합총점", 0), errors="coerce").fillna(0)
        + pd.to_numeric(rank_base.get("사고발생", 0), errors="coerce").fillna(0) * 0.05
    )
    rank_base = rank_base.sort_values(["랭킹점수", "종합총점"], ascending=False).head(20)
    show_cols = [
        c
        for c in ["시도", "시군구", "법정동", "위험알림", "사고알림", "종합총점", "전세가율", "거래건수", "사고발생", "랭킹점수"]
        if c in rank_base.columns
    ]
    st.dataframe(rank_base[show_cols], hide_index=True, use_container_width=True)

with tab_report:
    st.markdown("#### 이상치 상세 내용")
    report_cols = [
        c
        for c in [
            "계약년월",
            "위험알림",
            "사고알림",
            "사고집계범위",
            "사고발생",
            "임차권등기",
            "보증사고",
            "종합총점",
            "요약설명",
            "사후검증",
        ]
        if c in view.columns
    ]
    report_view = ensure_month_columns(view)[report_cols].sort_values("계약년월", ascending=False).copy()
    if "계약년월" in report_view.columns:
        report_view["계약년월"] = ensure_month_columns(view).loc[report_view.index, "계약년월표시"]
    st.dataframe(report_view, hide_index=True, use_container_width=True)

    latest_summary = latest.get("요약설명", "")
    latest_validation = latest.get("사후검증", "")
    st.markdown(
        f"""
        <div class="report-box">
          <div class="report-title">상세 리포트</div>
          <div class="report-text">
            <b>요약설명</b><br>{latest_summary if pd.notna(latest_summary) and str(latest_summary).strip() else "선택 월의 요약설명이 비어 있습니다."}
            <br><br>
            <b>사후검증</b><br>{latest_validation if pd.notna(latest_validation) and str(latest_validation).strip() else "선택 월의 사후검증 내용이 비어 있습니다."}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab_data:
    st.markdown("#### 원천 결과 테이블")
    base_cols = [
        c
        for c in [
            "계약년월",
            "시도",
            "시군구",
            "법정동",
            "전세가율",
            "거래건수",
            "근저당_건수",
            "임차권_건수",
            "보증사고_건수",
            "구조적위험총점",
            "발생경보총점",
            "종합총점",
            "위험알림",
            "사고알림",
        ]
        if c in view.columns
    ]
    data_source_view = ensure_month_columns(view)
    data_view = data_source_view[base_cols].sort_values("계약년월", ascending=False).copy()
    if "계약년월" in data_view.columns:
        data_view["계약년월"] = data_source_view.loc[data_view.index, "계약년월표시"]
    st.dataframe(data_view, hide_index=True, use_container_width=True)
