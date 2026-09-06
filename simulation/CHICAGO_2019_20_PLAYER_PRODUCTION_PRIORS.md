# Chicago 2019-20 Second-Year Production Prior v0.1

- 상태: `BOX_PRIOR_RANGE_PASS / TRANSFER_PRODUCTION_PASS / IMPACT_MODEL_HOLD`
- 기준일: 2026-09-06
- 상위 원장: `simulation/CHICAGO_2019_20_PLAYER_GAME_DONOR_VECTOR.md`
- 적용 역할선: 65경기·18선발·1,395분 `PROVISIONAL_LOCK`
- 원고 게이트: `CLOSED`

## 결론

주인공 2년차 BASE 중심선은 다음과 같다.

> **12.0득점·9.0리바운드·2.2어시스트·1.6스틸·0.9블록 / 36분**  
> **TS .530·3PA 3.0·3P .320·USG 15.0%**

1,395분 환산 중심은 약 **465득점·349리바운드·85어시스트·62스틸·35블록**, 경기당 **7.15득점·5.37리바운드·1.31어시스트·0.95스틸·0.54블록**이다.

이는 조기 스타가 아니다. 루키보다 약한 손 운반·클로즈아웃 돌파와 감속 뒤 짧은 패스가 늘었지만, 하프코트 1차 창조·타이트 핸들·고난도 점퍼는 아직 없다. 팀 공격의 1차 축은 LaVine이고 가드 개발 possession은 Coby·Satoransky에게 남는다.

## 1. 비교군 — 루키 9명을 그대로 추적

성과를 본 뒤 2년차 성공 사례만 고르지 않는다. O-15C1 루키 prior의 9인 비교군을 그대로 2019-20 두 번째 NBA 시즌까지 추적한다.

- Troy Brown Jr.
- Josh Okogie
- Chandler Hutchison
- Jacob Evans
- Rodions Kurucs
- Bruce Brown
- Hamidou Diallo
- Svi Mykhailiuk
- Keita Bates-Diop

2년차에 분이 줄거나 역할을 잃은 선수도 제외하지 않는다. 생존자 편향을 막기 위해 새로운 분 하한을 다시 적용하지 않았다. 단일 수치 권위는 `CHICAGO_2019_20_SOPHOMORE_WING_COHORT.csv`다.

| 항목 | 9인 중앙값 | 주인공 BASE | 위치 |
|---|---:|---:|---|
| PTS/36 | 12.8 | 12.0 | 중앙값 아래 |
| REB/36 | 6.2 | 9.0 | 고유 강점 |
| AST/36 | 2.7 | 2.2 | 1차 창조 미완성 |
| STL/36 | 1.4 | 1.6 | 상위 역할 |
| BLK/36 | 0.5 | 0.9 | 약한 쪽 도움수비 반영 |
| TOV/36 | 2.0 | 2.0 | 새 드라이브의 비용 유지 |
| PF/36 | 3.2 | 3.5 | 수비 완성 선지급 금지 |
| TS | .524 | .530 | 림·전환으로 소폭 상회 |
| 3PA/36 | 3.6 | 3.0 | 슈터 정체성 아님 |
| 3P | .333 | .320 | spacing 약점 잔존 |
| USG | 16.5% | 15.0% | 저사용률 연결자 |

비교군의 NBA Stats net rating 중앙값 -4.7은 관측 환경값일 뿐 인과 impact prior로 사용하지 않는다. 팀·라인업·상대가 다른 값을 주인공에게 복사할 수 없다.

## 2. LOW/BASE/HIGH

| 항목 / 36분 | LOW | BASE | HIGH | 기능 |
|---|---:|---:|---:|---|
| PTS | 10.5 | **12.0** | 13.5 | 전환·컷·풋백·제한적 closeout attack |
| REB | 8.2 | **9.0** | 9.8 | 리바운드→전환 S+ 뿌리 |
| AST | 1.7 | **2.2** | 2.7 | 감속 뒤 짧은 패스, point-forward 아님 |
| STL | 1.3 | **1.6** | 1.9 | 활동량·POA 보조·회복 범위 |
| BLK | 0.6 | **0.9** | 1.2 | 도움수비 타이밍 성장 |
| TOV | 2.4 | **2.0** | 1.6 | 새 운반·돌파의 실수 비용 |
| PF | 4.0 | **3.5** | 3.0 | 손 사용·closeout 편차 |
| TS | .500 | **.530** | .560 | 슛 완성보다 림 빈도 개선 |
| 3PA | 2.3 | **3.0** | 3.7 | 코너 spacing 존중 |
| 3P | .280 | **.320** | .350 | HIGH도 엘리트 슈터 아님 |
| USG | 13.5% | **15.0%** | 16.5% | LaVine·Coby possession 보호 |

