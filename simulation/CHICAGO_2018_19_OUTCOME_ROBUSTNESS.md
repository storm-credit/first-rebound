# Chicago 2018-19 Outcome Robustness Audit v0.1

- 상태: `BASELINE_ROBUST / BERNOULLI_RUNNER_REOPENED / EXACT_OUTCOME_HOLD`
- 기준일: 2026-09-06
- 상위 모형: `simulation/CHICAGO_2018_19_OUTCOME_MODEL.md`
- 파생 입력: `simulation/CHICAGO_2018_19_ROBUSTNESS_LEDGER.csv`
- 검산: `node tools/verify_chicago_2018_19_robustness.mjs`
- 원고 게이트: `CLOSED`

## 결론

Sportsbook Review closing moneyline과 별개 계열인 FiveThirtyEight Elo 경기 전 확률로 baseline을 바꿔도, 기존 BPM·conditional Bernoulli runner는 똑같이 `LOW 21승 / BASE 22승 / HIGH 22승`을 낸다. 따라서 G033 민감도가 단일 odds 파일 오류에서 생겼을 가능성은 낮다.

그러나 대체 impact proxy를 넣자 기존 runner가 실제 **56점 차 패배**를 약 +1.20점 impact만으로 승리로 바꿨다. 이는 baseline source 문제가 아니라 승패만 조건화하고 실제 점수차를 버린 runner의 구조적 결함이다.

따라서 PR #72의 실행 재현성은 유지하되, 그 `21~22승` 결과를 정본 후보로 사용하지 않는다. 현재 1차 대안인 score-margin residual runner의 범위는 **22~24승**이며, exact record는 계속 `HOLD`다.

모든 검증 조합에서 Chicago는 Atlanta 29승보다 아래이므로 4번째 lottery seed와 12.5%는 변하지 않는다.

## 1. 독립 baseline 감사

### 자료

- 계열: FiveThirtyEight NBA Elo game forecast archive
- 확보본: `Neil-Paine-1/NBA-elo/nba_elo.csv`
- 원파일 SHA-256: `be12a0ffcf49820ec967bfc4e838d477728a345753e4ebcc8e1b455cc98d8bff`
- Chicago 2018-19 정규시즌: 82경기, 날짜 중복·누락 0
- 파생 robustness ledger SHA-256: `ac28985d49cf3d912f1da49115a356f591f033a94dc8ebea5bcb92e3fe6f1f73`

Elo는 bookmaker closing odds의 독립 교차검증본이 아니다. 팀 Elo와 홈코트를 사용한 별도 경기 전 확률이므로 `ODDS_SOURCE_SINGLETON`은 해소하지 못한다. 대신 **baseline 확률 계열을 바꿔도 결과 민감도가 같은지** 검사한다.

| 비교 | 값 |
|---|---:|
| closing moneyline pB와 Elo pB 상관 | 0.8315 |
| 평균 절대차 | 0.0721 |
| RMSE | 0.0915 |
| 최대 절대차 | 0.2557 |

두 baseline은 충분히 다르지만, 기존 BPM runner에서는 둘 다 G033만 LOW에서 승→패로 바뀌었다.

| baseline | LOW | BASE | HIGH |
|---|---:|---:|---:|
| closing moneyline + BPM | 21 | 22 | 22 |
| Elo + BPM | 21 | 22 | 22 |

판정: `BASELINE_ROBUST_PASS / ODDS_SOURCE_SINGLETON_REMAINS`.

## 2. 대체 impact proxy

Basketball Reference BPM 한 계열에만 의존하지 않도록 Estimated RAPTOR의 `eRT`를 대체 proxy로 사용한다. 이는 box·on/off를 조합한 추정치이며 causal truth가 아니다.

- 자료: `Neil-Paine-1/NBA-elo/nba-estimated-raptor.csv`
- 원파일 SHA-256: `4650e8a6cef1242ec5a5da02df837c21f3c40f356ea81631cd93f851d9ba6c5d`
- 선수: Chicago 소속 구간의 Hutchison·7 donor·Parker·Portis
- 주인공 eRT stress prior: LOW -3.3 / BASE -1.5 / HIGH -0.5

주인공 prior는 비교군의 eRT 분포와 기존 BPM prior의 상대 위치를 대응시킨 stress range다. 정확한 선수 가치 정본이 아니다.

| 시나리오 | eRT impact 합계 |
|---|---:|
| LOW | -3.61점 |
| BASE | +44.16점 |
| HIGH | +70.70점 |

기존 conditional Bernoulli runner 결과:

| baseline | LOW | BASE | HIGH |
|---|---:|---:|---:|
| closing moneyline + eRT | 22 | 22 | 23 |
| Elo + eRT | 22 | 22 | 24 |

## 3. 발견된 구조적 결함

Elo+eRT HIGH는 다음 두 경기를 뒤집는다.

