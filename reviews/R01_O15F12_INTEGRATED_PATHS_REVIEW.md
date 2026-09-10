# O-15F12 총괄 자체 검토

- 기준일:2026-09-10
- 판정:`CONDITIONAL_72_GAME_PATHS_CONNECTED / FINAL_SEASON_HOLD`
- 독립성:`NOT_INDEPENDENT`

| 항목 | 결과 |
|---|---|
| 범위 | 전반 잔여15날짜29개 분 배정안·522개 조건,이전3날짜 입력 재사용 |
| 시간 | 모든 새 안에5인 조합·선발 최소3분·선수 시간 일치; 연장2날짜53분 유지 |
| 잔차와 역할 | ±1초 관측 잔차와 Hartenstein39초/Reid7초 모델 이동을 구분 |
| 0분 함정 | Bonga/Hampton/Kira 실제0분을 Trent/Bey/Hayes의0분으로 복사하지 않음 |
| 가용성 | 신규 선수 등록은 조건,기존 증분은 양의 관측 또는Coach's Decision DNP만 허용 |
| 시즌 연결 | 6경로마다43+29 중복 없는72날짜;지표별prior·피로 전후반 일치 |
| 거래 | Fournier 미합류안을 Orlando 이탈 입력과 결합하지 않고 제외 |
| 라이벌 | 동일 유효rating과분정책을 두 날짜에 적용;최종 능력 prior 아님 |
| 미지선수 | 포함된 Hall/Riller 계수의 구간 부호 검사,0대체 없음 |
| 승패 | BASE31~33 조건부; GSW/POR 계열 차이 유지,0점 경계 미정 |
| 상대 기록 | Chicago 승수 변화+상대 팀별 변화 합계0;리그전체 순위 미계산 |
| 후속 | 시즌 결산·순위·픽 보드,같은분감사 반복 불요 |

신규 회귀검사4개와 통합 검증·git diff --check를 적용했다. 이것은 독립 인력 검수나 원격 CI 통과 선언이 아니다. 기존 O-15F11 산출물의 입력은 수정하지 않았다. 정본 v0.30 PARTIAL·원고 CLOSED·manuscript_allowed false 유지.
