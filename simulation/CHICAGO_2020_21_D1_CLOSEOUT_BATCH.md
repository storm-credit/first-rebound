# O-15F14-P — Chicago 2020–21 D1 종료 묶음

- 기준: `main` `9ce3b21`; [채택 준비 색인](CHICAGO_2020_21_ADOPTION_READINESS.md), [CP2 통합 검토](../design/CP2_INTEGRATED_REVIEW_PACKET.md), [전체 7개 게이트](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md).
- 현재 판정: `D1_EXACT_EXECUTION_OPEN / CP2_CONDITIONAL_CONTINUATION_ALLOWED`.
- 목적: 이미 회수한 세부 사실을 반복 수집하지 않고 **D1을 닫는 데 필요한 최소 증거와 그 증거가 없을 때의 다음 실행**을 한곳에서 관리한다. 여기서 새 거래·부상·계약·시즌을 채택하지 않는다.

## 1. 확정 가능한 현재 위치

K1의 Chicago 31–41·Minnesota 24–48 정규시즌 **추천**, L2의 Chicago WAS 원정 승리→IND 원정 탈락 **사건 추천**, CP2의 사전 기록된 **잠정 추첨·픽 결산**은 이미 있다. 이는 완료된 조건부 산출물이며 이번 묶음에서 재계산하지 않는다. [K1](CHICAGO_2020_21_SEASON_RECOMMENDATION.md) · [L2](CHICAGO_2020_21_EXECUTION_CLOSEOUT.md) · [잠정 추첨](NBA_2021_PROVISIONAL_DRAFT.md).

정확 실행에 필요한 F1~F5의 **전체 PASS는 0/5**, A1~A3의 **최종 채택은 0/3**, K_HEALTH·K_REGISTRATION·K_TRANSACTIONS·K_METHOD_EVENTS의 **종료는 0/4**다. 이는 증거 행 수나 완료된 조건부 계산 수가 아니라 **게이트 판정**이다. 전체 7개 매크로 게이트는 1완료·1진행·5대기, 진행 중 포함 6개가 남는다. 완료율로 환산하지 않는다.

이 패킷에서 `PASS`는 해당 경로가 요구한 근거·산술·승인된 선택을 충족한 상태, `HOLD`는 **열린 채로 증거/결정을 기다리는 상태**, `FAIL`은 특정 실행 경로가 반증되어 대안 경로와 파급 재계산이 필요한 상태다. `HOLD`는 PASS·종료·면제가 아니다. F의 증거가 없어도 A의 비교안은 준비할 수 있지만 A의 **최종 채택과 K 종료는 하지 않는다**. F는 사실/계약 경로를 검증하는 관문이고, A는 그 통과 경로 중 대체 세계 사건을 선택하는 별도 관문이므로 순환하지 않는다.

## 2. F1~F5를 한 묶음으로 닫는 증거 기준

