# 2021 Washington–Chicago–Portland Transaction Cascade

- 기준일: 2026-09-06
- 선행 가정: `Chicago 22 protagonist → Golden State 28 Hutchison → Portland 37 Evans → Lakers 39 Trent → Washington 44 Bonga → Sanon undrafted/Olimpija`
- 판정: `CONDITIONAL_TRANSACTION_STRUCTURE_PASS / PORTLAND_NO_TRADE_PRIMARY / EXACT_OUTCOMES_HOLD`
- 정본성: 선행 드래프트 사슬과 2020-21 팀 성적이 확정되지 않았으므로 계산 후보이며 정본이 아니다.

## 왜 2021 거래를 지금 보되 잠그지는 않는가

2018 드래프트에서 밀린 선수의 계약·거래 기능이 몇 년 뒤 원역사와 충돌하는지는 지금 구조 감사한다. 그러나 2021년 실제 거래가 대체 역사에서도 발생하는지는 2018-19부터 시즌별 승수·로터리·로스터를 시간순으로 계산한 뒤 결정한다.

따라서 이번 감사는 두 질문만 닫는다.

1. Chicago에 Chandler Hutchison이 없더라도 2021년 실제 세 팀의 목적을 만족하는 합법적 거래 구조가 존재하는가.
2. Portland에 Gary Trent Jr.가 없을 때 Norman Powell 거래를 누구로 자동 복사하지 않고 시작할 기준선은 무엇인가.

## 실제 2021 Chicago–Washington–Boston 기준선

2021년 3월 25일 실제 거래는 다음과 같았다.

| 팀 | 보냄 | 받음 | 실제 핵심 기능 |
|---|---|---|---|
| Chicago | Daniel Gafford, Chandler Hutchison, Luke Kornet | Daniel Theis, Javonte Green, Troy Brown Jr. | Nikola Vučević 영입 뒤 센터·수비 뎁스 보강 |
| Washington | Troy Brown Jr., Moritz Wagner | Daniel Gafford, Chandler Hutchison | 센터 운동능력·림 보호 보강 |
| Boston | Daniel Theis, Javonte Green | Moritz Wagner, Luke Kornet | 세금 절감과 빅맨 재구성 |

대체 역사에서 Hutchison은 Chicago 선수가 아니다. 실제 전체 귀환을 그대로 복사하면 Chicago는 Gafford와 Kornet의 합계 $3,767,981만 보내고 Theis·Green·Brown 합계 $9,890,821을 받는다. 2017 CBA의 해당 비납세팀 동시 거래 허용액 $6,693,967을 넘으므로 원거래는 불성립한다. 현금은 salary matching을 고치지 못하고, 주인공이나 Washington의 Trent를 Hutchison 자리에 자동 삽입해서도 안 된다. 참고로 실제 Hutchison 급여는 $2,443,440이며 실제 Chicago outgoing 합계는 $6,211,421이다.

## Hutchison 없는 최소 6인 구조

### 이동

| 팀 | 보냄 | 받음 |
|---|---|---|
| Chicago | Gafford → Washington, Kornet → Boston | Theis, Green ← Boston |
| Washington | Wagner → Boston | Gafford ← Chicago |
| Boston | Theis, Green → Chicago | Wagner ← Washington, Kornet ← Chicago |

Troy Brown Jr.와 Gary Trent Jr.는 Washington에 남는다. Hutchison은 Golden State 후보 분기에 있으므로 이 거래에 등장하지 않는다. 실제 현금 $1.3m와 $0.25m는 이 구조의 필수 조건이 아니며 정확한 현금 이동은 `HOLD`다.

### 2020-21 급여 검산

| 팀 | outgoing | incoming | 허용 검산 | 판정 |
|---|---:|---:|---:|---|
| Chicago | $3,767,981 | $6,517,981 | 비납세 구간 `175% + $100,000 = $6,693,967` | `PASS`, 여유 $175,986 |
| Washington | $2,161,920 | $1,517,981 | incoming이 outgoing보다 작음 | `PASS` |
| Boston | $6,517,981 | $4,411,920 | 납세팀의 더 엄격한 `125% + $100,000`에도 통과 | `PASS` |

