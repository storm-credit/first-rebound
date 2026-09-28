# Chicago 2020–21 A1 — Lakers 두 접촉 사건의 건강 경로 선택 준비

- 상태: `AUTHOR_CHOICE_PREPARED / NO_HEALTH_BRANCH_SELECTED / NO_GATE_CHANGE`.
- 범위: 대체 세계의 **Lakers Davis·LeBron 건강 하위 달력**. A1은 전체 리그의 선수 가용성도 포함하므로 아래 선택 하나가 A1 전체 PASS가 아니다.
- 선행 권위: [AY 2/14 접촉 선수](../research/O15F14AY_DAVIS_INJURY_POSSESSION_LINEUP.md), [AZ Davis 결장 30경기](../research/O15F14AZ_DAVIS_WINDOW_CONTACT_AUDIT.md), [BA 3/20 Hill 접촉](../research/O15F14BA_LEBRON_HILL_CONTACT_CAUSAL_GATE.md), [BB LeBron 20+6 달력](../research/O15F14BB_LEBRON_20_PLUS_6_GAME_CONTACT_AUDIT.md), [재현 45경기 집합](../simulation/CHICAGO_2020_21_DUAL_HEALTH_EXPOSURE.json).
- 기존 작가 확정: Chicago 원클럽·2020 Draft·T1~T4/R1·Hall 5/9 재계약 생략·McGee 거래 생략. **Lakers 건강 경로는 작가 미확정.**

## 왜 작가 선택인가

