# Validation Plan

## Goal

경보가 단순한 노이즈인지, 실제 사고 증가를 선행하는 신호인지 검증합니다.

## Suggested Metrics

1. Alert-to-incident uplift

경보 발생 지역과 미발생 지역의 이후 사고 증가율을 비교합니다.

2. Lead time analysis

경보 발생 후 3개월, 6개월, 12개월, 24개월 내 사고 증가 여부를 확인합니다.

3. Precision-style validation

Warning 또는 Critical 지역 중 실제 사고 증가가 관측된 지역의 비율을 계산합니다.

4. Recall-style validation

사고 급증 지역 중 사전에 Warning 또는 Critical 경보가 있었던 지역의 비율을 계산합니다.

5. Case study

강서구 화곡동, 강동구 길동 등 실제 위험 신호가 뚜렷한 지역을 대상으로 지표별 시계열과 사고 발생 시점을 비교합니다.

## Notes

본 프로젝트는 정책 점검 우선순위 산정 목적의 조기경보 모델입니다. 따라서 일반적인 classification accuracy보다, 경보 이후 사고 증가 여부와 사전 탐지 리드타임이 더 중요한 평가 기준입니다.

