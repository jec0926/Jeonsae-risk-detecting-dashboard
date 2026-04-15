# JeonSAFE: 전세사기 지역 리스크 조기경보 대시보드

공공데이터 기반으로 전세사기 위험 신호를 지역 단위에서 탐지하고, 실제 사고 발생규모와 선행 위험지표를 함께 보여주는 Streamlit 대시보드 PoC입니다.

이 저장소는 기존 DAB 프로젝트 산출물을 GitHub 포트폴리오로 설명할 수 있도록 재구성한 버전입니다. 원본 분석 파일과 발표자료를 직접 수정하지 않고, `github_ready/` 안에 실행 가능한 앱, 샘플 데이터, 문서, API 연동 골격을 분리했습니다.

## 1. 핵심 컨셉

전세사기 위험을 단순 점수로만 보여주지 않고, 지표의 역할을 분리합니다.

| 구분 | 역할 | 주요 지표 |
| --- | --- | --- |
| 실제 발생규모 | 위험 분류의 기준이 되는 결과 지표 | 보증사고 건수, 임차권등기 건수, 사고발생 합계 |
| 선행 위험지표 | 발생규모를 예측하거나 설명하는 변수 | 전세가율, 거래건수, 근저당 설정 건수, 신규계약비율, 소형주택비중 |

즉, “전세가율이 높으니 위험하다”가 아니라 “보증사고와 임차권등기 발생규모가 큰 지역을 위험 기준으로 보고, 전세가율과 근저당 등은 그 위험을 설명하는 선행 변수로 활용한다”는 구조입니다.

## 2. 주요 기능

- 시도, 시군구, 법정동 단위 지역 필터
- 최신 월 기준 위험 경보와 사고 경보 표시
- 종합위험점수, 구조위험점수, 발생경보점수 추이
- 보증사고, 임차권등기, 근저당, 전세가율 등 지표별 월별 시각화
- 최신 월 기준 위험지역 랭킹
- 경보 상세 테이블과 원천 결과 테이블
- HUG, 등기정보광장 Open API 연동을 위한 커넥터 구조

## 3. Dashboard Preview

Streamlit 앱은 다음 흐름으로 구성됩니다.

1. `종합 리포트`: 선택 지역의 최신 위험 상태와 점수 추이
2. `위험 지표 추이`: 실제 발생규모와 선행 변수의 월별 변화
3. `위험지역 랭킹`: 최신 월 기준 상위 위험지역 비교
4. `경보 상세`: 경보 발생 월과 요약 설명
5. `데이터`: 모델 산출 결과 테이블 확인

## 4. Data

GitHub 업로드를 위해 원본 대용량 파일은 직접 포함하지 않고, 실행 가능한 압축 결과 데이터와 샘플 데이터를 포함합니다.

| File | Description |
| --- | --- |
| `data/jeonsafe_dashboard.csv.gz` | 대시보드 실행용 압축 결과 데이터 |
| `data/sample_risk_result.csv` | 구조 확인용 샘플 데이터 |
| `scripts/build_dashboard_dataset.py` | 원본 결과 파일에서 GitHub용 대시보드 데이터를 재생성하는 스크립트 |

## 5. Open API 연동 계획

API 키는 저장소에 포함하지 않습니다. `.env.example`을 `.env`로 복사한 뒤 로컬 환경에서만 입력합니다.

| Source | Purpose | Unit |
| --- | --- | --- |
| HUG 분양보증사고현황 API | 보증사고 발생규모 보강 | 시도 |
| 등기정보광장 근저당 설정 API | 선행 위험변수 보강 | 시군구 |
| 등기정보광장 임차권등기 설정 API | 실제 발생규모 보강 | 시군구 |

관련 정리는 `docs/api_sources.md`, API 테스트 메모는 `docs/api_test_notes.md`에 있습니다.

## 6. Repository Structure

```text
github_ready/
  README.md
  requirements.txt
  .env.example
  .gitignore
  app/
    streamlit_app.py
  data/
    jeonsafe_dashboard.csv.gz
    sample_risk_result.csv
  docs/
    architecture.md
    api_sources.md
    api_test_notes.md
    dashboard_design.md
    data_dictionary.md
    model_design.md
    portfolio_upgrade_direction.md
    validation_plan.md
  scripts/
    build_dashboard_dataset.py
  src/
    jeonsafe/
      __init__.py
      anomaly.py
      config.py
      scoring.py
      tools/
        api_status.py
        base.py
        hug_api_tool.py
        iros_api_tool.py
```

## 7. Run

```bash
cd DAB/github_ready
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

브라우저에서 `http://localhost:8501`로 접속합니다.

원본 결과 파일에서 대시보드 데이터를 다시 만들려면 다음 명령을 실행합니다.

```bash
python scripts/build_dashboard_dataset.py
```

## 8. Environment Variables

```bash
cp .env.example .env
```

`.env`에는 로컬 테스트용 API 키만 입력합니다. 실제 키가 들어간 `.env` 파일은 `.gitignore`에 의해 GitHub에 올라가지 않습니다.

## 9. Portfolio Pitch

이 프로젝트는 “상 수상작”으로 포장하기보다, 기존 분석 산출물을 서비스형 데이터 제품으로 보완한 포트폴리오 PoC로 설명하는 것이 적합합니다.

- 실제 사고 발생규모와 선행 위험지표를 분리한 리스크 정의
- 지역 단위 의사결정에 맞춘 대시보드 UX
- Open API 확장을 고려한 커넥터 구조
- 경보 발생 이후 실제 사고 증가 여부를 검증할 수 있는 설계
- GitHub에서 바로 실행 가능한 Streamlit 포트폴리오 구성

