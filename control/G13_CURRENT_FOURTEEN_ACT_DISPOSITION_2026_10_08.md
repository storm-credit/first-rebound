# 14막 현행 출구 지원 판정표

상태: **원 14막·42소막·60함수의 현행 지원 합성 준비 / 독립 검문 대기**. 이 문서는 새 정본·사건·좌표·whole 역사 완료를 만들지 않는다.

## 현재 범위

**10/14는 서로 다른 한정 지원 범주의 합계**다: 기존 bounded 기능 출구 수용 5(A01–05), 선택된 한정 실행 지원 2(A06/A09), 조건부 협상 표본 지원 1(A07), 새 root literal 기능 출구 수용 2(A08/A10). 이 수를 10개 whole 역사 완료나 42소막 전체실행 완료로 읽지 않는다. 미래 막 출구는 A11–14 **4개**다.

| 막 | 원 선택 · 비용 · 출구 | 현행 범위 |
|---|---|---|
| A01 | 개인 과시 대신 팀의 가장 낮은 일을 받아들임 · 즉시 인정·자유시간 · **팀에 다시 나올 이유를 얻음** | PRIOR_ACCEPTED_BOUNDED_FUNCTIONAL_EXIT |
| A02 | 빅맨 지위를 버리고 윙 기술·학사 책임을 배움 · 익숙한 서열·주전 지위 · **프렙 졸업과 NCAA 진입 근거** | PRIOR_ACCEPTED_BOUNDED_FUNCTIONAL_EXIT |
| A03 | 기여할 수 있는 좁은 역할을 반복 · 개인 쇼케이스·출전 불만 · **대학 소속과 드래프트 평가 자료** | PRIOR_ACCEPTED_BOUNDED_FUNCTIONAL_EXIT |
| A04 | 과장된 공격 완성도 대신 성장 증거 제시 · 지명 순번 불확실성 · **Chicago의 계약·개발 책임** | PRIOR_ACCEPTED_BOUNDED_FUNCTIONAL_EXIT |
| A05 | 자기관리 재발의 기회를 잃고 반복 준비 · NBA 출전 기회·편한 생활 · **로테이션과 약한 손·직선 공격 신뢰** | PRIOR_ACCEPTED_BOUNDED_FUNCTIONAL_EXIT |
| A06 | LaMelo의 창조와 LaVine의 득점을 살림 · 온볼 기회와 빠른 승리 욕망 · **K1/L2 잠정 탈락·2021 #10/#39** | CURRENT_SELECTED_BOUNDED_EXIT_SUPPORT |
| A07 | 엘보 카운터를 실제 압박에서 시험 · 효율 변동·기존 베테랑의 분 · **첫 장기 계약 협상 표본** | CONDITIONAL_ACCEPTED_SAMPLE_SUPPORT |
| A08 | E2 협상과 동료 자원의 동시 비용 수용 · 싼 계약 신화·무제한 전력 보강 · **공동 에이스 권한과 예산 책임** | ROOT_ACCEPTED_LITERAL_FUNCTIONAL_EXIT |
| A09 | 대표팀에서 제한적 권한 공유 · 보험·허가·캠프와 개인 훈련 시간 · **완전 화해 없는 협력·다음 시즌 부하** | CURRENT_SELECTED_BOUNDED_EXIT_SUPPORT |
| A10 | 짧은 자가 창조와 더 나은 다음 선택을 결합 · LaVine과 클로징 권한·수비 부담 · **최우선 코어 후보, 우승 자격 시험** | ROOT_ACCEPTED_LITERAL_FUNCTIONAL_EXIT |
| A11 | 공격·수비 출력과 동료 선택을 분담 · 리그 최고 평가와 시리즈 패배의 간극 · **MIN과 첫 파이널 패배 후보·구조적 결함 노출** | FUTURE_ACT_EXIT_PENDING |
| A12 | LaMelo·LaVine·주인공 비용을 함께 감당 · 벤치 깊이·역할·새 계약 · **개인 증명과 팀 실패를 분리, 재대결 자격 재획득** | FUTURE_ACT_EXIT_PENDING |
| A13 | 수비 리바운드 뒤 유리한 동료의 득점을 만듦 · 자기 슛의 영광·패스 실패 책임 · **CHI–MIN 재대결 승리와 주제 회수 후보** | FUTURE_ACT_EXIT_PENDING |
| A14 | 분·계약·폭발력 감소를 받아들임 · 지위와 마지막 계약 규모 · **원클럽 은퇴·후배가 이어받는 준비 습관** | FUTURE_ACT_EXIT_PENDING |

## prior 라벨 뒤의 실제 근거

