# O-15G15D — Orlando 2022-01-23 투웨이 자리와 세 번째 가드 경로

- 기준 `main` `1605e6b` (PR #186). [G15B의 두 조건부 240분 증명](../simulation/CHICAGO_2021_22_G15B_REVIEW.md)과 [G15C 계약 연표](O15G15C_ORLANDO_CONTRACT_CHRONOLOGY.md)를 잇는 **자리 분류 감사**다. 어느 계약·출전·승패도 새로 채택하지 않는다.
- 1차 규칙: [NBA Communications 2021-07-27 공식 발표, Roster-Related Rules](https://pr.nba.com/nba-board-of-governors-play-in-roster-rules-2021-22-season/). 2021–22 기본 동시 계약 한도는 표준 NBA 계약 **15명 + 투웨이 2명**, 한 경기 활동 명단은 최대 **15명**, 각 투웨이 선수의 정규시즌 활동 명단은 최대 **50경기**다. 같은 시즌 투웨이 계약의 1월 15일 서명 마감은 적용하지 않는다. 하드십 추가 자리의 별도 허가 여부는 이 발표만으로 판정하지 않는다.
- 원역사 날짜: [Orlando 2022–23 공식 미디어 가이드](https://cdn.nba.com/teams/uploads/sites/1610612753/2022/11/orlando-magic-media-guide-2022-23.pdf) 인쇄 230–231쪽(파일 117쪽). 이는 **사후 거래 연표**이며 대체세계의 실제 계약서가 아니다.

| 거래 후 시점 | 원역사 투웨이 1 | 원역사 투웨이 2 | 기록이 허용하는 말 |
|---|---|---|---|
| 2021-08-11 | Ignas Brazdeikis 재계약 | 두 번째 자리 이 표만으로 미확인 | 당일 전체 명단 완성 주장이 아님 |
| 2021-10-26 | Brazdeikis | Mychal Mulder 영입 | 두 투웨이 계약을 동시에 보유하는 원역사 경로 |
| 2022-01-06 | Brazdeikis | Mulder 방출 후 Admiral Schofield 영입 | 1/23에 두 계약을 **가상 세계에서도 유지한다면** 투웨이 2/2 |

G15B의 **O15A Herbert PG12**와 **O15C Gravett PG12** 두 240분 증명은 모두 Brazdeikis·Schofield에게 양수 분을 준다. 두 선수의 위 투웨이 연쇄를 대체세계에서도 채택하고 계약 유형을 유지하는 분기에서는 1/23 투웨이 자리가 **2/2**다. 따라서 O15C에 Gravett를 **세 번째 투웨이 계약자로 덧붙이는 방법은 불가능**하다. 2021–22의 투웨이 1월 15일 마감 면제는 슬롯을 셋으로 늘리지 않는다. 기존 둘 중 하나의 방출·표준계약 전환은 가능성만 있는 **새 사건**이며 G15B의 동시 출전 증명을 그대로 재사용할 수 없다.

| 조건부 경로 | 현재 증명의 변화 비용 | 확인 전 상태 |
|---|---|---|
| O15A: Herbert 내부 PG12 | 새 가드 계약은 없지만 **ORL33 지명 제안 ≠ 계약·등록**. Herbert의 계약 형식, 당일 활동, PG 수행, 36분의 수비/공간 비용이 필요 | `ROLE_AND_REGISTRATION_HOLD` |
| O15C-표준: Gravett 별도 표준 NBA 계약 | Brazdeikis·Schofield 동시 출전은 유지할 수 있지만, 대체 ORL의 그날 **표준계약 점유 0~15**를 전원·계약일·방출일로 산출해야 한다. 빈자리가 없으면 누군가의 실제 분·계약을 잃는다 | `STANDARD_SLOT_AND_COST_HOLD` |
| O15C-하드십: Gravett 새 10일/단기 계약 | [당시 NBA의 하드십 추가 자리 사례](https://www.nba.com/news/los-angeles-lakers-isaiah-thomas-10-day-contract)는 일반 15명 한도를 넘는 경로가 있었음을 보인다. **가상 ORL의 1/23 특정 결장·적용 규정·리그 허가**는 별도다. 12/17·12/27 두 계약을 1/23까지 연장하지 않는다 | `HARDSHIP_ELIGIBILITY_AND_APPROVAL_HOLD` |
| O15C-투웨이 교체 | 하나를 비우거나 표준으로 전환해야 하므로 G15B의 Brazdeikis·Schofield 동시 분 배정을 폐기·재증명한다. 이 시즌의 서명일 규칙은 장애가 아니어도 50활동경기·자리·급여는 감사 대상 | `NEW_MINUTE_WITNESS_REQUIRED` |

**공통 미확정값:** 2021 여름~2022-01-23 대체 ORL의 15명 표준계약 전원, Herbert 33번 실제 계약, Mobley3/Nnaji의 계약·등록, Brazdeikis·Schofield 연쇄의 대체세계 채택, 당일 15명 활동·의료, 각 투웨이의 활동경기 사용량, 하드십 허가. [원역사 부상 보고서](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2022-01-23_05PM.pdf)에 이름이 없다는 사실은 이 값을 채우지 않는다. 원역사 1/23 출전선수를 가상 ORL로 복원하지 않는다.

NotebookLM CLI는 공식 규칙과 미디어 가이드 **두 출처**로 2/2 슬롯 산술을 재확인했다. 이는 공유된 원문에 대한 **연결 분석**이지 독립 검수 횟수가 아니다. Anti-Gravity CLI는 로그인된 상태로 같은 규칙 URL을 요청했지만 headless `RunCommand` 권한 요구가 자동 거부되어 이번에도 검증된 자료가 없다. 도구 실패를 규칙 부재나 가상 계약 허가로 해석하지 않는다.

다음 종료 조건은 대체 ORL의 2021 여름~1/23 **날짜별 표준계약 점유표**와 G15B 양수 분 선수 각각의 계약/활동 증거를 만드는 것이다. 그 뒤 O15A 역할 비용 또는 O15C 계약 경로 하나를 선택 후보로 비교한다. G14 ORL4 `ROLE_HOLD`·DET4 `PRIOR_HOLD`, 시즌/정확 실행 미선택, `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`를 유지한다.
