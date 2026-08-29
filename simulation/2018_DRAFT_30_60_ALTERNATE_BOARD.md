# 2018 Draft Picks 30-60 Alternate Board v1.0

- 상태: `PASS_WITH_SECOND_TEAM_IMPACT_HOLD`
- 범위: 주인공의 Atlanta 30순위 지명 이후 30~60순위
- 원고 게이트: `CLOSED`
- 계산 권위: `simulation/ATLANTA_2018_19_CAUSALITY_LEDGER.xlsx`의 `2018 Draft Board`

## 결론

31개 픽을 모두 원장상 확인하되, 실제 결과와 다른 픽은 네 개로 제한한다.

| 순번 | 실제 | 대체 세계 | 판정 | 직접 하류 파급 |
|---:|---|---|---|---|
| 30 | Atlanta — Omari Spellman | Atlanta — 주인공 | CHANGED | Atlanta 로스터·분·82경기 |
| 49 | San Antonio — Chimezie Metu | San Antonio — Omari Spellman | CHANGED | Spurs 2018-19 분·경기 |
| 56 | Dallas — Ray Spalding | Dallas — Chimezie Metu | CASCADE | Dallas 계약·분 |
| 58 | Denver — Thomas Welsh | Denver — Ray Spalding | CASCADE | Denver 계약·투웨이 슬롯 |

나머지 27개 픽은 `UNCHANGED`다. 한 명이 밀렸다는 이유로 31번부터 전원을 한 칸씩 미루지 않는다.

## 왜 34번 Atlanta가 Spellman을 다시 뽑지 않는가

실제 34번은 Atlanta가 독자적으로 선수를 고른 뒤 보유한 픽이 아니다. Charlotte가 Devonte' Graham의 권리를 받으며 2019년·2023년 2라운드 픽 두 장을 Atlanta에 줬다.

대체 세계에서 Atlanta는 이미 30번으로 주인공이라는 개발형 포워드 자리를 채웠다. 같은 구간에서 Spellman까지 중복 지명하는 것보다 Charlotte가 지시한 가드 선택과 두 장의 미래 자산을 유지하는 편이 당시 거래 입력에 맞다.

## Spellman 통과 게이트

| 순번 | 팀 | 유지 이유 |
|---:|---|---|
| 39 | Lakers | 25번으로 Moritz Wagner를 이미 지명해 스트레치 빅 개발 슬롯이 겹친다. Isaac Bonga의 장기 윙/볼핸들러 프로필을 유지한다. |
| 40 | Brooklyn | Nets는 Rodions Kurucs를 장기간 추적했다. Spellman이 남았다는 이유만으로 실제 스카우팅 우선순위를 폐기하지 않는다. |
| 44 | Washington | Wizards는 당시 계약 선수 수와 추가 로스터 계획 때문에 해외 스태시 Issuf Sanon을 의도적으로 택했다고 설명했다. |
| 49 | San Antonio | Spellman은 Spurs 워크아웃을 거쳤고, 동시대 최종 보드에서도 패싱·슈팅·역할 이해도가 Spurs에 맞는 선수로 평가됐다. 여기서 첫 명확한 역전이 발생한다. |

CBS의 최종 목 드래프트는 Spellman을 Lakers 39번에, Sports Illustrated는 Washington 44번에 놓았다. 이는 그가 30번 이후 즉시 사라질 선수가 아니라는 증거지만, 목 드래프트의 순번을 실제 선택처럼 복사하지는 않는다. 각 팀의 중복 포지션·스카우팅·스태시 의도를 별도로 적용한 뒤 San Antonio 49번에서 닫는다.

## 제한된 연쇄 이동

### 56번 Dallas — Chimezie Metu

Metu는 실제 49번 선수다. Spellman에게 자리를 내줘도 운동능력형 PF/C라는 프로필과 2라운드 보드 지위가 사라지지 않는다. Dallas가 실제로 확보한 56번·60번 거래 구조를 유지하면서 56번의 Ray Spalding 대신 Metu를 택한다.

### 58번 Denver — Ray Spalding

Spalding은 동시대 NBA 빅맨 보드에서 지명 가능한 2라운드 그룹에 있었고 Thomas Welsh는 그 아래 `in the mix` 그룹이었다. Denver의 개발형 빅 슬롯은 유지하되 58번에서 Spalding이 Welsh를 앞선다.

### Thomas Welsh — 미지명 후 역할 보존 후보

