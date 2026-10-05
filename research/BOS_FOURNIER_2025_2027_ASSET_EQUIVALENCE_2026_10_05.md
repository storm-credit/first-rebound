# Boston Fournier 2025·2027 자산 동일성 — 한정 증인

2026-10-05 / 기준 main `b089d5f` / 판정 **SUPPORTING_ONLY**.
[수치·출처 지문 원장](BOS_FOURNIER_2025_2027_ASSET_EQUIVALENCE_2026_10_05.json).

## 확인 범위

[Boston Bane 거래 공지](https://www.nba.com/celtics/news/pressrelease/celtics-complete-three-team-trade-grizzlies-trail-blazers)는 MEM 자체2025 2R 취득을 확인한다. 승인된 Bane30 목적 거래는 `2020_DRAFT_RJ_HAMPTON_RELANDING_BOARD.md`에 유지된다. [Boston Fournier 공지](https://www.nba.com/celtics/news/pressrelease/celtics-acquire-evan-fournier)는 Teague와 미래2R 두 장의 실제 거래를 확인한다. [Orlando June10 구단 보유 기사](https://www.nba.com/magic/news/orlando-magic-have-great-opportunity-add-several-quality-players-through-draft-next-few-years-20210610)는 BOS/MEM2025 중 뒤2R와 BOS2027 2R의 원역사 거래 후 보유를 확인한다.

이번 작성은 기존 `NBA_2021_L_ASSET_CHAIN_SOURCES.json`의 직접 본문 회수 기록을 사용했다. 새 웹 회수나 비공개 원계약 검문은 수행하지 않았다. Boston 공지의 UTC11/21과 동부11/20 차이는 기존 기록대로 보존한다.

## 모든 순번 분기

최종 BOS 순번을 b, MEM 순번을 m이라 할 때 각각31~60이며 서로 다르다. 가능한 순서쌍870개 모두에서 Orlando 후보 자산은 `max(b,m)`, 보완 앞순번은 `min(b,m)`이다. 승수 동률이면 공식 추첨과 최종 순번 결정이 아직 미정인 입력이다. 최종 순번 자체의 동률 분기는 없다. 실제2025 순번·전달팀은 null이다.

BOS2027은 구단 보유 기사에 이름 붙은 자체2R이다. 실제 최종 순번은 null이다. 이 두 사실과 선택함수는 역사 자료로 지지된다. 실제2025 미래 전달 결과를 채택하지 않는다.

`NBA_2021_DRAFT_ASSETS.md`의 June Kemba 교환은 별도 조건부 후속안이다. 해당 안은 같은2025 쌍의 앞순번을 OKC에 보내며, March25 Fournier의 뒤순번을 다시 지출하지 않는다. June안을 March25 실행 의무로 소급하지 않는다.

## 두 asset branch를 아직 종료하지 않는 이유

S2는 모든 적용 입력의 닫힌 구간 또는 완전한 출처 기반 분기 증인을 요구한다. 현재 방향 승인은 Fournier Boston 이동과 Bane 목적 거래를 보존하지만 정확 픽 보호·우선권 조항을 승인하지 않았다. June 구단 보유 스냅샷과 March 실제 거래 발표를 합쳐도 **대체세계 March25의 전체 선행 의무·우선권이 동일하다**는 증인이 자동으로 생기지는 않는다. 검색에서 다른 Boston 거래가 발견되지 않았다는 사실은 그 동일성 인증이 아니다.

따라서 `2025_2R_ownership_priority`와 `2027_2R_ownership_priority`는 역사 자산 정체성·순번 함수에 대한 supporting witness이며 complete_domain=false다. 비공개 원계약 원문을 새 필수조건으로 만들지는 않는다. 관련 선행 의무와 우선권의 완전한 공개 연결, 또는 관련 법적 입력의 동일성을 독립적으로 입증하는 증인이면 충분하다. 동일성을 새 법적 가정으로 선언하는 것만으로는 선택된 S2를 충족하지 않는다.

이전 감사의 “한정 종료 가능”은 자산 정체성과 모든 순번 분기 함수까지였다. register의 두 branch 명칭은 ownership/priority 전체를 포함하므로 그 완료와 동일하지 않다. 이 범위 차이를 이번 실제 산출물에 명시했다.

당일TPE capacity/charge·Boston 전체비용은 HOLD, 새 작가선택0·미래 전달선택null·법적행승격0이다. 원고는 CLOSED다.
