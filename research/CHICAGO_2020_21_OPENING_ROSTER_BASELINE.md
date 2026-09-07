# Chicago 2020-21 Opening Roster & Minute Baseline

- 상태: `EVIDENCE_BASELINE_PASS / 15_PLUS_2_STRUCTURE_PASS / DEADLINE_EVENTS_HOLD`
- 적용 범위: O-15F 실제 opening roster·계약 계층·정규시즌 총분·대체 세계 직접 치환
- 선행 정본: `2020 Draft 1~60 AUTHOR_APPROVED / LOCKED`
- 원고 게이트: `CLOSED`

## 결론

실제 Chicago의 2020-21 개막 명단은 **표준계약 15명 + 투웨이 2명**이었다. 대체 세계에서는 `Chandler Hutchison → 주인공`, `Patrick Williams → LaMelo Ball` 두 자리만 1대1로 바뀐다. 따라서 별도 방출 없이도 **표준계약 15명 + 투웨이 2명**이 그대로 성립한다.

LaMelo는 Patrick과 같은 전체 4순위 슬롯이므로 2020-21 rookie-scale 구조도 같은 자리에서 치환된다. 4순위 실제 첫해 금액 $7,068,360을 계약 계산 기준선으로 둘 수 있다. 다만 주인공은 정확한 2018 지명 순번이 아직 `HOLD`이므로 Hutchison과 정확 급여가 같다고 잠그지 않는다. 두 사람 모두 1라운드 표준계약이라는 계약 계층과 로스터 자리만 통과한다.

## 1. 실제 opening roster

`simulation/CHICAGO_2020_21_ROSTER_MINUTE_BASELINE.csv`가 선수·계약 계층·정규시즌 Chicago 총분의 단일 산술 원장이다.

| 구분 | 선수 수 | 대체 세계 처리 |
|---|---:|---|
| 표준계약 | 15 | Hutchison 대신 주인공, Patrick 대신 LaMelo |
| 투웨이 | 2 | Devon Dotson·Adam Mokoka 유지 |
| 합계 | 17 | roster cut 불필요 |

Marko Simonović는 draft-and-stash 선수이므로 2020-21 Chicago 15인 또는 투웨이 자리를 차지하지 않는다.

## 2. 실제 시즌 총분 기준선

실제 Chicago는 단축된 72경기에서 31승 41패를 기록했다. 선수별 Chicago 소속 총분은 **17,380분**, 선발 자리는 **360개**다. 72×240분보다 100분 많은 것은 팀 기준 연장 4회분에 해당한다.

| actual player | G/GS | MIN | opening status |
|---|---:|---:|---|
| Coby White | 69/54 | 2,156 | opening |
| Zach LaVine | 58/58 | 2,034 | opening |
| Patrick Williams | 71/71 | 1,983 | opening; LaMelo 직접 치환 |
| Thaddeus Young | 68/23 | 1,652 | opening |
| Garrett Temple | 56/25 | 1,528 | opening |
| Lauri Markkanen | 51/26 | 1,317 | opening |
| Tomas Satoransky | 58/18 | 1,307 | opening |
| Denzel Valentine | 62/3 | 1,036 | opening |
| Nikola Vucevic | 26/26 | 848 | deadline in |
| Wendell Carter Jr. | 32/25 | 792 | deadline out |
| Daniel Theis | 23/14 | 574 | deadline in |
| Otto Porter Jr. | 25/6 | 540 | deadline out |
| Ryan Arcidiacono | 44/0 | 450 | opening |
| Daniel Gafford | 31/11 | 383 | deadline out |
| Troy Brown Jr. | 13/0 | 237 | deadline in |
| Javonte Green | 16/0 | 128 | deadline in |
| Luke Kornet | 13/0 | 94 | deadline out |
| Cristiano Felicio | 18/0 | 84 | opening |
| Al-Farouq Aminu | 6/0 | 67 | deadline in |
| Chandler Hutchison | 7/0 | 64 | opening; 주인공 직접 치환 |
| Adam Mokoka | 14/0 | 56 | two-way |
| Devon Dotson | 11/0 | 50 | two-way |

## 3. 직접 치환과 추가 분 필요량

실제 제거 선수의 시즌 총분은 `Patrick 1,983 + Hutchison 64 = 2,047분`이다. 대체 세계의 provisional BASE는 다음과 같다.

| 선수 | BASE | 기능 |
|---|---:|---|
| 주인공 | 68경기·58선발·1,938분·28.5 MPG | 선발 SF/PF, POA 보조수비, 리바운드→grab-and-go, 숏롤 첫 패스 |
| LaMelo | 64경기·32선발·1,760분·27.5 MPG | 1차 창출 후보, 전환 패스, 장신 볼핸들러 |
| 합계 | 3,698분 | direct pool보다 1,651분 큼 |

따라서 `3,698 - 2,047 = 1,651분`은 다른 실제 선수에게서 같은 날짜로 이전해야 한다. 이 수치는 **배분 완료값이 아니라 O-15F1 player-game 원장의 BASE 목표량**이다.

