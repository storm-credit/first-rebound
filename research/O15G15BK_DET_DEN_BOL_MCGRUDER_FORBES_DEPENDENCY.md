# O-15G15BK — 2022년 1월 Bol–McGruder 취소와 Forbes 거래의 선행 조건

- 선행: [Detroit 1/23 원역사 박스](O15G15AB_DETROIT_JAN23_ORIGINAL_BOX_AND_BRANCH_BOUNDARY.md), [Denver 1/23 자리 다리](O15G15BJ_DENVER_JAN23_ROSTER_SLOT_BRIDGE.md).
- 판정: `HISTORICAL_RESCISSION_VERIFIED / ALT_TRANSACTION_CHAIN_HOLD`. 이 문서는 거래 의존성을 찾은 것이며 대체 거래·경기 결과를 확정하지 않는다.
- [분기 원장](../simulation/O15G15BK_DET_DEN_JAN2022_TRADE_BRANCHES.json)과 [검사기](../tools/check_o15g15bk_trade_chain.py)는 선수 소유의 양립 가능성만 확인한다. 급여 매칭·픽 소유·의료·상대 동의 검사가 아니다.

## 원역사: 발표, 취소, 후속 거래

| 날짜 | 직접 근거 | 원역사에서 확인되는 범위 |
|---|---|---|
| 1/10 | [Detroit 구단 발표](https://www.nba.com/pistons/news/detroit_pistons_acquire_bol_bol) | Bol Bol을 Denver에서 받고 McGruder와 드래프트 대가를 보낸다고 **발표**. 최종적으로 유지된 거래라는 뜻이 아니다. 구단의 [당일 해설](https://www.nba.com/pistons/news/pistons-add-7-foot-2-bol-in-a-deal-too-good-to-pass-up/)은 2021년 Brooklyn 거래로 취득한 네 2라운드 픽 중 가치가 낮은 픽을 언급하나, 대체세계의 정확한 픽 소유·보호조건은 `HOLD`. |
| 1/13 | [Detroit 구단의 취소 기사](https://www.nba.com/pistons/news/trade-off-so-pistons-happy-to-welcome-mcgruder-back/), [NBA의 보도](https://www.nba.com/news/pistons-rescind-trade-nuggets-bol-bol) | 의료검사를 통과하지 못해 거래가 취소됐고 McGruder가 Detroit에 돌아왔다. Bol의 의료 불승인이 보도된 원역사 사유다. 1/10 발표를 최종 자산 이동으로 장부에 넣지 않는다. |
| 1/19 | [NBA 공식 거래 추적기](https://www.nba.com/news/2021-22-nba-trade-tracker) | Denver가 Forbes를 받고, Boston이 **Bol·Dozier**를, San Antonio가 Hernangómez·미래 2라운드 픽·현금을 받았다. 추적기는 Bol–McGruder 거래를 공식 완료 거래로 싣지 않는다. |
| 1/23 | [Detroit 구단 경기 기사](https://www.nba.com/pistons/news/pistons-push-nuggets-to-the-wire-but-come-up-short/), [원역사 박스](https://www.nba.com/game/det-vs-den-0022100707/box-score) | McGruder는 Denver행 예정이 취소된 뒤 Detroit 선수로 Denver전에 출전했다. `23:38 / 4 FGA / 6점`은 원역사 관측 행이다. |

## 대체세계의 두 조건부 분기

| 분기 | 1/10→1/13 조건 | 1/19 Forbes 원형 거래 | 1/23 명단·분 영향 |
|---|---|---|---|
| `R` — 취소 유지 | 해당 의료·거래 취소가 대체세계에도 유지된다고 **가정**. Bol은 Denver에, McGruder는 Detroit에 남는다. | Bol을 Boston으로 보낼 선행 소유 조건은 충족할 수 있다. Dozier·미래 픽·현금·급여·상대 동의는 여전히 별도 `HOLD`. | G15BJ의 Forbes 포함 15+2와 G15BI의 Forbes20분은 **다른 조건도 충족될 때만** 유효. Detroit G15AB의 McGruder 행도 계약/활동/역할과 새 공격 기회가 필요하며 원역사 수치를 이식하지 않는다. |
| `C` — 거래 완료 가정 | Bol이 대체 Detroit에, McGruder가 대체 Denver에 간다는 **반사실 후보**. 실제 Bol 의료 결과를 뒤집는 이유와 양쪽 거래 성립·드래프트 대가가 필요하다. | Denver가 Bol을 이미 보냈다면 **동일한 원형 거래로 Bol을 Boston에 또 보낼 수 없다**. 원형 1/19 거래만 `BLOCKED`; 다른 선수/자산, 상대 수락, 급여/CBA를 갖춘 **새 거래를 통한 Forbes 취득 가능성**은 미검증 `HOLD`. | McGruder의 Detroit 원역사 행은 제거하고 Denver에서도 그 관측 분을 재사용하지 않는다. 검증된 대체 Forbes 거래가 없다면 G15BI의 Forbes20분과 G15BJ의 원역사 15+2 한 자리 교체 가정은 재작성 필요. Bol의 Detroit 1/23 출전/건강/분도 0건 확정. |

두 분기는 원역사 관측과 대체세계 가정을 분리하기 위한 비교다. `R`은 **후속 거래의 가능 경로**, `C`는 **현재 보드와 충돌하는 경로**이며 어느 것도 작가확정이 아니다. [G15AF](O15G15AF_DETROIT_NAMED_ROSTER_TO_OPENING_GATE.md)는 원역사 2021-09-04 Brooklyn 거래가 Detroit에 2라운드 픽 네 장을 보냈지만 대체 실행은 `HOLD`라고 기록한다. 따라서 `C`에서 1/10 드래프트 대가를 지급하려면 **그 거래의 대체 실행 또는 다른 실명 픽 소유**를 먼저 증명해야 한다. 2020 지명 변경, 2021 Gordon A 정확 실행, Detroit P0-B의 Plumlee/급여/16인 자리 문제도 독립적으로 남는다. 의료 결과를 단순히 다른 세계라서 바꾸거나, 원역사에서 취소된 거래의 대가를 지급했다고 기록하지 않는다.

| 구분 | 이번 판정 |
|---|---|
| 사실 | 원역사의 1/10 발표·1/13 취소, 1/19 공식 Forbes 거래의 Bol/Dozier 이동, 1/23 McGruder 원역사 출전. |
| 추론 | 원형 Forbes 거래에는 Denver의 1/19 Bol 보유가 선행한다. Bol을 Detroit에 실제로 보낸 분기와 원형 Forbes 거래는 양립하지 않는다. |
| 후보 | `R`의 취소 유지와 후속 거래 재검증, 또는 `C`의 의료·자산·대체 거래 재설계. |
| 작가확정 | 이번 0건. Bol–McGruder 대체세계 결과, Forbes 취득, 1/23 양 팀 명단/분/득점, 장기 커리어 `HOLD`. |

다음은 `R`에서 Detroit의 **1/23 McGruder 재서명·당일 활동과 2021 P0-B 16인 정리**, Denver의 Forbes/Dozier 거래 조건을 날짜별로 연결한다. `C`는 작가 선택 이전에 대체 거래와 의료·픽 비용을 제시해야 한다. Chicago D1 F1–F5 `0/5`·A1–A3 `0/3`·K `0/4`, G14 DET/ORL 및 G16/G17은 그대로다. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`; 7묶음 1완료·1진행·5대기, 진행 중 포함 남은 6묶음.
