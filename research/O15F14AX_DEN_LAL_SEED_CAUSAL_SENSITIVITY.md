# O-15F14-AX — Denver–Lakers 1라운드 대진의 단일 경기 민감도

- 판정: `F038_L2_BRACKET_REPRODUCED / PRE_PLAYOFF_CAUSAL_STABILITY_HOLD`.
- [재현 JSON](../simulation/CHICAGO_2020_21_K1_L2_SEED_SENSITIVITY.json) · [생성/검문 도구](../tools/build_chicago_2020_21_k1_l2_seed_sensitivity.py) · [원래 대진](../simulation/CHICAGO_2020_21_K1_L2_BRACKET_BRIDGE.md).
- 질문: [2월 Lakers 맞대결 선례](O15F14AW_DEN_LAL_HARTENSTEIN_HEAD_TO_HEAD_PRECEDENT.md)의 **대체 Denver 로스터와 Davis 건강 사건**을 다시 평가할 때, F038의 Denver 3번–Lakers 6번 대진을 얼마나 쉽게 잃는가?

## 사실과 계산 범위

[NBA 2/14 Lakers @ Denver 공식 경기책](https://statsdmz.nba.com/pdfs/20210214/20210214_LALDEN_book.pdf)은 Denver **122–105** 승리와 Davis `14:14`를 기록한다. [NBA 부상 보도](https://www.nba.com/news/anthony-davis-exits-lakers-game-vs-nuggets)는 Davis의 선행 아킬레스건 문제와 경기 중 재악화를 분리해 설명한다. [NBA의 4/22 복귀 보도](https://www.nba.com/news/lakers-anthony-davis-ends-30-game-injury-absence-against-mavs)는 원역사 30경기 결장을 기록한다.

[NBA 4/15 Boston @ Lakers 공식 경기책](https://statsdmz.nba.com/pdfs/20210415/20210415_BOSLAL_book.pdf)은 Boston **121–113** 승리와 Lakers의 Davis(오른쪽 종아리), James(오른쪽 발목), Drummond(오른발 엄지발가락) 부상 미출전을 기록한다. [Boston 구단의 경기 전 기사](https://www.nba.com/celtics/gamepreview/preview-20210415-boslal)도 Davis·James 부재를 동시대에 명시한다. 4/15 PDF SHA-256은 `7c2f4b69830061075fed1a059690f70052f0555c2482dc7d84193850d4990186`이다. 두 날짜는 **원역사 관측**이지 대체 세계 승패나 의료 결과가 아니다.

[F038 조건부 72경기 원장](../simulation/NBA_2020_21_FULL_SEASON.json)의 서부 상위는 Utah 52, Phoenix 51, Denver 47, Clippers 47, Dallas 42, Lakers 42, Portland 41승이다. 기존 F038 동률 순위에서 Denver 3·Clippers 4, Dallas 5·Lakers 6이다. [L2 플레이인](../simulation/CHICAGO_2020_21_EXECUTION_CLOSEOUT.json)을 적용하면 Denver–Lakers **3–6**이 된다. F038의 변경 경기 목록에는 아래 2/14·4/15 원역사 결과가 없다.

## 다른 모든 F038/L2 결과를 고정한 한 경기 반전 시험

| 시험 | 승수 이동 | 서부 시드·Denver 첫 상대 | Denver가 진출할 때 다음 상대의 출처 |
|---|---|---|---|
| F038/L2 기준 | 없음 | Denver 3–Lakers 6 | Phoenix 2–Portland 7 승자 |
| **4/15 BOS–LAL만 반전** | Lakers 43(+1), Boston 35(-1). Denver 47·Dallas 42 유지 | **Denver 3–Dallas 6**; Lakers는 5번으로 Clippers 4번 상대 | Phoenix–Portland 승자. Boston은 동부 7번을 유지해 L2 플레이인 참가 집합은 변하지 않음 |
| **2/14 LAL–DEN만 반전** | Denver 46(-1), Lakers 43(+1) | **Denver 4–Lakers 5**; Clippers 3–Dallas 6 | Utah 1–Memphis 8 승자. 같은 두 팀이 1라운드에 만나도 홈코트와 2라운드 갈래가 달라짐 |

계산은 기존 F038 승수·동률 순서를 시작점으로 사용한다. **변경된 팀이 새 승수 동률에 들어가는 시험은 금지**했으므로 새 NBA 동률 판정은 이 표에 숨어 있지 않다. 두 반전 모두 2021 플레이인 7~10위 참가 집합과 L2 승자를 그대로 둘 수 있는 순위 시험이며, 실제 경기를 다시 시뮬레이션한 결과가 아니다. NBA의 1–8, 2–7, 3–6, 4–5 대진 규칙은 [기존 연결 문서](../simulation/CHICAGO_2020_21_K1_L2_BRACKET_BRIDGE.md)의 공식 출처를 따른다.

**경기 ID 교정:** 저장소의 사건 ID는 `날짜_홈_원정`이다. [원경기 CSV](../simulation/NBA_2020_21_REGULAR_GAME_BASELINE.csv)의 `2021-04-15_LAL_BOS`(113–121), `2021-02-14_DEN_LAL`(122–105)을 생성기가 직접 찾고 원역사 승자에게 `-1`·패자에게 `+1`이 적용됐는지 검사한다. PR #311 첫 JSON의 두 ID는 원정·홈을 뒤집어 표기했으며 승수 계산 자체에는 쓰이지 않았다. 그 잘못된 출처 연결은 이 교정으로 폐기한다.

## A1이 다시 계산해야 할 원역사 건강 창

[NBA Davis 복귀 보도](https://www.nba.com/news/lakers-anthony-davis-ends-30-game-injury-absence-against-mavs)는 2/14 Denver전 뒤 4/22 Dallas전 복귀 전까지 **30경기 결장·Lakers 14승 16패**를 기록한다. [기준 1080경기 CSV](../simulation/NBA_2020_21_REGULAR_GAME_BASELINE.csv)의 2/16 Minnesota전부터 4/19 Utah전까지 Lakers 30경기를 날짜·홈/원정·점수로 다시 집계해 같은 `14–16`을 얻었다. 이 구간의 16개 원역사 패배와 점수차는 [재현 JSON](../simulation/CHICAGO_2020_21_K1_L2_SEED_SENSITIVITY.json)의 `historical_davis_absence_window.original_losses`에 실명 상대와 함께 있다. 그중 원점수차 5점 이내는 2/20 Miami `-2`, 2/22 Washington `-3`, 3/3 Sacramento `-3`, 3/20 Atlanta `-5` 네 경기다. **가까운 점수차는 Davis 복귀 시 승리할 확률이나 가상 점수 보증이 아니다.**

[NBA의 3/20 LeBron 발목 부상 보도](https://www.nba.com/news/lebron-james-leaves-lakers-game-with-right-ankle-injury-will-not-return)는 그날 Atlanta전에서 별도 접촉 후 James가 이탈한 사건을 기록한다. 30경기 창을 이 날짜 기준으로 분리하면 3/20 **이전 13경기 7–6**, 3/20 Atlanta전 **1경기 0–1**, 이후 **16경기 7–9**다. F038의 변경 경기 ID와 이 30경기의 교집합은 **0개**다. 즉 F038의 Lakers 42승·6번 시드는 Davis의 원역사 결장 구간과 그 사이 LeBron 사건의 경기 결과를 그대로 둔 조건부 계산이다. A1에서 Davis 재악화나 결장 길이를 달리 고르면 30경기 중 영향을 받는 날짜·상대와 LeBron의 독립 건강 사건을 구분해 재계산해야 한다. 16패를 모두 승리로 뒤집거나 James 부상까지 자동 삭제하지 않는다.

## 인과 판정과 다음 작업

**추론:** 대체 Denver는 원역사 2월 로스터의 Hampton 분을 가질 수 없으므로 2/14 경기와 Davis 재악화의 동일 재현을 당연시할 수 없다. 한편 선행 아킬레스건 문제, 다른 부상·코치 선택, 상대팀 변화가 있어 **재부상 회피나 Lakers의 추가 승리도 자동 사실이 아니다**. 4/15은 Davis가 원역사에 빠진 실제 패배 중 하나라서 *대진 경계 시험*에 적합하지만, 그날 James·Drummond도 결장했고 Boston이 121점을 냈다. Davis 한 명의 복귀가 8점 차를 뒤집는다는 예측으로 읽지 않는다.

**실행 순서:** A1 후보 달력에서 2/14의 선행 건강과 경기 중 사건, 그 뒤 Davis 결장 구간을 별도로 선택/검문한다. 그 선택과 Denver의 Bey/Hampton 차이가 정규시즌 경기 결과에 미치는 범위를 F038과 다시 연결한 뒤 F5 후보 1라운드 상대·분·5인조·승패를 계산한다. 현재 Denver–Lakers 3–6은 **F038을 고정할 때만** 유효하다. 4/15만 바뀌면 Denver–Dallas 3–6, 2/14만 뒤집히면 Denver–Lakers 4–5라는 시험 결과를 최종 대진으로 승격하지 않는다. 다른 경기/시즌 순위, 상대 건강, 플레이인 및 2라운드 실제 결과는 열린 입력이다.

**분류:** NBA 경기책·부상 보도는 원역사 **사실**, F038/L2 승수와 재현 JSON은 **조건부 계산**, 두 단일 경기 반전은 **후보 민감도**, Davis 건강·승패·시리즈는 **작가 미확정**이다. F5/A1/A3·K_HEALTH/K_METHOD_EVENTS `HOLD`; F `0/5`·A `0/3`·K `0/4`, 7행 1완료·1진행·5대기/미완료 6개. `PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 `CLOSED`, 원고 금지. Codex가 NBA 원문과 F038/L2를 직접 대조했다.

[결과 비공개 Claude 산술 검문](../reviews/R01_O15F14AX_SEED_SENSITIVITY_CLAUDE.md)은 두 대진 반전 계산을 독립 재현했으나, 기존 DEN/LAC 동률의 중요성을 잘못 축소한 설명은 기각했다. 이는 원자료 독립 검증이나 G16 PASS가 아니다. Anti-Gravity·NotebookLM과 전체 source-blind 편집 검수는 이 국소 작업에서 `NOT_RUN`이다.
