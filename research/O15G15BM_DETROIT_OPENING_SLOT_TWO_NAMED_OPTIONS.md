# O-15G15BM — P0-B 개막 초과 한 자리의 두 실명 경로

- 선행: [G15AF 원역사/대체 명단](O15G15AF_DETROIT_NAMED_ROSTER_TO_OPENING_GATE.md)의 `16`, [G15AH 개막 0분 후보](O15G15AH_DETROIT_AUG6_CAP_AND_OPENING_SLOT_SCREEN.md), [G15BL 1월 별도 계약](O15G15BL_DETROIT_JAN23_STANLEY_CONTRACT_AND_HARDSHIP_GATE.md).
- 판정: `TWO_NAMED_SLOT_WITNESSES / CONTRACT_CAP_50_GAME_AND_BUTTERFLY_HOLD`. 두 경로는 **자리 수만** 15+2가 되는 후보이며 어느 쪽도 실행·작가확정이 아니다. [입력 JSON](../simulation/O15G15BM_DETROIT_OPENING_SLOT_OPTIONS.json)과 [집합 검사기](../tools/check_o15g15bm_detroit_slot_options.py)는 G15AF 실명 기준을 재사용한다.
- `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, 신규 작가확정 0건.

## 원역사와 적용 규칙

[Detroit 2021-08-17 발표](https://www.nba.com/pistons/news/detroit-pistons-sign-luka-garza-and-chris-smith-two-way-contracts)는 **Garza와 Chris Smith가 투웨이**였다고 밝힌다. [8/18 구단 문답](https://www.nba.com/pistons/chatmailbox/pistons-mailbag-august-18-2021)은 이 두 자리가 차서 Pickett에게 세 번째 투웨이를 줄 수 없고, Pickett은 Exhibit 10으로 캠프·Motor City Cruise 경로를 갖지만 **다른 NBA 팀이 계약할 수 있다**고 설명한다. [9/29 구단 문답](https://www.nba.com/pistons/chatmailbox/pistons-mailbag-september-29-2021)은 원역사 Nets/Jordan 처리 뒤 Garza를 표준계약으로 올리고 Pickett을 빈 투웨이에 넣었다고 설명한다. 이는 P0-B에서도 그 순서·상대 거래가 성립했다는 증거가 아니다.

[NBA의 2021-07-27 공식 2021–22 규칙 발표](https://pr.nba.com/nba-board-of-governors-play-in-roster-rules-2021-22-season/)는 동시 계약 상한 **표준 15+투웨이 2**, 투웨이 선수의 정규시즌 **활동 명단 최대 50경기**, 투웨이 급여 **0년차 최소급의 50%**를 밝힌다. 활동 명단은 실제 출전 경기보다 넓다. [Detroit의 Garza 시즌 회고](https://www.nba.com/pistons/news/2021-22-rewind-pistons-rookie-garza-works-to-find-his-way-in-modern-nba)의 원역사 **32경기 출전**은 대체 Garza가 투웨이로 50경기 상한을 지킬 수 있다는 증명이 아니다.

[Detroit의 2021-08-06 발표](https://www.nba.com/pistons/features/detroit-pistons-sign-free-agents-kelly-olynyk-trey-lyles-and-restricted-free-agent-saben)는 Olynyk·Lyles·Lee가 함께 **서명됐다고 공개**하되, 정확 금액·리그 통지 순서는 밝히지 않는다. [G15AO](O15G15AO_DETROIT_DISCLOSED_AGREEMENT_CAP_TIMING.md)는 Lyles 합의가 Olynyk보다 먼저 리그에 통지됐다면 예상 급여도 캡에 들어갈 수 있음을 이미 기록했다. Lyles를 빼는 후보는 **합의 자체를 안 하는 반사실 사건**부터 명시해야 하며, 10월 단순 방출을 8월 캡룸으로 소급하지 않는다.

## 조건부 개막 자리 비교

공통 출발은 G15AF의 `P0-B same-other-events`: 정본 Patrick7·Kira16, **미선택 DB1 Suggs5**, Plumlee 잔류, 그 외 원역사 서명·9/4 Nets 거래·Jordan 방출이 모두 가능하다고 **가정**한 2021-10-20 표준 **16명**이다. 원역사 Pickett·Smith 투웨이까지 동일하게 놓으면 **16 표준+2 투웨이**여서 규정 상한을 넘는다. G14 조건부 240분에 등장하는 10명은 `Kira/Joseph/Suggs/Josh Jackson/Diallo/Patrick/Grant/Olynyk/Stewart/Plumlee`이며, Garza·Lyles·Pickett·Smith는 그 10명에 없다. 어느 후보도 G14 10명을 **직접** 제거하지 않는다. 이 출발 자체의 8/6 cap, Nets/Charlotte 상대 수락과 2021 드래프트 자산은 모두 **아직 해소되지 않은 선행 HOLD**다. 아래 15+2는 이 HOLD들을 통과했다고 가정하는 *자리 산술의 필요조건*일 뿐 실제 적법 명단 판정이 아니다.

| 후보 | 바꾸는 실명 사건 | 개막 자리의 **조건부 산술** | 실제 비용·남은 증거 |
|---|---|---|---|
| `A` Garza 투웨이 유지 | 원역사 **9/24 Garza→표준 전환을 실행하지 않는다**. 8/17 Garza·Smith 투웨이를 유지한다. | 표준 `16−Garza=15`; 투웨이 `Garza+Smith=2`. Pickett은 원역사 9월 투웨이가 아닌 Exhibit 10/Cruise **후보**. | Pickett은 타 팀 표준/투웨이 제안에 노출되고 원역사 Detroit 1/23 DNP 행도 보존할 수 없다. Garza의 대체 시즌 활동 명단 **50경기 누적**, 실제 계약 변경 허용·급여, 장기 육성 및 추후 표준 전환 자리가 필요하다. 50경기에 닿으면 **추가 활동 명단 배치를 멈추거나** 새 표준 자리를 마련해 전환해야 한다. 원역사 1/23 Garza `Out`를 대체 건강으로 복사하지 않는다. 8/6 Olynyk cap 문제는 그대로다. |
| `B` Lyles 미계약 | 원역사 **8/6 Lyles 서명/그보다 앞선 합의 통지 자체를 하지 않는다**. 다른 G15AF 사건과 Garza 표준 전환은 비교 조건으로 유지한다. | 표준 `16−Lyles=15`; 투웨이 `Pickett+Smith=2`라는 **원역사 후속 사건 유지 가정**. | Lyles의 다른 팀 착지·계약·그 팀 분은 미정. [1/23 Detroit 구단 기사](https://www.nba.com/pistons/news/pistons-push-nuggets-to-the-wire-but-come-up-short/)의 원역사 Lyles **센터 교대**와 `21:18/11 FGA/18점` 행을 제거하고 Plumlee 등에게 새 역할·공격 기회 비용을 배분해야 한다. [NBA 공식 2022-02-10 거래 추적기](https://www.nba.com/news/2021-22-nba-trade-tracker)의 **Lyles·Josh Jackson→Sacramento / Bagley→Detroit** 원형 거래도 Lyles 부재로 재설계한다. Lyles 미합의는 G15AO의 통지 급여 한 항목을 없앨 수 있는 **조건부 방향**일 뿐, 전체 8/6 Team Salary·Olynyk 계약 통과가 아니다. |

`A`는 G14 10명과 원역사 1/23 Lyles 역할을 직접 제거하지 않아 **다음 세부 검증의 우선 후보**다. 우선순위는 작가확정이나 전체 법적 가능성 순위가 아니다. Pickett 권리·50활동경기·Garza 계약 변경 시점의 막힘이 크면 `B`와 다시 비교한다. `B`는 8월 캡에 유리할 **수 있는** 방향이나 1월 센터 분·2월 Bagley 거래에 직접 파급하므로 단순 절약안으로 취급하지 않는다. 둘 다 Plumlee의 Charlotte 거래 미실행, Olynyk cap, 9/4 Nets 거래 수락과 DB1 선택을 해결하지 않는다. 이 공통 선행 조건이 닫히지 않으면 어느 후보도 실행 판정으로 승격하지 않는다.

| 구분 | 이번 판정 |
|---|---|
| 사실 | 원역사 Garza·Smith 투웨이, Pickett Exhibit 10→투웨이의 구단 설명, 2021–22 NBA 15+2/투웨이 50활동경기 규칙, Lyles 8/6 서명 및 1/23·2/10 역사 사건. |
| 추론 | 다른 사건을 고정하면 `A`와 `B` 각각 하나의 실명 표준 자리를 뺀 산술 결과는 15+2다. 32 **출전**과 50 **활동**은 다른 계수다. |
| 후보 | `A`를 다음 검증 우선, `B`를 계약·장기 거래 파급 비교안으로 보존. 실명 수신 팀·계약 금액과 모든 대체 승패는 `HOLD`. |
| 작가확정 | 이번 0건. `A/B` 어느 선수 이탈·팀 착지·급여·의료·2021 DB1도 선택하지 않았다. |

다음은 `A`의 **Garza 2021–22 날짜별 활동 명단 50경기**와 Pickett의 Exhibit 10/Cruise 권리·타 팀 위험을 검산하고, `B`는 Lyles의 가능한 착지와 1/23 앞코트·2/10 거래 재설계의 실명 비용을 채운다. Chicago D1 F1–F5 `0/5`·A1–A3 `0/3`·K `0/4`, G14 DET/ORL 및 G16/G17은 그대로다. 7묶음 1완료·1진행·5대기, 진행 중 포함 남은 6묶음.

[G15BN](O15G15BN_DETROIT_GARZA_TWO_WAY_50_GAME_ENVELOPE.md)은 `A`의 실제 경기 날짜 82개에 50활동경기 상한을 겹쳐 가장 빠른 소진일과 필요한 비활동 경기 수를 계산했다. 활동/비활동의 실제·대체 경기별 원장은 아직 없으므로 후보의 적법성 PASS가 아니다.
