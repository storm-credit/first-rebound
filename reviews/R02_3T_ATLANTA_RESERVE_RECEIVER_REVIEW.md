# R02-3T Atlanta Reserve Receiver Review

- 대상: `ATL_REMAINDER_POOL` 183.1분의 동일 날짜 실명 수취자 배정
- 판정: `PASS_WITH_PRODUCTION_OUTCOME_HOLD`
- 원고 게이트: `CLOSED`

| 맹점 | 통제 | 판정 |
|---|---|---|
| 회계 브리지를 가상 선수로 남기는가 | 29개 날짜·31개 행을 Anderson·Poythress·Plumlee·Hamilton에게 전부 배정 | PASS |
| 결과를 보고 수취자를 고르는가 | Anderson 복귀 전후의 역할 순서와 실제 관측 최고분 상한을 승패 계산 전에 고정 | PASS |
| 같은 날짜 가용성이 없는 선수를 쓰는가 | ESPN Atlanta 박스스코어 `PLAY/DNP-CD` 등재 필수, 미등재 시 다음 순위로 이동 | PASS |
| 한 선수에게 과도한 분을 몰아주는가 | 실제 2018-19 단일 경기 최고분을 조정 경기분 상한으로 사용 | PASS |
| DNP를 실제 출전으로 오인하는가 | DNP-CD는 가용성 증거이며, 분을 받는 날짜만 대체 세계 추가 출전으로 별도 계산 | PASS |
| Anderson 재활 기간을 무시하는가 | 공식 시즌 리뷰의 첫 16경기 결장 뒤 11월 19일 복귀를 phase 경계로 사용 | PASS |
| B.J. Johnson을 억지로 끼워 넣는가 | 후보 감사에는 포함하되 겹치는 잔여 날짜의 우선순위 수취자가 있어 0분 | PASS |
| 핵심 육성 분을 침범하는가 | Young·Huerter·Collins의 실제 분 변화 없음 | PASS |
| 팀 총분에 새 분을 더하는가 | Spellman -805.0 + 주인공 621.9 + 수취자 183.1 = 0.0 | PASS |
| 분 배정만으로 개인 기록·승패를 만드는가 | 득점·효율·피로·경기 영향·승패 전부 HOLD | PASS |

## 수치 검산

- 잔여분이 있는 날짜: 29
- 배정 행: 31
- 실명 수취자: 4명
- Anderson: 105.6분
- Poythress: 48.6분
- Plumlee: 17.5분
- Hamilton: 11.4분
- 합계: 183.1분
- 미배정 날짜: 0
- 날짜별 잔액: 0.0분
- 공개 정수 선수분 대체 후 합계: 19,853분

## 중단선

G3는 `PASS_WITH_BRIDGE`에서 `PASS`로 올라간다. 다만 이 원장은 분만 닫았으며 개인 생산성과 다음 경기 가용성은 만들지 않았다. production prior·피로 규칙·고정 hash를 결과 전에 사전등록하기 전에는 대체 승패를 실행하지 않는다.
