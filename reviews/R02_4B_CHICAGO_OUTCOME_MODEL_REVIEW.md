# R02-4B Chicago Outcome Model Blindspot Review

- 대상: `simulation/CHICAGO_2018_19_OUTCOME_MODEL.md`
- 원장: `simulation/CHICAGO_2018_19_OUTCOME_LEDGER.csv`
- 판정: `PROVISIONAL_RUN_PASS / CANON_OUTCOME_HOLD`
- 원고 게이트: `CLOSED`

## 총평

82경기를 빠짐없이 실행하고 실제 결과와 같은 latent를 세 시나리오에 적용한 절차는 재현 가능하다. BASE·HIGH는 실제 22승을 유지하고 LOW만 Orlando전 한 경기를 잃어 21승이 된다. 시카고의 lottery seed와 12.5% 확률은 전 범위에서 유지된다.

그러나 이 실행은 정본 승수를 선택하기 위한 충분조건이 아니다. odds 원자료가 단일 계통이고, BPM은 작은 표본·라인업·박스 사건이 섞인 비인과 proxy다. 특히 LOW 선택은 Orlando–Brooklyn 플레이오프 대진을 바꾸므로 `21승`을 작은 지역 수정으로 취급할 수 없다.

## PASS

| 점검 | 판정 |
|---|---|
| 영향 경기만 골라 실행했는가 | 82경기 전체 입력, `NONE` 5경기까지 보존 — PASS |
| 실제 결과를 못 맞춘 baseline이 있는가 | 조건부 latent로 실제 22-60 전수 재현 — PASS |
| 시나리오마다 난수를 다시 뽑았는가 | 같은 seed·event별 `h`와 `u` 사용 — PASS |
| scale을 Chicago 결과로 맞췄는가 | 직전 시즌 리그 1,230경기로 독립 교정 — PASS |
| 홈·원정 vig를 방치했는가 | 양쪽 moneyline 정규화 — PASS |
| 반전된 상대팀 승수를 무시했는가 | LOW에서 Orlando +1승과 playoff seed 파급 명시 — PASS |
| lottery 확률을 승수만 보고 임의 변경했는가 | seed 4 유지 확인 뒤 12.5% 보존 — PASS |
| Coby를 주인공의 장기 상한과 겹쳤는가 | 2019 실제 역할만 비교 — PASS |

## 남은 BLOCKER

| 등급 | 쟁점 | 조치 |
|---|---|---|
| BLOCKER | closing odds가 Sportsbook Review 계통 하나뿐 | 독립 archive 또는 당시 보드 캡처로 82경기 교차검증 |
| BLOCKER | BPM 차이를 직접 causal point impact로 사용 | lineup/on-off 또는 대체 impact proxy로 방향·민감 경기 재검증 |
| HIGH | Hutchison·JaKarr·Alkins 등 소표본 BPM | shrinkage 또는 역할군 prior 적용 결과와 비교 |
| HIGH | fatigue를 명시적으로 0 처리 | 17.45분 역할에서 0 가정의 근거 또는 사전 감산 규칙 고정 |
| HIGH | LOW의 Orlando +1승이 playoff 대진 변경 | LOW 채택 시 동부 1라운드 cascade를 별도 계산 |
| MEDIUM | closing line의 timestamp 정의가 archive 설명에 의존 | 원자료 필드 정의와 마감 기준을 문서화 |

## 반대 가능성

### 실제 22승을 그대로 두면 역사 보존 편향 아닌가

BASE에서 승패가 하나도 바뀌지 않는 것은 impact가 0이라는 뜻이 아니다. 시즌 합계 proxy는 +26.15점이지만, 동일 latent의 임계치를 넘는 경기가 없었다. 다만 BPM 입력의 불확실성 때문에 이것을 `22승 정답`으로 승격하지 않는다.

### LOW의 -5.70점으로 한 경기가 뒤집히는 것은 과민하지 않은가

시즌 합계가 아니라 G033의 `u`가 baseline과 LOW counterfactual 확률 사이에 놓였기 때문이다. 조건부 시뮬레이션에서는 작은 확률 이동도 임계 경기 하나를 바꿀 수 있다. 해당 경기를 숨기는 대신 민감 사건으로 공개하는 것이 맞다.

### 4번째 seed가 확실하면 Coby White를 LOCK해도 되지 않는가

seed와 7순위 보존은 강하지만, exact 정규시즌 원장이 아직 닫히지 않았고 지명 보드에는 의료·워크아웃·프런트 판단 같은 비수치 조건도 있다. 현재 단계에서는 `RETENTION_STRONG_LEAN`이 적절하다.

### fatigue가 정말 필요한가

주인공은 평균 17.45분이고 시즌 73경기라 큰 감산은 부당할 가능성이 높다. 반면 늦게 농구를 시작한 루키이며 후반 33경기에 476분이 집중된다. 효과가 작더라도 0을 암묵적으로 두지 말고, 0 또는 제한적 감산을 결과를 보기 전에 정해야 한다.

## 판정

- 82경기 baseline·event ID·동일 latent 재현: `PASS`
- 2017-18 logit scale 교정: `METHOD_PASS / SOURCE_SINGLETON`
- LOW 21승·BASE 22승·HIGH 22승 실행: `PROVISIONAL_RUN_PASS`
- exact Chicago record: `21~22 RANGE / HOLD`
- Chicago 4번째 lottery seed·12.5%: `ROBUST_PASS`
- 실제 7순위·Coby White: `RETENTION_STRONG_LEAN / EVENT_HOLD`
- Patrick Williams: `REOPEN_REQUIRED / HOLD`
- 원고 게이트: `CLOSED`