| ID | 이미 재사용할 결과 | 정확 종료에 필요한 최소 판정 | 못 얻으면 |
|---|---|---|---|
| F1 Chicago 거래 | [비납세 범위](CHICAGO_2020_21_TAX_BOUND.md)에서 알려진 상단 $127,017,028·미포함 순증 `R_CHI≤$5,609,972` 조건, [R 구성](CHICAGO_2020_21_RESIDUAL_COMPONENTS.md)의 타팀 계약/빈자리 분류 | **3/25 거래 당시** 적용되는 R의 전체 상한 또는 실제 구성과 양측 incoming/outgoing charge를 결합해 비납세 자격·matching을 같은 사건에서 판정 | 기본급 matching 여유만으로 Theis/Green 정확 거래 PASS 불가; 승인된 선수 이동 방향을 폐기하지 않고 `K_TRANSACTIONS=HOLD` |
| F2 Boston Fournier | [자산 연쇄](NBA_2021_ASSET_CHAIN.md)의 MEM2025 출처·TPE 사용 보도/후대 잔액, [BOS 급여](BOSTON_DENVER_2020_21_PAYROLL.md)의 조건부 apron 여유 $5,381,195 | 수취일 Fournier **전체 charge**에 쓴 TPE 당일 가용액/다른 사용, 두 2R의 보호·우선권·가용성과 미포함 팀 부담을 연결 | 후대 $11.05m 잔액 역산을 당일 허가서로 승격하지 않고 거래/픽 소유 `HOLD` |
| F3 Denver Gordon | [실행 조항](CHICAGO_2020_21_EXECUTION_TERMS.md)의 공개 bonus matching, [후속](NBA_2021_EXECUTION_RESOLUTION.md)의 후행 보호 종료 보도, [DEN 급여](BOSTON_DENVER_2020_21_PAYROLL.md)의 조건부 apron 여유 $6,684,733 | **선행 1R이 실제 전달되는 분기와 2R로 전환되는 분기를 각각** 후행 1R 연결·소멸 조건과 대체 Denver의 자산 우선권/가용성·거래일 charge에 결합 | 선행 2R 전환을 후행 1R 전달로 가정하지 않고 Gordon 거래 정확 실행 `HOLD` |
| F4 Orlando Hall·후속 등록 | [등록 원장](ORLANDO_2020_21_REGISTRATION_LEDGER.md)의 5경기 추가 일반계약 1자리, [사전 보고](../research/O15F14N_HALL_MAY9_16_FOUR_PLAYER_STATUS.md)·[최종 미출전](../research/O15F14O_HALL_FIVE_FINAL_BOX_ABSENCE.md)의 4인 20행, [계약 비용](NBA_2020_21_REGISTRATION_COSTS.md)의 Hall 전액 비용안, [ORL 급여](ORLANDO_2020_21_PAYROLL_BOUND.md)의 조건부 apron 여유 $14,720,745 | §6.08의 3연속 부상 결장·서명 시점의 계속 결장 전망 요건을 **A1 대체 건강 달력에 대조**하고, A2에서 대체 리그의 신청/허가 사건·기간을 명시하며, 계약/팀 charge와 미포함 팀 부담을 결합. 실재하지 않는 대체 세계의 리그 문서를 요구하지 않는다 | 원역사 미출전 20건을 대체 허가로 읽지 않고 A2·`K_REGISTRATION=HOLD`; 비용 0 근거가 없어도 전액 비용안은 유지 |
| F5 Denver McGee | [후속](NBA_2021_EXECUTION_RESOLUTION.md)의 2023 top46·2027 무보호 보도와 Grant TPE 후보, F4에 연결된 후속 등록 | 2023 보호 시 **종료/이월**과 해당 2R 가용성, Grant TPE의 당일 실제 사용 가능액·다른 사용 및 거래일 팀 비용을 결합 | Hartenstein 단독 matching 실패 판정을 보존하고 별도 예외의 실제 사용·자산 전달을 `HOLD` |

위 금액은 각 문서가 정한 **서로 다른 시점·정의의 조건부 여유**다. Chicago의 6(j) 비납세 검사를 다른 세 팀의 apron 검사와 합산하지 않는다. 공개 보도·2차 계약표·산술 시험은 분야별 문서의 출처 등급대로만 사용한다. 실재하지 않는 리그 원장이나 미공개 계약 문구를 만들어 빈칸을 닫지 않는다.

## 3. 사실 통과 뒤의 최종 채택

| 선택 | 이미 있는 검토안 | 최종 채택 전에 필요한 것 |
|---|---|---|
| A1 건강/분 | K의 1,079행 조건부 가용성·J1 Terry 후반 공백 | 대체 세계의 건강 달력 선택과 F4 등록 자격에 미치는 영향. 실존 선수의 새 진단·의료 예후 창작 금지 |
| A2 Hall 행정 사건 | 기존 네 선수 결장·Hall hardship 사용 추천 | F4와 맞는 **대체 세계의 신청·리그 허가 사건** 선택. 원역사 허가 자동 복사 금지 |
| A3 시즌/사건 | K1/BPM 전체 경로·L2 동서부 플레이인 추천 | F1~F5·A1/A2와 모순 없는 단일 정규시즌/사건의 최종 작가 채택, 이후 추첨·픽 소유 재검증 |

