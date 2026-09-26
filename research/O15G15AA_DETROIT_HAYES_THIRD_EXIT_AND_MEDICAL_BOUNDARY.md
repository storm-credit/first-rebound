# O-15G15AA — Detroit 1/23 Hayes 세 번째 이탈과 의료 경계

- 시작점: `main` `9092b8d`의 [G15Y 세 경기 원장](O15G15Y_2022_01_23_THREE_GAME_PLAYER_FLOW.md). 그 문서는 원역사 Detroit에서 Bey·Cade 두 행을 우선 계산했으나, **원역사 Killian Hayes의 양수 출전 행을 누락**했다.
- 판정: `THIRD_ORIGINAL_ROW_FOUND / REPLACEMENT_ROLE_AND_MEDICAL_HOLD`. 정본을 재선택하지 않고 이탈 집합과 조건부 비용만 교정한다.
- `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`; 신규 작가확정 0건, `author_locked=false`, `season_selected=false`, `exact_execution_cleared=false`, `manuscript_allowed=false`.

## 1. 서로 다른 확정 수준의 세 이탈 행

[NBA 2022-01-23 DET@DEN 최종 박스](https://www.nba.com/game/det-vs-den-0022100707/box-score)에서 원역사 Detroit Hayes는 `24:42`, `5 FGA`, `8점`, `3 TOV`를 기록했다. [NBA 19:30 ET 부상 보고 4쪽](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2022-01-23_07PM.pdf)은 그를 **Available / 오른쪽 엉덩이 타박상**으로 적는다. `Available`과 실제 `24:42`는 각각 사전 상태와 사후 관측이다.

| 원역사 Detroit 선수 | 원역사 1/23 박스 | 대체 역사 팀 경로 | 강도 |
|---|---:|---|---|
| Saddiq Bey | `30:42`, 11 FGA, 11점 | [2020 정본](../canon/PROJECT_FREEZE.md) Denver 22순위 | **지명 팀 작가확정**, 2022 Denver 계약·출전 `HOLD` |
| Killian Hayes | `24:42`, 5 FGA, 8점 | [2020 정본](../canon/PROJECT_FREEZE.md) New Orleans 13순위 | **지명 팀 작가확정**, 2022 New Orleans 계약·출전 `HOLD` |
| Cade Cunningham | `36:14`, 15 FGA, 18점 | [2021 DB1](../simulation/NBA_2021_FULL_DRAFT_COMPARISON.json) Charlotte 1순위 | **비교안 후보**, 지명·2022 팀 `HOLD` |

따라서 **2020 작가확정만 적용해도** 원역사 Detroit의 Bey+Hayes `55:24`, 16 FGA, 19점은 대체 Detroit의 원역사 관측 행으로 남을 수 없다. **2021 DB1까지 조건부 적용하면** 세 행은 `91:38`, 31 FGA, 37점이다. 이 합은 세 선수가 원역사에서 차지한 *선수별 출전 행의 크기*이지 대체 Detroit의 비어 있는 경기 시계 91:38이나 재배분해야 할 31 FGA·37점의 정답이 아니다. 세 선수는 다른 선수와 동시 출전했으며, 상대 Denver 자체도 Bey/Nnaji 이동 조건에서 바뀐다. 기존 G15Y의 Bey+Cade `66:56`은 계산 오류가 아니라 **Hayes를 포함하지 않은 불완전한 부분집합**이었다.

## 2. 의료·가드 자리에서 다른 팀 기록을 복사하지 않는다

같은 공식 부상 보고는 원역사 Chicago의 Patrick Williams를 **Out / 왼쪽 손목 인대 파열**, 원역사 New Orleans의 Kira Lewis Jr.를 1/24 경기 기준 **Out / 오른쪽 ACL/MCL**, 원역사 Detroit의 Hayes를 **Available / 오른쪽 엉덩이 타박상**으로 적는다. 프로젝트 정본의 팀은 각각 **Detroit Patrick 7·Detroit Kira 16·New Orleans Hayes 13**이다. 다른 팀에서 겪은 일정·출전·재활의 누적을 대체 팀에 자동 이식하지 않는다. 이 보고에서 대체 Detroit Patrick/Kira의 1/23 건강을 직접 읽을 수 없고, DB1 Suggs5도 원역사 Orlando의 당일 건강으로 Detroit 활동을 확정할 수 없다.

원역사 Detroit의 가드 Hayes `24:42`와 조건부 이탈 Cade `36:14`를 뺀 뒤, 대체 Kira·Suggs에게 각각 그 분을 그대로 주면 단순 치환이 된다. 먼저 두 선수의 **2020·2021 서명, 1/23 보유·활동, 팀 의료 경로**, 그리고 기존 Cory Joseph·Rodney McGruder·Saben Lee 등과의 볼 권한을 날짜별로 대조해야 한다. Patrick과 기존 Isaiah Stewart의 앞코트/윙 시간도 같은 240분 안에서 함께 검산한다. 원역사 Stewart `26:42`를 자동 보존하지 않는다.

## 3. 구분과 다음 검증

| 분류 | 이번 판정 |
|---|---|
| 사실 | NBA 원역사 Hayes 박스와 시간 명시 부상 보고; 정본의 2020 Hayes NOP13·Bey DEN22 |
| 추론 | 두 2020 지명 결과만으로도 원역사 Detroit Hayes+Bey 행을 현 팀 성적으로 복사할 수 없다 |
| 후보 | DB1 Cade CHA1·Suggs DET5가 성립하면 Detroit 가드 역할과 Denver 상대의 새 분/공격 예산 필요 |
| 작가확정 | 이번 0건. 1/23 대체 Detroit 명단·의료·가드 96분·FGA/득점·승패 모두 `HOLD` |

다음 단계는 원역사 Detroit 나머지 양수 분을 이름별로 확인하고, **2020 확정 집합만 적용한 분기**와 **DB1 추가 분기**를 따로 계산하는 것이다. 2020–21 Chicago 정확 시즌, G14 Detroit `PRIOR_HOLD`, Orlando `ROLE_HOLD`, G16/G17은 그대로다. 7개 매크로 게이트는 1완료·1진행·5대기, 진행 중 포함 6개가 남는다.

[이번 CLI·제한 source-blind 검토](../reviews/R01_O15G15AA_THIRD_EXIT_CLI_AND_SOURCE_BLIND.md)는 NotebookLM의 공식 PDF 한정 성공, Antigravity의 headless 권한 거부, Claude의 원역사 팀 혼동을 각각 기록한다. 검토 횟수를 독립 출처나 G16 통과 횟수로 세지 않는다.

### 후속 — G15AB 원역사 전체 박스 대조

[G15AB](O15G15AB_DETROIT_JAN23_ORIGINAL_BOX_AND_BRANCH_BOUNDARY.md)는 NBA 페이지 내장 박스의 **양수 분 10명·DNP 3명**을 직접 추출해 팀 `240:00 / 75 FGA / 19 FTA / 111점 / 22 TOV`와 대조했다. Hayes 발견은 유지하되, 원역사에서 이탈하지 않은 나머지 7명의 대체세계 계약·등록·분도 자동 보존하지 않는다. 2020 확정만의 제거 집합과 DB1을 더한 집합을 분리한다.
