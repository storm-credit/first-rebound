# R02-4D Chicago Outcome Robustness Blindspot Review

- 대상: `simulation/CHICAGO_2018_19_OUTCOME_ROBUSTNESS.md`
- 판정: `MODEL_REOPEN_CORRECT / MARGIN_CANDIDATE_PASS / EXACT_RECORD_HOLD`
- 원고 게이트: `CLOSED`

## 총평

독립 Elo baseline이 기존 21/22/22 결과를 재현한 것은 closing probability 입력의 강건성을 보여준다. 그러나 eRT stress가 56점 차 Boston 패배를 뒤집은 순간, conditional Bernoulli runner를 exact 역사 선택에 사용할 수 없다는 것이 드러났다. 기존 결과를 방어하지 않고 모형 권한을 회수한 판단이 맞다.

score-margin residual은 주인공이 직접 만든 기대점수 변화와 실제 경기의 나머지 우연을 분리한다. 1점 차 경기만 반응해 물리적 개연성은 크게 개선된다. 다만 deterministic margin 이동도 하나의 단순화이므로 exact record는 계속 열어둬야 한다.

## PASS

| 점검 | 판정 |
|---|---|
| 같은 odds 미러를 독립 출처로 오인했는가 | Elo를 별도 baseline으로 구분 — PASS |
| 기존 PR 결과를 지키려고 반례를 숨겼는가 | G027 -56점 반전을 blocker로 공개 — PASS |
| margin을 본 뒤 유리한 경기만 선택했는가 | 82경기에 동일 margin 식 적용 — PASS |
| eRT를 causal truth로 격상했는가 | stress proxy로 제한 — PASS |
| fatigue를 캐릭터 약점과 이중 계산했는가 | 0 기본값과 별도 stress 분리 — PASS |
| 승수 범위가 lottery 경계를 넘는가 | 22~24 모두 4번째 seed — PASS |

## 남은 BLOCKER

| 등급 | 쟁점 | 조치 |
|---|---|---|
| HIGH | actual margin+delta는 분산·득점 순서를 생략 | exact 결과 선택 전 대표 민감 경기 lineups 확인 |
| HIGH | eRT fictional-player prior -3.3/-1.5/-0.5 | 2018 rookie role cohort와 수축 규칙을 별도 검산 |
| MEDIUM | Elo archive는 odds 독립 검증이 아님 | `ODDS_SOURCE_SINGLETON` 유지 |
| MEDIUM | 1점이 정확히 0을 넘을 때 연장 확률 생략 | 정본 경기 선택 시 연장·마지막 possession 별도 설계 |
| MEDIUM | Coby 유지가 수치상 안전해도 프런트 보드 판단은 별도 | 팀 need·대체 후보 비교 뒤 작가 승인 |

## 반대 가능성

### 확률 모형인데 56점 패배가 뒤집힐 수도 있지 않은가

새 세계선 전체를 다시 무작위로 추첨한다면 가능하다. 그러나 이 프로젝트는 주인공이 직접 건드린 사건만 바꾸고 나머지 실제 역사를 보존한다. +1.20점 수준의 국소 변화로 -56점 결과 전체를 재추첨하는 것은 최소 접촉 원칙과 맞지 않는다.

### actual margin을 쓰면 실제 역사 보존 편향 아닌가

맞는 위험이다. 그래서 이를 최종 truth가 아니라 primary candidate로 둔다. 다만 실제 우연을 같은 잔차로 보존하는 것은 같은 W/L만 보존하는 것보다 국소 counterfactual에 더 적합하다. 향후 대표 민감 경기의 lineup과 마지막 possession을 별도로 검토해야 한다.

### 22~24승이면 23승을 중심값으로 고르면 되지 않는가

BPM BASE는 22승, eRT BASE는 23승이다. proxy 선택이 정확 승수를 결정하므로 평균을 취해 23승으로 잠그는 것은 근거가 아니다. 현재 필요한 결정은 exact record보다 먼저, 4번째 seed 보존과 Coby 보드 유지 여부다.

## 판정

- 기존 Bernoulli runner exact 권한 회수: `PASS`
- score-margin residual: `PRIMARY_MODEL_CANDIDATE_PASS`
- fatigue 0 기본값: `MODEL_DEFAULT_PASS / CHARACTER_TRAIT_NOT_LOCKED`
- exact Chicago record: `22~24 / HOLD`
- 4번째 lottery seed·12.5%: `ROBUST_PASS`
- 7순위·Coby: `RETENTION_PASS_CANDIDATE / AUTHOR_LOCK_REQUIRED`
- Patrick Williams: `HOLD`
