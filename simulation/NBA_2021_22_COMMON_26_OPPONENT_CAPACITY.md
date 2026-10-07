# 2021–22 Chicago 상대 26팀 공통 조건부 역할 함수

SOURCE_BOUND_CONDITIONAL_ROLE_FUNCTIONS_26_NOT_DATED_LEGAL_EXECUTION

기존 DET/NOP와 TOR을 제외한 **26팀·72날짜**에 한 생성기를 적용했다. 각 팀은 2020–21 S2 May16 명명 seed를 **가상으로 유지하거나 합법 갱신한다는 조건**에서 9–10명 양수, 12명 작업 active, 12×240초 블록, 팀 14,400선수초를 구성한다. HOU 원17STD에는 당시 hardship2가 포함돼 해당2를 이월하지 않고15명만 사용한다. MIN14STD/1TW, PHX15STD/1TW의 빈 슬롯은 임의 선수로 채우지 않았다. 2021–22 실제 등록·건강·승패를 선택한 것이 아니다.

## 소스와 경계

- `design/CHICAGO_2021_22_OPPONENT_FINITE_DISPATCH_SCOPE_2026_10_07.json#/teams/{TEAM}`의 May16 S2 roster state/DB1 권리/전체1034개 raw 보고행 중 해당26팀916개/원인 충돌을 한 번에 소비한다. `NBA_Player_Movement` raw SHA와 소비행916개의 actor·일자·유형·GroupSort를 직접 대조했다.
- `simulation/NBA_2020_21_REGULAR_CLOCK_COMPLETION.json`의 May16 선수분은 가상 역할 후보 우선순위에만 쓴다. `simulation/NBA_2020_21_FINAL859_OBSERVATIONS.csv`의 G/F/C 선발 분류는 가능한 가상 포지션 입력이며 2021–22 출전분이나 의료 근거가 아니다. PG 창조자는 해당 G 선수에게 부여한 가상 코칭 과제다.
- 원역사 Signing/Waive/Trade/Conversion/Claim을 자동 실행하지 않는다. 같은 GroupSort 거래는 상대 팀/선수·권리·보호급여를 원자로 대조해야 한다. DB1 미선택 권리는 NBA UPC나 명단 선수가 아니다. DET A/B와 TOR T1을 함께 보면 Kelly Olynyk(HOU↔DET), Trey Lyles(SAS↔DET), Dragic·Achiuwa(MIA↔TOR), Mykhailiuk(OKC↔TOR)의 조건부 중복이 생긴다. 원자 이동 없이 동시 명단으로 승격하지 않는다.
- Chicago 상태는 채택된 58 NORMAL/24 COBY_OUT 원장의 정확 game_id/date/home/away를 조인했다. 상대 명단·건강·경제·승패/OT는 모두 날짜별 typed HOLD이고 원 May16 이벤트 ID를 요청된 2021–22 게임 ID로 바꿔 쓰지 않는다.

## 완료와 실제 남은 입력

조건부 **역할 함수 26/26**, 요청 날짜 **72/72**를 원천 연결했다. 역할 fixture 누락팀 0개. 그러나 합법 계약/선수이동 interval 미실행 **26팀·72날짜**, 실제 실행 가능한 상대 날짜 0개다. 이 gap은 각 팀별 새 조사 프로젝트가 아니라 명명된 계약갱신과 원자 거래의 공통 compiler 입력이다.

BOS의 AP1, OKC의 AP1/SG16, HOU의 SG16, SAC의 S14A–D는 실제 중요한 미선택 분기다. 다른 팀의 `known_causal_conflict_inputs`도 역사 거래 자동복사 전에 확인한다. 한 팀의 미선택을 26팀 전체 정지 사유로 삼지 않는다.

## 팀별 역할 요약

| 팀 | 양수 | G/F/C 원형 출처 | 경기키 | 별도 중요 분기 |
|---|---:|---|---:|---|
| ATL | 10 | 4/5/1 | 4 | 없음 |
| BKN | 10 | 4/5/1 | 3 | 없음 |
| BOS | 10 | 6/3/1 | 3 | AP1_KEMBA_HORFORD_BROWN_16_UNSELECTED |
| CHA | 10 | 4/3/3 | 3 | 없음 |
| CLE | 10 | 3/5/2 | 4 | 없음 |
| DAL | 10 | 4/4/2 | 2 | 없음 |
| DEN | 10 | 3/5/2 | 2 | 없음 |
| GSW | 10 | 5/3/2 | 2 | 없음 |
| HOU | 10 | 3/6/1 | 2 | SG16_PICK16_SENGUN_ASSIGNMENT_UNSELECTED |
| IND | 10 | 3/5/2 | 4 | 없음 |
| LAC | 10 | 3/4/3 | 2 | 없음 |
| LAL | 10 | 3/5/2 | 2 | 없음 |
| MEM | 10 | 5/4/1 | 2 | 없음 |
| MIA | 10 | 4/4/2 | 4 | 없음 |
| MIL | 10 | 4/5/1 | 4 | 없음 |
| MIN | 10 | 2/5/3 | 2 | 없음 |
| NYK | 10 | 5/3/2 | 4 | 없음 |
| OKC | 10 | 2/5/3 | 2 | AP1_SG16_ACTORS_ASSETS_UNSELECTED |
| ORL | 10 | 2/6/2 | 4 | 없음 |
| PHI | 10 | 5/2/3 | 4 | 없음 |
| PHX | 10 | 3/5/2 | 2 | 없음 |
| POR | 9 | 3/5/1 | 2 | 없음 |
| SAC | 10 | 4/4/2 | 2 | S14A_D_SABONIS_FOUR_TEAM_DIRECTION_UNSELECTED |
| SAS | 10 | 4/4/2 | 2 | 없음 |
| UTA | 9 | 4/3/2 | 2 | 없음 |
| WAS | 10 | 4/4/2 | 3 | 없음 |

원고 0. PROJECT_FREEZE v0.30 PARTIAL, 설계·원고 CLOSED. 새 정본/REGISTER/중앙 dispatcher 변경 없음.
