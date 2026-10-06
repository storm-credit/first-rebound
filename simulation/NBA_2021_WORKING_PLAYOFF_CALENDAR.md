# 2021 플레이오프 전체 작업 달력 — 15시리즈88경기

2026-10-07 / main `76cd80b` / **ALL_15_SERIES_88_DATE_MODELS_ADOPTED_AS_WORKING_CALENDAR**.

[기존 시즌 설계 위임](../canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json)에 따라 [비교·검문한 후보 달력](NBA_2021_PLAYOFF_CALENDAR_CANDIDATE.json)의15시리즈88날짜와 홈 배치를 **작업 설계 입력으로 채택**했다. 기존 선택 시리즈 승자/길이·F038 성적·대진은 바꾸지 않았다. 새 중요 결과·금융·픽 선택은 없다. [채택 실행표](NBA_2021_WORKING_PLAYOFF_CALENDAR.json), [적용·검문기](../tools/apply_2021_working_playoff_calendar.py).

전체 입력이므로 다음 건강·등록·감독계획 소비자는 이 작업 달력을 읽는다. 생성 당시 후보 파일은 근거 이력으로 보존하며 기존false는 그 후보의 권위 범위다. 날짜 모델은 채택했지만 실제NBA대체세계일정/중계·구장예약·이동시간·리그접수를 인증한 것은 아니다.

기존 원자료 검문과 기계 검사를 재사용해 2–2–1–1–1 홈 패턴, 팀/LA공유 홈 날짜 충돌0, 부모 시리즈 종료와 자식 시작의 비경기일, May22~Jul22 창, 기존 W6 확장/W7 이동, 시리즈 길이를 확인했다. 종료된 원역사 경기의 의료 사건·개인 박스·2OT를 새 세계에 복사하지 않는다.

[DEN–LAL6경기 작업 감독계획](DEN_LAL_2021_DATED_COACH_PLAN.json)의 날짜/홈/승자를 일치 검문했다. 다른14시리즈82경기의 개별 승자 배열은null이며 감독·건강·정확 분 적용도 미완료다. 날짜 사이 간격은 달력 일수이며 회복시간·의료 부하의 인증이 아니다. 다음PHX건강을 DEN–LAL에서 자동 이월하지 않는다.

`working_calendar_adopted=true`, `working_games_adopted=88`, `coach_plan_games_applied=6`, `other_coach_plan_games_remaining=82`. 실제 일정 인증·전체 건강·전체 감독 실행·A3/K/시즌/원고는false/HOLD다. 본 채택은 최종 회차 기능/Context Pack을 만들지 않는다. v0.30 PARTIAL·설계/원고 CLOSED·미완료큰묶음6.
