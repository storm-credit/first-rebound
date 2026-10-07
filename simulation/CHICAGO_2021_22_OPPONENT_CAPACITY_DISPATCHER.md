# Chicago 2021–22 공통82키 dispatcher와 조건부 용량 색인

기준 main `51ab52af234c67ec1f34fe4dade717ba2bad9561`. 원CSV·S2 seed·DB1 권리·raw event의 소비 필드와 역할/명단/active/시계를 직접 연결했다. 기존 경제/시즌 조상 생성기는 다시 실행하지 않는다. root의82CSV/6조합초별 primitive 독립검문과 동일총분 PG/SG 교환반례 거부를 수용했다. 새 계약·건강·승패·중요방향 선택은0이다.

## 조회와 범위

`dispatch(game_id, chi_state=None, include_clock=False, root=ROOT)`는 정확 날짜·양팀·입력 포트·용량 후보와 HOLD를 반환한다. `chi_state="NORMAL"` 또는 `"COBY_OUT"`은 별도 소비자가 선택한 날짜 건강모델의 연결 키이며 dispatcher의 새 선택이 아니다. `include_clock=True`는 source_game_id를 보존한 원증인과 requested_game_id를 함께 반환한다. 재사용 날짜에 원증인 날짜를 덮어쓰지 않는다. 다른 CHI 상태는 `CHI_STATE_OUTSIDE_VERIFIED_ROLE_DOMAIN`으로 거부해 새 역할함수 필요를 드러낸다. [범위 입력](../design/CHICAGO_2021_22_OPPONENT_FINITE_DISPATCH_SCOPE_2026_10_07.md)을 소비하는 한 JSON이다.80개 문서를 만들지 않았다.

| 날짜키 상태 | 키수 | 반환 내용 |
|---|---:|---|
| 원DET/NOP 한정 검문된 조건부 용량 | 2 | DET4/NOP2의6조합 색인·규정시간48/양팀240 |
| 후속DET/NOP 재사용 후보 | 4 | 동일 용량ID, 해당날짜 계약/소속/가용 interval HOLD |
| SAC/ORL 부분 stencil | 6 | 아직 전체 상대 함수가 없는 typed port |
| 기타25팀 | 70 | 팀별 미완typed port25개 |

용량6개는 원11/DET9/NOP6블록의 매구간·선수분·active/소속을 직접 대조했다. 원2키의 `original_pair_source_date_binding_verified:true`는 원검문 증인 날짜 일치만 뜻한다. `dated_operating_interval_implementation_completed:false`와 `source_interval_proven_for_requested_date:false`는82전행에 남아 whole계약 날짜구현으로 승격하지 않는다. 나머지4재사용 날짜는 같은 용량의 수학적 사용 후보이며 날짜별 등록·가용 조건을 통과한 실행일이 아니다. `actual_executable_selected_dates:0`은 정직한 현재 범위이며 검토된 원용량이 없다는 뜻이 아니다. 원규정시간 증인을 실제 건강/날짜/OT/승패 선택으로 읽지 않는다.

## 미완 입력의 typed port

27개 port는 team·적용 interval·명명된STD/TW 계약가족·미서명권리/Tender/UPC·source/권위·양수가용 조건·active12–15·five-player 정수초 블록·position/creator 규칙·OT 분기를 요구한다. 새로운27가족을 창작하지 않았고 `provided_function:null`이다. 실제사적접수/장부 전체나 원건강 진단을 새 필수 gate로 넣지 않았다. 명명된 공개 제약과 합법한 가상 구현의 경제 구간을 받는다.

첫 새port는TOR `0022100046`(10/25)이다. Powell/Trent/Hood/Bonga의 변경 선행과 DB1 Giddey8/Banton46/Hauser48의 권리/계약 구분은 scope 원천을 그대로 따른다. 바로 다음DET10/23은 reuse HOLD이다. reported1034행을 새가상거래로 적용하지 않는다.

## 원천 검문

고정source핀만 보지 않고 원CSV identity/OT, S2 May16 fullroster classification/hardship, DB1 holder/player/order/unsigned flags, rawfeed1034 actor/date/type/GroupSort/index를 재구축한다. Loaded object 및 반환 input context는 별도physical JSON/CSV와 동등해야 한다. 역할 시계는 실제 CHI primitive11·원DET9·NOP6블록과 구간별 직접 대조하고 반환객체를caller에서 재검사한다. 인덱스는 원source pointer를 유지하며 결과·가입·불확정 interval을 새확정값으로 바꾸지 않는다.

## 7행 진행표 — 원scope 기준시점

[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md) 우선. 아래는원scope가 보존한f90d3bc snapshot이다.

| 번호 | 작업 | 상태 |
|---|---|---|
| 1 | 2020 드래프트 연쇄 | 완료. 기존 작가 선택·연쇄 보존 |
| 2 | Chicago 2020–21 | 완료(S2 유한 가상 실행). 정규1080·L2 6·playoff88/총1174경기·2348팀. 법적12/12·F5/5·A3/3·K4/4·시즌true. 전체 명단/슬롯 공백0·작업active12–15·벤치8·H00초기영구이탈2·승인거래8·origin/control60 검문. 실제 의료/금융/접수·미래권리 전달은 별도 미인증 |
| 3 | 2021–23 거래·계약 | 진행. M1/A 여름 완료·CHI–DET/NOP 동시시계·FY22 17명 한날짜 계약/비용 연결 검문. 중요방향·두시즌 미완료 |
| 4 | 주인공·라이벌 장기 커리어 | 17시즌 행동/비용·A09–A14 27인과후보 연결. H2·RC1·AW2·NM1 중요 결과·후속 정확 실행 미완료 |
| 5 | 결말·전체 구조 | 14막42소막·국소기능43/경로25/없는17/source53. A09두기능 조건부진입미선택·등록증분0. 전체G13 미완료 |
| 6 | 집필 규격·Context Pack | 독서110/110·S1 규격 완료·국소기능43·설계샘플2/실제Pack0·전체G13/G14 미완료 |
| 7 | 통합·독립 검수·작가 승인 | G15/G16/G17 전체 미완료. 국소 독립 검문을 전체G16/G17로 계산하지 않음 |

미완료큰묶음5·6번까지4·v0.30 PARTIAL·설계/원고CLOSED·실제Pack0·원고0. 전체macro3/REGISTER/중앙/Git승격0.
