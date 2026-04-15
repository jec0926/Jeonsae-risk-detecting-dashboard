# Model Design

## Objective

JeonSAFE는 지역 단위 전세사기 위험을 월별로 모니터링하기 위한 조기경보 스코어링 엔진입니다. 개별 거래가 사기인지 분류하는 모델이 아니라, 특정 지역에서 위험 조건이 누적되는 시점을 탐지하는 데 초점을 둡니다.

## Unit of Analysis

- Time: 계약년월
- Region: 시도, 시군구, 법정동
- Aggregation levels: 전국, 시도, 시군구, 법정동

## Feature Groups

### Structural Risk

구조적 위험은 사고가 발생하기 전 누적될 수 있는 시장 조건을 의미합니다.

- 전세가율
- 거래건수
- 신규계약비율
- 소형주택비중_60이하
- 근저당_건수

### Incident Signal

발생경보는 실제 사고 또는 사고에 가까운 법적/보증 신호를 의미합니다.

- 임차권_건수
- 보증사고_건수
- 강제경매_건수
- 사고율

## Scoring

각 지표는 지역-월 단위로 정규화한 뒤 구간 점수로 변환합니다. 이후 구조적 위험 점수와 발생경보 점수를 분리 합산하고, 최종적으로 종합점수를 산출합니다.

```text
구조적위험총점 = 전세가율_점수 + 거래건수_점수 + 신규계약_점수 + 소형주택_점수 + 근저당권_점수
발생경보총점 = 임차권_점수 + 보증사고_점수 + 강제경매_점수 + 사고율_점수
종합총점 = 구조적위험총점 + 발생경보총점
```

## Alert Logic

이상치 탐지는 단일 임계값이 아니라 시계열 변화와 peer group 내 상대 순위를 함께 봅니다.

- Month-over-month change
- Rolling 24-month average multiple
- Same-month peer rank
- Minimum transaction gate

Alert level:

- `None`: 유의미한 구조적 위험 신호 없음
- `Warning`: 주요 구조 지표 1개 이상 또는 복수 지표 상승
- `Critical`: 거래건수와 근저당권 동시 상승 또는 3개 이상 구조 지표 동시 상승

## Why Rule-Based?

전세사기 데이터는 label leakage 위험이 큽니다. 예를 들어 보증사고나 임차권등기를 target 또는 동시점 feature로 사용하면 사전예측이 아니라 사후탐지가 될 수 있습니다. 따라서 본 프로젝트는 설명 가능성과 정책 활용성을 우선해 규칙 기반 조기경보 엔진으로 설계했습니다.

