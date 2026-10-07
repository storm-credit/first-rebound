# Chicago2021–22 M1: 82날짜·두 상태 조건부 분 carrier

INDEPENDENTLY_REVIEWED_CONDITIONAL_82DATE_TWO_STATE_REGULATION_CARRIER

82개 관측 game_id/date/home/away에 NORMAL과 COBY_OUT을 실제로 구성했다.164행·1,804개 순서없는5인 블록·9,020개 선수블록 셀이다. 날짜별 상태 선택0이며82경기를 모두 건강/출전/승패 확정한 원장은 아니다.

## 실제 구성한 분과 명단

두 상태 모두 Markkanen32·Caruso18·주인공32, 포지션마다48분, 정규48분/240팀분,11블록/5명 중복0·LaMelo 또는LaVine 창조자 조건을 만족한다. NORMAL양수10명; COBY_OUT양수11명이며 Coby PG10→Satoransky10/SG8→Valentine8을 적용한다. 기존R21A28/22와 다른 M1이다.
각 행은 reviewed SQ1의15STD·2TW를 유지하는 조건 아래 양수 전원과 std-first0분 수신자를12명 active로 구성하고 나머지3STD inactive를 명시했다. NORMAL0분 active2명, COBY_OUT0분 active1명이다. 최소12/최대15 size-domain 중 실제 구성은12명이다. 남은0분 임상상태는 null이며 inactive는 운영 분류, 부상 진단이 아니다.
Coby-out은 Coby를 그 후보의 active/양수에서 제외하는 조건이다. 다른 복합 결장은 처리하지 않았다. active filler의 가용성은 admitted운영조건이고 실제 의학 사실이 아니다. TW2는 별도 Two-Way Roster에 남고 active/inactive에 넣지 않아 어느82상태 조합에도 TWactive0이다. 개막50제약 및 나중50초과 예외의 미확인 발효시점에 기대지 않는다.

## 날짜·시간 경계

같은 관측 날짜를 쓰는 것은 routine schedule **가설**이다. 원일정의 감염·연기·접촉 사건을 복사하지 않는다. 기존원자료 재수집0, historical대체승패0. 원M1 FREEZE의 옛 SHA를 다시쓰지 않고 현행 승인32/18·실제position/5인 의미를 직접 대조한다.
역사적OT 진단이 있는 날짜2개를 각 행에 보존했다. 본 증인은 regulation-only이다. 역사적OT를 새OT로 승격하지 않으며 새OT가 없었다고도 선택하지 않는다. 전체경기 분을 완료하려면 명시적 no-OT 모델 혹은 새OT5인/가용성/clock 연장 증인이 필요하다.

## 원천과 재현

[2017CBA](https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf) PDF412/printed390 XXIX1–3 직접본문·raw/textSHA, reviewed [NBA2021로스터 규칙](https://pr.nba.com/nba-board-of-governors-play-in-roster-rules-2021-22-season/) 입력을 연결했다. 기본12active와3STDinactive를 실제 검사하며 실제리그접수 인증을 요구하거나 주장하지 않는다.
`python -B tools/build_chicago_2021_22_m1_dated_working_minutes.py --check --self-test`. source지문·map31핀·normalM1 고정예산·날짜/회원/5인/수신자/active/OT/권위 변조를 거부한다. 자기통제는 독립검문으로 세지 않는다.
다음은 날짜별 상태 선택/다른 결장, 상대82명의 dated roster+minute 쌍과 생산성/impact 방법의 조인이다. 여기서 결과·우승·2022계약·AP1/SG16을 선택하지 않았다.

[입력지도](../design/CHICAGO_2021_22_FINITE_IMPLEMENTATION_MAP_2026_10_07.md) · [현행로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md) · [누적 기능 등록기](../control/G13_FINAL_FUNCTION_REGISTER.md)

|번호|묶음|상태|
|---|---|---|
|1|2020드래프트 연쇄|완료|
|2|Chicago2020–21|S2완료|
|3|2021–23거래·계약|M1 날짜별 두 상태 carrier 완료; 실제 날짜별 모델/양팀/결과 미선택|
|4|장기 커리어|후속시즌 입력 대기|
|5|결말·전체 구조|전체기능표 미완료|
|6|집필규격·Context Pack|현행 누적등록기 참조·Pack0|
|7|통합·독립·작가 승인|최종CLOSED|

미완료 큰 묶음5. v0.30 PARTIAL / 설계·원고CLOSED / 원고0.
