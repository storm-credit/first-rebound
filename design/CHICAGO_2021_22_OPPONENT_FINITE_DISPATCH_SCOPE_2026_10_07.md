# Chicago 2021–22 상대 입력의 유한 범위·dispatcher 입력

기준 main `f90d3bc91ae7ca5f7768434d3813260cb15e2b05`. 이 문서와 JSON은 정적 원천 감사·연결 입력이다. 새 역할함수27개·계약가족·건강·승패를 생성하거나 확정하지 않았다. Root 독립 정적 검문을 완료했으며 실행 연결기는 아직 구현하지 않았다.

## 1. 82키를 29팀 입력에 연결

| 구분 | 팀 | 전체 키 | 첫 두 검문키를 뺀 남은 키 | 다음 단위 |
|---|---|---:|---:|---|
| 검문된 조건부 전체 규정시간 함수 | DET·NOP | 6 | 4 | 동일 용량 함수 + 해당 날짜의 소속/계약/가용 조건 확인 |
| 기존 부분 stencil | SAC·ORL | 6 | 6 | SAC S14A–D·Metu 등록 / ORL 가드12분 빈칸 |
| 새 전체 상대 함수 미작성 | 나머지25팀 | 70 | 70 | 팀별25함수, 각 날짜에서 공동 소비 |
| 합계 | 29팀 | 82 | 80 | 미완 전체 상대 함수27개 |

DET·NOP의 한정 수용은 원래 날짜의 조건부 용량 구성이다. 이후4날짜가 이미 검문·선택됐다는 뜻은 아니다. SAC의 원8명 position budget은 S14A 비교이며 ORL은 ROLE_HOLD이다. 새 역할함수의 빈 입력과 대체세계 실제 건강/원계약 인증을 구분한다.

## 2. 하나의 입력 등록기

JSON `teams`는29팀 각각 S2 May16의 검문된 명단 object/계약 분류, DB1의 조건부 권리, 원 frozen feed의 reported 이벤트 row pointer, 역할함수/HOLD, 해당 경기키를 연결한다. `game_keys`는82개의 정확 game_id·date·home·away와 현재 M1 NORMAL/COBY_OUT pointer를 연결한다. 32/18/P32는 현재M1이며 구R21A28/22를 섞지 않는다.

동결 feed의 해당29팀·2021-05-17~2022-04-10 원자료 풀은 개막전 555행/499개 GroupSort와 시즌중 479행/404개 GroupSort다. 원자료를 새로 수집하지 않았다. 이 수는 가상 필수 작업/거래 승인 수가 아니다. GroupSort는 공동 거래를 중복 선수 행에서 묶는 source identifier이고 실제 원자적 거래 순서의 인증은 아니다.

reported 이벤트는 `APPLICATION_REVIEW_REQUIRED`, `CHANGED_CANON_PREDECESSOR`, `UNSELECTED_AP1_SG16_DIRECTION`으로 분리했다. `fictional_event_applied:false`가 전행에 남는다. 원 자료의 player/date/type/TEAM_ID/GroupSort를 직접 연결하되 계약금액·보너스·모든 픽 조건이 이 feed로 완전해졌다고 주장하지 않는다. 계약기간이 실제로 끝나거나 새 양수 선수의 소속이 바뀌는 구간만 명명된 입력을 더 받는다. HOU의 May16 표준17명은 당시 명명된 hardship2를 함께 보존한 출발점이며, 2021–22 예외나17명 등록을 자동 상속하지 않는다.

## 3. 최소 다음 batch

1. 29팀 공통 roster-state/event registry와82키 dispatcher를 먼저 구현한다. 같은 팀 상태·역할함수는 여러 날짜가 소비한다.
2. 바로 다음 DET `0022100030`(2021-10-23)은 기존 함수 재사용 후보다. 새80개 pair 문서를 만들지 않는다.
3. 첫 새 상대 TOR `0022100046`(2021-10-25)부터 named operating/role 입력을 받는다. Powell TOR 잔류와 원Trent/Hood TOR 이벤트가 충돌하고, Bonga 원TOR 영입은 변경WAS 미서명권리 사슬을 건너뛸 수 없다.
4. TOR DB1은 Giddey#8/Banton#46/Hauser#48이다. Scottie Barnes 원TOR 계약이나 David Johnson 원TOR TW를 DB1 선수의 계약으로 복사하지 않는다. 권리·Tender·NBA UPC는 각각 구현해야 한다. Powell 새 계약과 Lowry 원MIA/Precious/Dragic 반환 가족도 후보 입력으로 명시한다.
5. SAC 두deadline boolean/Metu 등록과 ORL 지정가드12분을 국소 보완한다. 이후25팀 함수는 각 팀 상태/변경 구간을 기준으로 batch화한다.

