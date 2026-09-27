# O-15F14-AT — K1/L2 조건부 플레이오프 대진 연결

- 판정: `K1_L2_BRACKET_REPRODUCED / SERIES_EXECUTION_HOLD`.
- 원입력: [K1 전체 리그 F038](NBA_2020_21_FULL_SEASON.json)의 동·서부 정규시즌 시드와 [L2 플레이인](CHICAGO_2020_21_EXECUTION_CLOSEOUT.json)의 세 경기씩. [재현 JSON](CHICAGO_2020_21_K1_L2_BRACKET.json)은 [도구](../tools/build_chicago_2020_21_k1_l2_bracket.py)로 두 원입력에서 생성한다.
- NBA 규칙: [2021 플레이인 설명](https://www.nba.com/news/2021-nba-play-in-tournament-schedule)에서 7/8전 승자가 7번, 최종전 승자가 8번 시드를 얻는다. [NBA 첫 라운드 일정](https://www.nba.com/news/2021-nba-playoffs-first-round-schedule)에서 1–8, 2–7, 3–6, 4–5 짝을 대조한다. 규칙만 적용하며 원역사 시리즈 결과는 이 세계에 이월하지 않는다.

## 입력과 산출

| 구분 | F038 정규시즌 1~10위 | L2 진출 | K1+L2 첫 라운드 |
|---|---|---|---|
| 동부 | PHI, BKN, MIL, NYK, ATL, MIA, BOS, IND, WAS, CHI | BOS 7번, IND 8번 | PHI–IND, BKN–BOS, MIL–MIA, NYK–ATL |
| 서부 | UTA, PHX, DEN, LAC, DAL, LAL, POR, GSW, MEM, SAS | POR 7번, MEM 8번 | UTA–MEM, PHX–POR, **DEN–LAL**, LAC–DAL |

**사실/재현:** 위 시드와 플레이인 승자는 저장소의 *조건부* F038·L2 입력이다. 두 자료는 각각 `selected=false`이고 L2는 추천안이다. 2021 NBA 대진 규칙에 따르면 이 조합에서 Denver 3번의 첫 상대는 Lakers 6번이다. Portland는 7번이므로 Phoenix 2번의 첫 상대다. 재현 도구는 플레이인 참가 순서, 승자의 적법성, 최종 7·8번, 16팀 구성과 Denver–Lakers 대진을 검사한다.

**기존 연구의 적용 범위:** [원역사 Denver 10경기](../research/O15F14Z_DENVER_2021_PLAYOFF_NONTRADE_SCREEN.md)의 Portland 6경기→Phoenix 4경기, McGee `33:49`·Nnaji `17:39`, [조건부 18구간 명단 치환](../research/O15F14AO_DENVER_NNAJI_OTHER_PLAYOFF_STINTS.md)은 실제 역사 비교 및 동일 대진을 가정한 민감도 시험이다. **K1+L2 Denver 플레이오프의 출전분·상대·Jokić 6/13 퇴장·시리즈 결과 증인이 아니다.** 원역사 사실과 계산은 삭제하지 않는다. 다른 시즌/플레이인 분기를 택하면 대진을 그 분기에서 다시 산출한다.

**추론:** K1+L2에서 Denver가 Lakers를 이겨야 2라운드에 오른다. 그때 Phoenix가 Portland를 이기면 Denver–Phoenix, Portland가 Phoenix를 이기면 Denver–Portland가 **2라운드**에 가능하다. Denver의 선행 Lakers 시리즈와 상대편 Phoenix–Portland 시리즈의 승자·경기 수·날짜가 미선택이므로 원역사 Denver–Portland **1라운드** 6경기나 6/7~13 Denver–Phoenix 경기책을 같은 날짜·분·득점의 대체 경기로 승격할 수 없다. 원역사 Lakers–Phoenix 1라운드도 이 조합에서는 다른 대진이므로 서부 전체의 일정·부상·후속 계약 시점에 나비효과가 생긴다.

**다음 F5 검문:** Denver–Lakers 1라운드의 후보 경기별 건강·등록·실명 로테이션/5인조·분·포제션/승패를 구성하고, Phoenix–Portland와 Utah–Memphis 등 상대 경로의 결과를 조건부로 연결한다. Denver의 McGee 거래 생략 및 Nnaji 이탈, Bey/Hartenstein 잔류는 이미 승인된 방향이므로 그대로 입력한다. Cleveland의 Varejão C1/C2 선택과 팀 비용도 별도 열린 입력이다. 원역사 10경기 이름 치환을 K1+L2 분 원장으로 복사하지 않는다.

**게이트:** F5·A1/A3·K_METHOD_EVENTS는 `HOLD`; F1~F5 `0/5`, A1~A3 최종 채택 `0/3`, 네 K 종료 `0/4`. 작가의 K1/L2 최종 시즌·플레이오프 결과 확정은 0건. 7개 매크로 중 1완료·1진행·5대기, 미완료 6개. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, 원고 금지.

[Claude 제한 반증 기록](../reviews/R01_O15F14AT_BRACKET_CLAUDE_SCOPE.md)은 1라운드 짝을 재확인했으나 2라운드 Denver–Portland 가능성을 놓친 문장을 기각했다. 새 NBA 원자료로 세지 않는다.