A1~A3는 기존 Chicago 원클럽, 2020 지명 연쇄, Theis/Green 선수 이동 A, R1/T1~T4 방향을 **재승인받는 질문이 아니다**. 이 단계 전에는 `author_locked=false`, `season_selected=false`, `exact_execution_cleared=false`다. `G17` 전체 설계 승인과도 별개다.

A1의 세부 달력과 A3의 시즌/플레이인 대안은 [채택 준비 색인](CHICAGO_2020_21_ADOPTION_READINESS.md) 및 [L1~L4 비교](CHICAGO_2020_21_EXECUTION_CLOSEOUT.md)에서 가져온다. A2의 Hall 경로는 [등록 원장](ORLANDO_2020_21_REGISTRATION_LEDGER.md)의 자리 수와 §6.08 조건에 맞추며, 그 경로가 성립하지 않으면 **자리 조정/분 재배정 대안**을 사건·비용과 함께 제시한다. 대안 목록을 만들어 두는 것은 승인이나 원역사 사실의 변경이 아니다.

## 4. 반복 조사 중지선과 다음 실행

1. F1~F5를 **한 번의 거래일 실행 묶음**으로 다룬다. 새 자료가 나올 때 해당 필드·시각·팀·출처 등급과 판정에 미치는 효과를 위 표에 반영한다. 이미 확인된 1080경기, K1/L2, Hall 5경기, 기존 급여 기본표를 새 PR마다 다시 계산하지 않는다.
2. 특정 정확 필드를 공개 자료에서 더 확인하지 못하면 `미확인/0 아님`, 해당 F와 연결된 K를 **열린 `HOLD`**로 남기고 **같은 검색·같은 대체 자료로 재시도하는 작업을 중단**한다. 새로운 원계약/당일 장부/리그 판단/신뢰할 만한 동시대 출처가 발견되거나 명시적 실패 경로의 대안이 제시됐을 때 재개한다. 이 중지선은 게이트 면제가 아니다.
3. 정확 F1~F5가 닫히기 전까지 최종 시즌·2021 실제 순번·계약을 정본화하지 않는다. 이미 승인된 CP2에 따라 [D2 2021 선수·계약](../design/CP2_INTEGRATED_REVIEW_PACKET.md)의 **조건부 후속**을 계속한다. 기존 [60픽 비교](NBA_2021_FULL_DRAFT_COMPARISON.md)와 [G1A/E2 예산](CHICAGO_2021_23_CONTINUATION.md)은 완료 입력으로 재사용한다. 이 ID는 일곱 매크로 게이트의 추가 번호가 아니다. 다음 실행은 `CHI 잠정 #10/#39·백업 C 실명 취득·Caruso 예외 순서`의 한 경로를 거래일/등록일로 연결하는 것이다. 이 역시 정확 계약 채택이 아니다. F 경로가 실패하면 CP2 산출물은 **계속 잠정**이며 영향을 받은 입력과 후손만 다시 계산한다. 실패한 사실 위에 최종 픽을 고정하지 않는다.
4. 새로운 F 증거 또는 비용이 재계산된 대안 경로로 다섯 묶음의 정확 실행이 성립하면 A1~A3를 한 검토 패킷에서 판정한다. 그런 다음 단일 시즌/플레이인→추첨/픽 소유 재검증→네 K 묶음 PASS→D1 종료를 순서대로 수행한다. 특정 경로 `FAIL`이면 이유와 후속 자리·분·자산 비용을 남긴 뒤 영향을 받은 갈래만 다시 계산한다. `HOLD`가 하나라도 최종 사건에 남으면 D1을 종료하지 않는다.

**완료 시점은 달력 날짜가 아니라 4단계의 실제 통과로 결정한다.** 이 패킷 자체는 D1 종료가 아니다. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, `manuscript_allowed=false`를 유지한다.

문서 단독 반증에서 발견한 HOLD·CP2·F4 승인 표현의 빈틈과 처리 범위는 [R01 검토 기록](../reviews/R01_O15F14P_D1_CLOSEOUT_BLIND.md)에 둔다.