이 계산은 계약의 기본급을 사용한 구조 감사다. trade bonus·unlikely bonus·당일 팀 급여의 정확한 리그 장부는 거래 발생을 정본화할 때 다시 확인한다.

### 팀 동기 검산

- Chicago는 실제 거래의 중심이던 Theis를 받아 Vučević 뒤 센터층을 보강하고 Green의 수비 에너지도 얻는다. Brown을 얻지 못하는 것이 Hutchison 부재의 실제 비용이다.
- Washington은 Wagner를 Gafford로 바꾸며 Thomas Bryant 공백 뒤 림 러닝·수비 기능을 얻는다. 실제 거래에서 부차적으로 받은 Hutchison의 윙 뎁스는 Trent와 잔류 Brown이 있는 대체 로스터에서는 필수 조건이 아니다.
- Boston은 Theis와 Green을 내보내 Wagner와 Kornet을 받으므로 실제의 세금 절감 방향을 보존한다.

판정은 `CAP_PASS / TEAM_MOTIVE_PASS / CONDITIONAL_PRIMARY_LEAN`이다. Chicago가 2021년 3월에도 실제와 같은 플레이인 추격·Vučević 후속 보강 동기에 도달한다는 뜻은 아니다. 그 발생 여부는 O-15B~D의 시즌·로터리·Vučević 거래 계산 뒤 결정한다.

## Gary Trent Jr.의 Washington 경로와 2021 RFA

### 계약·권리

- Lakers 39 Trent 후보가 실제 Portland 계약과 같은 3년 최소급 구조를 받으면 2019 Anthony Davis 3팀 거래로 Washington에 이동할 수 있다.
- 2라운드 지명자의 계약이 첫 세 시즌 뒤 끝날 때 구단이 qualifying offer를 제시하면 2017 CBA상 RFA가 된다.
- 세 시즌의 Bird clock은 첫 시즌 뒤 거래로 팀을 옮겨도 이어지므로 Washington은 2021년에 Bird 권리를 이용해 cap을 넘겨 재계약할 제도 경로를 가진다.
- 정확 QO는 대체 역사 Trent의 2020-21 선발·총분과 단축 시즌 적용을 확인해야 한다. 실제 Toronto의 QO·3년 약 $52m 계약을 Washington에 복사하지 않는다.

### 거래 마감일 판정

| 후보 | 판정 | 이유 |
|---|---|---|
| Washington이 Trent 유지 | `PRIMARY_BASELINE` | 위 6인 구조가 Trent 없이 성립한다. 값이 미확정인 젊은 슈터를 salary filler로 내보낼 이유를 새로 만들지 않는다. |
| Trent를 Chicago로 보내 Hutchison 대체 | `REJECT_AUTOMATIC_SUBSTITUTION` | 포지션·계약 껍질이 비슷해도 선수 가치와 팀 필요가 다르며, Chicago 주인공의 윙 분과도 새로 충돌한다. |
| Trent를 Boston으로 이동 | `LOW / MOTIVE_BLOCKED` | Boston의 실제 목적은 세금·로스터 정리이며 추가 젊은 가드를 요구했다는 근거가 없다. |
| Washington이 별도 팀에 Trent 거래 | `MARKET_HOLD` | 대체 역사 2019-21 생산과 제안 자산이 있어야 판정 가능하다. |

따라서 `TRENT_DEADLINE_KEEP_PRIMARY / RFA_CONTROL_PATH_PASS / EXACT_QO_AND_CONTRACT_HOLD`다. Brown 잔류와 Trent의 동시 보유는 Washington 윙·가드 분을 바꾸므로 2019-21 player-game 원장에서 비용을 치른다.

Trent를 Chicago로 보내는 별도 계산은 급여상 가능하다. Chicago가 Gafford·Kornet을 보내고 Theis·Trent를 받으면 incoming $6,663,861로 허용액보다 $30,106 낮다. 하지만 Washington이 받는 Gafford·Green이 Trent의 대체 역사 가치에 충분한지는 그의 2019-21 생산 없이는 판정할 수 없다. 따라서 이 안은 `CAP_PASS / VALUE_HOLD`이며 주 분기가 아니다.

