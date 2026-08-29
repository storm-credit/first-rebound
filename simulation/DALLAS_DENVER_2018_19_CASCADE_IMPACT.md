# Dallas / Denver 2018-19 Cascade Contract Impact v1.0

- 상태: `CASCADE_CONTRACT_PASS / GAME_OUTCOMES_HOLD`
- 범위: 2018 Draft 56번 Chimezie Metu와 58번 Ray Spalding의 계약·로스터·직접 대결 파급
- 계산 권위: `simulation/ATLANTA_2018_19_CAUSALITY_LEDGER.xlsx`의 `Cascade Impact`
- 원고 게이트: `CLOSED`

## 결론

Dallas와 Denver의 연쇄 이동은 **계약층에서 닫을 수 있다**. 두 팀 모두 대체 선수를 실제 밀려난 선수의 팀별 개발 슬롯 안에서 시작시키면 핵심 로테이션 분을 자동 침범하지 않는다.

| 팀 | 실제 슬롯 | 대체 세계 | BASE | 경기층 재개 조건 |
|---|---|---|---|---|
| Dallas | Spalding 표준 NBA 계약 + Texas assignment | Metu가 같은 계약 계층 | NBA 1경기·1분, Texas 29경기 | 1분 초과 또는 1월 31일 다른 방출 선택 |
| Denver | Welsh 투웨이 + 외부 G League 배정 | Spalding이 Welsh 투웨이 슬롯 대체 | NBA 11경기·36분, G League 20경기 | 36분 초과 또는 다른 출전 날짜 |

이 BASE는 두 선수의 정확한 대체 세계 기록이 아니다. **새 팀에서 공짜 분을 만들지 않는 계약·로스터 출발점**이다.

## Dallas — Metu가 Spalding의 표준 계약 슬롯을 대체

실제 Dallas는 56번 Ray Spalding과 표준 NBA 계약을 맺었고 Texas Legends로 배정했다. Spalding은 Dallas에서 NBA 1경기·1분만 뛰었고 Texas에서는 29경기·26선발·평균 30.1분을 기록했다.

대체 세계의 Metu도 다음 계층에서 시작한다.

- 투웨이가 아닌 표준 NBA 계약
- Texas Legends assignment 가능
- NBA BASE 1경기·1분
- Texas BASE 29경기
- Dallas 핵심 빅맨 분을 자동 차감하지 않음

2019년 1월 31일 Dallas는 New York과의 대형 거래에서 선수 수를 맞추며 Spalding을 방출했다. 대체 세계에서도 Metu가 가장 가까운 방출 후보지만, 선수 평가가 달라질 수 있으므로 **Metu 방출을 자동 확정하지 않는다**. `JAN31_WAIVER_CHOICE_HOLD`로 두고 다음 중 하나가 생길 때만 Dallas 거래층을 다시 연다.

1. Metu가 BASE 1분을 넘겨 실제 다른 선수의 분을 받는다.
2. Dallas가 1월 31일 Metu 대신 다른 선수를 방출한다.
3. 그 선택이 이후 계약·경기 가용성을 바꾼다.

## Denver — Spalding이 Welsh의 투웨이 슬롯을 대체

2018-19 규정에서 팀은 표준 15인 외에 투웨이 선수 두 명을 둘 수 있었다. 실제 Denver의 두 자리는 Thomas Welsh와 DeVaughn Akoon-Purcell이 차지했다.

따라서 58번이 Spalding으로 바뀌면 최소 변화는 다음과 같다.

- Spalding → Welsh가 실제 받은 투웨이 슬롯
- Akoon-Purcell → 두 번째 투웨이 슬롯 유지
- Welsh → 같은 Denver 투웨이 슬롯을 중복 취득할 수 없음

Spalding의 Denver BASE는 Welsh의 실제 11경기·36분과 G League 20경기다. Spalding에게 Dallas의 표준 계약이나 Texas 29경기를 자동 복사하지 않는다. **지명 순번이 아니라 Denver가 실제 58번에게 부여한 계약 구조**를 우선한다.

## Welsh 후속 경로 수정

기존 `PROVISIONAL_ROLE_PRESERVED`는 통과하지 못했다. Denver의 두 투웨이 자리가 Spalding과 Akoon-Purcell로 모두 차므로 Welsh에게 같은 자리를 다시 줄 수 없다.

