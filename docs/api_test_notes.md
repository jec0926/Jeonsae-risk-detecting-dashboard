# API Test Notes

This note records local connectivity checks without exposing service keys.

## HUG 분양보증사고현황 API

Endpoint:

```text
https://www.khug.or.kr/accidentDistributionGuaranteeStatus.do
```

Observed behavior:

- HTTP connection succeeds.
- Response is XML.
- Using common key parameter candidates such as `serviceKey`, `key`, `apiKey`, `authKey`, and common header candidates still returned:

```text
resultCode = 11
resultMsg = NEED API KEYS.
```

Interpretation:

- The endpoint is reachable, but the exact authentication parameter or additional required parameters must be confirmed from the issued HUG Open API guide.
- The connector supports a configurable key parameter through `HUG_GUARANTEE_ACCIDENT_KEY_PARAM`.

## IROS 근저당권/임차권등기 API

Endpoints:

```text
https://data.iros.go.kr/openapi/cr/rs/selectCrRsRgsCsOpenApi.rest?id=0000000070
https://data.iros.go.kr/openapi/cr/rs/selectCrRsRgsCsOpenApi.rest?id=0000000078
```

Observed behavior:

- HTTP connection succeeds.
- Response is XML.
- Passing each issued key as `key` reached the API layer and returned:

```text
returnCode = APIERROR-0012
returnMessage = 필수 요청인자가 누락되었습니다.
```

Interpretation:

- The API key and endpoint combination are plausible.
- Required request parameters must be filled from the IROS application/detail guide.
- The connector accepts arbitrary keyword parameters through `fetch(**params)` so those required fields can be added without changing the application structure.

