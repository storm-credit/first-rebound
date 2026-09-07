# R01 Chicago 2020-21 Pre-Deadline Outcome Blindspot Review

- 대상: `simulation/CHICAGO_2020_21_PREDEADLINE_OUTCOME_ROBUSTNESS.md`
- 성격: `ORCHESTRATOR_SELF_REVIEW / NOT_INDEPENDENT`
- 판정: `REPRODUCTION_PASS / CENTRAL_PLAY_IN_BAND_PASS / EXACT_RECORD_AND_TRANSACTION_BLOCKED`
- 원고 게이트: `CLOSED`

## 총평

43경기 실제 점수차와 same-date donor delta를 결합해 큰 점수차가 임의로 뒤집히는 결함을 막았다. 미래 표본을 포함하는 BPM·RAPTOR만으로 20~21승을 선언하지 않고, 3월 24일 날짜 제한 NBA E_NET을 추가해 중심 집합을 19~21승으로 넓힌 점이 핵심이다.

19~21승은 모두 Chicago를 동부 8~10위 플레이인 경쟁권에 둔다. 따라서 마감일 매수 동기는 견고하지만 정확 Vučević 거래는 아직 증명되지 않았다.

## 통과

| 점검 | 판정 |
|---|---|
| 43경기 event ID·실제 19-24·점수차 부호 | PASS |
| minute ledger와 game ID·날짜·matchup 1:1 결합 | PASS |
| BPM·RAPTOR_EB·date-cutoff E_NET_EB 세 계열 | PASS |
| 두 가상 선수 박스 귀속과 impact 이중 합산 방지 | PASS |
| second-night 10경기·두 선수 공동 피로 stress | PASS |
| Young 0:38 날짜별 영향·시즌 net zero 분리 | PASS |
| 중심 반전이 실제 1점 차 두 경기로 제한 | PASS |
| Chicago·상대팀 승패 동시 변경 해석 | PASS |
| 대체 성적 뒤에만 거래 게이트 개방 | PASS |

## 남은 blocker

1. BPM·RAPTOR는 retrospective rating이므로 3월 24일 당시 프런트 정보와 동일하지 않다.
2. E_NET은 날짜 제한이지만 Patrick·Temple·Satoransky의 실제 lineup 결과에 내생적이다.
3. E_NET LOW 14승과 BPM HIGH 26승은 모형 위험 tail이며 정본 후보로 평균하거나 투표할 수 없다.
4. G003·G018의 반전은 possession-level 재생성이 없으므로 exact 19·20·21 중 하나를 고를 근거가 부족하다.
5. 대체 세계에는 LaMelo가 있고 Patrick이 없으므로 실제 거래의 포지션·나이곡선·지명권 가치가 달라진다.
6. 실제 Vučević 거래와 Hutchison이 필요한 3팀 거래를 한 묶음으로 유지하거나 폐기하면 안 된다.

## 반대 가능성

### 세 BASE 중 둘이 21승이면 21승을 잠가도 되는가

아니다. RAPTOR BASE는 피로 stress에서 20승이고, 날짜 제한 E_NET BASE는 모든 피로값에서 19승이다. 모형 계열의 다수결은 인과 증거가 아니다.

### 더 좋은 성적이면 실제 Vučević 거래가 더 확실하지 않은가

매수 동기는 강해진다. 그러나 LaMelo·주인공의 성장 시간축은 30세 센터와 두 장의 1라운드 지명권을 교환할 비용 판단을 바꾼다. 동기 유지와 정확 패키지 유지는 별도 판정이다.

### Young 38초는 삭제해도 되는가

승패에는 영향이 없지만 분 보존 원장에는 필요하다. outcome-neutral이라는 이유로 roster conservation 증거를 삭제하지 않는다.

## 판정

- outcome runner·원장 재현: `PASS`
- exact Chicago record: `{19,20,21} CENTRAL / HOLD`
- 동부 위치: `8~10 / PLAY_IN_BAND_PASS`
- Vučević 매수 동기: `ROBUST_PASS`
- 실제 Vučević 패키지: `BOARD_REQUIRED / HOLD`
- 3팀 거래: `SEPARATE_EVENT_HOLD`
- 독립 검토: `REQUIRED BEFORE FINAL CANON FREEZE`
