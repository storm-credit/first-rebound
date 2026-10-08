# A12 FY26 선택 코어 역할·비용 입력

기준 main `2e630100bf98e83bff79f8e45314e70d9a0bde1c`. 상태: 입력 준비 완료·독립 검문 및 FY26 감독 선택 대기. 원고 CLOSED.

## 계약 입력과 시점

수용된 FY26 named15와 G11 계약 결합 검문을 재사용한다. 2026-07-07 12:18 ET에 기존 UPC6+새 UPC9=15STD/0TW가 같은 합법 가족 조건에서 결합한다. 이는 실제 NBA 접수 인증이 아니며, July7 비시즌 등록과 뒤의 정규시즌 역할 창은 별개다. FY말 June30을 선수 서비스 종료일로 바꾸지 않는다.

| 선수 | July7 법적 유형 | normal/apron 급여 | 선수 fullcash |
|---|---|---|---|
| Lauri Markkanen | LIVE_EXISTING_2025_UPC_YEAR2 | 41754690 | 41754690 |
| Alex Caruso | LIVE_EXISTING_2025_UPC_YEAR2 | 20877345 | 20877345 |
| Wendell Carter Jr. | SELECTED_NEW_OWN_BIRD_WC26B | 18000000 | 18000000 |
| Protagonist | SELECTED_NEW_OWN_BIRD_P26A | 3/10*C26world | 3/10*C26world |
| Zach LaVine | EXERCISED_EXISTING_2022_UPC_YEAR5 | 48967380 | 48967380 |
| Coby White | SELECTED_NEW_OWN_BIRD_CW26B | 20000000 | 20000000 |
| Chris Duarte | LIVE_EXISTING_2025_UPC_YEAR2 | 12000000 | 12000000 |
| Walker Kessler | SELECTED_NEW_OWN_BIRD_K26A_NOT_QO_ACCEPTANCE | 12000000 | 12000000 |
| LaMelo Ball | LIVE_EXISTING_LM1_EXTENSION_YEAR3 | {'ordinary': '29/100*C24_original', 'legal_HigherMax_only': '87/250*C24_original', 'HigherMax_selected': False} | {'ordinary': '29/100*C24_original', 'legal_HigherMax_only': '87/250*C24_original', 'HigherMax_selected': False} |
| Jaime Jaquez Jr. | EXERCISED_SAME_2023_RSC_YEAR4 | 2301/1250*S23(16,3) | 2301/1250*S23(16,3) |
| Thaddeus Young | SELECTED_NEW_ONE_SEASON_MIN26_A | M26(2,1) in common IV6(h)-eligible oneYear family | M26(10,1) |
| Javonte Green | SELECTED_NEW_ONE_SEASON_MIN26_A | M26(2,1) in common IV6(h)-eligible oneYear family | M26(7,1) |
| Joe Wieskamp | SELECTED_NEW_ONE_SEASON_MIN26_A | M26(2,1) in common IV6(h)-eligible oneYear family | M26(5,1) |
| Denzel Valentine | SELECTED_NEW_ONE_SEASON_MIN26_A | M26(2,1) in common IV6(h)-eligible oneYear family | M26(10,1) |
| Tomas Satoransky | SELECTED_NEW_ONE_SEASON_MIN26_A | M26(2,1) in common IV6(h)-eligible oneYear family | M26(10,1) |

원 LaMelo C24 계수와 LaVine 원 2022 UPC의 PO를 유지한다. 코어 급여 감액·새 capworld·HigherMax 결과를 선택하지 않는다. 선수별 계약/가족 포인터와 source SHA는 JSON에 있다.

## 같은 비용, 서로 다른 새 역할 후보

| 후보 | 주인공 | LaMelo | LaVine | 다른 8명 양수·벤치 | 시계 |
|---|---:|---:|---:|---|---|
| A32 | 32분 | 28분 | 30분 | 원 분배 유지 | 24×120초·5포지션×48분=240분 |
| B34 | 34분 | 28분 | 28분 | A32와 동일 | 두 번째 블록 SG만 LaVine→주인공 |

두 안 모두 15STD/0TW, 새 후보 active13/inactive2, court5+다른 active8이다. 양수11명과 0분 Green/Satoransky를 명명한다. 원 FY25 시계는 구조·이름 근거로만 재사용하며, FY26 건강·감독 호출·실제 경기 스틴트는 아직 선택하지 않는다. 상대·날짜·gameid·OT는 null/미선택이다.

권고: A32를 비교 기준으로 두고 B34의 2분 역할 이동을 한정 시험 후보로 root에 인계한다. B34는 주인공의 노동을 늘리고 LaVine의 2분을 덜어낸다. 두 후보는 같은 계약 급여·cash·Γ이며, 출전 시간은 공 소유 시간이나 효율의 증거가 아니다. 새로운 가격 할인이나 벤치 보강을 약속하지 않는다. B34의 변경은 120–240초 블록 SG의 LaVine→주인공 하나이며 다른 23블록과 PG/SF/PF/C는 그대로다. LaMelo의 첫 연결과 LaVine의 남은 바깥 수신·득점 준비 기능을 보존한다. 주인공의 추가 120초 과제는 짧은 연결·무볼 재배치·담당 코너 복귀 노동이며 추가 드리블/슛 할당이나 성공 판정이 아니다. 가용성은 지속 위임에 따른 별도 새 설계 선택 후보이며 임상 추론이나 FY25 건강 상속이 아니다.

## 비용을 지우지 않는 연결

선택 current Salary: `173599415+L26(C24_original)+3/10*C26world+2301/1250*S23(16,3)+5*M26(2,1)`.

