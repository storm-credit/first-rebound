# R02-4A Chicago Production Prior Blindspot Review

- 대상: `simulation/CHICAGO_2018_19_PLAYER_PRODUCTION_PRIORS.md`
- 판정: `PRIOR_RANGE_PASS / OUTCOME_INPUTS_HOLD`
- 원고 게이트: `CLOSED`

## 총평

주인공의 루키 박스 범위는 73경기·1,274분 역할과 성장 정본에 맞는다. 9.5득점·8.5리바운드/36 중심은 Hutchison보다 리바운드가 강하고, 공격 제1옵션으로 너무 빨리 뛰어오르지는 않는다. 4.61득점·4.12리바운드의 경기당 중심선은 한국 팬의 과열 기대에는 실망스럽고 NBA 내부에서는 쓸 수 있는 프로젝트 윙이라는 W자 평가를 만든다.

## PASS

| 점검 | 판정 |
|---|---|
| 결과를 보고 비교군을 골랐는가 | 지명 범위·포지션·분 기준을 먼저 명시 — PASS |
| Hutchison 기록을 그대로 복사했는가 | 득점·리바운드·수비 사건을 역할에 맞게 분리 — PASS |
| 1,274분을 곧바로 스타 생산성으로 바꿨는가 | 17분 로테이션과 음수 영향 proxy 유지 — PASS |
| 실존 donor 성과를 삭제했는가 | 476분 차감 뒤 전원 역할 잔존 — PASS |
| 박스 이전량을 팀 점수로 오독하는가 | 팀 결과 직접 합산 금지 명시 — PASS |
| Coby White와 포지션을 억지로 겹쳤는가 | 2019 주인공은 1차 가드가 아님 — PASS |

## 남은 BLOCKER

| 등급 | 쟁점 | 조치 |
|---|---|---|
| BLOCKER | closing moneyline `pB` 출처·마감 시각 미고정 | 77경기 전수 입력 원장을 만들기 전 outcome 실행 금지 |
| BLOCKER | BPM을 causal impact로 오인할 위험 | plug-in 방향성 검사로만 두고 logit 입력 금지 |
| BLOCKER | 독립 logit scale 부재 | Chicago 결과와 무관한 리그 표본으로 교정 |
| HIGH | JaKarr·Alkins 소표본 극단값 | 실제 BPM 그대로 승패에 사용하지 않음 |
| HIGH | +64 리바운드를 팀 총리바운드 증가로 오독 | 동료 리바운드 귀속 재분배를 별도 원장화 |
| HIGH | 0~+2승 방향 범위를 정확 23승으로 선택 | exact standings 계속 HOLD |
| HIGH | 주인공이 있으니 Patrick Williams를 자동 삭제 | 2019-20 역할·lottery 뒤 2020 보드 재개방 |

## 반대 가능성

### 리바운드 8.5/36가 과장이라는 반론

핵심 윙 비교군의 최대가 Hutchison 7.4라서 중앙값보다 높다. 그러나 주인공의 유일한 S+ 뿌리가 리바운드→전환이며 Spellman은 같은 시즌 8.7/36이었다. 9.5 상한을 넘기지 않고 득점·3점·파울 비용을 남기므로 역할 특화 범위로 수용 가능하다.

### BPM -3.0이 너무 좋다는 반론

신인 윙 비교군 P75 -3.1보다 약간 높다. 이는 공격 기술이 아니라 수비 리바운드와 전환 시작의 즉시 번역을 반영한다. HIGH도 -1.8로 평균 이하에 묶었고, exact 승패에는 아직 사용하지 않으므로 범위 prior로는 통과한다.

### Coby White를 보존하려고 승수를 좁혔다는 반론

현재 plug-in 범위의 상한 24승은 다음 lottery 팀 Atlanta 29승과 5승 차다. Coby 보존은 원하는 결과를 위한 계수 조정이 아니라 4번째 seed가 유지되는 구조적 귀결이다. 다만 상대팀 standings와 outcome runner가 열려 있으므로 사건 확정은 하지 않는다.

## 판정

- 박스 prior 범위·비교군·환산법: `PASS`
- 실존 선수 476분 차감·96:35 반환의 생산성 사건량: `PASS`
- BPM plug-in: `AUDIT_ONLY`
- 정확 개인 기록·경기 승패·최종 22~24승 중 한 값: `HOLD`
- 2019 4번째 seed·12.5%: `ROBUST_LEAN`
- 실제 7순위와 Coby White: `RETENTION_STRONG_LEAN / EVENT_HOLD`
- 2020 Patrick Williams: `REOPEN_REQUIRED / HOLD`
