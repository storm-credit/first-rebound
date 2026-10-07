# 2021–23 Chicago 원조건 선택 경로 최종 날짜 연결

상태: 원 매크로3의 유한 의존성 연결 완료 · 이 신규 소비기 독립 검문 대기. 중앙 완료 승격은 root 소유.

## 일곱 경로

| 선수 | 선택 소유 | 연결 |
|---|---|---|
| Nikola Vucevic | ORL | 원계약·Gamma 보존, 기존 Chicago 성장 방향 유지 |
| DeMar DeRozan | SAS | 원계약·Gamma 보존, 기존 Chicago 성장 방향 유지 |
| Lonzo Ball | NOP | 원계약·Gamma 보존, 기존 Chicago 성장 방향 유지 |
| Alex Caruso | CHI | 원계약·Gamma 보존, 기존 Chicago 성장 방향 유지 |
| Lauri Markkanen | CHI | 원계약·Gamma 보존, 기존 Chicago 성장 방향 유지 |
| Zach LaVine | CHI | 원계약·Gamma 보존, 기존 Chicago 성장 방향 유지 |
| Protagonist | CHI | 원계약·Gamma 보존, 기존 Chicago 성장 방향 유지 |

## 비용과 시간

- 2021: M1/A/SQ1의 10상태·60가족·600상태를 소비. 기존 NTMLE hardcap을 유지하며 최종 apron 상단 128,914,775 / 143,002,000, 여유 14,087,225.
- 2022: E2 22/23.76/25.52/27.28m, CX1 50m, LaVine 직접 Bird 5년 및 Young/Sato·TW가족. Kessler RSC로 기존 한 예약을 대체하고 Stanley 원 2,351,532 전액을 별도 보존. normal 162,976,941 / apron 164,614,941. 새 hardcap이 없으므로 음수 apron screen을 불법이라고 판정하지 않는다.
- 2023: Coby 12m×3와 법정 최소 4계약, 원 live9, R23 [0,16,371,000], 완전한 FA/QO 및 미사용 예외 정리를 소비. M/S는 법정 prepared 함수이며 임의 양수가 아니다. July7 J16 RSC 후 conservative annual normal/apron 상단은 `157912834+R23+6/5*S23(16,1)`.
- June22는 지명권 선택·UPC 등록 변화0이며 당시 STD/TW는 미인증. July7 유효 RT 뒤 RSC가 14→15STD/0TW를 만든다. normal unsigned hold는 같은 120% 급여로 한 번 대체한다. apron RT 차액은 `(6/5-alpha_RT)*S1`이며 일반적으로 0이 아니다.
- J16 Year4 reference는 `S3*767/500`. 모든 연도 최소 급여 제약 및 `M4<=6/5*S3*767/500`, `max(4/5,max_y M_y/S_y)<=alpha_RT<=6/5`를 유지한다. 정확 prepared cents 반올림 인증은 하지 않는다.
- Dotson/Cook standard QO는 Oct2까지 outstanding. 미수락 만료 후에도 normal FA Amount와 ROFR을 보존하며 apron의 expired QO만 제거한다. 새 UPC/현금 지급은 발생하지 않는다.
- LM1 July7 12:01 연장은 당해 급여·등록 Δ0. 2024–28 C24의 25%/법정 자격을 만족하는 30%와 고정 초년 기준 8% 함수다. MVP/수상은 선택하지 않았다. Duarte/Kessler Oct1 notice는 FY24 급여만 추가한다.

## 입력과 검문 범위

원칙의 역사 스냅샷, 원7명 계약 경로, 현행 2021/2022/2023 가족, LM1·J16 및 비용 독립 검문을 물리 SHA와 내용으로 연결한다. 반환 객체를 원디스크 독립 파싱과 비교하고 alias 오염을 거부한다. 조상 생산기는 재실행하지 않는다.
이 출력은 admitted lawful fictional implementation의 유한 연결이다. 실제 사적 금액·접수·지급·임상·외국법 전체 인증이나 원래 모든 역사 사건을 확정하는 증인이 아니다.

## 원조건 잔여와 후손

원 매크로3의 명명 입력 잔여는 0. 신규 소비기의 root/G11 독립 검문과 중앙 승격이 남는다. 다른 59신인 UPC, 전30팀 2023–24 시즌, 미보고 미래 계약을 새 선행 gate로 추가하지 않는다. 새 실제 선택이나 의무가 생기면 해당 비용·권리 포트만 재개한다.

## 프로젝트 진행

| 묶음 | 상태 |
|---|---|
| 1 기반 | 완료 |
| 2 첫 시즌 | 완료 |
| 3 2021–23 Chicago | 유한 날짜 연결 완료·신규 검문 대기 |
| 4 장기 커리어 | 미완료 |
| 5 설계 전체 | 미완료 |
| 6 Context Pack | 미완료 |
| 7 최종 승인 | 미완료 |

중앙 기준 미완료 큰 묶음 5개 / 6번까지 4개. v0.30 PARTIAL · CLOSED · Pack0 · 원고0.

## 고정 원천

