# Chicago 2020-21 Pre-Deadline Player Production Priors v0.1

- 상태: `BOX_PRIOR_RANGE_PASS / TRANSFER_PRODUCTION_PASS / 43_GAME_INPUT_PASS / IMPACT_PROXY_AND_OUTCOME_HOLD`
- 적용 구간: 2020-12-23~2021-03-24, Chicago 43경기
- 상위 역할선: 주인공 43경기·43선발·1,219분, LaMelo Ball 43경기·25선발·1,191분
- 원고 게이트: `CLOSED`

## 결론

마감일 전 BASE 중심선은 다음과 같다.

| 선수 | PTS/36 | REB/36 | AST/36 | STL/36 | BLK/36 | TS | 3PA/36 | 3P | USG |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 주인공 | **14.5** | **9.8** | **3.2** | **1.7** | **1.0** | **.555** | **3.6** | **.335** | **17.0%** |
| LaMelo | **18.0** | **6.8** | **7.2** | **1.7** | **0.4** | **.535** | **6.0** | **.335** | **21.5%** |

역할분을 적용한 참고선은 주인공 **11.42점·7.72리바운드·2.52어시스트**, LaMelo **13.85점·5.23리바운드·5.54어시스트**다. exact 정수 박스와 경기별 실적은 아직 정본이 아니다.

주인공은 3년차에 공격 성장의 보상이 처음 명확히 보이지만 제1옵션은 아니다. LaVine이 1차 득점원이며, LaMelo가 가장 많은 가드 창출을 맡고, Coby의 2차 득점 개발분도 남는다.

## 1. 주인공 3년차 종단 비교군

성과를 본 뒤 성공 사례만 다시 고르지 않는다. 2018-19 루키 prior에서 시작한 9인 윙 비교군을 세 번째 NBA 시즌인 2020-21까지 그대로 추적했다. `CHICAGO_2020_21_THIRD_YEAR_WING_COHORT.csv`가 산술 권위다.

- 8명은 NBA 분을 기록했다.
- Jacob Evans는 NBA 출전분이 없어 `NO_NBA_MINUTES`로 남긴다. 탈락 표본을 삭제하지 않는다.
- active 8인의 중앙값은 약 11.38득점·7.22리바운드·2.29어시스트·1.41스틸·0.70블록, TS .525다.

주인공 BASE가 중앙값보다 높은 것은 무조건적인 연차 성장 때문이 아니다. 2년차에 잠근 약한 손 운반·클로즈아웃 돌파 위에 3년차의 `리바운드 종료→grab-and-go`, 숏롤 첫 패스, 전환 중 방향 전환을 얹은 결과다. 그래도 사용률은 17%이고 타이트 핸들·풀업 창출·상시 point-forward 권한은 없다.

### LOW/BASE/HIGH

| 항목 / 36분 | LOW | BASE | HIGH |
|---|---:|---:|---:|
| PTS | 13.0 | **14.5** | 16.0 |
| REB | 9.0 | **9.8** | 10.6 |
| AST | 2.6 | **3.2** | 3.8 |
| STL | 1.4 | **1.7** | 2.0 |
| BLK | 0.7 | **1.0** | 1.3 |
| TOV | 2.7 | **2.3** | 1.9 |
| PF | 3.6 | **3.2** | 2.8 |
| TS | .525 | **.555** | .580 |
| 3PA | 2.8 | **3.6** | 4.4 |
| 3P | .310 | **.335** | .365 |
| USG | 15.5% | **17.0%** | 18.5% |

BASE에서도 새 볼 운반 비용 때문에 TOV/36은 2년차 2.0에서 2.3으로 오른다. 공격 성장에 실수 비용이 없다는 설계를 금지한다.

## 2. LaMelo Chicago 역할 수축

LaMelo의 Charlotte 손목 부상 전 관측치는 41경기·21선발·1,174:03, 약 **20.0득점·7.36리바운드·7.70어시스트·1.99스틸 / 36분, TS .562, 3P .375**다. 이는 상한을 확인하는 자료이지 Chicago 기록의 복사본이 아니다.

Chicago에서는 LaVine의 1차 득점, Coby의 26:34 개발분, Satoransky의 잔존 조직 역할과 공존한다. 그래서 BASE를 Charlotte 관측치보다 득점·리바운드·어시스트·스틸·효율 모두 낮게 둔다. HIGH만 Charlotte 손목 전 역할과 비슷한 상한이다.

| 항목 / 36분 | LOW | BASE | HIGH |
|---|---:|---:|---:|
| PTS | 16.0 | **18.0** | 20.0 |
| REB | 6.2 | **6.8** | 7.4 |
| AST | 6.2 | **7.2** | 7.8 |
| STL | 1.3 | **1.7** | 2.0 |
| BLK | 0.2 | **0.4** | 0.6 |
| TOV | 4.1 | **3.7** | 3.3 |
| PF | 3.9 | **3.6** | 3.3 |
| TS | .500 | **.535** | .565 |
| 3PA | 5.2 | **6.0** | 6.8 |
| 3P | .300 | **.335** | .375 |
| USG | 19.5% | **21.5%** | 23.5% |