Welsh는 실제로 Denver와 투웨이 계약을 맺었다. 대체 세계에서도 미지명 자유계약으로 Denver 투웨이 후보가 되는 것이 가장 작은 변화다. 다만 Denver가 Spalding을 지명한 뒤 같은 투웨이 슬롯과 계약 구조가 그대로 성립하는지는 아직 검산하지 않았으므로 `PROVISIONAL_ROLE_PRESERVED`다.

## 승수 파급 안전선

Spellman이 들어가는 자리는 실제 Metu의 신인 슬롯이다. Metu의 2018-19 San Antonio NBA 역할은 29경기·145분, 평균 5.0분으로 대부분 가비지타임이었다. 따라서 Spellman에게 Atlanta의 실제 805분을 그대로 복사하지 않는다.

현 단계의 사전 안전선은 다음과 같다.

- San Antonio의 실제 48승 34패는 불변 결과가 아니라 기준선이다.
- Spellman의 NBA 분은 우선 Metu의 145분 개발 슬롯에서 시작한다.
- Austin Spurs 배정과 계약 차이 때문에 추가 분이 생기면 같은 날짜의 실제 가용 선수 분에서 차감한다.
- Atlanta와 San Antonio의 두 직접 대결은 양쪽 로스터 파급이 함께 닿는 경기로 승격한다.
- Spurs의 날짜별 가용성·Spellman 분·결과 영향이 닫히기 전 2019 standings와 lottery는 `FINAL` 금지다.

## 계산량 통제 판정

- 전수 확인: 31픽
- 실제 유지: 27픽
- 직접 변경: 2픽
- 연쇄 변경: 2픽
- 심층 추적 팀: Atlanta·San Antonio·Dallas·Denver
- 승수 재계산이 즉시 필요한 두 번째 팀: San Antonio

Dallas의 56번과 Denver의 58번은 우선 계약·로스터 분 원장만 연다. 정규시즌 핵심 로테이션을 실제로 침범했다는 증거가 나오기 전에는 전 경기 승수 모델로 확장하지 않는다.

## 다음 게이트

1. San Antonio의 2018-19 날짜별 Metu NBA/G League 이동과 145분을 원장화한다.
2. Spellman의 계약·Austin assignment·출장 안전선을 사전등록한다.
3. Atlanta–San Antonio 두 경기와 Spurs 전체 로스터 파급을 판정한다.
4. Dallas의 Metu, Denver의 Spalding·Welsh가 실제 정규시즌 분을 바꾸는지 계약층에서 검사한다.
5. 그 뒤에만 Atlanta·상대팀 승패와 2019 순위·로터리를 계산한다.

## 출처

- [NBA — 2018 Draft Trade Tracker](https://www.nba.com/2018-draft-trade-tracker)
- [Atlanta Hawks — actual 2018 picks](https://www.nba.com/hawks/news/hawks-acquire-trae-young-select-kevin-huerter-omari-spellman-2018-nba-draft)
- [San Antonio Express-News — Spurs target Spellman for workout](https://www.expressnews.com/spurs-nation/article/Spurs-target-Villanova-s-Spellman-others-for-12994749.php)
- [Sports Illustrated — final 2018 mock and Spellman/Spurs fit](https://www.si.com/nba/2018/06/21/nba-mock-draft-2018-trade-rumors-final-picks-deandre-ayton-trae-young)
- [CBS Sports — final 2018 mock](https://www.cbssports.com/college-basketball/news/2018-nba-mock-draft-final-look-and-projection-of-both-rounds-before-teams-pick-thursday-night/)
- [Washington Wizards — Issuf Sanon roster/stash plan](https://www.nba.com/wizards/wizards-plan-second-round-pick-issuf-sanon)
- [Brooklyn Nets — Rodions Kurucs scouting history](https://www.nba.com/nets/news/feature/2018/12/28/brooklyn-nets-rookie-rodions-kurucs-had-a-breakout-month-in-december)
- [NBA — 2018 big-man board](https://www.nba.com/da-big-board-bigs-2018-draft)
- [Denver Nuggets — Thomas Welsh two-way contract](https://www.nba.com/nuggets/news/thomas-welsh-signs-two-way-contract-071918)
- [Basketball-Reference — Chimezie Metu](https://www.basketball-reference.com/players/m/metuch01.html)
- [Pounding the Rock — Chimezie Metu rookie-season review](https://www.poundingtherock.com/2019/5/4/18523491/2018-2019-spurs-player-reviews-chimezie-metu)