- **A01–02**: [원 audit](../design/A01_A02_SUBACT_EXIT_AUDIT_2026_10_07.json) `/act_exit_rows/0..1`. 다음 훈련/공 준비의 이유와 프렙 졸업·별도 여름 NCAA 진입 근거의 한정 pass다. 당시 A01-S1 기본 준비 부족은 후행 같은 체험 [W 선택](../design/A01_E2_LITERAL_COST_WITNESS_SELECTED_OVERLAY_2026_10_08.json)과 수용 Blueprint 보충을 참조하며 원 audit 이력을 덮지 않는다.
- **A03–04**: [기관/동료 bridge](../design/A03_A04_FINITE_EXIT_BRIDGE_2026_10_07.json) `/A03_teammate_assignment`, `/A04_institutional_responsibility`, `/audit_promotion`. 동료의 직접 좁은 재배정과 가상 Chicago RSC·개발 과제 인수가 안내보다 강한 직접 근거다. 정확 지명·개인 박스·실임상은 추가하지 않는다.
- **A05**: [원 audit](../design/A05_SUBACT_EXIT_AUDIT_2026_10_07.json) `/act_exit_row`, `/subact_exit_rows/2`. 예정 기회 한 번 상실, 개발/복귀, 두 첫 벽 이양 수령·한정 재배정의 운영 신뢰다. 생활 완치/전체 포제션 안정성은 아님.
- **A06/A09**: [현행 선택 join](../design/A06_A08_A09_CURRENT_SEASON_EXIT_JOIN_2026_10_08.json) `/A06_current_S2_join`, `/A09_private_cooperation_return_join`와 [독립 수용](../reviews/A06_A08_A09_CURRENT_SEASON_EXIT_JOIN_G11_INDEPENDENT_REVIEW_2026_10_08.json). 선택 K1/L2·F1·#10/#39 및 허가·위험 비용을 낸 한국 private cooperation/Chicago 준비 복귀를 재사용한다. A09의 공개대회·메달·병역은 별도며 미래 NBA 경기 결과가 원 private 협력/복귀 출구의 새 조건은 아니다.
- **A07**: [원 조건부 audit](../design/A07_A08_SUBACT_EXIT_AUDIT_2026_10_07.json) `/act_exit_rows/0`와 [변경 수비 평가](../design/A07_CHANGED_DEFENSE_ROLE_EVALUATION_2026_10_07.json). 원 두 MISS와 새 두 수비 관측을 좋은/실패 자료로 함께 전달한다. 국소 판단·32분 배분을 시즌 기록/QO/계약 수락으로 바꾸지 않는다.

## A08/A10 옛 HOLD의 현재 대체

[A08 root 판정](../reviews/A08_CURRENT_LITERAL_EXIT_ROOT_DISPOSITION_2026_10_08.json)은 E2 예산 비용과 5개의 명시적 코치 허용 창·두 마무리 조건/상호 비용으로 **원 한정 기능 막 출구**를 수용했다. 원문은 경기별 공동 에이스 후보다. 지속·영구지위나 두 득점 성공을 필수로 추가하지 않으며 부모의 false/pending는 생성 이력으로 유지한다.

[A10 root 판정](../reviews/A10_CURRENT_LITERAL_EXIT_ROOT_DISPOSITION_2026_10_08.json)은 Game1 실패/조기 이양·LaVine 공유 클로징/수비 비용 뒤 QUAL1의 자격 setting와 독립 시리즈 비용 관측을 연결해 원 최우선 코어 후보·우승 자격 시험을 수용했다. 옛 QUAL1 미선택 HOLD는 이 범위에서 해소된다. 시리즈 승리·타이틀·전체82·영구 효율은 원 한정 출구의 추가 조건이 아니다.

두 판정의 물리 source pins와 원 CP2 choice/cost/exit를 직접 대조했다. 다른12막을 자동 수용하거나 원 부모·중앙 상태를 다시 쓰지 않는다.

## 실제 남은 네 막