선수 fullcash의 최소계약5는 `3*M26(10,1)+M26(7,1)+M26(5,1)`이다. M26(2,1) Salary와 지급 cash를 혼동하지 않으며 환급은 시즌 뒤다. R26_N/R26_A/N26/A26와 whole normal/apron/tax/cash는 null이므로 0으로 더하지 않는다.

원 6범주 current Salary, 고유 Γ, FA/QO/FRN, unsigned draft/RT, 당해 예외, 명단·floor·tax·cash를 그대로 참조한다. 새 역할분배는 두 후보 간 계약비용 Δ0이다. 합법적 Bird/minimum 서명 자체가 신규 hardcap을 만들지 않으며, 높은 apron 합계가 해당 서명의 자동 위법 판정은 아니다. 이후 거래 제약이나 다른 유효 트리거는 지우지 않는다.

## 정보 접근과 원 함수

2026-06-17 허가된 CHI 자체 영상 검토에서 주인공은 자기 조기 도움·복귀 오류를 본다. July7 계약/역할 준비의 동기로 연결하되, 영상이 가격의 유일한 원인이었다고 주장하지 않는다. 접근 범위는 자기 행동·보이는 동료 반응·허가된 자기 영상·전달된 코치 과제다. 동료 마음·MIN 사적 예산·미래 결과는 알지 못한다.

기존 EF52–54의 entry/choice/cost/exit·생성 당시 pending/미합의 문구를 보존한다. 새 계약 입력 수용은 별도 후행 사실이다. 기존 연습 실패를 새 Finals 실패나 FY26 실전으로 다시 명명하지 않는다. 현행 명칭의 이전 register 대신 실제 60행 A14 register의 행52–54와 독립 root peer를 대조했다.

| 원 기능 | 원 국소 출구 | 현재 새 입력/남은 포트 |
|---|---|---|
| A12-EF-001 (52) | 유지할 사람과 기능을 구분 | Root chooses one FY26 coach role family, then assigns P a bounded own-film/current-contract comparison: retained person, next-link function, corner/help-return worker, and own demand in separate columns. Team/agent authority remains separate. This packet prepares input; it does not assert that this follow-up briefing has happened. |
| A12-EF-002 (53) | 속도와 책임의 분산 | After root coach/availability choice, use a bounded authorized two-combination task and inspect own extra carry versus short link and assigned corner return. Observe teammates visible stop/change-of-direction and next link; no scored basket or improved efficiency required or awarded by this packet. |
| A12-EF-003 (54) | 재대결을 선지급하지 않음 | A later separately selected bounded season/qualification route needed for original Act exit rematch qualification. Dates, scores, awards, Finals rematch and title remain unselected. No repeated nine-contract or all82/all30 private audit is required to choose a small role trial. |

S1 이름·기능 비교와 S2 속도·책임 시험은 기존 국소 증인이 있다. 새 FY26 15계약과 역할에 결합할 선택·관측 포트2개를 남긴다. 원 Act의 재대결 자격 재획득은 별도 후속 시즌/자격 경로1개다. 이 입력은 MVP·첫우승·전체82결과·재대결을 선지급하지 않는다. 새 9계약 재작성, 전체30팀·임상·사적 접수 전수 게이트를 추가하지 않는다.

## 실제 검문

15개 계약행의 60포인터, join12/film6 물리 핀, 세 독립 peer의 원 핀, EF52–54 정확 이양, 48블록/240포지션셀·고유5명·13/2 분할을 직접 대조했다. CBA PDF453 XXIX1–2의 active12–15·bench8·14/15 aggregate를 직접 읽었다. 검사 작성자는 본 에이전트이며 독립 peer 수용은 아직 아니다. 정적 파일이므로 constructor 음성 검사0, 계약 producer 재실행0, 새 외부 검색0.

중앙 register/disposition은 main snapshot과 A12 의미 projection을 분리한다. 후행 무관 진척문구가 원 A12 근거를 자동 STALE로 만들지 않으며 민감한 A12 원문 변경은 새 대조가 필요하다.

## 진행표

| 단계 | 항목 | 상태 |
|---:|---|---|
| 1 | 2020 드래프트 연쇄 | 완료 |
| 2 | 2020–21 세계·시즌 | 완료 |
| 3 | 2021–23 계약·선택시즌 | 완료 |
| 4 | 장기 커리어·막 출구 | 진행 |
| 5 | G13 사건·기능·최종배치 | 미완료 |
| 6 | 집필규격·Context Pack | 미완료 |
| 7 | 통합·독립·최종승인 | CLOSED |

미완료4 / 6번까지3. freeze v0.30 PARTIAL·Pack0·원고0·CLOSED.

### 핵심 파일

- [FY26 named15 계약 결합](../simulation/CHICAGO_2026_NAMED15_CONTRACT_JOIN_2026_10_08.json)
- [그 결합 독립 검문](../reviews/CHICAGO_2026_NAMED15_CONTRACT_JOIN_G11_REVIEW_2026_10_08.json)
- [원 CP2](../design/CP2_ACT_SUBACT_PACKET.json)
- [실제 60행 함수 등록기](../control/G13_A14_FUNCTION_EXECUTION_REGISTER_2026_10_08.json)
- [A11 자체 영상 이양](../simulation/A11_F26_SELECTED_ROLE_COST_AND_VIDEO_HANDOFF_2026_10_08.json)
- [본 구조 데이터](A12_FY26_SELECTED_CORE_ROLE_AND_COST_INPUT_2026_10_08.json)
