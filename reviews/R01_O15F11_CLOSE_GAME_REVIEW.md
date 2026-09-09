# O-15F11 총괄 자체 검토

- 판정: `CLOSE_GAME_ALLOCATION_AND_SENSITIVITY_PASS / SEASON_HOLD`
- 독립성: `NOT_INDEPENDENT`

| 확인 항목 | 결과 |
|---|---|
| O-15F10 산술 | 상대 상수 혼입·prior 계열 누락·전반 피로·본문 표 오류 정정 |
| 기준선 분리 | 미선택 교체 메뉴를 미지 선수로 바꿔도 36개 기준선 동일 |
| 입력 계보 | 지표별 선행 43경기 재사용, 후반 29날짜 가지 간 기준선 일치 |
| 접촉 누락 | 제거 선수 없는 GSW/LAL도 18개 미정 접촉에 포함 |
| 분·조합 | 11안 모두 240분, 5인 역할 조합·선발 최소3분·선수 시간 일치 |
| 가용성 | DNP Coach's Decision 후보만 기존 선수 추가 분 허용; 타팀 부상 복사 없음 |
| 영향 | 198조건, 양 팀 부호 대칭; 미지 계수의 절편만 승패로 세지 않음 |
| 동일 선수 | Portland 두 날짜 같은 정책·같은 지표별 Evans rating 구간 연결 |
| 추천 | 기존 선수 분담 / Hutchison 비활성은 작업 가정. 실제 사건·최종 승패 미승인 |
| 접전 | GSW와 1/30 Portland의 계열 불일치를 결과 미정으로 보존 |
| 남은 작업 | 전반 나머지15접촉·라이벌·시즌 단일 경로·순위·픽 |

검증 명령: `test_chicago_2020_21_season_connection.py`, `build_chicago_2020_21_season_connection.py`, `build_chicago_2020_21_close_games.py`, `crosscheck_chicago_2020_21_impact.py`, `git diff --check`.
원고 게이트 CLOSED. 독립 검수 완료나 자동 원격 CI 통과로 표현하지 않는다.