43경기 active는 여전히 계산 BASE다. Charlotte에서 발생한 오른손 손목 골절을 자동 삭제하거나 Chicago에 자동 복사하지 않는다.

## 3. 실제 선수 생산성 이전량

직접 제거된 Patrick Williams·Chandler Hutchison의 마감일 전 실제 생산성을 전부 제거하고, 여섯 secondary donor에는 해당 구간 실제 생산성에 순차감 비율을 선형 적용한다. `CHICAGO_2020_21_PREDEADLINE_TRANSFER_PRODUCTION.csv`가 산술 권위다.

| 제거 계층 | 분 | PTS | REB | AST | STL | BLK | TOV |
|---|---:|---:|---:|---:|---:|---:|---:|
| Patrick+Hutchison 직접 제거 | 1,256:25 | 418.00 | 227.00 | 56.00 | 31.00 | 31.00 | 65.00 |
| secondary donor 순차감 | 1,153:35 | 433.77 | 178.63 | 157.77 | 32.13 | 7.25 | 58.34 |
| 합계 | **2,410:00** | **851.77** | **405.63** | **213.77** | **63.13** | **38.25** | **123.34** |

두 가상 선수 BASE의 박스 귀속 합계와 비교하면 다음 방향이다.

| 항목 | 두 선수 BASE | 제거 관측량 | 귀속 차이 |
|---|---:|---:|---:|
| 득점 | 1,086.49 | 851.77 | **+234.72** |
| 리바운드 | 556.81 | 405.63 | **+151.17** |
| 어시스트 | 346.56 | 213.77 | **+132.79** |
| 스틸 | 113.81 | 63.13 | **+50.68** |
| 블록 | 47.09 | 38.25 | **+8.85** |
| 턴오버 | 200.29 | 123.34 | **+76.95** |

이 표는 선수별 박스 귀속 변화다. **Chicago 팀 득점에 +235점을 더하거나 팀 어시스트에 +133개를 더하는 계산이 아니다.** 두 선수의 높은 사용률과 패스 사건은 LaVine·Coby·Satoransky 및 동료의 슛·어시스트 귀속을 다시 나눈다. 추가 턴오버도 함께 비용으로 남는다.

Young의 0:38 gross bridge는 시즌 순감이 0이므로 aggregate 이전량에서 제외한다. O-15F3 경기별 outcome에서는 두 날짜의 lineup·피로 stress로만 처리한다.

## 4. 43경기 입력 원장

`CHICAGO_2020_21_PREDEADLINE_IMPACT_INPUTS.csv`는 각 날짜의 두 선수 BASE 기대 박스, 날짜별 donor 차감분에 구간 평균 생산성을 선형 적용한 제거량, 둘의 차이를 기록한다.

- 43개 event ID가 O-15F1 minute ledger와 일치한다.
- 두 선수 추가분 합계와 2,410분 제거량이 일치한다.
- 모든 행의 `impact_status`는 `HOLD`다.
- box delta는 다음 outcome 모형의 감사 입력이지 score-margin 변화량이 아니다.

## 5. 방화벽과 다음 단계

- BOX prior 범위: `PASS`
- 실제 선수 생산성 이전량: `PASS`
- 43경기 box attribution 입력: `PASS`
- exact FGA·FTA·ORB/DRB·정수 경기 박스: `HOLD`
- causal impact proxy·점수차 변환: `HOLD`
- alternate 마감일 성적: `HOLD`
- LaMelo 손목 사건: `INJURY_EVENT_HOLD`
- Vučević 및 3팀 거래 발생: `HOLD`

O-15F3에서는 score-margin 잔차를 보존하고 최소 두 impact 계열을 사용한다. 박스 귀속 증가를 팀 득점으로 직접 합산하는 runner는 허용하지 않는다.

## 출처

- [NBA Communications — LaMelo Ball 2020-21 Rookie of the Year](https://pr.nba.com/lamelo-ball-2020-21-kia-nba-rookie-of-the-year/)
- [NBA — 2020-21 Rookie Ladder final](https://www.nba.com/news/kia-rookie-ladder-final-edition-2021)
- [NBA Stats — 2020-21 player traditional data](https://www.nba.com/stats/players/traditional?Season=2020-21&SeasonType=Regular%20Season)
- [NBA Stats — 2020-21 player advanced data](https://www.nba.com/stats/players/advanced?Season=2020-21&SeasonType=Regular%20Season)
- [NBA Stats — Chicago player box scores through 2021-03-24](https://www.nba.com/stats/players/boxscores?DateFrom=12%2F23%2F2020&DateTo=03%2F24%2F2021&Season=2020-21&SeasonType=Regular%20Season&TeamID=1610612741)
- [NocturneBear/NBA-Data-2010-2024 — NBA V3 box-score public mirror](https://github.com/NocturneBear/NBA-Data-2010-2024)