새 계약·중요 trade·#16 방향을 이 문서가 선택하지 않았다. 부족한 입력을 누락비용0/자동 원수락/원부상·승패로 채우지 않는다. 이미검문한S2 법적12·DET/NOP 원증인·WAS192 등은 새 사건이 없으면 다시검문하지 않는다.

## 4. 3번 원 종료조건

[현행 실행 의존성](MACRO3_CURRENT_EXECUTION_DEPENDENCIES_2026_10_07.md)과 [원 closeout](CHICAGO_2021_23_MACRO3_CLOSEOUT.md)의 다섯 행은 2021지명·자산 / Chicago여름 / DeRozan·Lonzo·Vucevic 파급 / 2022계약 / 2023후속이다. 계약·소속/권리·비용·분·결과·named 나비효과를 같은 경로로 연결해야 한다. 82규정시간 용량 준비만으로3번을 닫지 않으며 현실사적장부/접수전체나 정확미래전달을 새 필수조건으로 추가하지 않는다. 미선택중요방향은 해당 승격만 보류한다.

## 5. 출처·검문 범위

repository source SHA는BOMstrip·CRLF/CR→LF 정규화다. frozen NBA feed raw SHA는 3d9d7a6dd7ccd39ddfdd1799a26ef9901b44682d85a26f05239b468a8ae92e3a이며 raw bytes를 바꾸지 않았다. JSON의 `source_sha256`와 각 pointer는 실제읽은 현재원본을 가리킨다. 중앙 진행표/조건은 고정main snapshot을 기록해 root의 다음 중앙문서 갱신으로 소급변조하지 않는다. 정적 source/count 검문만 했고 생성기/constructor 음성검문을 새로 주장하지 않았다.

## 6. 7행 진행표 — 고정 기준시점

[현행 로드맵](WORLD_BIBLE_COMPLETION_ROADMAP.md)을 참고한다. 아래는 f90d3bc snapshot으로, 다음 main 현황을 대체하지 않는다.

| 번호 | 작업 | 상태 |
|---|---|---|
| 1 | 2020 드래프트 연쇄 | 완료. 기존 작가 선택·연쇄 보존 |
| 2 | Chicago 2020–21 | 완료(S2 유한 가상 실행). 정규1080·L2 6·playoff88/총1174경기·2348팀. 법적12/12·F5/5·A3/3·K4/4·시즌true. 전체 명단/슬롯 공백0·작업active12–15·벤치8·H00초기영구이탈2·승인거래8·origin/control60 검문. 실제 의료/금융/접수·미래권리 전달은 별도 미인증 |
| 3 | 2021–23 거래·계약 | 진행. M1/A 여름 완료·CHI–DET/NOP 동시시계·FY22 17명 한날짜 계약/비용 연결 검문. 중요방향·두시즌 미완료 |
| 4 | 주인공·라이벌 장기 커리어 | 17시즌 행동/비용·A09–A14 27인과후보 연결. H2·RC1·AW2·NM1 중요 결과·후속 정확 실행 미완료 |
| 5 | 결말·전체 구조 | 14막42소막·국소기능43/경로25/없는17/source53. A09두기능 조건부진입미선택·등록증분0. 전체G13 미완료 |
| 6 | 집필 규격·Context Pack | 독서110/110·S1 규격 완료·국소기능43·설계샘플2/실제Pack0·전체G13/G14 미완료 |
| 7 | 통합·독립 검수·작가 승인 | G15/G16/G17 전체 미완료. 국소 독립 검문을 전체G16/G17로 계산하지 않음 |

미완료 큰묶음5·6번까지4. v0.30 PARTIAL·설계/원고CLOSED·실제Pack0·원고0. 전체원장/중앙/Git변경0.

## Root 독립 검문

원 CSV82키/현재M1 두 상태, S2의29팀 seed object, DB1 상대 권리58개를 직접 대조했다. 원 feed1034행의 index·GroupSort·날짜·선수·팀·type를 실제 필드로 확인했고, 555/479행과499/404 source group을 별도로 재계수했다. 저장소14지문과 main 고정5스냅샷을 검문했다. 상대27함수·미래계약·날짜 가용성·승패가 생성되거나 인증된 것은 아니다.