## 실제 Portland–Toronto Powell 거래 기준선

실제 Portland는 2021년 3월 25일 Trent와 Rodney Hood를 보내고 Norman Powell을 받았다. Hood는 주로 급여와 차기 시즌 유동성, Trent는 22세 득점·슈팅과 RFA 통제권이었다. Portland는 과세선 위에서 Powell의 Bird 권리를 함께 받아 2021년 여름 5년 $90m 재계약을 할 수 있었다.

대체 역사에서는 Portland가 37에서 Jacob Evans를 뽑았으므로 Trent가 없다. Hood만으로 Powell의 급여 매칭은 가능하지만, Toronto가 실제로 받은 젊은 자산의 가치는 사라진다.

## Portland 대안 보드

| 후보 | 급여/권리 | 가치·팀 판단 | 판정 |
|---|---|---|---|
| Portland 거래 철수 | 급여 계산 불필요 | Simons·Little을 지키고 Evans에게 Trent 생산을 선물하지 않음 | `PRIMARY_BASELINE` |
| Hood + Evans | 구조상 가능 후보 | Evans가 2021년까지 검증된 20분대 3&D가 됐다는 별도 성과표 없이는 Toronto가 Trent 대신 받을 가치 부족 | `CONDITIONAL_ONLY` |
| Hood + Nassir Little + 미래 2라운드 | 구조상 가능 후보 | 젊은 윙 통제권을 주지만 Little의 실제 Portland 성장 경로를 새로 이동시킴 | `BEST_POWELL_ACQUISITION_ALT / NOT_LOCKED` |
| Hood + Anfernee Simons | 구조상 가능 | Toronto 수용성은 높지만 Portland가 더 큰 Aaron Gordon 협상에서도 보호한 상한 자산을 expiring Powell에 쓰는 반증이 큼 | `PORTLAND_REJECT_LEAN` |
| Hood + Zach Collins | 구조상 검토 가능 | 부상, 2021 RFA, 높은 QO/cap hold가 Toronto의 유동성 목적에 불리 | `REJECT` |
| Hood + 미래 1라운드 | 보호픽 조정 선행 필요 | Covington 거래의 2021 보호 1라운드로 미래 픽 운용이 묶여 있고 expiring Powell에 과도함 | `LOW` |

현재 판정은 `PORTLAND_NO_TRADE_PRIMARY`다. 이것은 Powell이 반드시 Toronto에 남는다는 뜻이 아니다. Knicks·Philadelphia 등 당시 시장 후보 또는 Toronto 잔류를 별도 비교해야 하므로 `POWELL_DESTINATION_HOLD`다.

## 나비효과 원장

| 최초 원인 | 달라지는 실제 사건 | 밀려나는 자산·역할 | 다음 연결 | 현 상태 |
|---|---|---|---|---|
| Chicago 22에서 주인공 후보 | Hutchison이 Chicago에 없음 | Chicago의 Brown 수취와 Washington의 Hutchison 수취 제거 | Brown·Trent Washington 분, Chicago 2021 wing minutes | 6인 대체 구조 `CONDITIONAL_PASS`; 발생은 O-15D HOLD |
| Portland 37 Evans 후보 | Trent가 Portland에 없음 | Powell 거래의 핵심 젊은 RFA 자산 제거 | Powell 시장, Portland playoff minutes, 2021 Bird rights | `PORTLAND_NO_TRADE_PRIMARY`; 정확 행선지 HOLD |
| Lakers 39 Trent 후보 | 2019 AD 거래로 Trent가 Washington 이동 | 실제 Bonga의 Washington NBA 자리 제거 | Trent 2019-21 생산·RFA, Bonga stash 경로 | 권리 구조 PASS; 분·계약 HOLD |
| Portland가 Powell을 못 얻음 | 실제 2021-22 Powell 5년 $90m Portland 계약의 선행 Bird 권리 없음 | Powell의 Portland 27경기·플레이오프 분과 후속 Clippers 거래 자동 보존 금지 | 2021 FA·2022 Portland 거래 원장 | `DOWNSTREAM_OPEN`, 해당 시즌 도달 때 계산 |

