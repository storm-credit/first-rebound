# O-15G15AE — Detroit 8월 15인 관측과 9월 Nets 거래의 자리 비용

- 시작점: `main` `8aa6bb8`, [G15AD](O15G15AD_PLUMLEE_OLYNYK_CAP_AND_DATE_BRIDGE.md)의 P0-B 동시 보유 비용. 판정: `AUGUST_RELATIVE_SLOT_STRESS / SEPTEMBER_TRADE_NOT_PORTABLE / OPENING_ROSTER_HOLD`.
- `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`; `author_locked=false`, `season_selected=false`, `exact_execution_cleared=false`, `manuscript_allowed=false`. 신규 작가확정 0건.

## 1. 원역사 날짜별 관측

| 날짜 | 원자료가 말하는 사실 | 말하지 않는 것 |
|---|---|---|
| 2021-08-12 | [Detroit 구단 분석](https://www.nba.com/pistons/features/olynyk-deal-made-possible-stewarts-rapid-progress-opens-pistons-offense)은 **표준계약 15명**이고 Hamidou Diallo의 제한적 FA 문제가 아직 열렸다고 쓴다. Olynyk·Lyles·Cory Joseph·Frank Jackson의 합류/재계약, Isaiah Livers 표준계약도 언급한다. | 이 기사 한 건은 15명 전원 명부·선수별 급여, 대체세계 15명, 10월 개막 명단을 제공하지 않는다. 8월 관측 15를 그날의 대체세계 절대 상한·완성 명단으로 쓰지 않는다. |
| 2021-08-18 | [Detroit 후속 문답](https://www.nba.com/pistons/chatmailbox/pistons-mailbag-august-18-2021)은 여전히 표준계약 15명, Diallo 향후 서명 시 자리 처리가 필요하다고 설명한다. Garza/Chris Smith 투웨이와 Pickett 캠프 계약은 표준계약과 구별한다. | 실제 Diallo 서명·방출/거래의 날짜와 대체세계 상대를 확정하지 않는다. |
| 2021-09-04 | [Brooklyn 구단 공식 발표](https://www.nba.com/nets/news/2021/09/04/brooklyn-nets-complete-trade-detroit-pistons): Detroit는 **Doumbouya+Okafor**를 보내고 **DeAndre Jordan+2022/2024(WAS)/2025(GSW)/2027 2R 네 장+현금**을 받았다. 선수계약 수는 거래 순간 2→1이다. | 대체세계의 Doumbouya/Okafor 보유·Brooklyn 수락, 네 픽·현금 조건, Jordan 보장급여·후속 방출이 자동 성립하지 않는다. |
| 2021-09 후속 | [NBA 선수 이동 원장](https://www.nba.com/news/nba-player-movement-2021)은 원역사 Detroit가 Jordan을 방출했다고 기재한다. [NBA 보도](https://www.nba.com/news/deandre-jordan-signs-with-lakers-after-buyout-trade)는 9/9 Lakers 계약을 기록한다. | 거래 2→1을 개막 때까지 `−1`로만 세거나, Jordan 방출의 팀 급여 비용을 0으로 간주하지 않는다. 방출일·보호급여·set-off는 별도 원장 필요. |

## 2. P0-B에서의 최소 자리 스트레스 — 조건부 산술

[2020 작가확정](../canon/PROJECT_FREEZE.md)은 원역사 Detroit의 Hayes/Bey 대신 Patrick7·Kira16을 둔다. [미선택 DB1](../simulation/NBA_2021_FULL_DRAFT_COMPARISON.md)은 원역사 Detroit Cade 대신 Suggs5와 Detroit37 Aldama 권리를 제안한다. **8/12 원역사 표준 15명이 Hayes·Bey·Cade를 포함하고, 나머지 서명/보유 사건이 모두 동일하며, Patrick·Kira·Suggs가 각각 표준계약으로 치환되고, Plumlee와 Olynyk을 동시에 보유한다**는 시험에서만 아래 산술을 사용한다. 출발 15명에는 Plumlee가 없다. 그는 [8/6 Charlotte 거래](https://www.nba.com/hornets/press-releases/charlotte-hornets-acquire-mason-plumlee-and-draft-rights-jt-thor)로 Detroit를 떠났다.

`원역사 15 − (Hayes, Bey, Cade 3) + (Patrick, Kira, Suggs 3) + (미거래 Plumlee 1) = 16명`.

이 `16`은 **8/12 대체 명단의 사실 또는 그날 규정 위반 판정이 아니다.** DB1 미선택, 실제 대체 서명/다른 거래 미확인, 훈련캠프와 정규시즌 등록 기준 차이 때문이다. Aldama 37번은 **지명권**일 뿐 서명 전 표준 자리를 차지하지 않는다. 이 시험에서 Aldama까지 표준계약으로 서명하면 `17`, Olynyk 미취득 P0-A라면 동일 가정에서 `15`가 되지만, 그 역시 후속 사건 없는 계산이다. 따라서 이 **8/12 가정 명단**을 10월 개막 15인에 연결하려면 적어도 하나의 이름 있는 표준계약 이탈 또는 다른 구성 변경을 날짜별로 보여야 한다. 원역사의 9월 이동이 대체세계에서 그대로 성립하는지는 별도다. 실제 대체 명단을 먼저 재구성하면 이 최소치도 달라질 수 있다.

9월 원역사 Nets 거래와 Jordan 후속 방출은 표면상 선수 자리 2개를 비우는 순서지만, **Doumbouya·Okafor의 대체 보유, Brooklyn의 대체 2R/현금 제안 수락, Jordan의 2021–22 보장급여와 buyout**을 증명해야 P0-B의 비용에 넣을 수 있다. 그 거래가 성립해도 당시 다른 신규 서명·Diallo·Aldama의 자리와 cap room, Olynyk 영입의 **8월 선행 비용**은 별도다. 9월 거래를 8/6 Olynyk의 소급 자금원으로 쓰지 않는다.

## 3. 지위와 다음 확인

| 지위 | 내용 |
|---|---|
| 사실 | 원역사 8/12·8/18 표준 15명 관측과 Diallo 미해결, 9/4 Nets 거래 자산 방향, 원역사 Jordan 후속 방출. |
| 추론 | 같은 8월 명단을 유지하는 P0-B는 Plumlee 한 명의 자리와 급여를 추가로 처리해야 한다. 9월 원역사 선수 이동만으로 8월 cap 경로가 소급 해결되지 않는다. |
| 후보 | 16/17/15 산술은 엄격한 `same-other-events` 시험이며 대체 역사 명단·계약 사실이 아니다. Nets 거래의 대체 실행도 HOLD. |
| 작가확정 | 이번 0건. 대체 8/12·10/20·1/23 명단, Aldama 계약, Olynyk/Plumlee 동시 보유, Nets 거래와 Jordan 처리 모두 HOLD. |

다음은 8/12 원역사 15명 **이름 전체**와 각 대체 선수 서명·방출·픽 권리 사건을 채워 10/20 표준 15인까지 연결하고, Olynyk 8/6 취득 자금과 Nets 9월 거래의 보장급여를 분리하는 것이다. G14 Detroit `PRIOR_HOLD`·Orlando `ROLE_HOLD`, Chicago 2020–21 정확 시즌, G16/G17은 미완료다. 7개 매크로 게이트는 1완료·1진행·5대기, 진행 중 포함 6개가 남는다.

[도구별 근거·제한 맹점 기록](../reviews/R01_O15G15AE_ROSTER_CLI_AND_SOURCE_BLIND.md)을 참조한다.
