# O-15F14-BA — 3/20 LeBron–Hill 접촉의 선행 조건

- 판정: `HISTORICAL_ACTOR_CONFIRMED / ALTERNATE_CONTACT_AND_HEALTH_HOLD`.
- 범위: Chicago 2020–21 D1의 A1 건강, F5 Denver 첫 대진, K_HEALTH·K_METHOD_EVENTS. 원고나 새 건강 사건을 쓰지 않는다.
- 선행: [AX 시드 민감도](O15F14AX_DEN_LAL_SEED_CAUSAL_SENSITIVITY.md) · [AY Davis 접촉 선수](O15F14AY_DAVIS_INJURY_POSSESSION_LINEUP.md) · [AZ Davis 결장 30경기 원장](O15F14AZ_DAVIS_WINDOW_CONTACT_AUDIT.md).

## 원역사의 사건과 활성 세계선의 분리

| 분류 | 확인한 범위 |
|---|---|
| **원역사 사실** | [NBA 2020 시즌 프리뷰](https://www.nba.com/news/hawks-expectations-soar-for-2020-21)는 Atlanta의 Solomon Hill FA 영입을 기록한다. [NBA 3/20 보도](https://www.nba.com/news/lebron-james-leaves-lakers-game-with-right-ankle-injury-will-not-return)는 Lakers–Hawks전 Hill의 스틸 시도 중 James와의 접촉, James의 오른쪽 발목 부상·이탈을 기록한다. [공식 최종 박스](https://statsdmz.nba.com/pdfs/20210320/20210320_ATLLAL.pdf)에는 Hill `18:25`, James `10:36`, Hawks `99–94`, Davis의 오른쪽 종아리 부상 미출전이 있다. 최종 박스는 접촉 순간의 플레이바이플레이나 대체 세계의 출전 증명이 아니다. |
| **저장소의 기존 조건부 계산** | `2021-03-20_LAL_ATL`은 [AZ JSON](../simulation/CHICAGO_2020_21_DAVIS_WINDOW_CONTACT_AUDIT.json)의 F038 859경기 부분에 있다. 원역사 Lakers `−5`; RAPTOR/BPM 모두 `−5`의 `ALL_TESTED_RETAIN`, `changed_in_f038=false`. 이 계산은 Hill–James 원역사 사건을 지운 건강 대체안이 아니다. |
| **인과 추론** | Hill의 *원역사 영입*은 대체 세계의 Atlanta 등록·당일 출전·동일 포제션을 자동 보증하지 않는다. 반대로 활성 Chicago 경로에서 Atlanta가 달라졌다는 직접 근거도 현재 찾지 못했다. Hill이 빠졌거나 James 부상이 사라진다고 단정할 수 없다. Davis 2/14 사건과 LeBron 3/20 사건은 서로 다른 접촉이지만, 3/20 Lakers의 인원·경기 흐름은 앞선 Davis 가용성에 영향을 받을 수 있다. 따라서 두 건강 분기의 계산상 독립성도 가정하지 않는다. |
| **후보·작가확정** | 3/20 원역사 접촉/후속 결장을 유지하는 안과, 선행 로스터·5인조·경기 흐름 변화로 접촉 재현을 보류하는 안은 모두 미선택 후보. Hill의 이적·LeBron의 의료 결과·Lakers 추가 승수·대진을 이 메모에서 새로 잠그지 않는다. **신규 작가확정 0건.** |

이전 [Atlanta 주인공 분기 사전 계산](../simulation/ATLANTA_2019_23_ROLE_MINUTE_PRECALC.md)의 Hill 분 교환은 현재 Chicago 주인공 세계선의 권위가 아니다. [활성 Chicago 후반 입력 검토](../simulation/CHICAGO_2020_21_POSTDEADLINE_INPUT_REVIEW.md)는 Atlanta의 새 직접 변경을 특정하지 못한 기준선 후보로 처리했으나, 이것도 Hill의 3/20 정확 출전과 접촉을 최종 확정하지 않는다.

## A1에서 필요한 순서

1. Atlanta의 2020 Hill 영입/3월 20일 등록을 활성 세계선의 다른 드래프트·거래·계약 경로와 대조한다. 변경 근거가 없으면 **조건부 원역사 유지 입력**으로 표기하되, 승인된 정본이라고 부르지 않는다.
2. Lakers의 Davis 2/14 이전 건강, Denver 2/14 포제션, 그 뒤 30경기 가용성을 별도로 놓는다. 3/20 Atlanta전의 Hill·James 5인조/포제션과 접촉 재현 가능성을 검문한다. 원역사 최종 박스만으로 정확 접촉의 대체 재현을 증명하지 않는다.
3. LeBron 사건을 보존/변경하는 후보별로 3/20 당일과 후속 Lakers 경기의 가용성·상대 분·승패를 1080경기 원장에 연결한다. 의료 회복 기간이나 경기 반전을 원역사 점수차로 예측하지 않는다.
4. Lakers 승수·동률/시드, Denver 첫 상대와 1·2라운드 분/승패, 플레이인·추첨·후행 계약을 다시 검산한다. [AX](O15F14AX_DEN_LAL_SEED_CAUSAL_SENSITIVITY.md)의 한 경기 반전은 대진 민감도이지 새 시즌 결과가 아니다.

**검증 한계:** NBA 3/20 공식 웹 플레이바이플레이는 이번 접근에서 동적 표만 노출했고, 당시 공식 경기책 전체 PDF와 CDN API는 접근되지 않았다. 따라서 정확 접촉 시각·그때 코트 열 명은 여기서 인증하지 않는다. Codex가 NBA 보도·공식 최종 박스·기존 AZ 원장을 직접 대조했다. Anti-Gravity·NotebookLM·Claude·별도 source-blind 검수는 이번 국소 검문에서 `NOT_RUN`; 도구 재독을 독립 원자료로 세지 않는다.

현재 A1/F5/A3와 K_HEALTH·K_METHOD_EVENTS는 `HOLD`; F `0/5`, A `0/3`, K `0/4`. 7행 큰 작업은 1완료·1진행·5대기, 진행 중 포함 **6개 미완료**. `PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 `CLOSED`와 원고 금지는 그대로다.
