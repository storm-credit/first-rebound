# O-15G15AC — Plumlee·37순위 원역사 거래와 DB1 권리 충돌

- 시작점: `main` `dfe3dd5`; [G15AB](O15G15AB_DETROIT_JAN23_ORIGINAL_BOX_AND_BRANCH_BOUNDARY.md)의 2022-01-23 Detroit Plumlee 보유 미확정, [G14 10/20 조합](../simulation/CHICAGO_2021_22_PAIRED_REVIEW.md)의 조건부 Plumlee C24.
- 판정: `HISTORICAL_TRADE_NOT_PORTABLE_TO_DB1 / ASSET_AND_JAN23_FRONTCOURT_HOLD`. 기존 DB1의 픽·선수나 2020 정본을 바꾸지 않는다.
- `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, 신규 작가확정 0건, `author_locked=false`, `season_selected=false`, `exact_execution_cleared=false`, `manuscript_allowed=false`.

## 1. 원역사 거래와 DB1은 같은 권리 묶음이 아니다

[Charlotte 2021-08-06 공식 발표](https://www.nba.com/hornets/press-releases/charlotte-hornets-acquire-mason-plumlee-and-draft-rights-jt-thor)에 따르면 원역사 Charlotte는 **Detroit의 Mason Plumlee + JT Thor 지명권**을 받았고 **Balša Koprivica 지명권**을 Detroit에 보냈다. [NBA 2021 실제 드래프트 결과](https://www.nba.com/news/2021-nba-draft-results-picks-1-60)는 Thor를 Detroit가 고른 37번 뒤 Charlotte로, Koprivica를 Charlotte가 고른 57번 뒤 Detroit로 기재한다. 이는 실제 역사에서 맺어진 거래다.

[G7 2021 전체 드래프트 DB1 비교안](../simulation/NBA_2021_FULL_DRAFT_COMPARISON.md)은 `recommended_comparison=DB1`, `selected_scenario=null`, `other_draft_night_trades_executed=false`다. 같은 [JSON](../simulation/NBA_2021_FULL_DRAFT_COMPARISON.json)의 DB1~DB4 네 기본안은 아래 네 순번에서 일치한다.

| 자산·선수 | 원역사 2021 | DB1~DB4 **미선택 비교안** | 그대로 거래를 복사할 때의 충돌 |
|---|---|---|---|
| Mason Plumlee | Detroit → Charlotte | G14는 **Detroit 잔류를 조건부 입력**으로 사용 | 거래를 실행하면 G14의 Detroit C24 수신자가 사라짐. 유지하면 Charlotte의 원역사 센터 수신자가 사라짐 |
| 30순위 JT Thor | 원역사 37순위에서 Charlotte 취득 | **Utah 30순위 제안** | Detroit가 37번 Thor 지명권을 보낼 수 없음 |
| 37순위 | Detroit가 Thor 지명 뒤 Charlotte에 지명권 양도 | **Detroit Santi Aldama 제안** | 거래를 실행하면 Detroit Aldama 지명권·성장/자리와 Charlotte 수신자를 새로 판정해야 함 |
| 57순위 Balša Koprivica | Charlotte 지명 뒤 Detroit에 지명권 양도 | **New York 57순위 제안** | Charlotte가 DB1의 New York 보유 권리를 Detroit에 보낼 수 없음 |
| 58순위 | 원역사 New York Jericho Sims | **Charlotte Jay Huff 제안** | DB1의 Charlotte 자체 후보도 원역사 57번 보상과 다른 자산 |

DB1의 Utah30 Thor·Detroit37 Aldama·New York57 Koprivica·Charlotte58 Huff는 **제안된 드래프트 보드**다. 최종 선수 지명·계약·거래가 아니다. 원역사 거래를 DB1에 한 줄로 붙이면 **동일 선수 Thor의 선행 지명, Charlotte에 없는 Koprivica 권리, Detroit 37번 소유·선수 변경**을 한꺼번에 무시한다. 따라서 G14의 미실행 거래 `HOLD`는 단순히 “Plumlee를 Detroit에 둘지”의 문제가 아니다.

## 2. 두 비교 분기의 비용

| 조건부 분기 | 명시할 사건 | 2022-01-23 비용 |
|---|---|---|
| P0 — 원역사 Plumlee 거래 미실행 | Detroit가 기존 Plumlee 계약을 유지하는 경우 DB1의 Detroit 37번 권리와 Charlotte 58번 후보를 **별도** 보존. New York 57번은 Detroit 거래 보상이 아님 | Plumlee의 당일 Detroit 계약·등록·건강 및 출전, Stewart·Lyles의 앞코트 분 경쟁. Charlotte가 원역사에서 받았던 Plumlee/Thor의 대체 센터·포워드 경로 |
| P1 — 대체 Detroit–Charlotte 거래 신규 설계 | 원역사 보상 문구를 복사하지 말고 **현재 보유권·선수·급여·픽**으로 새 제안과 수락 이유를 제시. New York의 Koprivica 권리를 원하면 별도 NYK 거래가 필요 | Detroit의 C/PF 수신자와 37번 제안 재판정, Charlotte의 픽/급여 비용, 1/23 양 팀 명단·분·상대 경기 연쇄 |

P0/P1은 **비교를 위한 조건 이름**이며 어느 쪽도 추천·작가확정이 아니다. 원역사 거래가 미실행이면 Plumlee가 2022-01-23까지 반드시 Detroit에 남는다는 보장도 없다. 원역사 [Detroit 1/23 박스](https://www.nba.com/game/det-vs-den-0022100707/box-score)의 Stewart `26:42`와 Lyles `21:18`은 합이 우연히 `48:00`이지만 포지션별 독점 사용이나 대체 Plumlee의 무료 24분을 증명하지 않는다. G14의 10/20 Stewart24+Plumlee24를 1/23에 더하려면 기존 선수의 분·공격기회와 당일 상대 Denver의 변화까지 새로 계산해야 한다.

## 3. 근거 지위와 다음 게이트

| 구분 | 이번 결론 |
|---|---|
| 사실 | 원역사 Charlotte 공식 거래 발표와 NBA 실제 37/57 지명·양도 결과; 저장소 DB1~DB4의 30/37/57/58 제안 소유·선수 |
| 추론 | 같은 DB1 보드를 유지하면서 원역사 Plumlee+Thor↔Koprivica 거래를 그대로 실행할 수 없다 |
| 후보 | 거래 미실행 P0, 새 조건을 명시한 거래 P1 |
| 작가확정 | 이번 0건. 2021 실제 대체 거래·픽 37/57/58 최종 채택, Plumlee 2022-01-23 소유/건강/분, Charlotte 비용 모두 `HOLD` |

다음은 P0에서 **Plumlee 2020 계약 → 2021 거래 미실행 → 2022-01-23 보유**의 날짜별 조건과 Detroit·Charlotte 표준 자리/급여를 검산하는 것이다. P1은 자산·상대 수락 이유가 나온 뒤만 실행한다. Chicago 2020–21 정확 시즌, G14 Detroit `PRIOR_HOLD`·Orlando `ROLE_HOLD`, G16/G17은 유지한다. 7개 매크로 게이트는 1완료·1진행·5대기, 진행 중 포함 6개가 남는다.

[이번 CLI·제한 source-blind 검토](../reviews/R01_O15G15AC_TRADE_CLI_AND_SOURCE_BLIND.md)는 NotebookLM의 기존 NBA 드래프트 결과 한정 성공, 구단 발표 추가 실패, Antigravity 시간 초과, Claude의 Plumlee 이동 방향·DB1 37번 소유 혼동을 분리한다. 같은 원문을 읽거나 모델이 동의했다는 이유로 독립 출처·G16 PASS를 늘리지 않는다.
