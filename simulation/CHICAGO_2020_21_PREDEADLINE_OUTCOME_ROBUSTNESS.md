# Chicago 2020-21 Pre-Deadline Score-Margin Outcome Robustness v0.1

- 상태: `MARGIN_MODEL_REPRODUCED / CENTRAL_RECORD_19_21 / EXACT_RECORD_HOLD / TRANSACTION_GATE_OPEN`
- 적용 구간: 2020-12-23~2021-03-24, Chicago 실제 43경기
- 선행 권위: `CHICAGO_2020_21_PREDEADLINE_PLAYER_PRODUCTION_PRIORS`
- 원고 게이트: `CLOSED`

## 결론

실제 43경기 점수차를 보존하고 BPM, 수축 RAPTOR, 날짜 제한 수축 E_NET의 세 계열을 적용했다. BASE와 일정 피로 stress의 중심 기록은 **19~21승**이다. 실제 19승 24패를 유지하는 E_NET_EB, 20~21승을 만드는 RAPTOR_EB, 21승을 만드는 BPM이 함께 남으므로 정확 승수는 잠그지 않는다.

중심 범위의 동부 위치는 **8~10위권**이다. 따라서 Chicago가 2021년 3월 25일에 매수자로 행동할 수 있는 플레이인 경쟁 동기는 유지된다. 그러나 LaMelo·주인공이 들어온 젊은 코어의 시간축과 두 장의 1라운드 지명권 비용이 달라졌으므로 실제 Vučević 거래를 자동 유지하지 않는다.

## 1. 실제 기준선

- 실제 기록: 19승 24패
- 실제 동부 위치: 10위
- 실제 Chicago 득점과 최종 점수차: `CHICAGO_2020_21_PREDEADLINE_GAME_MARGIN_BASELINE.csv`
- 2021-03-24 동부 전 팀 기록: `CHICAGO_2020_21_2021_03_24_EAST_STANDINGS.csv`
- 같은 날짜 가상 선수 분·실존 선수 delta: 기존 minute ledger·donor vector
- back-to-back 두 번째 경기: 10경기

실제 점수차를 잔차로 사용하므로 작은 선수 rating 변화가 대패를 승리로 바꾸지 않는다. Chicago와 상대팀의 결과는 같은 경기에서 동시에 반전된 것으로 해석한다.

## 2. 세 impact 계열

### BPM — retrospective box prior

Basketball-Reference의 2020-21 시즌 BPM을 donor rating으로 사용한다. 주인공은 기존 2018 윙 비교군의 3년차 BPM과 2년차 prior를 연결해 `-3.0/-1.2/+0.3`, LaMelo는 Chicago 역할 수축과 실제 Charlotte 상한을 반영해 `-2.4/-0.5/+1.8`로 둔다.

BPM은 3월 24일 뒤 표본까지 포함하는 retrospective descriptor다. 작품 속 프런트가 당시 알고 있던 수치가 아니며, 날짜 제한 계열인 E_NET_EB와 동일한 권위를 주지 않는다.

### RAPTOR_EB — external-method retrospective stress

FiveThirtyEight의 2020-21 modern RAPTOR를 league-average 0으로 1,000분 수축한다.

\[
R_i^{EB}=\frac{MIN_iR_i}{MIN_i+1000}
\]

주인공 prior는 `-2.2/-0.8/+0.6`, LaMelo는 `-2.4/-0.5/+0.3`이다. 500·1,500·2,000분 regularizer도 별도 stress로 실행한다.

### E_NET_EB — date-cutoff lineup stress

NBA Stats의 2020-12-23~2021-03-24 `E_NET_RATING`만 사용한다. donor를 같은 구간 Chicago 팀 E_NET -0.6으로 1,000분 수축한다.

\[
R_i^{EB}=\frac{MIN_iR_i+1000(-0.6)}{MIN_i+1000}
\]

주인공 prior는 `-4.6/-2.0/0.0`, LaMelo는 `-5.5/-3.2/0.0`이다. LaMelo BASE -3.2는 실제 Charlotte 손목 전 41경기 날짜 제한 관측 anchor다. 이 계열은 미래 표본 누수는 없지만 lineup·상대·garbage time에 가장 크게 내생적이다.

## 3. 경기별 계산

\[
Impact_g=\frac{MIN_{P,g}R_P}{48}+\frac{MIN_{L,g}R_L}{48}+\sum_i\frac{\Delta MIN_{i,g}R_i}{48}
\]

\[
AlternateMargin_g=ActualMargin_g+Impact_g+Fatigue_g
\]

`delta_seconds = alternate - actual`이므로 donor 차감은 음수, 반환은 양수다. 가상 두 선수의 박스 증가분을 다시 더하지 않는다. impact rating 안에 공격·수비·사용률 비용이 압축되어 있으므로 박스 원장과 이중 합산하지 않는다.

## 4. 중심 실행과 stress

| proxy | LOW | BASE | HIGH |
|---|---:|---:|---:|
| BPM | 19 / 19 / 19 | **21 / 21 / 21** | 26 / 26 / 26 |
| RAPTOR_EB-1000 | 19 / 19 / 19 | **21 / 20 / 20** | 23 / 23 / 23 |
| E_NET_EB-1000 | 14 / 14 / 14 | **19 / 19 / 19** | 22 / 21 / 21 |