## 인과 경계

- 2021 세 팀 거래는 Hutchison 없이도 합법적이고 동기가 맞는 6인 구조가 존재하므로 **구조 blocker는 닫힌다**.
- 실제 거래 발생은 Chicago의 대체 2020-21 성적·Vučević 거래·플레이인 추격 동기가 아직 없으므로 **시간순 시뮬레이션 blocker가 남는다**.
- Portland의 판단은 Trent 대체자를 공짜로 만들지 않는 `NO_TRADE`에서 시작한다. Powell의 정확 행선지는 2021 시장 원장의 새 분기이며, Chicago 2018 착지 구조를 역으로 막지는 않는다.
- 따라서 2018 드래프트 후속 거래의 사전 구조 감사는 `TRANSACTION_CASCADE_SCREEN_PASS`, 정확 Chicago 22와 모든 후속 거래의 정본화는 계속 `HOLD`다.

## 맹점 방화벽

1. Trent의 실제 Portland 버블 성장과 2021 Toronto 계약을 Washington 경로에 복사하지 않는다.
2. Brown이 Washington에 남으면 실제 Chicago 분과 이후 거래·계약을 보존하지 않는다.
3. Powell이 Portland에 없으면 그의 27경기·플레이오프 분을 Evans·Hood·Simons 한 명에게 몰아주지 않는다.
4. Portland가 거래를 안 했다는 이유만으로 Powell의 Toronto 잔류·2021 UFA 목적지를 확정하지 않는다.
5. 2021 구조가 법적으로 가능하다는 사실을 거래 발생 확정으로 바꾸지 않는다. 2018-19부터 시간순 계산이 우선이다.
6. 미래 역사를 덜 바꾸는 선택을 목표함수로 쓰지 않는다. 당시 팀 필요·계약·자산가치가 먼저다.

## 출처

- [Chicago Bulls — 2021 세 팀 거래](https://www.nba.com/bulls/news/bulls-complete-three-team-trade-wizards-celtics)
- [Washington Wizards — Gafford·Hutchison 취득](https://www.nba.com/wizards/wizards-acquire-gafford-and-hutchison)
- [Boston Celtics — Wagner·Kornet 취득](https://www.nba.com/celtics/news/pressrelease/celtics-acquire-moe-wagner-luke-kornet-3-team-trade)
- [Washington Wizards — Gafford의 운동능력·수비 기능](https://www.nba.com/wizards/wizards-add-athleticism-defense-with-gafford-hutchison-trade)
- [NBA CBA 101 — Bird, RFA, trade matching](https://cdn.nba.com/manage/2021/03/2018-19-CBA.pdf)
- [NBA — Toronto의 Trent qualifying offer](https://www.nba.com/news/raptors-extend-qualifying-offers-to-gary-trent-jr-and-nando-de-colo)
- [NBA — 2021 거래 마감일 기록](https://www.nba.com/news/trade-deadline-deals-all-time-history)
- [Toronto Raptors — Trent·Hood 취득](https://www.nba.com/raptors/raptors-acquire-trent-jr-and-hood-portland)
- [NBA — Powell–Trent 거래](https://www.nba.com/news/report-raptors-trade-norman-powell-to-blazers)
- [Portland — Powell 재계약](https://www.nba.com/blazers/news/2021/8/6/trail-blazers-re-sign-norman-powell)
- [Portland — Covington과 2021 보호 1라운드 거래](https://www.nba.com/blazers/forwardcenter/report-trail-blazers-trade-robert-covington)
- [CBS Sports — Powell 거래의 Trent RFA·Hood 계약 기능](https://www.cbssports.com/nba/news/norman-powell-trade-deadline-grades-raptors-add-value-with-gary-trent-jr-trail-blazers-get-more-firepower/)
- [Blazer's Edge — Aaron Gordon 협상에서 Simons 보호 보도](https://www.blazersedge.com/2021/4/13/22382491/trail-blazers-aaron-gordon-nba-rumors-anfernee-simons-not-included-trade-package-pursuit)
