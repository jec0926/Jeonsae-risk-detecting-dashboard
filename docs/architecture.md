# JeonSAFE PoC Architecture

JeonSAFE PoC는 기존 전세사기 리스크 모델을 GitHub 포트폴리오로 설명할 수 있도록 재구성한 버전입니다. 핵심은 단순 점수 대시보드가 아니라, 실제 발생규모와 선행 위험변수를 분리해 보여주고 이를 상담형 인터페이스로 연결하는 것입니다.

## 1. Architecture

```text
Public/Open API Layer
  HUG guarantee accident API
  IROS mortgage registration API
  IROS lease-right registration API
        |
        v
Connector Layer
  src/jeonsafe/tools/hug_api_tool.py
  src/jeonsafe/tools/iros_api_tool.py
        |
        v
Feature / Cache Layer
  data/jeonsafe_dashboard.csv.gz
  scripts/build_dashboard_dataset.py
        |
        v
Risk Logic
  src/jeonsafe/scoring.py
  src/jeonsafe/anomaly.py
        |
        |
        v
Streamlit Dashboard
app/streamlit_app.py
```

## 2. Outcome vs Predictor

PoC에서는 위험지표를 두 그룹으로 나눕니다.

| Group | Role | Examples |
| --- | --- | --- |
| 실제 발생규모 | 위험 분류의 결과 기준 | 보증사고 건수, 임차권등기 건수, 사고발생 합계 |
| 선행 예측변수 | 발생규모를 예측하거나 설명하는 변수 | 전세가율, 거래건수, 근저당 설정 건수, 신규계약비율, 소형주택비중 |

이 구분을 명확히 하면 모델 설명력이 좋아집니다. 예를 들어 “전세가율이 높아서 위험하다”가 아니라, “실제 사고/임차권등기 발생규모가 높은 지역을 기준으로 위험을 정의하고, 전세가율과 근저당은 그 발생규모를 설명하는 선행 변수로 사용한다”고 말할 수 있습니다.

## 3. Dashboard Flow

1. 사용자가 시도, 시군구, 법정동을 선택합니다.
2. 최신 월 기준 경보와 핵심 지표를 보여줍니다.
3. 실제 발생규모와 선행 변수의 월별 추이를 분리해 보여줍니다.
4. 최신 월 기준 위험지역 랭킹으로 다른 지역과 비교합니다.
5. 경보 상세와 원천 테이블에서 판단 근거를 확인합니다.

## 4. API-Ready Design

현재 저장소는 실제 API 키를 포함하지 않습니다. `.env.example`에 필요한 환경변수 이름만 두고, 로컬 실행 시 `.env`에 키를 입력하는 구조입니다.

API 응답 구조나 필수 파라미터가 바뀔 수 있으므로 커넥터는 다음 역할만 담당합니다.

- endpoint와 인증값 관리
- 요청 파라미터 구성
- 응답 상태와 원문 payload 반환
- 후처리 로직과 분리

이렇게 나누면 API 문서가 업데이트되어도 대시보드와 모델 코드를 크게 바꾸지 않고 커넥터만 보완할 수 있습니다.

## 5. Portfolio Message

이 프로젝트의 포트폴리오 메시지는 “수상작”이 아니라 “공공데이터 기반 위험 의사결정 제품화 PoC”입니다.

- 기존 모델 산출물을 GitHub 공개 가능한 형태로 정리
- 실제 발생규모와 선행 변수를 분리한 리스크 설명 구조
- Open API 연동을 고려한 확장 가능한 커넥터 설계
- Streamlit 대시보드로 설명 가능한 포트폴리오형 UX
