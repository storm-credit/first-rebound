# A11 이전 첫 Finals 제외·두 시즌 종료점 결합

- 기준 main `38c09a44a7940760eebcd635629cc947fa5ea2dd`. 신규 root위임 종료점2+기존근거5, 독립 검문 대기.
- 완료범위는 이전7시즌의 **설계상 no-Finals endpoint 결합**이다. F26 Finals 시리즈 실행 완료가 아니다.

## 원 A09를 먼저 대조

[A09 조건부 원문](../design/A09_2023_24_CONDITIONAL_FUNCTIONS.json)은 H2미선택·season_selected=false다. [현재 공동훈련 실행](../design/A09_JOINT_ATTEMPT_SELECTED_EXECUTION_2026_10_08.json)과 [복귀 인계](../design/A06_A08_A09_CURRENT_SEASON_EXIT_JOIN_2026_10_08.json)도 private 협력/복귀/한정 NBA훈련만 선택했다. 2024 NBA seed·시리즈탈락은 선택되지 않았다. [장기 원제안](../design/CHICAGO_MINNESOTA_LONG_CAREER_PACKET.json)의 2라운드탈락은 후보이며 이번승인의 원천으로 소급하지 않는다. 원파일은 그대로 보존했다.

## 비교와 실제 위임 선택

| 2024 대안 | 깊이 | 선택 | 차이 |
|---|---|---|
| **MIL** | 동부 컨퍼런스 준결승 | **root선택** | 기존NPC 세계와 양립; 동일시즌 신규 종료점으로 명명 |
| BOS | 동부 컨퍼런스 준결승 | 미선택 | 새운영입력 필요, first제약상 추가이득없음 |
| CLE | 동부 컨퍼런스 준결승 | 미선택 | 별도명명상대입력 필요, 동일 first지원 |

[선택canon](../canon/DELEGATED_A11_PRIOR_NO_FINALS_ENDPOINTS_2026_10_08.json)은 root가 이번 권고 **2024 MIL R2 탈락 /2025 PHI R1 탈락**을 승인한 지시를 기록한다. Chicago 첫우승·MVP·코어이동·후기재대결·수신자·은퇴 선택이 아니다.

2024년은 CHI/MIL이 같은동부 브래킷의 R2에서 만나는 유효시드·R1진출 관계를 갖는 setting이다. seed·R1상대·날짜·승수·득점·실제박스·2024우승자는 null이다. 원 2023 MIL승리를 2024실행으로 복사하지 않는다.

2025년은 [기존 QUAL1](../simulation/A10_QUAL1_SELECTED_COST_WINDOW.json)의 CHI6/PHI3·R1기간2025-04-19..05-03·G1/G2 비용 관측을 보존하고, 그 관측 뒤 기간내 PHI시리즈승/CHI탈락 종료점만 선택한다. 원JSON winner=null은 이전생성이력이며 새canon은별도다. 시리즈길이·각경기승패/점수·다른팀우승은 미계산이고 선택하지 않았다.

## 이전7시즌 결합

| 시즌 | 근거 | 새 선택 여부 |
|---|---|---|
| 2018–19 | 승인CHI원 로터리 참가+공개nonplayoff규칙 한정추론 | 없음 |
| 2019–20 | 승인CHI원 lottery7+당시규칙, PO7시드 아님 | 없음 |
| 2020–21 | IND play-in 탈락,2021-05-20 | 없음 |
| 2021–22 | PHI R1탈락,2022-04-30 | 없음 |
| 2022–23 | MIL R1탈락,2023-04-21 | 없음 |
| 2023–24 | **MIL 동부준결승 탈락 endpoint** | 이번2중1 |
| 2024–25 | **PHI R1탈락 endpoint** | 이번2중1 |