각 칸은 `무피로 / -0.5 / -1.0 rating per 48`의 승수다. 피로 감산은 10개의 second-night에서 주인공과 LaMelo 두 사람에게만 적용한다. 두 선수에게 영구적인 체력 약점을 정본화하는 것이 아니라 43경기 연속 출전 가정의 민감도 검사다.

- 중심 BASE 집합: `{19,20,21}`
- primary 전체 stress: `14~26승`
- RAPTOR regularizer stress: `19~24승`

14승 E_NET LOW와 26승 BPM HIGH는 같은 권위의 정본 후보가 아니다. 각각 lineup 내생성 하방과 실제 Charlotte 상한을 두 선수에게 동시에 적용한 상방의 model-risk tail이다.

## 5. Young 0:38 bridge

Young의 38초는 2020-12-31에 반환하고 2021-03-12에 차감한다.

| proxy | 날짜별 절댓값 | 43경기 합계 | 승패 변화 |
|---|---:|---:|---:|
| BPM | 약 0.043542점 | 0 | 0경기 |
| RAPTOR_EB-1000 | 약 0.038813점 | 0 | 0경기 |
| E_NET_EB-1000 | 약 0.033749점 | 0 | 0경기 |

bridge를 포함한 실행과 제거한 실행의 승패는 전 행에서 같다. 따라서 이 38초는 roster conservation에는 필요하지만 대체 성적의 원인은 아니다.

## 6. 중심 민감 경기

| event | 실제 | BPM BASE | RAPTOR BASE 무피로 | RAPTOR BASE 피로 | E_NET BASE |
|---|---:|---:|---:|---:|---:|
| G003 2020-12-27 vs GSW | -1 패 | 승 | 승 | 패 | 패 |
| G018 2021-01-30 vs POR | -1 패 | 승 | 승 | 승 | 패 |

19승은 실제 결과 유지, 20승은 Portland전만 반전, 21승은 Golden State·Portland 두 경기가 반전되는 구조다. 두 상대가 서부 팀이므로 동부 다른 팀의 승수는 바뀌지 않는다.

## 7. 3월 24일 standings

| Chicago 기록 | 승률 | 동부 위치 해석 |
|---|---:|---|
| 19-24 | .442 | 실제 10위 |
| 20-23 | .465 | Indiana 20-23과 9·10위 동률권, 정확 tiebreak HOLD |
| 21-22 | .488 | Boston 21-23보다 위인 8위 |

정확 순위보다 견고한 결론은 세 경우 모두 플레이인·중위권 매수 경계라는 점이다.

## 8. Vučević 거래 연결

실제 Chicago는 다음 날인 2021-03-25 Orlando에서 Nikola Vučević와 Al-Farouq Aminu를 받고 Wendell Carter Jr., Otto Porter Jr., 2021·2023 1라운드 지명권을 보냈다.

현재 판정은 다음과 같다.

- 매수자 동기: `ROBUST_PASS`
- 센터 업그레이드 필요: `PLAUSIBLE / BOARD_REQUIRED`
- 실제 Vučević 패키지: `EXACT_TRANSACTION_HOLD`
- Washington–Chicago–Boston 3팀 거래: `SEPARATE_EVENT_HOLD`

19~21승은 실제 거래 동기를 제거하지 않는다. 반대로 더 나은 성적만으로 두 장의 1라운드 지명권 지출을 자동 정당화하지도 않는다. O-15F4에서 `실제 Vučević 패키지 유지 / 더 작은 센터 거래 / 거래 없음`을 당시 자산·나이곡선·LaVine 계약창·LaMelo·주인공 성장시간으로 비교한다.

## 9. 한계

- BPM과 RAPTOR는 3월 24일 뒤 표본을 포함하는 retrospective rating이다.
- E_NET은 날짜 제한이지만 causal on/off가 아니며 lineup 구성에 내생적이다.
- 세 계열 모두 possession-level clutch 재생성, 상대 로테이션 반응, 슛 분산을 생략한다.
- LOW/HIGH는 model-risk 경계이며 동일 가중 확률분포가 아니다.
- 정확 기록을 서사 편의로 고르면 거래 비용 판단을 오염시킨다.

## 출처

- [NBA Stats — Chicago 2020-21 team box scores](https://www.nba.com/stats/team/1610612741/boxscores?DateFrom=12%2F23%2F2020&DateTo=03%2F24%2F2021&Season=2020-21&SeasonType=Regular%20Season)
- [NBA Stats — 2020-21 player advanced, date filter](https://www.nba.com/stats/players/advanced?DateFrom=12%2F23%2F2020&DateTo=03%2F24%2F2021&Season=2020-21&SeasonType=Regular%20Season)
- [Basketball-Reference — 2020-21 NBA advanced](https://www.basketball-reference.com/leagues/NBA_2021_advanced.html)
- [FiveThirtyEight — modern RAPTOR by team](https://github.com/fivethirtyeight/data/blob/master/nba-raptor/modern_RAPTOR_by_team.csv)
- [Chicago Bulls — 2021-03-25 Vučević 거래 발표](https://www.nba.com/bulls/news/bulls-acquire-all-star-nikola-vucevic-and-al-farouq-aminu-trade-magic)
