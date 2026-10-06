# 2021 플레이오프 날짜별 승패 작업 모델

2026-10-07 / 기준 main `1401b74`.

[기존 시즌 설계 위임](../canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json) 아래 [15시리즈의 선택 승자와 길이](NBA_2021_DELEGATED_PLAYOFF_RESULTS.json)를 보존하고, [이미 채택한 88날짜](NBA_2021_WORKING_PLAYOFF_CALENDAR.json)에 개별 승패 작업 모델을 연결했다. [실행표](NBA_2021_DATED_PLAYOFF_RESULT_MODELS.json), [생성·검문기](../tools/apply_2021_dated_playoff_results.py).

DEN–LAL의 기존 6경기는 변경 없이 연결했고, 다른 14시리즈의 82경기를 새 작업 모델로 선택했다. 시리즈 승자·길이 변경은 0이다. 새 원역사 관측 사실이나 확률 예측이 아니다. 각 시리즈의 `selection_reasons`는 개별 승패를 정한 설계 이유이며 실제 경기 점수와 인과를 인증하지 않는다. 원역사의 특정 슛·부상·연장전을 가져오지 않는다.

| 시리즈 | 게임 순서에서 승리 팀 | 작업 설계 이유 |
|---|---|---|
| PHI–IND | PHI PHI IND PHI PHI | 새 상대 IND의 홈 1승, PHI의 홈 우위·내선 우위 |
| BKN–BOS | BKN BKN BOS BKN BKN | BOS 홈 1승과 BKN의 공격 선택 보존 |
| MIL–MIA | MIL MIL MIL MIL | 기존 4–0 선택 유지 |
| NYK–ATL | ATL NYK ATL ATL ATL | ATL 원정 2승까지 별도 경기 실행이 필요 |
| UTA–MEM | MEM UTA UTA UTA UTA | MEM 첫 승 이후 UTA의 네 승리 |
| PHX–POR | PHX POR PHX POR PHX PHX | POR 두 승리와 PHX 마지막 두 승리 |
| DEN–LAL | DEN LAL LAL DEN LAL LAL | 기존 승인된 6경기 보존 |
| LAC–DAL | DAL DAL LAC LAC DAL LAC LAC | DAL의 첫 두 승리 이후 LAC의 조정 |
| PHI–ATL | ATL PHI PHI ATL PHI ATL ATL | ATL 마지막 홈·원정 연속 승리 |
| BKN–MIL | BKN BKN MIL MIL BKN MIL MIL | MIL 마지막 홈·원정 승리, 원부상 자동 이식 없음 |
| UTA–LAC | UTA UTA LAC LAC LAC LAC | LAC의 수비·작은 라인업 조정 선택 |
| PHX–LAL | PHX PHX LAL LAL PHX LAL PHX | 2–2–1–1–1 홈 배치에서 홈팀 7승, 부상에 따른 공짜 승리를 만들지 않음 |
| ATL–MIL | ATL MIL MIL ATL MIL MIL | MIL 마지막 두 승리 |
| LAC–PHX | PHX PHX LAC PHX LAC PHX | PHX의 첫 두 승리와 원정 마무리 |
| MIL–PHX | PHX PHX MIL MIL MIL MIL | PHX 홈 두 승리 이후 MIL 네 승리 |

사실: 기존 정본의 시리즈 선택·달력·DEN–LAL 6승패. 추론: 홈 우위·전술 설명이 이 선택에 맞는다는 설계 판단. 작가 위임 선택: 새 82개의 작업 승패. 미확정: 경기 점수·박스·전체 건강·등록·법적 실행·시즌 최종 인증. `score_model`/`actual_box`는 null이다.

검문은 각 행이 참가팀 승자인지, 네 번째 승리 뒤 경기가 없는지, 최종 승리·시리즈 길이가 기존 선택과 같은지, 88날짜·홈 배치가 원입력과 같은지 확인한다. 점수 임의 삽입·의료 승격·시즌 승격은 거부한다. PROJECT_FREEZE v0.30 PARTIAL·설계/원고 CLOSED·원고 0을 유지한다.
