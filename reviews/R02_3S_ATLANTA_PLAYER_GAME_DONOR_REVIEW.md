# R02-3S Atlanta Player-Game Donor Review

- 대상: Atlanta 2018-19 주인공 날짜별 출전·Spellman donor·Erie assignment
- 판정: `PASS_WITH_NAMED_RECEIVER_HOLD`
- 원고 게이트: `CLOSED`

| 맹점 | 통제 | 판정 |
|---|---|---|
| 실제 결과를 보고 출전일을 고르는가 | `donor ≥7.0`, 경기당 16.0분 상한을 결과 계산 전에 고정 | PASS |
| Spellman 46경기·11선발을 그대로 복사하는가 | 주인공 43경기·0선발, 선발·부상·개인 기록 미복사 | PASS |
| 주인공 분을 실제 팀 총분에 더하는가 | 805.0분을 주인공 621.9 + remainder 183.1로 완전 분할 | PASS |
| 잔여 183.1분을 삭제하는가 | 날짜별 `ATL_REMAINDER_POOL` 회계 브리지 유지 | PASS_WITH_HOLD |
| 회계 브리지를 가상 선수로 오인하는가 | 개인 기록·명단·서사 부여 금지 | PASS |
| Young·Huerter·Collins 분을 편의상 깎는가 | 1차 donor 외 핵심 육성 분 보호 | PASS |
| 지각과 Erie를 같은 징계로 묶는가 | 11월 19일 NBA 기회 상실과 12월 7~22일 개발 결정을 분리 | PASS |
| 실제 Spellman 부상을 복사하는가 | hip/ankle injury 비복사 명시 | PASS |
| NBA와 Erie를 같은 날 모두 뛰는가 | 여섯 Erie 경기와 같은 날짜 NBA 분 0 | PASS |
| G League 정확 기록을 근거 없이 만드는가 | 6경기·24~30분 범위만 잠그고 개인 박스스코어 HOLD | PASS |
| 43경기만 직접 접촉으로 보고 나머지를 동일 처리하는가 | 43 DIRECT / 39 ROSTER, IDENTICAL 0 | PASS |
| donor vector만으로 승패를 확정하는가 | 성과·영향 prior와 대체 승패 전부 HOLD | PASS |

## 수치 검산

- Spellman 출전: 46경기
- 실제 donor: 805.0분
- 7분 이상 후보: 44경기·636.0분
- 2018-11-19 상실: 14.1분
- 주인공: 43경기·621.9분·14.46 MPG
- Atlanta remainder: 183.1분
- 일자별 donor balance 오류: 0
- Erie: 6경기 일정·NBA 동시 출전 0

## 중단선

이 단계에서 G2 사전등록은 `PASS`, G3 분 보존은 `PASS_WITH_BRIDGE`다. `ATL_REMAINDER_POOL`의 동일 날짜 실명 수취자를 검증하기 전에는 개인 박스스코어·경기 영향·승패를 열지 않는다.
