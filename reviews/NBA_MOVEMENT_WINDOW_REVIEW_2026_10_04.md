# NBA 거래 데이터 구간 검수 — 2026-10-04

기준 main `0a6bfca`, 대상 [연구](../research/NBA_MOVEMENT_WINDOW_EVIDENCE_2026_10_04.md) / [원행·대조 JSON](../research/NBA_MOVEMENT_WINDOW_EVIDENCE_2026_10_04.json) / [재현기](../tools/build_nba_movement_window_evidence.py).

## 원자료·새 증거

NBA 공식 거래 페이지의 소비 코드에서 직접 관측한 공식 JSON URL을 회수했다. full snapshot9,927행/4,196,976bytes를 읽고 지문을 대조했다. 최신500행 UI로 축소하지 않았다. 공식 새 원자료는 이 feed1개이며 소비 JS3개와 모델 재분석을 독립 자료3~5개로 부풀리지 않는다.

Chicago2일 전체리그Trade61행18그룹에서 상대팀 송출 행까지 읽었으며 관련5행4그룹/송출player-linked후보0이다. Young서명만으로 Summer를 제외하지 않으며, 추가 Harrison/Lemon방출에서 잔급0을 추정하지 않는다. 법적 TPE origin 수는 null이다.

Orlando53일 창의28행18그룹을 기존 구단 가이드와 대조했다. 후반15행 중11건 일치, 해제3건은feed에없고 HallMay9 계약 문구1건이 다르다. guide-only를 삭제하거나 genericwaive의 계약종류 미표시를 계약 모순으로 세지 않았다. HallMay9 생략·4월계약유지는 작가 선택을 보존한다. 기존53일 명단과 원본35후반행은 수정0이며 동일 자리 수를 새 완료로 계수하지 않는다.

## 실제 도구 실행과 독립성

| 도구 | 회수 | 범위 |
|---|---|---|
| Codex 자료 조사 | 새 NBA공식feed와 JS 소비관계 회수; 부모 직접 파일/행·가이드 대조 | 공식 공개목록 증거이며 법적 전체 계약 인증 아님 |
| Antigravity | [회수 JSON](NBA_MOVEMENT_AG_2026_10_04.json),87.223초 exit0/최종응답UNVERIFIED | CLI실행·응답회수는 성공, 지정Hall행 원문검증 실패·새증거0 |
| NotebookLM | [file source 등록](NBA_MOVEMENT_NLM_SOURCE_2026_10_04.json) 성공 / [분석](NBA_MOVEMENT_NLM_2026_10_04.json)27.872초 exit0/analysis_success | 제공한 파생EvidencePack1출처만의 대조. 동일NBA자료 반복의독립근거 증가0 |
| 독립 Codex | `/root/independent_finish_scope` 읽기 전용 raw/코드/JSON·후속MD 검문 회수 | 실질결함 미발견, 전체S2/G16통과 아님 |
| Claude / 전체 source-blind | 이번 NOT_RUN | Claude 이전 SESSION_USAGE_LIMIT 이후 해제증거 없음. 전체독립검수로 확대하지 않음 |

NotebookLM은 누락3건·Hall문구충돌·필터링/시각/급여/대체세계 경계를 확인했다. ‘유용한 근거는 날짜/선수/동작에만 한정’ 표현은 공개 계약라벨 자체의 수집 가능성을 없애는 규칙으로 채택하지 않았다. 라벨은 출처 주장으로 보존하고 법적 분류는 별도 검증한다. PLAYER_ID의 양수 값을 계약형식 인증으로 승격하지 않는다.

## 검문

[5개 위험 검사](NBA_MOVEMENT_WINDOW_CHECKS_2026_10_04.json): 상대팀 송출 발견, draft consideration0ID 제외, 수취/송출 구분, 양수player권리 후보와 법적 증명 구분, 변경 snapshot거절. 변경은 추가LF바이트로 시험했고 원문 의무의 전수성 검사가 아니다. 저장 JSON `--check` 재현과가이드15행11/1/3을 확인했다. 독립자는 실제raw 지문·카운트/송출본문·누락/충돌 및 MD권한을 별도 대조했다.

동적feed는지문변경시재검문하고 frozen입력을자동승격하지 않는다. 기존가이드 원장SHA도보존해두자료의변경을구분한다. 신규코드는저장된입력필터/대조만담당하며승인경로나급여를생성하지않는다.

F3 조사에서 새 Charlotte/거래당사자 공식 후보는 필요한 conversion/priority 본문을 회수하지 못했다. 기존보호 문구를 새증거로 세지 않았고 Denver등록부·후손0변경이다.

S2정상검사 결과 법적12HOLD·F0/5 A0/3 K0/4·season_selected=false/manuscript_allowed=false. 최종회차0·실제Pack0·미완료6·v0.30 PARTIAL·설계/원고CLOSED·원고0. 전체마감 게이트를통과했다고보고하지않는다.
