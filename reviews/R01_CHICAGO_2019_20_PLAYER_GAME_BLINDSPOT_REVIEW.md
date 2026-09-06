# R01 Chicago 2019-20 Player-Game Blindspot Review

- 대상: `simulation/CHICAGO_2019_20_PLAYER_GAME_DONOR_VECTOR.md`
- 성격: `ORCHESTRATOR_SELF_REVIEW / NOT_INDEPENDENT`
- 판정: `PASS_FOR_ROLE_PROVISIONAL_LOCK / PRODUCTION_BLOCKER`
- 원고 게이트: `CLOSED`

## 총평

65경기·18선발·1,395분은 같은 날짜 팀 총초와 시즌별 선수 총분을 동시에 보존한다. 독립 원인 없는 DNP 두 경기를 만들던 O-15C4 BASE 63경기보다 65경기가 인과적으로 낫다.

다만 `보호 0분`을 매 경기 고정으로 해석하면 donor가 거의 없는 날짜에 원장이 성립하지 않는다. 시즌 순감 0과 당일 gross 이동을 분리한 것이 핵심 교정이다. 이 gross bridge를 생산성 공짜 이전으로 취급하면 안 된다.

## PASS

| 점검 | 판정 |
|---|---|
| 65경기 실제 일정만 쓰는가 | PASS |
| 경기별 팀 총초를 보존하는가 | 65/65 PASS |
| 3개 연장 경기 총분을 보존하는가 | PASS |
| 주인공 1,395분이 실제 총분 위에 더해지는가 | 전량 순차감 — PASS |
| 보호 선수 시즌 총분이 줄어드는가 | 전원 순감 0 — PASS |
| 센터 분을 SF/PF에게 넘기는가 | 4명 경기별 고정 — PASS |
| Coby·LaVine 분을 줄이는가 | 경기별 변경 0 — PASS |
| 18선발을 새로 만드는가 | Hutchison 10+Harrison 8 — PASS |
| 승패를 보고 출전·선발을 고르는가 | 시간·역할 규칙만 사용 — PASS |

## 남은 맹점

1. Markkanen·Dunn의 19:34 gross bridge는 시즌 순감 0이어도 경기별 lineup과 피로를 바꾼다. O-15C6 outcome 입력에서 0으로 지우지 않는다.
2. Arcidiacono·Young은 초기 donor 부족을 메운 뒤 다른 날짜에 일부 분을 돌려받는다. 시즌 순차감만으로 경기 생산성을 배분하면 날짜별 효과가 어긋난다.
3. Harrison 선발 8개 이전은 역할상 가능하지만, 그의 남은 2선발과 244:20의 POA 수비 기능을 후속 생산성 모델이 보존해야 한다.
4. 65경기 무결석은 가용성 가정이지 내구성 S급 선언이 아니다. 이후 시즌에 자동 복사하지 않는다.
5. 정수 분 배정은 서사 역할선이다. 실제 교체 시각·파울 트러블·가비지타임을 정확히 재현한다고 주장하지 않는다.
6. 본 검토는 독립 검수가 아니다. O-15C6 생산성·승패 묶음의 최종 정본 승격 전 별도 독립 맹점 검토가 필요하다.

## 다음 통과 조건

- 주인공 2년차 LOW/BASE/HIGH 생산성 prior
- changed player-game별 actual→alternate 생산성 이전
- Markkanen·Dunn gross bridge의 fatigue 민감도
- 65경기 score-margin outcome과 standings
- 2020 lottery seed·추첨 사건 뒤 Patrick Williams 보드

