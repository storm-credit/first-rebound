# O-15G15BQ — Drummond·Ariza→Wright→Joseph·픽의 선행 검문

- 기준: `main` `19c8a1f`, [G15BP 픽 계보](O15G15BP_DETROIT_BAGLEY_PICK_ORIGIN_AND_ROUTING.md), [2020 Detroit 지명 정본](../canon/PROJECT_FREEZE.md), [G14 조건부 Detroit 분](../simulation/CHICAGO_2021_22_PAIRED_REVIEW.md).
- 판정: `HISTORICAL_UPSTREAM_CHAIN_VERIFIED / ALTERNATE_WRIGHT_JOSEPH_AND_PICK_ROUTE_HOLD`. 새 거래·픽·출전·시즌·작가확정 0건. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`.

## 날짜별 원역사와 대체세계 검문

| 날짜·사건 | 원역사 근거 | 대체세계에서 확인할 조건 |
|---|---|---|
| 2020-02-06 Drummond → Cleveland | [Cleveland 구단 발표](https://api-hub-dev.nba.com/news/cavaliers-acquire-drummond-official-release)는 Detroit가 Knight·Henson과 CLE/GSW **2023년 2R 중 더 불리한 한 장**을 받은 거래를 명시한다. | 2020년 Patrick7·Kira16·Stewart19 지명 **이전** 사건이다. 기존 Chicago 2019–20 접촉이 Detroit/Cleveland의 당시 성적·거래 동기를 바꿨는지 별도 대조한다. 후행 지명 변경만으로 이 선행 픽 취득을 소급 취소하지 않지만, 대체세계 동일 거래 실행도 자동 확정하지 않는다. |
| 2020-11-24 Houston → Detroit | [Detroit의 Wright 거래 발표](https://www.nba.com/pistons/news/detroit-pistons-acquire-delon-wright-dallas-three-team-trade)는 Detroit가 앞서 Christian Wood 거래에서 **Ariza와 16번 Stewart 지명권** 등을 얻었다고 설명한다. [Kira 지명 검토](../simulation/2020_DRAFT_KIRA_LEWIS_RELANDING_BOARD.md)는 이 16번을 Kira로 바꾸되 Wood·Ariza 거래 경제를 자동 보존하지 않는다. | 정본은 **Detroit Kira16·Stewart19**다. 같은 16번 권리 취득 거래가 Kira 지명 아래에도 상대 동의·보호 1R/2R·급여 조건을 통과하는지 확인한다. Ariza 보유를 검증하지 않고 다음 Wright 취득으로 뛰지 않는다. |
| 2020-11-27 Ariza → Oklahoma City, Wright → Detroit | [Detroit 공식 발표](https://www.nba.com/pistons/news/detroit-pistons-acquire-delon-wright-dallas-three-team-trade)와 [Oklahoma City 공식 발표](https://www.nba.com/thunder/news/acquisitions-201127)는 Detroit가 Ariza를 보내 Wright를 받는 3팀 거래를 기록한다. OKC는 Ariza·Justin Jackson·Dallas 경유 2023/2026 2R을 받았다. | Ariza가 위 Wood 거래에서 실제로 Detroit에 와 있어야 하며 Dallas·OKC의 같은 거래 수락과 급여/픽 조건도 필요하다. [F12 조건부 Chicago–Detroit 분](../simulation/CHICAGO_2020_21_INTEGRATED_PATHS.md)은 Wright의 분을 조정했지만, **Wright 보유를 증명한 독립 증거는 아니다**. 취득 실패 시 그 두 Detroit 경기의 Wright 분부터 다시 배분한다. |
| 2021-03-25 Wright → Sacramento | [Sacramento 공식 발표](https://www.nba.com/kings/news/kings-acquire-delon-wright)는 Detroit가 Joseph와 2021·2024 2R을 받았다고 적는다. [Detroit 구단의 FA 설명](https://www.nba.com/pistons/features/pistons-free-agency-primer-and-what-it-might-say-about-role-they-see-cade-cunningham-rookie)은 Joseph의 2021–22 `$12.6m` 중 `$2.4m` 보장 구조가 당시 Detroit의 캡룸 동기였음을 설명한다. | Wright가 실제로 Detroit에 남아 있고, Kira·Patrick 중심 대체 명단에서도 Detroit/Sacramento가 같은 선수·픽·보장계약 교환에 동의해야 한다. 2024 픽과 Joseph 최초 유입은 함께 움직인다. 어느 한쪽만 떼어 G14 10/20 Joseph 24분이나 Bagley 대가에 복사할 수 없다. |
| 2021-07-31~08-10 Joseph 방출·재서명 | [G15AI 계약 날짜 장부](O15G15AI_JOSEPH_ROOM_EXCEPTION_SEQUENCE_GATE.md)는 두 계약과 보장액·room MLE를 분리했다. | Wright 거래가 유지돼도 방출/재서명·예외 자격·대체 급여·10/20 활동은 **추가** 조건이다. Wright 거래 하나로 G14 Joseph 분을 PASS 처리하지 않는다. |
| 2021-08-06 / 2022-02-10 자산 사용 | [G15AU](O15G15AU_DETROIT_AUG6_CONSIDERATION_LEDGER.md)는 8월 Houston 가상 대가를, [G15BP](O15G15BP_DETROIT_BAGLEY_PICK_ORIGIN_AND_ROUTING.md)는 2월 Bagley 원형 대가를 비교한다. | Drummond 2023 및 Wright 2024 권리가 대체세계에서 실제 취득·보유되더라도 **8월에 송출한 픽은 2월에 재사용할 수 없다**. 두 시점 중 거래 실행은 모두 HOLD다. |

### 2020-02-06 이전 Chicago 직접 접촉 범위

[2019–20 Chicago 경기 기준선](../simulation/CHICAGO_2019_20_GAME_MARGIN_BASELINE.csv)과 [기존 조건부 결과 원장](../simulation/CHICAGO_2019_20_OUTCOME_LEDGER.csv)을 날짜로 결합하면, Drummond 거래 전 Chicago–Detroit **4경기**, Chicago–Cleveland **3경기**다. 저장된 각 경기의 BPM/NET_EB × LOW/BASE/HIGH **6개 조건**에서 `base_flip`, `fatigue_05_flip`, `fatigue_10_flip`은 모두 `0`이었다(7경기×6행). 즉 **이 원장의 직접 맞대결 승패는 그대로**였으며, 양 구단의 Drummond 거래 전 승수 변화를 Chicago와의 직접 경기 결과에서 찾지는 못했다. 이 42행은 타 구단과의 연쇄 경기·프런트의 판단·선수 가치·의료/급여를 검증하지 않으므로 **대체 Drummond 거래 실행 PASS는 아니다**.

## 2022-02-10 픽의 출처 표현 차이

[NBA 공식 거래표](https://www.nba.com/news/2021-22-nba-trade-tracker)는 Milwaukee가 Sacramento 경유 픽과 Detroit 경유 픽을 하나씩 받고 Sacramento도 Detroit 경유 픽 하나를 받았다고 적는다. 반면 [Golden State의 2022–23 DiVincenzo 미디어 가이드](https://cdn.nba.com/teams/uploads/sites/1610612744/2022/10/Golden_State_Warriors_2022_23_Media_Guide.pdf)는 Detroit의 2023·2024 픽 **두 장이 Milwaukee로 갔다**고 요약한다. 두 문서는 **최종 수취와 중간 경유 또는 서로 다른 법적 픽**을 구별하지 않는다. 같은 2024 자산인지, Sacramento가 별도 픽을 Milwaukee로 보냈는지 원계약/공식 자산 ID 없이는 확정하지 않는다. 미디어 가이드의 요약으로 NBA 표의 Sacramento 수취 행을 지우거나 세 장의 Detroit 픽을 만들지 않는다.

## 판정과 다음 확인

| 구분 | 결과 |
|---|---|
| 사실 | 위 원역사 날짜·선수·픽 거래, 정본 Kira16·Stewart19, F12/G14의 저장된 조건부 분. |
| 추론 | 대체 Wood/Ariza 거래가 실패하면 원형 Wright 취득 경로도 실패하고, 그 경우 원형 Wright→Joseph·2024 픽 취득과 F12/G14 분을 순차 재검산해야 한다. 2020년 Drummond 거래는 2020 드래프트 변화보다 앞선다. |
| 후보 | Wood/Ariza→Wright→Joseph 원형 유지, 또는 실패한 첫 고리부터 새 합의·등록·분·픽 경로를 만드는 비교안. 어느 것도 실행 승인/정본이 아니다. |
| 작가확정 | 이번 0건. Detroit 2020/2021 대체 거래, Joseph 활동, 2023/2024 픽 사용, Bagley 4팀 합의는 `HOLD`. |

## 검증 레이어 실행 범위

- **Anti-Gravity CLI 1.2.12:** Detroit·Oklahoma City 공식 URL 두 개의 직접 판독을 45초 제한으로 요청했다. 대화 `c672e34b-9473-4b7f-8fd9-d4c07df2c178`은 제한 시점에 `status=SUCCESS`이나 `response=""`였고 CLI가 부분 출력이라고 표시했다. **본문/독립 Evidence Pack 0건**이다.
- **NotebookLM CLI:** 기존 비정본 작업실에 Oklahoma City 공식 URL 추가는 실패했다. 대신 위 날짜 고리의 **Codex 작성 비정본 요약**을 텍스트 소스 `99d3a8d4-459c-41c7-91b9-09ebf724d1c2`로 넣어 그 소스 하나만 질의했다(대화 `37a4e8ef-bc8c-470b-b0a4-14ab5a02d531`). 원형 거래의 선행 조건과 조건부 분으로 거래를 증명하는 **순환 논증 위험**을 되짚었으나, 입력을 되풀이한 **공유 자료 분석**이며 새 공식 근거나 독립 검증은 0건이다.
- **Codex:** 공식 발표 원문·정본·저장된 경기 원장을 대조했다. **Claude 독립 반증 및 별도 source-blind 검수는 이번 변경에서 `NOT_RUN`**이다. G16 전체 독립 검수나 G17 승인이 아니다.

다음은 **Kira16 권리 취득의 11/24 Wood·Ariza 거래 조건**을 대체 Detroit 자산과 대조한 뒤 11/27 Wright 3팀 수락·급여, 3/25 Joseph 보장계약 동기, 8/6/2/10 픽 보유를 같은 시간선으로 잇는 것이다. 공식 거래 원계약/자산 ID가 나오기 전 2024 픽의 Milwaukee 최종 도착을 확정하지 않는다. Chicago D1 F1–F5 `0/5`, A1–A3 `0/3`, K 네 묶음 `0/4`; 전체 7묶음 1완료·1진행·5대기, 진행 중 포함 남은 6묶음.
