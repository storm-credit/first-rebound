# R01 Chicago 2019-20 Outcome Blindspot Review

- 대상: `simulation/CHICAGO_2019_20_OUTCOME_ROBUSTNESS.md`
- 원장: `simulation/CHICAGO_2019_20_OUTCOME_LEDGER.csv`
- 판정: `REPRODUCTION_PASS / EXACT_OUTCOME_BLOCKED / NOT_INDEPENDENT`
- 원고 게이트: `CLOSED`

## 총평

65경기 score margin과 player-game donor를 모두 사용해 큰 점수차가 작은 proxy 변화로 뒤집히는 기존 결함을 제거했다. BPM과 수축 NET_EB의 무피로 BASE가 모두 22승을 내지만 fatigue stress와 HIGH 경계에서 21·24승이 살아 있다. 정확 22승을 선택하기에는 근거가 부족하다.

가장 중요한 하류 변화는 승수 외곽이 아니라 lottery seed다. 24승 분기는 Chicago와 Charlotte를 7·8번에서 교환하므로 실제 4순위 추첨을 유지할 수 없다. Patrick Williams 보드를 먼저 여는 것도 금지해야 한다.

## 통과

| 점검 | 판정 |
|---|---|
| 65경기 전수와 event ID 1:1 결합 | PASS |
| 실제 22-43·점수차 부호 재현 | PASS |
| 실제 팀 총분과 donor delta 사용 | PASS |
| Markkanen·Dunn gross bridge 반영 | PASS |
| 소표본 NET rating 수축 | PASS |
| back-to-back 9경기 명시 stress | PASS |
| 실제 2점 차 이상 경기 반전 없음 | PASS |
| 상대팀 승수와 lottery seed 파급 기록 | PASS |
| Washington의 lottery 입력 24-40 사용 | PASS |

## 남은 blocker

| 등급 | 쟁점 | 조치 |
|---|---|---|
| BLOCKER | 두 proxy 모두 변경 전 Chicago 시즌에 내생적 | 독립 impact 계열 또는 lineup-informed 범위로 교차검증 |
| BLOCKER | 주인공 impact prior가 box prior와 완전히 식별되지 않음 | 수비·리바운드·usage를 분리한 범위 검산 |
| HIGH | NET_EB 1,000분 regularizer가 임의 선택 | 500·1,500·2,000분 sensitivity 추가 |
| HIGH | fatigue가 주인공 당일 감산만 포함 | bridge receiver의 다음 경기 누적 효과 상한 검토 |
| HIGH | 24승 분기에서 실제 lottery 사건 불변 불가 | exact outcome 선택 뒤 고정 seed·공식 조합 재추첨 |
| MEDIUM | actual margin에 상대 선수 반응·clutch 재배치 없음 | 반전 3경기만 possession-level stress 후보 등록 |

## 반대 가능성

### BASE 두 개가 모두 22승이면 22승을 잠가도 되지 않는가

아니다. BPM BASE는 second-night -0.5에서 G017이 0.035점 차로 패배 전환된다. BASE 수렴은 22승의 강한 중심 증거지만 강건한 exact 판정은 아니다.

### NET_EB HIGH의 +113.25점은 2승 증가치로 자연스럽지 않은가

시즌 총합만 보면 가능하지만 raw on-court net rating은 lineup·상대·garbage time 영향을 포함한다. 특히 Hutchison의 -11.9를 수축해도 주인공과의 직접 causal 차이라고 볼 수 없다. 24승은 살아 있는 경계안이지 정본 답이 아니다.

### 21승도 seed 7이면 실제 4순위를 바로 유지해도 되지 않는가

조건부로는 가능하다. G017 반전으로 Charlotte가 24-41이 되어도 CHI 7·CHA 8은 유지된다. 하지만 exact outcome 자체가 HOLD이므로 현재 단계에서 단일 추첨 결과를 정본 승격하지 않는다.

### Patrick은 실제 프런트의 첫 지명이므로 유지가 자연스럽지 않은가

주인공이 없던 실제 역사에서는 그렇다. 활성 세계선에서는 2년차 SF/PF가 이미 1,395분과 18선발을 차지해 프런트의 포지션·성장시간 입력이 달라진다. 실제 4순위가 유지돼도 팀보드 재심사가 필요하다.

## 판정

- outcome runner·원장 재현: `PASS`
- attainable wins: `{21,22,24}`
- exact wins: `HOLD`
- 2020 lottery seed: `7~8 / BRANCH_OPEN`
- actual pick 4: `CONDITIONAL_RETENTION_ONLY`
- Patrick Williams: `REOPEN_REQUIRED / HOLD`
- 독립 검토: `REQUIRED`
- 원고 게이트: `CLOSED`
