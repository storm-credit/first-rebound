# O-15F14-BB — LeBron 20+6경기 결장 창과 시즌 원장 접촉

- 판정: `HISTORICAL_20_PLUS_6_CALENDAR_RECONCILED / ALT_HEALTH_AND_SEED_HOLD`.
- [31경기 재현 JSON](../simulation/CHICAGO_2020_21_LEBRON_WINDOW_CONTACT_AUDIT.json) · [생성/검문 도구](../tools/build_chicago_2020_21_lebron_window_contact_audit.py) · [BA 접촉 선행 조건](O15F14BA_LEBRON_HILL_CONTACT_CAUSAL_GATE.md) · [AZ Davis 30경기](O15F14AZ_DAVIS_WINDOW_CONTACT_AUDIT.md).

## 원역사 건강 달력

[NBA 3/20 보도](https://www.nba.com/news/lebron-james-leaves-lakers-game-with-right-ankle-injury-will-not-return)는 Atlanta의 Solomon Hill과 접촉한 뒤 LeBron이 2쿼터에 이탈했다고 기록한다. 그날 [공식 최종 박스](https://statsdmz.nba.com/pdfs/20210320/20210320_ATLLAL.pdf)의 James `10:36`은 **부분 출전**이지 결장 한 경기로 세지 않는다. [NBA 4/30 복귀 보도](https://www.nba.com/news/report-lebron-james-may-return-tonight-vs-kings)는 그 전 **20경기 결장과 Lakers 8–12**를 명시한다. [NBA 5/2 Raptors전 보도](https://www.nba.com/game/0022000974)는 그 경기 후반 James의 이른 이탈과 발목 불편을 기록한다. [NBA 5/15 Pacers전 영상 설명](https://www.nba.com/watch/video/20210515gametimelakers)은 이후 **6경기 결장 뒤 복귀**를 기록하고, [5/16 공식 박스](https://www.nba.com/game/lal-vs-nop-0022001072/box-score)는 마지막 경기 출전을 확인한다. 원역사 관측이지 대체 세계 의료 예측이 아니다.

| 구간 | Lakers 기준 원역사 일정·성적 | 조건부 원장 위치 | A1에서의 의미 |
|---|---:|---|---|
| 3/20 Atlanta | 부분 출전 1경기, 패배 `−5` | F038 1 | Hill 접촉의 사건일; 결장 20에 포함하지 않음 |
| 3/21–4/28 첫 결장 | **20경기 8–12** | F038 19, Remaining 1 | 이 중 **16경기**가 Davis의 2/16–4/19 결장 창과 겹침 |
| 4/30–5/2 첫 복귀 | **2경기 0–2** | F038 2 | 5/2의 발목 불편/후반 이탈을 다음 결장 창과 분리 |
| 5/3–5/12 두 번째 결장 | **6경기 4–2** | F038 4, Remaining 2 | 5/3 Denver 상대 Lakers `+4`도 여기에 포함 |
| 5/15–5/16 마지막 복귀 | **2경기 2–0** | F038 2 | 5/16까지 원역사 가용성 확인 |

생성기는 [1080경기 원점수 CSV](../simulation/NBA_2020_21_REGULAR_GAME_BASELINE.csv)에서 Lakers 31개 고유 경기 ID를 추리고, F038/Remaining/Boundary의 `game_summary`에 정확히 한 번씩 대응했다. 위 31개는 **F038 28·Remaining 3·Boundary 0**이며 전부 두 평점법 `ALL_TESTED_RETAIN`; F038 `changed_game_ids`와 교집합 0이다. 3/20 부분 경기와 첫 결장 16개를 합하면 Davis가 원역사에 빠진 동안 LeBron이 **부분 부상 이탈 또는 전경기 결장**한 경기 17개다. 이 교집합은 날짜 접촉이지, 두 부상이 의학적으로 서로 원인이라는 뜻이 아니다.

원점수차 5점 이내 패배는 첫 결장 4/22 Dallas `−5`, 첫 복귀 4/30 Sacramento `−4`, 두 번째 결장 5/7 Portland `−5`다. [기존 조건부 원장](../simulation/CHICAGO_2020_21_LEBRON_WINDOW_CONTACT_AUDIT.json)의 두 평점 구간은 4/22 Dallas전 Lakers 약 `−3.48…−4.99`, 5/7 Portland전 약 `−3.05…−3.27`로 여전히 패배 방향이다. 5/3 Denver전 원역사 Lakers `+4`는 조건부 RAPTOR 약 `+4.63…+4.84`, BPM 약 `+3.90…+3.93`으로 승리 방향이다. 이는 **원역사 LeBron 결장/복귀 입력을 유지한 계산**이다. 가상의 James 출전 또는 다른 건강 달력에서 승패가 어떻게 바뀌는지는 산출하지 않았다.

## A1·F5 재실행 범위

1. [BA](O15F14BA_LEBRON_HILL_CONTACT_CAUSAL_GATE.md)의 Hill 등록·3/20 포제션과 [AY](O15F14AY_DAVIS_INJURY_POSSESSION_LINEUP.md)의 Davis 2/14 접촉을 각각 검문한다. 3/20은 부분 출전으로 남기고 20+6 두 결장 창과 4개 복귀 경기를 섞지 않는다.
2. 대체 건강 후보에서 바뀐 Lakers 출전 날짜·상대 5인조·분·생산성을 31개 경기 원장 및 Davis 30경기 원장에 겹쳐 넣는다. 한 선수가 건강하다는 가정만으로 기존 원점수나 접전 패배를 반전시키지 않는다.
3. Lakers와 상대의 새 승패, 서부 동률/시드, L2 플레이인, Denver의 첫 상대와 1·2라운드 분·결과를 다시 산출한다. 특히 5/3 Denver전은 첫 Dallas/Denver 대진과 관계되는 **직접 맞대결**이지만 다른 승자 후보는 아직 만들지 않았다. 2021 추첨·후행 계약/픽도 승수 변경 시 이어서 검문한다.

**분류:** NBA 기사·박스의 20+6 결장과 3/20 부분 출전은 원역사 **사실**. 8–12·4–2 성적, 31개 원장 위치와 두 평점 방향은 저장소 **재현 계산**. 대체 의료 달력·추가 승패·대진은 **후보 미산출**. **신규 작가확정 0건**이며 S0/S1/S2·C1/C2 작가 선택도 이 검문에서 하지 않는다.

Codex가 NBA 공식 자료와 1080경기·세 JSON을 직접 대조했다. 생성기를 연속 두 번 실행해 출력 해시가 같은지 확인하고 Python 구문·상대경로를 검사한다. 이번 국소 작업에서 Anti-Gravity·NotebookLM·Claude·source-blind는 `NOT_RUN`; 독립 원자료나 G16 통과로 세지 않는다. F5/A1/A3·K_HEALTH/K_METHOD_EVENTS는 `HOLD`, F `0/5`·A `0/3`·K `0/4`; 7행 1완료·1진행·5대기/미완료 6개, `PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 `CLOSED`.