각 시나리오는 한 줄로 묶어 사용한다. HIGH 리바운드와 HIGH 슈팅에 LOW 턴오버를 별도 조합하는 식의 능력치 합성은 금지한다.

## 3. 루키에서 2년차로 무엇이 변하는가

BASE /36 기준 변화는 다음과 같다.

| 항목 | 루키 | 2년차 | 변화 |
|---|---:|---:|---:|
| PTS | 9.5 | 12.0 | +2.5 |
| REB | 8.5 | 9.0 | +0.5 |
| AST | 1.7 | 2.2 | +0.5 |
| STL | 1.3 | 1.6 | +0.3 |
| BLK | 0.8 | 0.9 | +0.1 |
| TOV | 1.8 | 2.0 | +0.2, 새 드라이브 비용 |
| TS | .500 | .530 | +.030 |
| 3PA | 2.3 | 3.0 | +0.7 |
| 3P | .280 | .320 | +.040 |

수치 상승의 원인은 `운동능력 자동 성장`이 아니다. 루키 시즌 실패 영상, 약한 손 반복, closeout 첫발, 두 번째 수비가 오기 전 짧은 패스라는 제한된 기술 묶음이다. grab-and-go와 숏롤 첫 패스의 자동화는 2020-21 이후다.

## 4. 실제 선수 생산성 순이전량

O-15C5의 시즌 순차감에 실제 2019-20 선수 시즌 생산성을 선형 적용한다. `CHICAGO_2019_20_TRANSFER_PRODUCTION.csv`가 산술 권위다.

| 순차감 1,395분에서 제거되는 관측 귀속 | 합계 |
|---|---:|
| 득점 | 577.41 |
| 리바운드 | 241.80 |
| 어시스트 | 100.58 |
| 스틸 | 72.62 |
| 블록 | 21.97 |

주인공 BASE와 비교한 선수 박스 귀속 방향은 약 다음과 같다.

| 항목 | 주인공 BASE | 제거 관측량 | 귀속 차이 |
|---|---:|---:|---:|
| 득점 | 465.00 | 577.41 | -112.41 |
| 리바운드 | 348.75 | 241.80 | +106.95 |
| 어시스트 | 85.25 | 100.58 | -15.33 |
| 스틸 | 62.00 | 72.62 | -10.62 |
| 블록 | 34.88 | 21.97 | +12.91 |

이 차이는 **선수별 박스 귀속**이지 팀 총생산성 변화가 아니다. 줄어든 슛·어시스트·스틸 기회 일부는 LaVine·Coby·동료에게 재귀속된다. 특히 `-112득점`을 Chicago 팀 득점에서 그대로 빼거나 `+107리바운드`를 팀 리바운드에 그대로 더하지 않는다.

Markkanen·Dunn의 gross 19:34 bridge는 시즌 순감 0이므로 이 표에 넣지 않았다. O-15C6B에서는 날짜별 fatigue와 lineup 변화로만 다룬다.

## 5. impact 방화벽

O-15C2B가 점수차 없는 Bernoulli runner의 구조적 결함을 확인했다. 따라서 이번 단계에서 BPM·net rating 하나를 골라 65경기 승패를 실행하지 않는다.

- 박스 prior: `PASS`
- 시즌 생산성 순이전: `PASS`
- exact FGA·FTA·ORB/DRB·정수 박스: `HOLD`
- causal impact proxy: `HOLD`
- 65경기 outcome·정확 승수: `HOLD`
- 2020 standings·lottery·Patrick Williams: `HOLD`

O-15C6B에서는 같은 player-game 원장에 최소 두 개의 score-margin impact proxy를 적용하고, Markkanen·Dunn bridge와 back-to-back 피로를 독립 stress로 둔다.

## 출처

- [NBA Stats — 2019-20 sophomore traditional per-36](https://www.nba.com/stats/players/traditional?PerMode=Per36&PlayerExperience=Sophomore&Season=2019-20&SeasonType=Regular%20Season)
- [NBA Stats — 2019-20 sophomore advanced](https://www.nba.com/stats/players/advanced?PlayerExperience=Sophomore&Season=2019-20&SeasonType=Regular%20Season)
- [NBA Stats — Chicago 2019-20 선수 totals](https://www.nba.com/stats/team/1610612741/players-traditional?Season=2019-20&SeasonType=Regular%20Season)

