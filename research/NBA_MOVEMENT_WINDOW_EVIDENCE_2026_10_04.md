# NBA 공식 거래 데이터 — Chicago 2019 / Orlando 2021 구간 대조

기준 main `0a6bfca` / 2026-10-04. **공식 공개 목록의 원자료 증인**, 전체 법적 실행 인증 아님. [재현 기록](NBA_MOVEMENT_WINDOW_EVIDENCE_2026_10_04.json) / [도구](../tools/build_nba_movement_window_evidence.py).

## 공식 원자료와 읽은 범위

[NBA 거래 페이지](https://www.nba.com/players/transactions)가 사용하는 [NBA Player Movement JSON](https://stats.nba.com/js/data/playermovement/NBA_Player_Movement.json)을 직접 회수했다. 4,196,976bytes·9,927행·2015-07-01~2026-10-02, SHA256 `3d9d7a6dd7ccd39ddfdd1799a26ef9901b44682d85a26f05239b468a8ae92e3a`.

페이지 chunk→80805 모듈→공유 앱의 fetch 함수→공식 JSON의 rows 연결을 직접 확인했다. JSON에 세 스크립트의 URL/byte/SHA와 짧은 관측 코드를 기록했다. UI는 최신500행만 표시하지만 이번 입력은 전체 JSON이다. 전체4MB는 임시 캐시, 이번 구간의 원행은 저장소 JSON에 남겼다. 이 동적 URL을 나중에 재조회해 다른 지문이 나오면 자동 대체하지 않고 재검문한다.

사실/추론/후보/작가확정은 아래 범위로 구분한다. 현재 NBA의 사후 공개 목록은 당시 계약서·정확 접수시각·모든 법적 의무와 같지 않다.

## Chicago — Young 전후 계약 송출 후보

**FACT:** 2019-07-06~07의 전체리그 Trade61행/18그룹을 읽었다. Chicago 관련5행/4그룹은 아래다. `TEAM_ID`는 수취팀이고 `Additional_Sort`가 상대팀인 거래 행이 있어, Chicago 팀 행만 필터하지 않았다.

| 날짜 | 선수/대가 | 공식 목록의 사건 |
|---|---|---|
| 7/6 | Thaddeus Young | 신규 Contract 서명 |
| 7/6 | Shaquille Harrison | 방출 |
| 7/6 | Walt Lemon Jr. | 방출 |
| 7/7 | Tomas Satoransky | Washington→Chicago 수취 |
| 7/7 | draft consideration | Chicago→Washington, PLAYER_ID0 |

이 두 날짜의 상대팀 행에서도 Chicago발 **player-linked 거래 송출 후보0**을 확인했다. 보존한 전체61행으로 재검문할 수 있다. 더 긴7/1~2020-11-18 공개 창도 Chicago 관련Trade는 위 Satoransky그룹2행뿐이다. 기존 가이드의 Young/Satoransky 날짜만으로 읽지 못했던 Harrison/Lemon 방출을 추가 원자료에 연결했다.

**추론:** [Young Y5](CHICAGO_2019_YOUNG_SIGNING_BOUNDARY.md)의 당시 신규TPE 발생 목록을 좁히는 실제 공개 증거다. **후보:** 승인 세계에서 다른 계약 송출이 없다는 연결과 당시 계약/산입 증인이 닫히면 해당 Y5에 사용한다. **작가확정:** 새0, 기존 방향 유지.

`PLAYER_ID>0`만으로 Standard 계약인지, 미서명 draft rights인지, 적법 TPE 발생인지 판정하지 않는다. 이번 결과의 legal_TPE_origin_count는 null이다. Contract 표시는 Summer를 구분하지 않으며, 어느 계약연도의 서명 당시 양수 보호든 Summer 배제에 유효할 수 있다. Harrison/Lemon 방출은 보장/상계/잔여 급여0을 뜻하지 않는다. date의 자정 값과 GroupSort 크기를 당일 접수 순서로 읽지 않는다. Y1–Y5·전체R의 법적 종료는 이번 미인증이다.

## Orlando — 53일 창과 가이드 누락/충돌

**FACT:** 2021-03-25~05-16의 Orlando 관련 전체그룹28행/18그룹을 회수했다. 3/25의 세 거래와 상대팀 수취 행까지 포함했다. 이것은 원역사 기록이고 Vučević/Aminu의 Chicago행·Hampton 수취를 대체세계에 되살리는 입력이 아니다.

기존 [구단 가이드 원행15개](D1_ORLANDO_CALENDAR_SOURCES_2026_10_02.json)의 4/12~5/16 구간과 해당팀의 feed12행을 날짜/PLAYER_ID/서명·해제에 따라 대조했다.

| 분류 | 개수 | 처리 |
|---|---:|---|
| 날짜·선수·동작 일치 | 11 | N번째 계약 표시는 가이드만의 근거; 방출행의 계약종류 미표시를 모순으로 세지 않음 |
| 가이드만의 해제 | 3 | 4/13 Cannady 일반계약, 4/27 Franks, 5/2 Hall 해제 보존 |
| 계약 문구 충돌 | 1 | 5/9 Hall: feed는10-Day, 가이드는잔여시즌. 차이를 숨기거나 원계약 확정으로 읽지 않음 |
| feed만의 추가 사건 | 0 | 이 대조 창/두 자료에 한정 |

**추론:** 공식 feed도 종료·해제 기록을 누락하거나 계약 라벨을 다르게 기재할 수 있다. 따라서 한 공식 목록의 absence를 사건 부재로 인증할 수 없다. 위3건은 정확히 이 대조에서 발견한 차이이며 feed의 모든 누락을 전수 발견했다는 주장이 아니다.

**작가확정 보존:** Hall5/9 신규 계약 생략은 그대로다. 4월 계약을 삭제하지 않으며, 5/9의 문구 충돌을 핑계로 새 계약을 복원하거나 급여·등록을 새로 계산하지 않는다. [기존 53일 증인](../simulation/ORLANDO_2021_DEADLINE_TO_FINAL_CALENDAR.json)의 모든 명단/35후반행도 변경하지 않았다. 기본명단·Birch 대체 방출·계약 자격/전체 차지·당일 순서는 여전히 별도 HOLD다.

## 검증과 다음 정확한 작업

[이번 검수](../reviews/NBA_MOVEMENT_WINDOW_REVIEW_2026_10_04.md)에 원자료·독립 반증·CLI 실행 범위를 기록한다. 재현기는 지정 full snapshot SHA가 바뀌면 거절하며 기존 가이드15행 전체를 대조한다. `--check`는 저장 JSON과 직접 재생성 결과가 같은지 검사할 뿐 계약/리그 승인 인증이 아니다.

다음은 새로 확인한 Harrison/Lemon의 방출 잔여 의무와 Young 당시 일반계약 분류, Orlando의 가이드-only 해제/기본명단·계약 자격을 연결하는 일이다. 같은53일 자리 수나 같은 TPE 여유를 새 검증으로 계수하지 않는다. 전체 법적12HOLD·F0/5 A0/3 K0/4·최종회차0·실제Pack0·미완료6·v0.30 PARTIAL·설계/원고CLOSED·원고0.
