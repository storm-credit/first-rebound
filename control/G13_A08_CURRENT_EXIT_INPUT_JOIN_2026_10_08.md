# A08 현행 출구 입력 연결

상태: **3소막 한정 근거 연결 준비 · root 독립 판정 대기**. 새 기능·사건·계약·출구를 선택하지 않는다.

## 결론

원 A08-S3 출구는 **“경기별 공격 권한과 준비 책임을 함께 가지는 공동 에이스 후보”**다. 원 성공기준은 자기/동료 마무리 **조건 설명**과 상호 비용이며 영구 공동 에이스 지정이나 두 득점 성공을 요구하지 않는다. 선택 E2의 동료 예산 비용과 Oct19 2022 다섯 코치 허용 호출은 이 한정 의미를 지원한다. 추가 관측·기관 모델 사건 부족은 **0**이며, 남는 작업은 root의 한정 통합 판정 **1**이다. whole Act/전체 G13 완료를 이 파일에서 선포하지 않는다.

## 원 출구와 현재 근거

| 소막·등록 함수 | 원 출구 | 기관/허용 조건 | 기능 관측과 현재 근거 |
|---|---|---|---|
| A08-S1 · EF001 · order40/slot383 | 선수 요구와 프런트 계약 권한이 구분된 코어 유지 제안 | 선수의 제안/에이전트 질문과 구단·선수의 UPC 합의를 분리 | B1/B2 한 장 비교·질문 → 현행 RT1–4 공개 비용/자리 비교 → 별도 선택 E2/CX1/LaVine 가족 및 보호/Γ 비용 연결 |
| A08-S2 · EF002 · order41/slot384 | 압박 속 라이브 패스의 사용/중단 조건 표본 | 해당 NBA 창의 적법 명명 가족·코치 허용·동일 시계 | G0 캐치 즉시 반환, G1 드리블 후 턴오버/복귀 시도, G2 다른 열린 후방길 안전 재전개 |
| A08-S3 · EF003 · order42/slot385 | 경기별 공격 권한·준비 책임을 가진 공동 에이스 후보 | 두 비교 창의 한정 코치 허용 | G3A 자기 짧은 창 시도/중단, G3B LaMelo 우위 이양 뒤 재관여 + 자기/동료 마무리 조건과 포제션 비용 설명 |

### 근거 포인터

- [원 CP2](../design/CP2_ACT_SUBACT_PACKET.json): `/acts/7`, `/subacts/21`–`/subacts/23`.
- [원 최종 기능](../design/A08_FINITE_FUNCTION_BATCH_2026_10_07.json): `/functions/0`–`/functions/2`; 원 entry/exit·훈련/제안 제한을 바꾸지 않는다.
- [현행 RT 비교](../design/A08_S1_CURRENT_RT_COST_SLOT_FAMILY_2026_10_07.json): `/formula_rows`, `/fictional_agent_handoff`. 원 768행을 다시 감사하지 않았다.
- [선택 코어 가족](../simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json): `/event_trace/5`, `/cost_on_2022_07_07`. E2는 direct Full Bird 가상 상호 합의다. 실제 지급/수락 인증이 아니다.
- [선택 계약·게임 연결](../design/A06_A08_A09_CURRENT_SEASON_EXIT_JOIN_2026_10_08.json): `/subact_exit_rows/3`–`/subact_exit_rows/5`, `/A08_selected_contract_and_game_join`.
- [수용 독립 검문](../reviews/A06_A08_A09_CURRENT_SEASON_EXIT_JOIN_G11_INDEPENDENT_REVIEW_2026_10_08.json): `/direct_checks`, `/source_sha256`, `/physical_source_checks/source_pins`. 생성 당시 부모 `independent_review_completed:false`를 고쳐 쓰지 않고 후행 수용 권위를 참조한다.
- [마무리 조건 설명](../design/A08_CONDITIONAL_GAME_CALL_FAMILY_2026_10_07.json): `/cp2_contract/S3_finish_conditions_explained_without_result_selection`.

## 권한·시간·비용 경계