| event | 실제 경기 | 실제 margin | eRT HIGH delta | 판정 |
|---|---|---:|---:|---|
| `G008` | 2018-10-31 Denver 108-107 Chicago | -1 | +1.70 | 물리적으로 가능한 민감 경기 |
| `G027` | 2018-12-08 Boston 133-77 Chicago | **-56** | +1.20 | 승리 반전 불가, runner 결함 |

기존 runner는 실제 W/L만 재현하도록 `u`를 조건화한다. 실제 margin을 사용하지 않으므로, 1점 패배와 56점 패배가 확률 임계치 근처에 놓일 수 있다. 이 방식은 Monte Carlo 민감도 도구로는 재현 가능하지만, 소설 정본의 특정 경기 결과를 고르는 도구로는 부적합하다.

이에 따라 다음 판정을 내린다.

- 기존 conditional Bernoulli 실행 로그: `AUDIT_HISTORY_PRESERVE`
- exact outcome 선택 권한: `REVOKED`
- G033 LOW 반전: `SENSITIVITY_ARTIFACT / NOT_CANON_CANDIDATE`
- runner: `REOPEN_REQUIRED`

## 4. score-margin residual 대안

첫 대안은 실제 경기의 우연 성분을 최종 margin 잔차로 보존하는 방식이다.

`counterfactual_margin = actual_chicago_margin + player_impact_delta - fatigue_delta`

이 방식은 주인공이 직접 바꾼 기대점수만 실제 경기 margin에 더한다. 56점 차 패배를 +1점 impact로 뒤집지 않으며, 실제로 임계치에 가까운 경기만 바꾼다.

### 실행 결과

| impact proxy | LOW | BASE | HIGH | 반전 경기 |
|---|---:|---:|---:|---|
| BPM | 22 | 22 | 23 | HIGH `G008` |
| eRT | 22 | 23 | 24 | BASE `G008`; HIGH `G008`,`G021` |

민감 경기:

- `G008`: Denver 108-107 Chicago, 실제 -1
- `G021`: San Antonio 108-107 Chicago, 실제 -1

두 경기 모두 1점 차이므로 +1점 안팎 impact에 반응하는 것이 물리적으로 일관된다.

score-margin residual은 `PRIMARY_MODEL_CANDIDATE`다. 다만 경기 내 득점 사건·라인업 재배치까지 재현하는 모형은 아니므로 exact 22·23·24승 중 하나를 아직 잠그지 않는다.

## 5. fatigue stress

주인공이 전날 NBA 경기를 뛰고 다음 날도 출전한 second night는 11경기, 총 184.48분이다.

두 감산을 사전 stress로 적용했다.

| 감산 | 시즌 impact 감소 | score-margin 결과 변화 |
|---|---:|---|
| -0.5점 / 48분 | -1.92점 | 없음 |
| -1.0점 / 48분 | -3.84점 | 없음 |

평균 17.45분·73경기 역할에서는 별도 fatigue를 크게 부과할 근거가 약하다. 부상·결장·Windy City 구간은 이미 분 원장에 반영되어 있다.

따라서 outcome 기본값은 `FATIGUE_DELTA = 0`으로 두되, second-night stress 결과를 감사 기록으로 보존한다. 이는 체력 문제가 없다는 캐릭터 정본이 아니라 중복 감산을 막는 모델 규칙이다.

## 6. standings·lottery·Coby 판정

| 항목 | 현재 판정 |
|---|---|
| Chicago exact record | `22~24 RANGE / HOLD` |
| Chicago lottery seed | `4 / ROBUST_PASS` |
| 1순위 확률 | `12.5% / ROBUST_PASS` |
| 실제 추첨 7순위 유지 | `RETENTION_PASS_CANDIDATE / AUTHOR_LOCK_REQUIRED` |
| Coby White 보드 | `TEAM_BOARD_PASS / RETENTION_STRONG_LEAN` |
| Coby exact 지명 | `HOLD` |
| Patrick Williams | `2019-20 AFTERMATH REQUIRED / HOLD` |

기존 21승 분기는 runner 결함에서 나온 결과라 standings 후보에서 제거한다. 22~24승 어느 경우에도 Atlanta 29승을 넘지 않으므로 lottery seed는 같다.

## 7. 다음 단계

1. score-margin residual을 NBA 결과 모형의 primary candidate로 독립 맹점 검토한다.
2. 22·23·24승을 하나로 잠그지 않은 채 2019 7순위와 Coby White 팀보드를 조건부 정본 후보로 제시한다.
3. 작가가 7순위·Coby를 승인하면 2019-20 player-minute·역할 원장을 시작한다.
4. Patrick Williams 보드는 2019-20 승수·lottery 뒤에만 연다.

## 출처

- [FiveThirtyEight data — NBA forecast archive 안내](https://github.com/fivethirtyeight/data/tree/master/nba-forecasts)
- [Neil Paine — NBA Elo archive](https://github.com/Neil-Paine-1/NBA-elo)
- [FiveThirtyEight historical NBA Elo 변수 정의](https://datahub.io/fivethirtyeight/nba-elo)
- [NBA — 2019 Draft lottery odds/order](https://www.nba.com/news/draft-lottery-odds-order-decided-official-release)