[NBA 2/14 Davis 부상 보도](https://www.nba.com/news/anthony-davis-exits-lakers-game-vs-nuggets)와 [공식 Denver 경기책](https://statsdmz.nba.com/pdfs/20210214/20210214_LALDEN_book.pdf)은 원역사 재악화와 당일 출전 `14:14`를 기록한다. [AY](../research/O15F14AY_DAVIS_INJURY_POSSESSION_LINEUP.md)의 공식 교대 재구성상 그 접촉 순간 Denver 코트에 Hampton·Nnaji가 없었다. [NBA 3/20 보도](https://www.nba.com/news/lebron-james-leaves-lakers-game-with-right-ankle-injury-will-not-return)는 Atlanta Solomon Hill과 LeBron의 별도 접촉을 기록하고, [BA](../research/O15F14BA_LEBRON_HILL_CONTACT_CAUSAL_GATE.md)는 Hill의 원역사 영입/출전과 활성 Chicago 세계선의 **동일 포제션 재현**을 구분한다. 두 원역사 사건의 선수 신원과 대체 세계 의료 결과는 서로 다른 주장이다.

대체 세계에서 원역사 건강 달력을 그대로 쓰는 것도 **명시적 설계 선택**이다. Davis 사건이 바뀌었다고 LeBron 사건이 자동으로 사라지는 것도 아니다. 반대로 두 달력을 원역사로 잠가도 거래·로스터·코치·상대 분이 달라진 다른 경기는 새로 검문해야 한다. 이 선택은 [S0/S1/S2 증거 기준](CHICAGO_2020_21_D1_EVIDENCE_STANDARD_DECISION_PACKET.md)과 별개로 보관하며, S1/S2의 `AUTHOR_MODELED` 허용을 작가가 선택하기 전에는 현행 S0를 바꾸지 않는다.

## 최소 재검토 경기 집합

[재현 도구](../tools/build_chicago_2020_21_dual_health_exposure.py)는 Davis 결장 30경기와 **사건 당일 2/14**를 합친 31개, LeBron 3/20 부분 경기·첫 결장 20·복귀 2·재결장 6·마지막 복귀 2의 31개를 결합한다. 두 집합의 교집합은 **17개**(3/20 부분 경기 + 3/21–4/19 공동 결장 16), 합집합은 **45개 고유 Lakers 정규시즌 경기**다. 2/14를 누락해 44개로 세거나, 30+31을 더해 61개로 세면 안 된다. 이는 날짜별 **최소 입력 검문 목록**이며 경기 결과 반전의 예측이나 플레이오프까지 포함한 상한은 아니다.

| 하위 선택 | 대체 건강 사건의 방향 | 먼저 다시 검문할 원경기 날짜 | 검증 비용·나비효과 |
|---|---|---:|---|
| **H00 — 두 원역사 건강 달력 유지** | Davis 2/14 재악화·30경기 결장, LeBron 3/20 부분 이탈·20+6 결장/복귀를 대체 세계의 **명시적 모델 입력**으로 채택 | 건강 달력의 새 날짜 변경 0. 다만 2/14·3/20 접촉 선행 로스터/포제션, F4/F5 거래·분과 F038의 다른 변경 경기는 검문 | 원역사 추가 부상/회피를 창작하지 않는 가장 작은 건강 분기. 원역사 의료 사건을 대체 세계에서 사실로 증명하지 못하므로 증거 기준의 모델 등급을 따른다. F038 Lakers 42승·DEN3–LAL6은 다른 시즌 입력도 유지할 때만 조건부 |
| **H10 — Davis 변경, LeBron 유지** | 2/14 재악화 또는 결장 길이에 새 후보를 만들되 LeBron 원역사 달력은 유지 | **31경기**: 2/14 + Davis 결장 창 30 | 새 의료 날짜·Davis 분/5인조·30경기 상대 결과 필요. 그중 17경기는 LeBron 창과 겹치므로 James 달력을 무조건 독립 게임 흐름으로 복사할 수 없다. 승수·시드·Denver 첫 상대/다음 라운드·lottery 재산출 |
| **H01 — Davis 유지, LeBron 변경** | Davis 원역사 달력 유지, 3/20 접촉/후속 결장에 새 후보를 만든다 | **31경기**: 3/20 부분 경기 + 20+2+6+2 | Atlanta Hill 등록·접촉 흐름, James의 새 날짜별 건강·Lakers 분/상대 결과 필요. 5/3 Denver 상대 원역사 Lakers `+4`는 두 번째 결장 창 안에 있으며 새 승패 예측이 아니다. 시드·Denver 대진·lottery 재산출 |
| **H11 — 둘 다 변경** | 각 사건의 새 날짜·건강 후보를 따로 만든 뒤 상호 접촉을 결합 | **45경기**: 두 집합 합집합 | 17개 겹침을 한 번만 계산하고 2/14·3/20 부분 경기부터 1080경기·플레이인·Denver 시리즈/2라운드·추첨·2021–23 후손까지 연결. 계산 범위와 불확실성이 가장 큼 |

**권고 후보: H00.** AY에서 Davis 재악화 장면의 직접 상대가 사라졌다는 증거가 없고, BA에서 Hill이 대체 Atlanta에 없다는 증거도 없다. 따라서 새 회복 기간이나 경기 승리를 발명하지 않고 두 원역사 건강 달력을 **작가 모델로 유지하는 쪽이 자료와 충돌할 가정을 가장 적게 추가**한다. 이것은 부상의 재현 확률에 관한 의학적 주장이나 작가 확정이 아니다. H10/H01/H11을 고르면 “부상 회피”라는 문구만으로는 부족하며 사건일·결장/복귀 날짜를 구체화한 뒤 해당 31/45경기와 후행 달력을 재실행해야 한다.

## 다른 게이트에 드는 비용과 결정 순서

- **명단·분:** Denver는 McGee/Nnaji 이탈·Hartenstein/Bey 잔류, Atlanta Hill 경로, Lakers 2/14·3/20·5월 건강과 각 경기 240분/5인조를 연결한다. 원역사 박스의 이름만 바꿔 경기 결과를 상속하지 않는다.
- **승패·플레이오프:** [AX 한 경기 민감도](../research/O15F14AX_DEN_LAL_SEED_CAUSAL_SENSITIVITY.md)는 4/15 Lakers 한 승 추가로 Denver 첫 상대가 Dallas가 되는 조건부 예를 보인다. 원역사 건강과 F038 승패를 모두 유지했을 때의 Denver–Lakers 3–6도 새 시리즈 승자는 아니다. Phoenix–Portland/Utah–Memphis 갈래도 실제 대진 결정 뒤 연결한다.
- **계약·픽:** Lakers 건강 선택은 F1 Chicago `R`, F2 Boston 예외/픽, F3 Denver Gordon 픽을 해결하지 않는다. 새 시드/플레이오프·추첨이 계약/픽 가치나 2021–23 거래를 바꾸면 후행 자산과 CBA를 다시 검문한다. [Cleveland C1/C2](../research/O15F14AA_CLEVELAND_VAREJAO_C1_C2_DECISION_PACKET.md)는 별도 작가 선택이다.
- **인물·역사:** 주인공의 Chicago 원클럽과 라이벌 Minnesota 성장축은 유지한다. Lakers 핵심 두 선수의 부상 달력을 바꾸면 실존 선수의 출전·수상·플레이오프 공로와 독자에게 보이는 역사 이탈 범위를 검토한다. 새 서사 장면이나 원고는 작성하지 않는다.

현재 권고를 작가에게 제시할 수는 있지만, H00도 **A1 전체 PASS, F5, K_HEALTH, 시즌/추첨 정본, 원고 개방을 자동으로 만들지 않는다.** S0/S1/S2와 C1/C2의 미선택 상태를 먼저 보존한다. 선택이 오면 사건/날짜를 결정 기록에 넣고, 해당 경기 집합과 후행 시즌을 재현·독립 반증한 뒤 PR→main으로 반영한다.

**분류:** NBA 경기책·당시 보도는 원역사 **사실**. 31/31/17/45 집합과 F038 시드는 저장소 **재현/조건부 계산**. H00~H11은 **후보**. 건강 관련 **신규 작가확정 0건**. 이번 패킷의 Antigravity CLI는 첫 호출에서 내부 command 권한 거부, 둘째 웹 전용 호출은 45초 제한에 본문 0건이어서 `NO_VERIFIED_BODY`. Claude CLI의 읽기 전용 반증 호출도 약 75초 동안 결과가 없어 중단해 `ATTEMPTED_NO_RESULT`; NotebookLM·source-blind는 `NOT_RUN`이다. 이 시도들을 독립 검증이나 G16 통과로 세지 않는다. F `0/5`, A `0/3`, K `0/4`, 7행 1완료·1진행·5대기/미완료 6개, `PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 `CLOSED`.