원5근거와 NBABylaws/2020시점 규칙은 [기존 first입력](../research/A11_CHICAGO_FIRST_FINALS_AND_FY25_SERVICE_INPUT_2026_10_08.json)의 pointer·핀을 그대로 재사용했다. 5새결과로 계수하지 않는다. 이전 first endpoint미선택2→0, 주인공의 2026 첫 Finals 목표와 양립한다. Chicago프랜차이즈 첫 출전이라는 뜻이 아니다. 7시즌 전체82/득점·현실증명이 완료됐다는 뜻도 아니다.

## 2026 동·서 경로 후보 — 미선택

| 안 | CHI 동부 | MIN 서부 | 비교 |
|---|---|---|---|
| **F26_NAMED_ROUTE_A 권고** | CHI2가 MIA7→CLE3→NYK1 상대 | MIN2가 LAL7→DEN3→SAS1 상대 | 2/7→3/6→1/4/5/8 반쪽 관계 |
| F26_NAMED_ROUTE_B | CHI1가 MIA8→CLE4→NYK2 상대 | MIN1가 LAL8→DEN4→SAS2 상대 | 1/8→4/5→2/3/6/7 반쪽 관계 |

Root가 요청한 명명 endpoint는 **CHI over MIA/CLE/NYK**, **MIN over LAL/DEN/SAS**다. 이 패킷은 그 추천과 유효 브래킷을 준비하며, root후속선택 전 nominal시드·각승자·qualification은 미선택이다. A는 두target2번, B는 두target1번 setting을 비교하며 승수/득점·누적시즌계산으로 도출한 값이 아니다.

각conference4팀·4시드 중복0, R1상보합9·R2상대quarter·conferencefinal반대half를 실제대조했다. 미지정나머지4시드는 충돌없는 팀으로 채우는 포트며 whole30팀계약을 새선행조건으로 만들지 않는다. MIA/LAL7·8은 해당연도 적법qualification/play-in 조건을 필요시 충족할 후보이지 이전실제seed복사나 이미실행된자격증명이 아니다.

[F26 root목표](../canon/DELEGATED_A11_F26_FIRST_FINALS_LOSS_SELECTION_2026_10_08.json)는 기존CHI/MIN Finals만 선택했다. 본3파일이 추가conference승자/수상·Finals스코어·개별stint를 선택하지 않는다. NYK 실제Towns roster/2025–26현실이동·원우승을 자동상속하지 않는다. MIN의같은연도명명계약/서비스/6비용과 양팀480분은 후속입력이다.

## 실무 인계와 한계

1. Root가 compatible동·서 route/qualification setting을 선택한다.
2. CHI FY25서비스15와 MINFY25 같은날 적법서비스·가용·6비용/480분을 결합한다. FY26July7 UPC는 June2026에 소급하지 않는다.
3. F26 actualfiction 시리즈패배·주인공판단/도움·동료비용·허용영상전달을 실행·독립검문한다. 옛국소실패를 Finals 플레이로 재명명하지 않는다.

이번 실제검문은 원 first입력 current24핀, A09 선택범위·기존 QUAL1 자격/관측·신규 endpoint2 및 nominal 브래킷2안의 반쪽/진출관계다. 정적파일이므로 constructor변조0·조상테스트반복0. 새독립peer 전이며 actualreceipt/건강/wholecost·wholeA11/G13/G14는false다.

## 진행표

| 번호 | 묶음 | 상태 |
|---:|---|---|
| 1 | 2020 드래프트 연쇄 | 완료 |
| 2 | 2020–21 세계·시즌 | 완료 |
| 3 | 2021–23 계약·선택시즌 | 완료 |
| 4 | 장기 커리어·막 출구 | 진행 |
| 5 | G13 사건·기능·최종배치 | 미완료 |
| 6 | 집필규격·Context Pack | 미완료 |
| 7 | 통합·독립·최종승인 | CLOSED |

미완료큰묶음4 / 6번까지3. v0.30 PARTIAL·CLOSED·Pack0·원고0.
