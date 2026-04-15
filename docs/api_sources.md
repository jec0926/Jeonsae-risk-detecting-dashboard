# Open API Sources

This project is designed to run without API keys by using the packaged dashboard cache at `data/jeonsafe_dashboard.csv.gz`. If issued service keys are configured through `.env`, the connector modules under `src/jeonsafe/tools/` can be used to refresh or augment the risk indicators.

Do not commit real service keys to GitHub. Use `.env.example` as a template.

## 1. HUG 분양보증사고현황 API

- Source: HUG
- Endpoint page: https://www.khug.or.kr/accidentDistributionGuaranteeStatus.do
- Config variable: `HUG_GUARANTEE_ACCIDENT_API_KEY`
- Optional key parameter variable: `HUG_GUARANTEE_ACCIDENT_KEY_PARAM`
- Current granularity: 시도 단위
- Role in JeonSAFE:
  - Actual accident/outcome indicator
  - Used as a scale indicator for observed guarantee-accident occurrence
  - Can supplement or replace cached guarantee accident counts when the key is available

Notes:

- The available geographic unit is currently understood as province/metropolitan city level.
- This means it is useful for macro monitoring and validation, while district-level prediction should still rely on district-level indicators where available.
- Local connectivity testing showed that the endpoint is reachable, but the exact authentication parameter or additional required parameters must be confirmed from the issued HUG API guide.

## 2. IROS 근저당권 설정 등기 API

- Source: 등기정보광장
- Application page: https://data.iros.go.kr/rp/oa/selectOapiAppl.do
- Endpoint: https://data.iros.go.kr/openapi/cr/rs/selectCrRsRgsCsOpenApi.rest?id=0000000070
- Config variable: `IROS_MORTGAGE_API_KEY`
- Current granularity: 시군구 단위
- Search real estate type: 건물
- Role in JeonSAFE:
  - Leading/predictor indicator
  - Used to explain and predict future guarantee accidents or lease-right registrations
- Mortgage growth can be interpreted as a structural risk signal
- Local connectivity testing returned `필수 요청인자가 누락되었습니다`, so the endpoint/key path is reachable but required search parameters must be added from the issued API guide.

## 3. IROS 임차권등기 설정 API

- Source: 등기정보광장
- Application page: https://data.iros.go.kr/rp/oa/selectOapiAppl.do
- Endpoint: https://data.iros.go.kr/openapi/cr/rs/selectCrRsRgsCsOpenApi.rest?id=0000000078
- Config variable: `IROS_LEASE_RIGHT_API_KEY`
- Current granularity: 시군구 단위
- Search real estate type: 건물
- Role in JeonSAFE:
  - Actual accident/outcome indicator
  - Lease-right registration count is used to measure observed regional incident scale
- Future occurrence can be modeled using leading indicators such as jeonse ratio, transaction volume, and mortgage registrations
- Local connectivity testing returned `필수 요청인자가 누락되었습니다`, so the endpoint/key path is reachable but required search parameters must be added from the issued API guide.

## 4. Missing or Changed Sources

Some original project sources or file structures may no longer be available in the same form. The portfolio version handles this by separating data roles:

- Outcome indicators:
  - 보증사고 건수
  - 임차권등기 건수
- Leading indicators:
  - 전세가율
  - 거래건수
  - 근저당권 설정 건수
  - 신규계약비율
  - 소형주택비중
  - rolling change, moving-average multiple, peer rank

If a source disappears or changes granularity, the dashboard can still run from the packaged cache and the connector can be updated independently.

## 5. Runtime Strategy

```text
Default demo mode
  -> data/jeonsafe_dashboard.csv.gz

Local research mode
  -> DAB/Data/Result/risk_parts/*.csv or *.parquet

API-enabled mode
  -> .env API keys
  -> HUG / IROS connectors
  -> refreshed indicators
  -> dashboard cache rebuild
```

This split keeps the GitHub portfolio reproducible while making it clear that real-time API integration is supported after key issuance.