- `research/MACRO3_2021_23_FINITE_EXIT_AUDIT_2026_10_08.json` — `40e01b77d63773d04f27202ae1d0197ccb5a733cf65a4f48f73abd2877e2c3ed`
- `canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json` — `253e4a4aa803cc493b0cb59715dd4eb74d4545abfe19a7161766fd7446cf9088`
- `canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json` — `9e6a4510d5f3bc2a04e667d65ac88e476583ae9de98be213f3be98165548d0ce`
- `simulation/CHICAGO_ORLANDO_2021_22_SELECTED_KEEPER_RESULTS.json` — `0b028cd28271954dc78c547475f128457cc9194d08797787e7fcd4ebf619c147`
- `simulation/CHICAGO_SAN_ANTONIO_2021_22_SELECTED_KEEPER_RESULTS.json` — `8a855d70fb97195e77caaca8062e093b7de2c9d2217c79c701fb4de1fd4fd14f`
- `simulation/CHICAGO_NEW_ORLEANS_2021_SELECTED_KEEPER_RESULT.json` — `d1975077c8879807d63763d77d58a2d89f8b481ec6c2964f0a6a9bf7a96138fd`
- `simulation/NBA_2022_23_NPC_CONTRACT_PORTFOLIO.json` — `123d07df572ac4350e9528b3f0b913b3013ad4d51584c88a94e78051b9c7af19`
- `canon/DELEGATED_2022_23_NPC_CORE_CONTRACT_EXECUTION_2026_10_08.json` — `0b03b3c9afa279b9537af21da44f70565407a284832dce71aeeb333489433da5`
- `simulation/NBA_2021_T1_SELECTED_DRAFT_EXECUTION.json` — `f8c78e99cce1b02a051c94339b550fdb52205d3988db8bbe69b780559c3bc306`
- `simulation/CHICAGO_2021_APPROVED_A_DRAFT_SIGNING_EXECUTION.json` — `11140e49baa665f18e267fa6419efa238302250b724fa51cfd3262b010b4a312`
- `research/CHICAGO_2021_A_FULL_COST_FAMILY_2026_10_07.json` — `7244beff7a120c5ca246a04e72b61586f3cfbe245487d5fc6479f5245fd78d9f`
- `simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json` — `e7d0f4b15bc06c7cd16a38d158b38a78871fb7372d412639e33bb20c31d225a7`
- `simulation/CHICAGO_2022_ROOKIE_SELECTED_EXECUTION.json` — `3c06967cf8c7171f815819efd3b4a71fb88ac77db3ae8798b34afeeeae93ce1c`
- `simulation/NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS.json` — `93264d2dff86a58ad10ca6975315c6c2167961f94f2517b6f5f79fa3113f2af8`
- `simulation/NBA_2022_23_GLOBAL_SELECTED_REGULAR_RESULTS.json` — `8e2a778fe646de3c6070be7dd3acc64199fe2a7c813e780916e380b099fa3889`
- `simulation/NBA_2022_SELECTED_FULL_POSTSEASON.json` — `b571c7645e006df1d63ead19e46343b4234034f10a9883539f52e0f9f7c7ff10`
- `simulation/NBA_2023_SELECTED_FULL_POSTSEASON.json` — `ecc876c91d1008285b944fd9b7e7213a1c3e54b94d0a2fea84cd82b2f7cb0407`
- `simulation/CHICAGO_2023_SELECTED_ROUTINE_EXECUTION.json` — `9a4f6db21d6ad50e2c6d6897f1c2dedbdf440cee89bae47019f4bd131f341790`
- `simulation/CHICAGO_2023_ROUTINE_COST_DOMAIN.json` — `13448f381896ee9da4da16e9716b98f7bb511ecd42b527dcba26802a64ba1f8d`
- `reviews/CHI_2023_SELECTED_ROUTINE_EXECUTION_G11_INDEPENDENT_REVIEW_2026_10_08.json` — `e9bfc3699dd2da3c4cfd6871e05f1b729748674018e617f098f3e5138065f169`
- `reviews/CHICAGO_2023_ROUTINE_COST_DOMAIN_G11_INDEPENDENT_REVIEW_2026_10_08.json` — `a05b70a2234dd9efd4f3243f2f6a0e03cc7402f91ec477b12b3864ff626a3fb7`
- `simulation/LAMELO_2023_SELECTED_EXTENSION.json` — `98f03115f8a71a7f2e0ac3f9376aae5f94647d62c8ce6d942b63881af629483d`
- `reviews/LAMELO_2023_SELECTED_EXTENSION_G11_INDEPENDENT_REVIEW_2026_10_08.json` — `abea927ebaac99d389a07d128b47d016adb0a387cc709e23a5e58b21597627d3`
- `research/CHICAGO_2023_NAMED_DRAFT_CLAIMS_AND_COST_PORTS_2026_10_08.json` — `b139af4af09a48dd1c9e345d17d05fc8e38f4cb021193f32bc3a09ed537f49e3`
- `canon/DELEGATED_2023_DRAFT_ORIGIN_DRAW_DECISION_2026_10_08.json` — `6df7f62328263c0b3864e2d4a05cb4a5b56edbd332d5d31556627c6b421d9292`
- `simulation/CHICAGO_2023_SELECTED_ROOKIE_EXECUTION.json` — `61979a4edc201e314cf7e523393fbe3131f8d3eec547b530ede260729a791511`
- `reviews/CHI_2023_SELECTED_ROOKIE_EXECUTION_G11_INDEPENDENT_REVIEW_2026_10_08.json` — `2cec63e86be97c86429667a1907312c59833e6d374b5cfc4617491abe337ee6c`
- `reviews/CHI_2023_J16_EXTERNAL_DISPOSITION_2026_10_08.json` — `e6ee358b1d845ce383a6e98def0849d9d508442a2bae7b7746fdebb94a187abc`
- `tools/build_macro3_2021_23_selected_dated_exit_join.py` — `05b2df546e35f81c05331db243273f9293d2b1131777a7254fd3346480e7f30c`
