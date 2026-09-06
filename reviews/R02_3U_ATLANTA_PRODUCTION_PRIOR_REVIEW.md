# R02-3U Atlanta Production Prior Blindspot Review

- 대상: `simulation/ATLANTA_2018_19_PLAYER_PRODUCTION_PRIORS.md`
- 판정: `BLOCKER / PRIOR_METHOD_HOLD`
- 원고 게이트: `CLOSED`
- R16 독립 검수 대체: `false`

## 보존 가능한 PASS

| 항목 | 통제 | 판정 |
|---|---|---|
| 새 선수 기여를 실제 팀 위에 더하는가 | 주인공+수취자와 제거된 Spellman의 같은 805분 차이만 계산 | PASS |
| 수취자의 기존 분을 또 더하는가 | 추가 183.1분만 rotation 항에 포함 | PASS |
| Young·Huerter·Collins 분을 침범하는가 | 핵심 3인 차감 0분 유지 | PASS |
| 박스 생산성과 영향치를 이중 계산하는가 | 박스 후보는 기록용, 승패에는 승인된 영향치만 사용 | PASS |
| 결과를 보고 케미 보너스를 넣는가 | 검증된 interaction이 없어 0으로 잠금 | PASS |
| 작은 추가분으로 임의 부상을 만드는가 | 자동 부상 금지, 임계 초과 시 availability HOLD | PASS |
| 정확한 대체 점수를 만드는가 | 정확 점수·점수차·연장 생성 금지 | PASS |
| prior 완료를 standings 완료로 오인하는가 | pB·workload·상대팀·lottery 별도 HOLD | PASS |

## BLOCKER

| 쟁점 | 독립 판정 | 필요한 수정 |
|---|---|---|
| 수축 근거 | `-2.75`, pseudo-minutes 750, band가 외부 표본에서 추정되지 않아 경험적 베이즈라고 부를 수 없음 | 외부/선행 코호트 교정 또는 공통평균 fallback 승인 |
| 박스 생산성 | 수취자 per-36 원값과 주인공 role adjustment가 수축·재현되지 않음 | 별도 box-prior 교정 전 개인 기록 HOLD |
| 피로 | M24/M72/M7 계수·G League 0.85·임계값 근거 부족 | 외부 교정과 독립 재검증 |
| logit scale | Atlanta 실제 원점수차로 만든 k=7.25는 pB 대비 변화 척도로 부적절 | 경기 전 기대 대비 잔차 또는 독립 리그 표본으로 교정 |
| 불확실성 결합 | 같은 방향 결합은 범위를 과소평가했으나 수정됨 | LOW=new LOW-donor HIGH, HIGH=new HIGH-donor LOW — **RESOLVED** |
| 단위 | points/100과 game margin 표현이 혼재했으나 수정됨 | 고정 100포제션 순평점 변화로 명시 — **RESOLVED** |
| hash 재현성 | event ID·byte order·2^53 변환이 미정이었으나 수정됨 | `ATL_2018_19_G001..G082`, big-endian 변환 명시 — **RESOLVED** |
| 검증기 범위 | expected 셀 자기일치 위주 | 수축 산식·상수·seed SHA·outcome blank를 독립 재계산 |

## 수정 수용선

v0.25에서는 상태를 `PRIOR_METHOD_HOLD`로 내린다. 같은 805분 차이·이중계산 금지·interaction 0·정확 점수 금지는 유지한다. LOW/HIGH comparator와 event ID/hash 규격은 수정됐지만 numeric prior·피로·logit scale은 교정 전 outcome runner에 넣지 않는다.

따라서 현재 변경은 방법론 후보와 BLOCKER를 투명하게 기록하는 정본 갱신으로만 병합할 수 있다. `PRIOR_PASS` 승격은 허용하지 않는다.