주인공의 역할 자료와 에이전트 질문만으로 프런트 계약 권한을 얻지 않는다. 후행 선택 계약 가족을 별도로 붙이며 그 내용을 원 B1/B2 시점에 소급 전달하지 않는다. 새 원고·대사·내면·비공개 정보 접근을 만들지 않는다. 원 기능의 순서는 EF001→EF002→EF003이며 원 beat의 정확 날짜는 null이다. 명명 계약 Jul7 2022와 선택 호출 Oct19 2022의 순서는 알려져 있다.

선택 호출은 `PUBLISHED_2022_0007`, MIA–CHI, `[0,20)`, `[40,60)`, `[80,100)`, `[120,140)`, `[160,180)`초다. 각 창 20초, 총 100초이며 새 팀 시간은 0이다. 같은 5인/포지션과 양팀 240분 검문은 수용 peer를 재사용한다. 이번 직접 검사는 호출 원 의미·허용·서로 겹치지 않는 창·CHI 14,400 player-seconds의 부분 연결이다. 전체 정규 결과나 실제 NBA 포제션을 재인증하지 않는다.

Jul7의 넓은 비용 예약과 후행 Kessler 서명·Stanley 보호 예약은 날짜별로 구분한다. 두 시점 상단을 더하거나 미수락 RT 예약을 실제 법정 급여로 만들지 않는다. 음의 apron 스크린 여유도 그 자체로 위법 판정이 아니다. 원 Γ와 적용 Bird/min/RSC/TW 법적 조건은 수용 가족의 범위대로 유지한다. 실제 비공개 장부·영수증 부재는 새 완료 gate가 아니다.

## 낡은 HOLD의 현재 의미

현재 whole-Act overlay의 추가 창은 **원 Act를 지속·영구 공동 에이스 권한으로 해석할 때만** 조건부다. 원 소막의 ‘경기별 후보’와 조건 설명에는 새 지속기간 문턱이 없다. 그러므로 추가 호출을 자동 필수화하지 않는다. 영구 지정·상시 클로징권을 새로 주장하려면 별도 근거가 필요하지만 이번에 그 강한 지위를 선택하지 않는다.

대표팀 실제 수락·메달·병역, 전체 임상, 새로운 MVP/타이틀·2028 수취인/득점은 이번 출구 입력이 아니다. 원 부모의 미실행/whole false는 생성 이력으로 보존한다. 새 중앙 상태 채택은 root 독립 판정 이후이며 원 60개 기능이나 Blueprint를 복제하지 않는다.

## 현재성 방법과 실제 검사

원 기준은 main `6dd065685839886f53b6b4fc15cd3613c1831859`이다. 변하는 등록기/whole-Act 파일은 그 commit의 전체 SHA를 이력으로 남기고 현행 **A08 세 행/Act 경계 projection**을 직접 비교했다. 무관한 후행 진척으로 전체 파일 SHA가 변해도 A08 핵심 projection 불변이면 자동 STALE로 만들지 않는다. A08 entry/choice/cost/exit·권한 의미가 바뀌면 이 근거를 다시 검문해야 한다.

실제 정적 검사: 원 3소막 choice/cost/exit, 등록 3함수 entry/exit/order/slot, 5호출의 원 의미·허용·비중복, 수용 peer의 3개 본체 핀과 소비 관련 5개 원천 핀, 변동 원천 A08 projection 2개와 참조 pointer를 대조했다. 생성기/constructor 음성 검사 0, 조상 전체 비용·법문·시즌 재감사 0, 새 독립 peer 0. 세부 현물 SHA·projection·원 literal은 동반 JSON에 있다.

## 진행

| 번호 | 공정 | 상태 |
|---|---|---|
| 1 | 2020 드래프트 연쇄 | 완료 |
| 2 | 2020–21 세계·시즌 | 완료 |
| 3 | 2021–23 계약·선택시즌 | 완료 |
| 4 | 장기 커리어·막 출구 | 미완료 — A08 한정 출구 근거 인계 |
| 5 | G13 사건·기능·최종배치 | 미완료 |
| 6 | 집필규격·Context Pack | 미완료 · Pack0 |
| 7 | 통합·독립·최종승인 | CLOSED |

미완료 큰 묶음 4개, 6번까지 미완료 3개. v0.30 PARTIAL · CLOSED · Pack0 · 원고0.
