# Chicago 2019-20 Score-Margin Outcome Robustness v0.1

- 상태: `MARGIN_MODEL_REPRODUCED / OUTCOME_SET_HOLD / LOTTERY_BRANCH_OPEN`
- 기준일: 2026-09-06
- 적용 범위: O-15C6B Chicago 2019-20 65경기 impact·standings·2020 lottery
- 원고 게이트: `CLOSED`

## 결론

실제 최종 점수차를 보존한 두 proxy와 사전 고정 LOW/BASE/HIGH prior를 65경기 전수에 적용했다. 무피로 기본 실행의 가능한 승수는 **21·22·24승**, second-night에 주인공 rating을 0.5~1.0점/48분 감산한 stress까지 합쳐도 외곽은 **21~24승**이다.

두 proxy의 BASE는 무피로에서 실제와 같은 22승에 수렴한다. 그러나 BPM BASE는 second-night 감산에서 21승으로 내려가고 NET_EB HIGH는 24승이므로 정확 22승을 정본화하지 않는다.

결과 집합은 Chicago의 2020 lottery seed를 **7~8번**으로 연다. 21·22승 분기는 실제 7번 seed와 4순위 추첨 사건을 보존할 수 있지만, 24승 분기는 Chicago와 Charlotte의 seed를 맞바꿔 고정 seed 재추첨이 필요하다. 따라서 실제 4순위와 Patrick Williams 지명은 계속 `HOLD`다.

## 1. 실제 기준선

- Chicago 실제 기록: 22승 43패, 65경기
- 실제 lottery 입력: Chicago 22-43 seed 7, Charlotte 23-42 seed 8, Washington 24-40 seed 9
- 실제 확률: seed 7은 1순위 7.5%·top four 약 31.9%, seed 8은 1순위 6.0%·top four 약 26.3%
- 실제 추첨: Chicago가 4순위로 상승
- 실제 지명: 4순위 Patrick Williams

Washington의 25-47 최종 기록이 아니라 2020 lottery 산정에 사용된 3월 11일까지의 24-40을 쓴다. Chicago·Charlotte는 재개 시즌에 참가하지 않았으므로 각각 65경기 기록이 lottery 입력이다.

`CHICAGO_2019_20_GAME_MARGIN_BASELINE.csv`는 NBA Stats TeamGameLogs의 65개 `GAME_ID`, Chicago 득점, `PLUS_MINUS`를 동결한다. player-game 분 원장과 event ID로 1:1 결합하며 결과를 본 뒤 경기 일부만 고르지 않는다.

## 2. 두 impact proxy

### BPM

Basketball-Reference의 2019-20 Chicago BPM을 사용한다. 주인공 prior는 LOW -3.2, BASE -1.6, HIGH -0.2다. BPM은 경기당 점수나 causal on/off가 아니므로 48분당 약 100 possession의 score-margin proxy로만 사용한다.

### NET_EB

NBA Stats의 선수 on-court NET_RATING을 Chicago 팀 NET_RATING -3.1로 empirical-Bayes 수축한다.

\[
R_i^{EB}=\frac{MIN_i R_i+1000(-3.1)}{MIN_i+1000}
\]

1,000분은 Max Strus·Mokoka·Harrison 같은 작은 표본이 outcome을 지배하지 못하게 하는 사전 고정 regularizer다. 주인공 prior는 LOW -4.0, BASE -2.0, HIGH 0.0이다. 이 값도 causal RAPM이 아니라 역할군 범위 stress다.

| 선수 | BPM | raw NBA NET | NET_EB |
|---|---:|---:|---:|
| Hutchison | -2.6 | -11.9 | -6.136 |
| Valentine | -0.6 | -5.0 | -3.723 |
| Harrison | 2.8 | 6.8 | 0.130 |
| Arcidiacono | -2.8 | -4.0 | -3.534 |
| Mokoka | -4.1 | 17.1 | -1.071 |
| Strus | 3.9 | 105.8 | -2.425 |
| Young | -1.2 | -6.2 | -5.003 |
| Markkanen | -0.6 | -2.0 | -2.441 |
| Dunn | -0.6 | -0.1 | -1.422 |

Markkanen·Dunn의 gross 19:34 bridge는 시즌 순감 0이라도 경기별 `delta_seconds`를 그대로 넣는다. 따라서 debit 날짜의 손실과 receiver 날짜의 회복이 모두 outcome에 반영된다.

## 3. 경기별 계산

각 경기의 기본 impact는 다음과 같다.

\[
Impact_g=\frac{MIN_{P,g}R_P}{48}+\sum_i\frac{\Delta MIN_{i,g}R_i}{48}
\]

\[
AlternateMargin_g=ActualMargin_g+Impact_g
\]

`delta_seconds = alternate - actual`이므로 실존 선수 분을 빼면 음수, 다른 날짜에 돌려주면 양수다. 조정 점수차가 0을 넘을 때만 승리로 판정한다. 실제 점수차를 쓰므로 큰 점수차 경기를 임의 Bernoulli 값으로 뒤집지 않는다.

## 4. 65경기 결과

### 무피로 기본 실행

| proxy | LOW | BASE | HIGH | 시즌 impact 합계 |
|---|---:|---:|---:|---:|
| BPM | 21승 | 22승 | 22승 | -56.57 / -10.07 / +30.62점 |
| NET_EB | 22승 | 22승 | 24승 | -3.00 / +55.12 / +113.25점 |

### second-night fatigue stress

주인공이 출전한 back-to-back 두 번째 경기는 9개다. 해당 경기에서만 주인공 rating을 0.5 또는 1.0점/48분 추가 감산한다.