Welsh는 삭제하지 않는다. 상태를 다음처럼 바꾼다.

```text
PROVISIONAL_ROLE_PRESERVED
→ SUPERSEDED
→ UNDRAFTED_FREE_AGENT_MARKET_HOLD
```

정확한 새 팀·캠프·G League 권리는 당시 관심 증거를 확보하기 전 지정하지 않는다. 다른 NBA 팀이 Welsh와 계약하면 그 팀을 새 파급 가지로 연다. 계약이 없으면 NBA 경기 파급은 0이다.

## Atlanta 직접 대결

| 팀 | 날짜 | 실제 결과 | 실제 대체 슬롯 분 | 팀 쪽 판정 |
|---|---|---|---:|---|
| Dallas | 2018-10-24 | Dallas 104-111 Atlanta | Spalding 0분 | `NO_DIRECT_MINUTES` |
| Dallas | 2018-12-12 | Dallas 114-107 Atlanta | Spalding 0분 | `NO_DIRECT_MINUTES` |
| Denver | 2018-11-15 | Denver 138-93 Atlanta | Welsh 0분 | `NO_DIRECT_MINUTES` |
| Denver | 2018-12-08 | Denver 98-106 Atlanta | Welsh 0분 | `NO_DIRECT_MINUTES` |

네 경기 모두 Dallas·Denver 쪽 실제 대체 슬롯이 0분이었다. 따라서 Metu·Spalding 이동만으로 결과를 바꾸지 않는다. 주인공의 Atlanta 쪽 분과 영향은 별도 player-game 원장에서 계산하므로 경기 결과 자체는 계속 `HOLD`다.

## 방화벽

- Metu에게 San Antonio의 실제 145.4분을 Dallas에서 복사하지 않는다.
- Spalding에게 Dallas의 표준 계약과 Texas 분을 Denver에서 복사하지 않는다.
- Welsh와 Spalding에게 같은 Denver 투웨이 슬롯을 중복 지급하지 않는다.
- Dallas 1분·Denver 36분을 넘기면 날짜별 donor와 경쟁 구간을 연다.
- 1월 31일 Dallas 방출 선택은 Metu의 역할 검증 전 자동 복사하지 않는다.
- Welsh의 새 팀을 편의상 만들지 않는다.
- Atlanta player-game 전에는 Dallas 33-49·Denver 54-28을 대체 세계 확정치로 쓰지 않는다.

## 판정

`CASCADE_CONTRACT_PASS / GAME_OUTCOMES_HOLD`

Dallas·Denver 계약층과 Atlanta 직접 대결의 상대 팀 쪽 0분은 닫혔다. 다음 선행조건은 Atlanta의 날짜별 주인공 가용성·Spellman donor vector다.

## 출처

- [Dallas Mavericks — Ray Spalding signing](https://www.nba.com/mavs/mavericks-sign-forward-ray-spalding)
- [Dallas Mavericks — Porziņģis trade and Spalding waiver](https://www.nba.com/mavs/mavericks-acquire-all-star-kristaps-porzingis-tim-hardaway-jr-courtney-lee-and-trey-burke-in-trade-with-knicks)
- [NBA G League — Ray Spalding](https://gleague.nba.com/player/1629034/ray-spalding)
- [Denver Nuggets — Thomas Welsh two-way contract](https://www.nba.com/nuggets/news/thomas-welsh-signs-two-way-contract-071918)
- [Denver Nuggets — Welsh and Akoon-Purcell two-way preview](https://www.nba.com/nuggets/news/1819-player-previews-akoon-purcell-welsh-091918)
- [NBA G League — contemporaneous two-way roster rule](https://windycity.gleague.nba.com/news/bulls-sign-brandon-sampson-to-two-way-contract)
- [Denver Nuggets — Welsh rookie-season recap](https://www.nba.com/nuggets/news/denver-nuggets-thomas-welsh-excited-for-nba-summer-league-070219c)
- [NBA — 2018-11-15 Atlanta at Denver](https://www.nba.com/game/atl-vs-den-0021800214)
- [Basketball-Reference — 2018-11-15 box score](https://www.basketball-reference.com/boxscores/201811150DEN.html)
- [NBA Hawks — 2018-12-08 Denver at Atlanta](https://www.nba.com/hawks/game/0021800380)
- [Basketball-Reference — 2018-12-08 box score](https://www.basketball-reference.com/boxscores/201812080ATL.html)