LaMelo의 Charlotte 실제 51경기·31선발·28.8분과 신인왕은 결과 비교 자료일 뿐 Chicago 기록으로 복사하지 않는다. 특히 2021년 손목 부상은 경기·상대·낙상 사건이 바뀌므로 자동 보존도 자동 삭제도 하지 않고 `INJURY_EVENT_HOLD`로 둔다.

## 4. donor 우선순위

| 층 | 선수 | 실제 총분 | 이유와 제한 |
|---|---|---:|---|
| 1 | Satoransky | 1,307 | LaMelo와 1차 볼 운반 기능이 가장 직접 중복; 존재·베테랑 조직 기능 유지 |
| 1 | Valentine | 1,036 | 보조 창출·윙 분 중복; 슈팅 기능과 일부 rotation 표본 유지 |
| 1 | Arcidiacono | 450 | 3~4번째 가드 분; roster 존재와 비상 ball security 유지 |
| 2 | Coby White | 2,156 | 선발 PG 실험이 LaMelo와 충돌; 삭제 금지, 유의미한 득점 개발분 유지 |
| 2 | Temple | 1,528 | 일부 가드/윙 분은 이동 가능하나 세 가드 조합의 수비 바닥 때문에 대폭 차감 금지 |
| 조건부 | Porter | 540 | 실제 가용 경기에서만 포워드 분 이동 가능; 결장분을 공짜 예산으로 쓰지 않음 |

LaVine·Markkanen·Young은 첫 donor 층에서 제외한다. Carter·Gafford·Kornet·Felicio의 센터 분도 가드/윙 두 명에게 직접 넘기지 않는다. 정확 1,651분은 경기별 active list와 포지션 조합을 통과해야 한다.

## 5. deadline 방화벽

실제 2021-03-25 Chicago는 Carter·Porter와 두 개의 1라운드 지명권을 Orlando에 보내 Vucevic·Aminu를 받았다. 같은 날 Gafford·Hutchison·Kornet이 나가고 Theis·Troy Brown Jr.·Javonte Green이 들어오는 3팀 거래도 했다.

대체 세계에서는 Hutchison이 2018년부터 Chicago에 없으므로 두 번째 실제 거래는 **원형 그대로 법적으로 발생할 수 없다**. 기존 구조 검토가 제시한 `Chicago Theis+Green / Washington Gafford / Boston Wagner+Kornet` 최소 대안은 가능성 검사를 통과했지만 사건 발생은 아직 `HOLD`다. Vucevic 거래도 대체 세계의 2021-03-24까지 성적·포지션 수요·픽 가치가 계산되기 전에는 확정하지 않는다.

그러므로 MIDSEASON 다섯 선수의 1,854분은 현재 donor pool이나 확정 유입분이 아니다. 먼저 opening roster로 마감일 전 경기들을 실행한 뒤 거래 발생 여부를 판정한다.

## 6. 다음 계산

1. 2020-12-23부터 2021-03-24까지 실제 active list·선발·분을 날짜별로 적재한다.
2. Patrick·Hutchison 분을 주인공·LaMelo에게 직접 연결한다.
3. 부족한 BASE 1,651분을 donor 우선순위에서 같은 날짜로 이전한다.
4. 주인공·LaMelo·Coby의 선발 및 볼 운반 역할을 단계적으로 재배치한다.
5. 마감일 직전 대체 승수와 팀 수요가 나온 뒤 Vucevic 거래와 3팀 거래를 각각 판정한다.

## 출처

- [Chicago Bulls — 2020-21 roster preview](https://www.nba.com/bulls/features/sam-smiths-2020-2021-chicago-bulls-roster-preview-0)
- [RealGM — Chicago 2020-21 opening day roster](https://basketball.realgm.com/nba/teams/Chicago-Bulls/4/Rosters/Opening_Day/2021)
- [NBA — 2020-21 15인 active roster와 투웨이 2자리](https://www.nba.com/news/teams-allowed-to-carry-15-players-on-active-roster-for-2020-21-season)
- [NBA — 2020-21 Chicago season preview](https://www.nba.com/news/2020-21-season-preview-chi)
- [NBA Stats — Chicago 2020-21 선수 총계](https://www.nba.com/stats/team/1610612741/players-traditional?Season=2020-21&SeasonType=Regular%20Season&PerMode=Totals)
- [Basketball-Reference — Chicago 2020-21 roster and totals](https://www.basketball-reference.com/teams/CHI/2021.html)
- [NBA Communications — LaMelo 2020-21 실제 신인왕·51경기 기준선](https://pr.nba.com/lamelo-ball-2020-21-kia-nba-rookie-of-the-year/)
- [Chicago Bulls — Vucevic·Aminu 거래](https://www.nba.com/bulls/features/bulls-acquire-all-star-nikola-vucevic-and-al-farouq-aminu-blockbuster-trade)
- [Chicago Bulls — Washington·Boston 3팀 거래](https://www.nba.com/bulls/news/bulls-complete-three-team-trade-wizards-celtics)