| proxy | 시나리오 | 기본 | -0.5 | -1.0 |
|---|---|---:|---:|---:|
| BPM | LOW | 21 | 21 | 21 |
| BPM | BASE | 22 | 21 | 21 |
| BPM | HIGH | 22 | 22 | 22 |
| NET_EB | LOW | 22 | 21 | 21 |
| NET_EB | BASE | 22 | 22 | 22 |
| NET_EB | HIGH | 24 | 24 | 24 |

fatigue stress의 목적은 주인공에게 확정 체력 약점을 부여하는 것이 아니다. 65경기 전수 출전과 21.46 MPG에도 second-night 비용을 0으로 숨기지 않는 민감도 검사다.

## 5. 실제와 달라지는 세 경기

| event | 실제 | 조건 | 조정 결과 | 직접 파급 |
|---|---|---|---|---|
| G017 2019-11-23 @ CHA | Chicago +1승 | BPM LOW 기본, BPM BASE fatigue, NET_EB LOW fatigue | Chicago 패 | CHI -1승, CHA +1승 |
| G001 2019-10-23 @ CHA | Chicago -1패 | NET_EB HIGH | Chicago 승 | CHI +1승, CHA -1승 |
| G025 2019-12-09 vs TOR | Chicago -1패 | NET_EB HIGH | Chicago 승 | CHI +1승, TOR -1승 |

모든 반전은 실제 1점 차 경기에서만 발생한다. 실제 2점 차 이상 경기는 이번 격자에서 하나도 뒤집히지 않는다.

## 6. standings·lottery 조건부 판정

| outcome | Chicago | Charlotte 파급 | Chicago lottery seed | 추첨 처리 |
|---|---:|---:|---:|---|
| 21승 분기 | 21-44 | 24-41 | 7 | 참가팀·seed·확률 동일, 실제 4순위 사건 유지 가능 |
| 22승 분기 | 22-43 | 23-42 | 7 | 실제 입력과 동일, 실제 4순위 사건 유지 |
| 24승 분기 | 24-41 | 22-43 | 8 | CHI·CHA seed 교환, 고정 seed 재추첨 필요 |

21승이어도 New York 21-45의 승률 .318이 Chicago 21-44의 .323보다 낮아 Chicago는 7번째로 나쁜 팀이다. 24승이면 Chicago .369는 Washington 24-40의 .375보다 낮지만 Charlotte .338보다 높아 8번째로 나쁜 팀이다.

따라서 현재 판정은 다음과 같다.

- 정확 Chicago record: `ATTAINABLE_SET {21,22,24} / HOLD`
- lottery seed: `7~8 / BRANCH_OPEN`
- seed 7의 실제 4순위: `CONDITIONAL_RETENTION_PASS`
- seed 8의 추첨 결과: `FIXED_DRAW_REQUIRED / HOLD`
- Patrick Williams: `REOPEN_REQUIRED / HOLD`

## 7. Patrick Williams 연결

4순위가 유지돼도 Patrick을 자동 지명하지 않는다. 2년차 주인공은 이미 18선발·1,395분의 SF/PF이며 리바운드·수비·closeout attack을 성장시키고 있다. Williams는 다포지션 포워드 수비와 장기 성장 시간을 직접 공유한다.

조건부 보드는 두 갈래로 연다.

1. **seed 7→실제 4순위 유지:** Williams·Avdija·Okoro·Haliburton·Vassell을 당시 정보로 비교한다.
2. **seed 8→고정 재추첨:** 새 정확 순번을 먼저 만든 뒤 그 순번까지 남은 선수로 보드를 다시 짠다.

후대 성공을 보고 Haliburton을 올리거나 Williams의 이후 계약을 보고 내리지 않는다. 2020 당시 프런트, 의료, 포지션 겹침, LaVine·Coby·Markkanen·주인공의 권한만 사용한다.

## 8. 한계와 다음 blocker

- BPM과 NET_EB는 서로 다른 계열이지만 둘 다 실제 시즌의 변경 전 lineup 결과를 포함한다.
- NET_EB의 1,000분 prior와 주인공 impact prior는 사전 고정했지만 독립적인 RAPM 계열 교차검증이 없다.
- 점수차 방식은 상대 슛 분산과 clutch possession 재생성을 생략한다.
- fatigue는 주인공 rating 감산만 다루며 실존 선수 bridge의 다음 경기 누적 피로는 별도 모델이 없다.
- 사용률 재귀속 비용은 주인공 impact prior 안에 압축되어 있고 별도 possession 원장으로 분해하지 않았다.

다음 O-15C6C는 독립 impact 계열 또는 lineup-informed 범위를 추가하고, exact outcome이 seed 8로 결정될 경우에만 2020 고정 lottery draw를 실행한다. 그 전에는 22승·4순위·Patrick 중 어느 것도 LOCK하지 않는다.

## 출처

- [NBA Stats — Chicago 2019-20 Advanced](https://www.nba.com/stats/team/1610612741/players-advanced?Season=2019-20&SeasonType=Regular%20Season)
- [NBA Stats — Chicago 2019-20 Box Scores](https://www.nba.com/stats/teams/boxscores?Season=2019-20&SeasonType=Regular%20Season&TeamID=1610612741)
- [Basketball-Reference — 2019-20 Chicago Bulls](https://www.basketball-reference.com/teams/CHI/2020.html)
- [NBA Communications — 2020 lottery order·records·odds](https://pr.nba.com/2020-nba-draft-tiebreakers/)
- [Chicago Bulls — seed 7 lottery odds와 실제 4순위 상승](https://www.nba.com/bulls/news/nba-draft-lottery-how-it-works-and-where-the-bulls-stand)
- [NBA — 2020 Draft 결과](https://www.nba.com/news/2020-nba-draft-results-picks-1-60)
