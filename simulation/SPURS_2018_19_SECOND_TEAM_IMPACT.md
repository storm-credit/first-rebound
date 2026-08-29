# San Antonio 2018-19 Second-Team Impact v1.0

- 상태: `SECOND_TEAM_BASELINE_PASS / GAME_OUTCOMES_HOLD`
- 범위: 2018 Draft 49번 Omari Spellman 이동이 San Antonio에 만드는 최소 파급
- 계산 권위: `simulation/ATLANTA_2018_19_CAUSALITY_LEDGER.xlsx`의 `Spurs Impact`
- 원고 게이트: `CLOSED`

## 결론

Spellman은 Atlanta에서 실제로 받은 805분을 San Antonio에 복사하지 않는다. 대체하는 자리는 실제 49번 Chimezie Metu의 신인 개발 슬롯이다.

| 기준 | 실제 Metu | Spellman 대체 세계 |
|---|---:|---:|
| NBA 계약 유형 | 다년 NBA 계약 | 같은 계약 계층 |
| NBA 경기 | 29 | 기준 29, 허용 24~31 |
| NBA 선발 | 0 | 0 |
| NBA 총분 | 145.4 | 기준 145.4, 허용 120~180 |
| NBA 평균분 | 5.0 | 허용 4~6 |
| Austin 경기 | 26 | 기준 26, 허용 20~28 |

San Antonio의 실제 48승 34패는 비교 기준선일 뿐 대체 세계의 확정 결과가 아니다. 다만 기준 시나리오에서는 실제 Metu의 저레버리지 역할을 그대로 대체하므로 자동 승패 변경을 만들지 않는다.

## 계약·배정 고증

Metu는 투웨이 선수가 아니었다. 2018년 9월 4일 Spurs와 다년 NBA 계약을 맺은 뒤 NBA 계약을 유지한 채 Austin으로 반복 배정·복귀했다. 2018-19 Austin 성적은 26경기·평균 27.3분이었다.

원장에는 2018년 10월 25일부터 2019년 3월 24일까지 확인되는 19개 assignment/recall 창을 기록했다. 이를 Spellman의 정확한 대체 일정으로 복사하지는 않는다. 기능은 다음 두 가지만 잠근다.

1. NBA 표준계약을 유지한 채 G League 개발 경기를 뛸 수 있다.
2. NBA와 Austin의 같은 날짜 경기에서 동시에 출전시킬 수 없다.

## 사전등록 안전선

| 시나리오 | NBA 경기 | 평균분 | 총분 | Austin 경기 | 승패 처리 |
|---|---:|---:|---:|---:|---|
| LOW | 24 | 4 | 120 | 28 | 자동 변경 없음 |
| BASE | 29 | 5 | 145.4 | 26 | 자동 변경 없음 |
| HIGH | 31 | 6 | 180 | 20 | 경쟁 구간이면 경기별 재검토 |

145.4분 초과분은 공짜로 만들지 않는다. HIGH의 추가 34.6분은 같은 날짜의 실제 심부 로테이션 선수에게서 가져와야 하며, 공여자·경기·당시 가용성을 명시하지 못하면 BASE로 되돌린다. Aldridge·DeRozan·Gay·Pöltl 등 핵심 역할은 보호한다.

## Atlanta 직접 대결

| 날짜 | 장소 | 실제 결과 | Metu 상태 | Spurs 쪽 대체 접촉 |
|---|---|---|---|---|
| 2019-03-06 | Atlanta | Spurs 111-104 | DNP-CD, 0분 | `NO_DIRECT_MINUTES` |
| 2019-04-02 | San Antonio | Spurs 117-111 | 0분 | `NO_DIRECT_MINUTES` |

두 경기 모두 Spurs의 실제 49번 슬롯이 코트에 들어오지 않았다. 따라서 Spellman 이동만으로 이 두 결과를 뒤집지 않는다. 주인공이 Atlanta 쪽에서 출전해 만드는 영향은 별도 player-game 원장에서 계산해야 하므로 결과 자체는 아직 `HOLD`다.

## 드래프트·승수 방화벽

- Spurs 역할 기준선은 닫혔다.
- Spurs 48승 34패는 아직 `BASELINE_ONLY`다.
- BASE 이하의 저레버리지 분만 확인되면 Spurs 쪽 자동 승패 변화는 0이다.
- 145.4분 초과 또는 경쟁 구간 출전이 한 번이라도 생기면 그 경기부터 시간순 결과 검토를 연다.
- Atlanta의 대체 승패, 상대팀 승패, 2019 standings·lottery는 계속 `FINAL` 금지다.
- Dallas의 Metu와 Denver의 Spalding/Welsh는 계약·로스터 층을 별도로 닫는다. 실제 핵심 분 침범이 확인될 때만 전 경기 모델로 확장한다.

## 출처

- [San Antonio Spurs — Metu signing](https://www.nba.com/spurs/news/spurs-sign-2018-second-round-pick-chimezie-metu)
- [RealGM — Metu NBA/G League totals and transactions](https://basketball.realgm.com/player/Chimezie-Metu/Summary/76976)
- [San Antonio Spurs — 2018-19 Austin recap](https://www.nba.com/spurs/news/san-antonio-assigns-chimezie-metu-austin-spurs-8)
- [Pounding the Rock — Metu rookie-season review](https://www.poundingtherock.com/2019/5/4/18523491/2018-2019-spurs-player-reviews-chimezie-metu)
- [ESPN — 2019-03-06 Spurs at Hawks](https://www.espn.com/nba/boxscore/_/gameId/401071641)
- [NBA Hawks — 2019-04-02 Hawks at Spurs](https://www.nba.com/hawks/game/0021801162-hawks-vs-spurs-san-antonio-tx-04-02-2019)
