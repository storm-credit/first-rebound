# Chicago FY25 — 기존 live UPC 다섯 연차 입력

새 비교가격·재계약 선택이 아니라 이미 선택된 기존 계약의 2025–26 해당 연차 전개다. Carter/P/LaVine은2022 시작 계약의4번째, Coby는2023 새 UPC의3번째, LaMelo는2024 확장term의2번째다. FY24 금액을 그대로 복사하지 않는다.

| 선수 | FY25 연차 | 기존 regular salary 참조 |
|---|---:|---:|
| Wendell Carter Jr. | 4 | 10,850,000 |
| Protagonist | 4 | 27,280,000 |
| Zach LaVine | 4 | 45,999,660 |
| Coby White | 3 | 12,000,000 |
| LaMelo Ball | 2 | 37,958,760 / 45,550,512 조건부 |

고정4명의 합계는 96,129,660달러다. LaMelo ordinary를 연결한5명 regular-base 합계는 **134,088,420달러**, 적법 HigherMax를 연결하면 **141,680,172달러**다. 두 분기의 수상 결과는 선택하지 않았다. 추가 원Γ·deemedcharges·다른선수는 이 부분합 밖에서 보존한다.

## 원 연차 pointer

- **Wendell Carter Jr.**: `simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json#/contract_terms/Carter`
  - 해당 연차: `simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json#/contract_terms/Carter/source_terms/extension_regular_salary_schedule/2025-26`
- **Protagonist**: `simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json#/contract_terms/Protagonist`
  - 해당 연차: `simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json#/contract_terms/Protagonist/source_terms/salary_2022_onward/3`
- **Zach LaVine**: `simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json#/contract_terms/LaVine`
  - 해당 연차: `simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json#/contract_terms/LaVine/salary/3`
- **Coby White**: `simulation/CHICAGO_2023_SELECTED_ROUTINE_EXECUTION.json#/named_contracts_and_rights/3`
  - 해당 연차: `simulation/CHICAGO_2023_SELECTED_ROUTINE_EXECUTION.json#/named_contracts_and_rights/3/salary_schedule/2`
- **LaMelo Ball**: `simulation/LAMELO_2023_SELECTED_EXTENSION.json#/selected_terms`

## LaMelo 2번째 확장연차

`C24=140,588,000`에 ordinary `27/100*C24=37,958,760`, qualified `81/250*C24=45,550,512`를 직접 Fraction으로 계산했다. 첫년 base의8% 고정 증가이며 복리가 아니다. 새2025cap이나 FY24첫년25%/30% 금액을 그대로 쓰지 않는다. legal HigherMax는 원II7 법적 조건을 만족할 때만 적용되고 MVP/수상 연도 선택은 없다.

C24는 이미 읽은 NBA 공식 발표의 저장된 관측 pointer로 연결했다. 원기록의 indexedbody 관측과 직접HTTP403 실패를 구분하고 이번에 새HTTP200 raw를 확보했다고 주장하지 않는다. 원법문·캡 전체를 다시 수집하지 않았다.

## 선택 이력과 유효 서비스

2022 wrapper의 selected_policy CX1/E2/LaVine form, 2023 Coby 신규선택 및 LaMelo LM1 선택을 직접 대조했다. 원 내포된 candidate false는 선택 전 생성이력이며 해당 필드를 수정하거나 또 승인요건으로 되돌리지 않는다. 이 문서 자체는 새 가격·계약을 선택하지 않는다.

각 rollover 행의 원FY24 current UPC/service pointer와 원 보호Γ를 연결했다. operative UPC·서비스 가족과 assignment/termination/rights-reset 미선택 조건을 유지하며 actual privatereceipt·실제임상·rendering은 인증하지 않는다. 최소·최대·CBA conformity는 보존하고 fiscal2026June30을 정확service종료일로 치환하지 않는다.

LaVine2026 PO48,967,380은 미래 계약의 참조항목일 뿐 행사되지 않았다. FY25 stated4년차45,999,660을 유지하며 optiontermination protection과 원Ex4 0..15% 가족을 지우지 않는다. Coby12m는3년 신규flat계약의3년차이며 2022 rookie amount/QO로 되돌리지 않는다.

## 등록·원장 경계

기존유효 STD함수5·신규UPC0·STD증분0·TW0이다. 완성15명조합·원장·floor·apron·배당·세금액은 인증하지 않는다. 이5의 새FAhold를 더하지 않지만 다른 선수 FA/QO/RT·unsigned·옵션·원Γ·기타충당 포트는 그대로다. root 후속 명명15 join에서 다른 계약과 함께 소비할 수 있다.

## 현재성·검문

실제 JSON pointer의 선수/연차/가격·원선택 범위, LaMelo Fraction과5 subtotal을 확인했다. 조상 생성기 재실행0·정적 constructor시험0·독립peer pending. 기존후보/중앙/Git 수정0이다.

- `research/CHICAGO_2025_NAMED_ROLLOVER_INPUT_PACKET_2026_10_08.json` — LF `f728fc6b7891422c0ce204bf61aa60a8fa7c21331bd4ade904017b78a057b006`
- `simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json` — LF `e7d0f4b15bc06c7cd16a38d158b38a78871fb7372d412639e33bb20c31d225a7`
- `simulation/CHICAGO_2023_SELECTED_ROUTINE_EXECUTION.json` — LF `9a4f6db21d6ad50e2c6d6897f1c2dedbdf440cee89bae47019f4bd131f341790`
- `simulation/LAMELO_2023_SELECTED_EXTENSION.json` — LF `98f03115f8a71a7f2e0ac3f9376aae5f94647d62c8ce6d942b63881af629483d`
- `research/CHICAGO_2024_25_A10_NAMED_ROLE_WINDOW_COST_FAMILY_2026_10_08.json` — LF `af4f3b340841251a50646fb05aeefcc415e95c4fc07b3c2e02e3f9af8bb14bb1`
- `canon/DELEGATED_LAMELO_2023_EXTENSION_DESIGN_SELECTION_2026_10_08.json` — LF `577cda6c17d836413834a8254364bf13328a521e7b8558a9b70e47c4abcbbc64`
- `canon/DELEGATED_CHI_2023_ROUTINE_CONTRACT_DESIGN_SELECTION_2026_10_08.json` — LF `9847a74948b79bcafa991e4f91884f5dc5f5a83f144a65996f3daa5bae09334c`

원고 CLOSED · 실제 private/wholeFY25 인증0.
