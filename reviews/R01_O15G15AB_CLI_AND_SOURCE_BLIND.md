# R01 — G15AB 원역사 박스·CLI·제한 맹점 검수

- 대상: [G15AB](../research/O15G15AB_DETROIT_JAN23_ORIGINAL_BOX_AND_BRANCH_BOUNDARY.md), 시작 `main` `1adeb18`. 이번 검토는 G16 독립 PASS가 아니다.
- **Codex 직접 조사:** NBA 공식 [DET@DEN 박스](https://www.nba.com/game/det-vs-den-0022100707/box-score)의 페이지 내장 `__NEXT_DATA__.props.pageProps.game.awayTeam`에서 선수 13행·팀 합계 추출. [고정 JSON](../simulation/NBA_2022_01_23_DET_ORIGINAL_BOX.json)은 원역사 관측만 저장하고 [검증기](../tools/check_o15g15ab_detroit_box.py)는 10양수+3DNP·240:00/75 FGA/19 FTA/111점/22 TOV 및 두 제거 분기를 계산한다. HTML 내장 행과 보이는 NBA 박스의 Bey/Hayes/Cade 행을 대조했다.
- **NotebookLM CLI:** 기존 공식 [19:30 ET 부상 보고](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2022-01-23_07PM.pdf) 출처 `c8189748-40fd-473a-afcc-f7cc35b396dd` 한정 질의에서 Hayes Available, Garza/Grant/Frank Jackson/Livers/Olynyk/Chris Smith Out을 확인했다. 보고서에 없는 선수의 건강·대체 계약은 답하지 않았다. 같은 PDF의 재질의는 독립 출처 추가가 아니다.
- **Antigravity CLI:** 공식 박스의 Joseph/Stewart/Stanley 분을 직접 읽도록 `read_url_content`/`view_file`만 요청했으나 40초 `print timeout`, `num_turns=0`, 최종 본문 0건이었다. `status=SUCCESS`를 원자료 판독 성공으로 읽지 않는다. 이번 AG Evidence Pack은 0건이다.
- **Claude CLI 제한 source-blind:** 도구 없이 사실 요약만 제공했다. Plumlee 2021 거래 선택 및 Grant/Olynyk 당일 의료·대체역사 이월 문제를 지적한 것은 **유효한 미해결 게이트**다. `55:24`와 그것을 포함하는 `91:38`을 다시 더해 `295:24`라고 한 이중계산은 **기각**하고 중첩 관계를 본문에 명시했다. 원역사 Kira NOP13과 정본 Hayes NOP13을 동시에 같은 세계에 넣어 충돌이라고 한 것은 **기각**한다. 원역사 Plumlee 거래와 Grant/Olynyk 결장을 대체세계 확정 사실로 취급한 부분도 기각한다.

**결과물 단독 맹점:** 원역사 나머지 7명은 '분 강제 이탈 대상이 아닌 관측 행'이지 대체세계 잔류·건강이 확인된 7명이 아니다. G14 10/20 조합과 1/23 공식 관측은 상대·날짜가 달라 포제션·출전시간을 직접 이월할 수 없다. 결정권은 기존 정본·G16/G17에 남긴다. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`.
