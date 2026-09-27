# O-15G15BO — Garza 투웨이 A의 2/10 거래 이후 표준 자리

- 선행: [G15BM A/B](O15G15BM_DETROIT_OPENING_SLOT_TWO_NAMED_OPTIONS.md), [G15BN 50경기 외피](O15G15BN_DETROIT_GARZA_TWO_WAY_50_GAME_ENVELOPE.md), [G15BK Bol–McGruder 분기](O15G15BK_DET_DEN_BOL_MCGRUDER_FORBES_DEPENDENCY.md).
- 판정: `POST_TRADE_SLOT_WITNESS / TRADE_ASSETS_CONVERSION_AND_PICKETT_HOLD`. [조건부 집합](../simulation/O15G15BO_DETROIT_GARZA_BAGLEY_SLOT_BRIDGE.json)을 [검사기](../tools/check_o15g15bo_detroit_garza_bagley_bridge.py)로 재계산했을 뿐 거래·계약 실행이나 작가확정이 아니다.
- `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED` 유지.

## 날짜가 있는 원역사 증거

| 사건 | 근거 | 대체세계 적용 경계 |
|---|---|
| 2021-08-18 Pickett의 Exhibit 10/Cruise 경로 | [Detroit 구단 문답](https://www.nba.com/pistons/chatmailbox/pistons-mailbag-august-18-2021)은 당시 Garza·Chris Smith가 두 투웨이 자리를 차지했고, 다른 NBA 팀이 Pickett에게 표준 또는 투웨이 계약을 제안할 수 있다고 명시한다. | 후보 A에서 Garza를 투웨이에 계속 두면 Pickett의 **Detroit 투웨이 계약은 자동으로 따라오지 않는다**. Cruise행도 본인의 선택·다른 팀 미계약이 필요하다. |
| 2021-10-25 Cruise 명단 | [Motor City Cruise의 실제 캠프 명단](https://detroit.gleague.nba.com/news/motor-city-cruise-announce-2021-22-training-camp-roster)은 Pickett·Smith가 원역사 **투웨이**라고 표기한다. | 원역사 명단을 후보 A의 Cruise 선수 자격·NBA 권리로 복사하지 않는다. 후보 A의 투웨이는 Garza·Smith다. |
| 2022-02-10 Bagley 4팀 거래 | [Detroit 공식 완료 발표](https://www.nba.com/pistons/news/acquire_marvin_bagley-iii/)와 [NBA 거래 원장](https://www.nba.com/news/2021-22-nba-trade-tracker)은 Detroit가 **Lyles·Josh Jackson을 보내고 Bagley를 받음**을 확인한다. Detroit는 픽 대가도 냈다. | Sacramento·Milwaukee·Clippers 동의, 2023/24 등 픽 원소유/보호, 선수 계약·급여 매칭과 앞선 나비효과가 모두 `HOLD`다. Lyles 없는 후보 B에는 원형 거래를 적용할 수 없다. |
| 2/10 경기 중 거래 완료 | [Detroit의 Memphis전 기사](https://www.nba.com/pistons/news/surging-memphis-d-tough-to-crack-for-pistons/)는 리그 검토를 거쳐 **3쿼터 도중** 거래가 공식화됐다고 적는다. | 그 경기 **시작 전부터** 한 자리가 비었다고 계산하지 않는다. 첫 경기 이후 명단 시험 날짜는 2/11 Charlotte전이다. Bagley의 2/11 출전은 [구단 기사](https://www.nba.com/pistons/news/hornets-put-on-a-scoring-clinic-to-top-pistons/)상 이적 후 신체검사·이동 때문에 불가했으나 계약 자리와 활동/출전은 별개의 계수다. |
| 투웨이→표준 전환 | [2022-04 Brooklyn 공식 NBA 기사](https://www.nba.com/news/nets-sign-kessler-edwards-to-contract-before-playoffs)는 James Johnson을 방출해 **빈 표준 자리**를 만든 뒤 Edwards의 투웨이 계약에 표준 전환 옵션을 행사한 실제 예를 든다. | Garza에게도 같은 계약 옵션·적용 금액·리그 접수 시점이 있다는 **개별 증거는 아직 없다**. 거래 뒤 빈 자리 하나는 필요한 명단 조건일 뿐 전환 계약 PASS가 아니다. |

## 후보 A의 세 단계 자리 산술

공통 선행은 G15AF의 Patrick7·Kira16 **정본** 및 Suggs5 **미선택 DB1 후보**, Plumlee 잔류, 그 외 원역사 8/6 계약·9/4 Nets 거래·Jordan 방출이 모두 성립하고, G15BK의 Bol–McGruder 취소 유지 `R` 등 **그 사이 다른 표준 인원 변동이 없다는 압박 가정**이다. 특히 1월 Stanley의 세 번째 10일 계약은 별도 예외·만료가 `HOLD`라서 2/10까지 표준 인원에 계속 합산하지 않는다.

개막 `15`의 추적은 G15AF 실명 집합과 같다. 8/12 원역사 표준 `15`에서 Hayes/Bey/Cade를 Patrick/Kira/Suggs로 **1:1 교체**, Plumlee 잔류 `+1→16`, Diallo 서명 `+1→17`, Nets 거래 `−2+1→16`, Jordan 방출 `−1→15`다. 후보 A는 Garza의 원역사 표준 전환 `+1`을 실행하지 않는다. 모든 상대 거래·서명이 성립했다는 전제의 집합 계산이다.

| 단계 | 조건부 표준 | 조건부 투웨이 | 결론 |
|---|---:|---:|---|
| 2021-10-20 후보 A 개막 | **15** | Garza·Smith **2** | Garza 원역사 9/24 표준 전환은 취소. Pickett은 투웨이가 아니다. |
| 2022-02-10 거래 **완료 후** | `15−Lyles−Josh Jackson+Bagley=14` | Garza·Smith **2** | 원형 4팀 거래가 실제로 대체세계에서도 통과한다는 가정일 때 **표준 인원이 15→14로 줄어 빈 자리 하나**가 생긴다. 2/10 경기 전 이용 가능한 자리로 소급하지 않는다. |
| 거래 뒤 Garza 표준 전환 **후보** | `14+Garza=15` | Smith **1** | Garza 계약 옵션·급여·50활동경기 이전 누적·리그 접수 `HOLD`. |
| 그 뒤 Pickett 투웨이 계약 **후보** | **15** | Smith·Pickett **2** | Pickett이 다른 NBA 팀과 계약하지 않았고 Detroit 제안을 수락해야 한다. 2021 가을 원역사 계약을 2022년 2월로 자동 지연하지 않는다. |

**반증 분기:** 4팀 거래가 상대 팀·자산·급여 때문에 실패하면 표준은 여전히 15이고 Garza의 전환 자리는 없다. Pickett이 다른 팀과 계약했거나 Cruise 경로를 택하지 않으면 마지막 투웨이 자리를 그 이름으로 채울 수 없다. 2/10 거래가 성립하더라도 **Garza를 계속 투웨이로 두고 활동을 제한하는 안**은 가능하므로 전환 자체를 의무로 취급하지 않는다. G15BN상 2/10은 원역사 일정의 Detroit 55번째 경기이고, 그날 Garza를 투웨이 **활동 명단에 넣으려면** 앞선 55경기 중 최소 5경기 비활동이 필요하다. 2/11 이후 전환 가능성은 이전 50활동경기 위반을 소급 치유하지 않는다.

Pickett의 중간 경로는 `8월 Exhibit 10 → 캠프 뒤 Cruise 선수/다른 NBA 팀 계약/해외 이동 중 하나 → 2월 Detroit 새 제안`으로 **아직 증거가 없는 갈림길**이다. Exhibit 10이 2월까지 Detroit NBA 권리를 예약한다는 뜻이 아니다. Garza가 2/10 이전 투웨이 활동 50경기를 이미 넘겼다면 나중의 표준 전환은 그 선행 위반을 고치지 못하므로 이 경로는 탈락한다.

| 선행 조건이 실패하면 | 막히는 단계 |
|---|---|
| 4팀 거래 상대 수락·픽/급여·의료 검토 실패 | 표준 `15→14`가 없어져 Garza 전환 자리도 없음 |
| Garza 계약 전환 옵션·적용액·리그 접수 미확인 | 거래로 빈 자리만 생기고 Garza 표준 전환은 미통과 |
| Pickett 타 팀 계약 또는 본인 미수락 | Garza 전환 뒤에도 두 번째 투웨이는 Pickett으로 채울 수 없음 |
| 2/10 이전 Garza 활동 50 초과 | 그 이전의 투웨이 사용 자체가 불가; 후행 거래/전환으로 복구 불가 |

| 구분 | 판정 |
|---|---|
| 사실 | 원역사 Pickett Exhibit 10·타 NBA 팀 계약 가능성, 2/10 Detroit `Lyles+Josh Jackson→Bagley` 및 경기 중 공식화, Edwards 표준 전환의 실제 선례. |
| 추론 | 원형 거래 및 다른 인원 유지 가정 아래 후보 A 표준은 `15→14`, Garza 전환 후보 후 `15`; Pickett 투웨이까지 성립하면 15+2. |
| 후보 | 2/10 거래 뒤 Garza 전환과 Pickett 새 투웨이 제안. 상대 팀·픽·급여·계약 옵션·활동/의료·Pickett 의사는 모두 `HOLD`. |
| 작가확정 | 0건. Bagley 거래·Garza 전환·Pickett 계약·DB1·2021–22 결과 어느 것도 선택하지 않았다. |

다음은 2/10 4팀 거래의 **Detroit가 실제로 소유한 두 픽과 타 팀 수락·급여 매칭**, 2/11 전후 후보 A 표준 인원 변동, Pickett의 G League/타 팀 상태, Garza의 날짜별 사용 필요 경기를 대조한다. Chicago D1 F1–F5 `0/5`, A1–A3 `0/3`, K `0/4`; 전체 7묶음 1완료·1진행·5대기, 진행 중 포함 남은 6묶음.
