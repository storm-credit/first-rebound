# O-15F14-AZ — Davis 결장 30경기와 F038 접촉 원장

- 판정: `HISTORICAL_30_GAME_COVERAGE_PASS / ALT_AVAILABILITY_AND_RESULTS_HOLD`.
- [30경기 재현 JSON](../simulation/CHICAGO_2020_21_DAVIS_WINDOW_CONTACT_AUDIT.json) · [생성/검문 도구](../tools/build_chicago_2020_21_davis_window_contact_audit.py) · [AX 시드 민감도](O15F14AX_DEN_LAL_SEED_CAUSAL_SENSITIVITY.md) · [AY 2/14 접촉 장면](O15F14AY_DAVIS_INJURY_POSSESSION_LINEUP.md).

## 30경기 전체의 저장소상 위치

[NBA의 Davis 복귀 보도](https://www.nba.com/news/lakers-anthony-davis-ends-30-game-injury-absence-against-mavs)는 2/14 Denver전 뒤 4/22 Dallas전 복귀 전까지 **30경기 결장·Lakers 14승 16패**를 명시한다. 생성기는 기준 1080경기 CSV에서 2/16~4/19 Lakers 경기 30개를 추려 각각의 날짜·원점수·승패를 아래 세 **기존 조건부 경기 원장**의 `game_summary`에 연결했다.

| 원장 | 연결 경기 | 범위 |
|---|---:|---|
| F038 `NBA_2020_21_FULL_SEASON.json` 859경기 부분 | 26 | 다른 팀의 조건부 변화가 있더라도 두 평점법에서 원승자 유지 |
| `CHICAGO_2020_21_REMAINING_PAIRED_IMPACT.json` | 3 | 2/20 Miami, 3/3 Sacramento, 3/28 Orlando |
| `CHICAGO_2020_21_BOUNDARY_PAIRED_IMPACT.json` | 1 | 2/22 Washington |
| **합계** | **30** | 원역사 `14–16`, 세 원장의 `ALL_TESTED_RETAIN` 30/30, F038 `changed_game_ids` 교집합 0 |

세 원장은 이 구간에서 중복 ID가 없다. **F038의 859경기 `game_summary`만 읽으면 네 경기가 빠진다.** 이는 시즌 전체에서 네 경기가 미계산됐다는 뜻이 아니라 앞선 두 원장에 기록됐다는 뜻이다. 생성기는 30 ID를 모두 찾고, 두 평점법의 Lakers 방향 구간이 원승자와 같은지 검사한다. 그 검사는 **기존 Davis 결장 달력을 유지한 조건부 계산**에만 적용된다.

## 원역사 5점 이내 여섯 경기

아래의 평점법 구간은 홈마진 부호를 Lakers 관점으로 변환했다. `+`는 Lakers 우세, `−`는 열세다. 원점수차와 모델 구간은 서로 다른 정의이며, 어떤 값도 Davis가 대체 세계에서 출전했을 때의 점수 예측이 아니다.

| 날짜·상대 | 원역사 Lakers 차 | 조건부 RAPTOR / BPM Lakers 차 구간 | 원장 |
|---|---:|---|---|
| 2/20 Miami | −2 | −2 / −2 | Remaining |
| 2/22 Washington | −3 | −1.82~−1.75 / −2.59~−2.54 | Boundary |
| 3/3 Sacramento | −3 | −3 / −3 | Remaining |
| 3/12 Indiana | +5 | +5 / +5 | F038 |
| 3/20 Atlanta | −5 | −5 / −5 | F038 |
| 3/28 Orlando | +3 | +1.26~+1.30 / +1.02~+1.09 | Remaining |

3/28은 원점수로 Lakers 3점 승리지만 Orlando 대체 선수/분을 반영한 **기존 조건부** 구간은 두 방법 모두 약 1점대 승리다. 이는 이미 F038 계열에 반영된 상대 변화이며, Davis 건강을 새로 바꾸는 효과가 아니다. 2/22의 원역사 Lakers 3점 패배도 상대 Washington 조건부 입력 뒤에는 두 방법 모두 패배를 유지하되 절댓값이 다르다. 원점수차 5점 이내라는 이유만으로 뒤집을 경기나 확률을 결정하지 않는다.

[NBA의 LeBron 3/20 부상 보도](https://www.nba.com/news/lebron-james-leaves-lakers-game-with-right-ankle-injury-will-not-return)는 Davis 창 안의 **별도 사건**이다. A1에서 2/14 Davis 재악화·30경기 가용성 중 하나라도 달라지면 이 30개 경기의 날짜별 Lakers 5인조·상대 입력·승패를 새로 계산하고, LeBron 사건은 독립 분기로 검문해야 한다. 변경 결과를 [AX의 서부 시드·Denver 첫 상대](O15F14AX_DEN_LAL_SEED_CAUSAL_SENSITIVITY.md)에 다시 입력한다. 현행 F038 결과 0/30 변경은 건강 변경안을 통과시키는 근거가 아니다.

**분류:** NBA 부상 보도·기준 경기 점수는 원역사 **사실**. 세 저장소 원장의 구간·승자 유지는 기존 **조건부 계산**. 건강 분기·30경기 새 결과는 **후보 미산출**, **작가확정 0**. F5/A1/A3·K_HEALTH/K_METHOD_EVENTS는 `HOLD`, F `0/5`·A `0/3`·K `0/4`, `PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 `CLOSED`.

Codex가 NBA 보도와 1080경기 기준 CSV·세 조건부 게임 원장을 직접 대조하고 생성기를 실행했다. 이 국소 검문에서 Anti-Gravity·NotebookLM·Claude·source-blind 독립 검수는 `NOT_RUN`; 전체 G16 검수로 세지 않는다.