| 막·창 | 이미 확보한 계약 입력 | 아직 미선택 좌표 | 관측·정보·배치의 유한 잔여 |
|---|---|---|---|
| A11 · 2025–26 | [FY25 named15](../simulation/CHICAGO_2025_NAMED15_CONTRACT_JOIN_2026_10_08.json) · source/peer 수용 | 최초 CHI–MIN Finals 패배의 연도·진출·결과, 필요 평가/수상 범주 | 선택 실패 창의 역할 분담·수비 도움 비용/구조 결함을 원 국소 기능과 연결. 계약이 건강/Finals 결과를 자동 만들지 않음 |
| A12 · 2026–27 | [FY26 named15](../simulation/CHICAGO_2026_NAMED15_CONTRACT_JOIN_2026_10_08.json) · 기존6+새9/holdonce/Γ/6비용 결합 수용 | 첫 실패 뒤 재대결 자격 경로/필요 창 | 선택 계약·벤치/역할 비용을 재분담/재시험과 재자격에 연결. 원 에이전트 질문의 미합의 이력은 유지하되 완료 UPC를 다시 미작성으로 만들지 않음 |
| A13 · 2027–28 | 완료 기간·권리/옵션 가족을 선택 창에 재사용. 당해15명/가용 전체선택이라고 주장하지 않음 | 재대결 승리·마지막 수신자·득점 인과 | 최소3막 상호 비용·이전 유사실패 → 수비/리바운드/전진/더 유리한 동료 이양/독립 수령·득점·신뢰 반응. 잠긴 기능과 수행 결과를 구분 |
| A14 · 2028–35 | 완료 장기 계약/원 Γ를 필요한 후기 대표창에서 재사용 | 정확 원클럽 은퇴·후기 전환 좌표 | 줄어든 분·지위·계약/폭발력 비용과 후배의 독립 준비. 기존 국소 표본을 전체 은퇴 실행으로 재명명하지 않음 |

좌표 미선택 중 FY27/FY28/… 매년15명 minimum 준비를 자동 다음 필수로 부활시키지 않는다. 선택된 역할/Finals/은퇴창에서 실제 영향을 주는 만료·옵션·거래·기간 공백만 명명 전이한다. S2 준수 가족의 Γ·서비스·법적 구간은 재사용하며 unknown을0으로 채우지 않는다. 실제 private 영수증이나 모든 NPC 원역사는 새 완료 gate가 아니다.

## G13 → G14 원 선행조건 보존

[Context Pack 원 규칙](../context-packs/README.md):

> 전체 Act/Sub-Act/회차 기능표와 역사 사건 원장이 잠기고, 해당 구간의 `ACTUAL_VERIFIED` Blueprint와 현행 Canon을 확보한 뒤 생성한다.

전체 역사 사건 원장 잠금을 사용 사건만의 부분 잠금으로 대체하지 않는다. 이는 모든17시즌을 동일 깊이로 전경기/실사적 역사 인증하라는 요구도 아니다. 60개 ACTUAL_VERIFIED Blueprint 참조는 사용권이며 60개 공개회차·780개 필수 사건이 아니다. [최종배치 입력](G13_FINAL_ALLOCATION_INPUT_INDEX_2026_10_08.json)과 [정보 준비11](G13_NULL_INFORMATION_BOUNDARY_ACCEPTED_INPUT_2026_10_08.json)는 준비된 입력이고 최종배치·장면 접근/POV 잠금은 아직 아니다. 최종 N 작업단위 전체 Pack은 원 선행조건 뒤 생성·검문한다. CLOSED에서 집필 전 Pack 검문은 가능하며 원고 사용 허가는 별도다.

## 현재성과 검사 범위

기준 main `17ade30f9560e7d87eb1d7d1c911f11f3921c0ee`. 등록기/옛 overlay는 이 commit의 전체 SHA를 역사로 보존하고 현행 소비 projection을 직접 비교한다. 무관한 후행 진척의 전체 SHA 변화가 새 STALE gate가 되지 않는다. 원 choice/cost/exit·권한·기능 source가 바뀌면 그 범위만 다시 검문한다.

실제 정적 대조: CP2 14막 선택/비용/출구와 42소막 출구, 현물 60함수 id/entry/exit/order, 60 Blueprint qualified 참조, 새 root 2판정 literal/pin, FY25/FY26 peer/등록 범위를 확인했다. A02-EF001은 원 E9 미답 exit가 아니라 **별도 가상 프렙 bridge 뒤 entry**와 등록 행을 대조한다. 원문/Blueprint/원 함수 복제0, 새 constructor/음성검사0, 조상 전체 법문·비용·시즌 재감사0. 현 sibling 독립 검문은 대기다.

## 진행

| 번호 | 공정 | 상태 |
|---|---|---|
| 1 | 2020 드래프트 연쇄 | 완료 |
| 2 | 2020–21 세계·시즌 | 완료 |
| 3 | 2021–23 계약·선택시즌 | 완료 |
| 4 | 장기 커리어·막 출구 | 미완료 — 네 미래 막 출구/좌표 |
| 5 | G13 사건·기능·최종배치 | 미완료 |
| 6 | 집필규격·Context Pack | 미완료 · Pack0 |
| 7 | 통합·독립·최종승인 | CLOSED |

미완료 큰 묶음4개, 6번까지3개. v0.30 PARTIAL · CLOSED · Pack0 · 원고0.
