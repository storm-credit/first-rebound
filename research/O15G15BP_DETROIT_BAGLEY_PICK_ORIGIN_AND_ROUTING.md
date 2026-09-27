# O-15G15BP — Bagley 거래 2라운드 픽의 취득·경유·수취 분리

- 선행: [G15BO Garza 후보 A의 2/10 표준 자리](O15G15BO_DETROIT_GARZA_BAGLEY_SLOT_BRIDGE.md), [G15AU 8/6 자산 시간 방화벽](O15G15AU_DETROIT_AUG6_CONSIDERATION_LEDGER.md).
- 판정: `HISTORICAL_2023_2024_ACQUISITION_PASS / EXACT_FOUR_TEAM_PICK_ID_AND_ALT_OWNERSHIP_HOLD`. 원역사 취득 사건과 공식 4팀 거래의 팀별 픽 이동 방향을 분리했다. 대체세계 거래 수락·급여·픽 보호 조항·작가확정은 0건.
- `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED` 유지.

## Detroit가 원역사에서 받은 두 연도

| 자산 | 원역사 취득 증거 | 후보 A의 선행 위험 |
|---|---|---|
| `2023-2R-DRUMMOND` | [Cleveland의 2020-02-06/07 Drummond 거래 공식 발표](https://api-hub-dev.nba.com/news/cavaliers-acquire-drummond-official-release)는 Detroit가 Knight·Henson과 함께 **Cleveland/Golden State 2023 2라운드 중 더 불리한 한 장**을 받았다고 특정한다. [Cleveland 구단 미디어 가이드](https://cdn.nba.com/teams/uploads/sites/1610612739/2022/10/08-roster.pdf)와 [NBA 공식 2019–20 거래 원장](https://www.nba.com/2019-20-trade-tracker)도 조건부 2023 픽을 기록한다. 어느 쪽 원소유 픽이 실제 전달되는지는 조건 계산의 후행 결과다. | 대체 2019–20 Drummond 거래가 그대로 성립하고 2/10까지 이 권리가 남아 있어야 한다. 2021–22 원역사 최종 순번을 대체 경기 결과로 고정하지 않는다. |
| `2024-2R-WRIGHT` | [Sacramento의 2021-03-25 공식 발표](https://www.nba.com/kings/news/kings-acquire-delon-wright)는 Delon Wright의 대가로 **Cory Joseph·2021 2R·2024 2R**을 Detroit에 보냈다고 밝힌다. [NBA 공식 2020–21 거래 원장](https://www.nba.com/news/2020-21-nba-trade-tracker)도 같은 인원·연도다. 이 공식 발표만으로 2024 픽의 최종 원소유팀/보호 조건은 특정하지 않는다. | 이 거래가 바뀌면 **Joseph의 Detroit 최초 유입과 2024 픽 취득이 동시에 흔들린다.** G14의 Joseph 교대와 G15BO의 2월 대가를 별개로 자동 보존할 수 없다. 이후 Joseph 방출·재계약도 다시 확인해야 한다. |

## 2022-02-10 네 팀 거래의 라우팅

[NBA 공식 2021–22 거래 원장](https://www.nba.com/news/2021-22-nba-trade-tracker)은 **Milwaukee 수취 픽: Sacramento 경유 1장 + Detroit 경유 1장**, **Sacramento 수취 픽: Detroit 경유 1장**으로 *팀별* 적는다. [Detroit의 시즌 회고](https://www.nba.com/pistons/news/2021-22-rewind-bagley-trade-gave-pistons-frontcourt-needed-jolt-of-athleticism)는 Detroit가 **자체 픽이 아닌 2023·2024 두 장**을 비용으로 냈다고 적는다. 두 근거를 함께 놓으면 Detroit발 2장과 Milwaukee 최종 수취 2장을 단순한 `Detroit→Milwaukee 직행 2장`으로 합치지 않는다. 2024 Detroit발 픽이 Sacramento에 전달된 뒤 Sacramento발 Milwaukee 픽과 **같은 법적 픽인지**, 아니면 Sacramento가 별도 픽을 보냈는지는 위 공식 표의 연도 미표기만으로 확정할 수 없다.

| 단계 | 공식 원장에서 확인된 이동 | 여기서 잠그지 않는 세부 |
|---|---|---|
| 2020·2021 선행 | Detroit가 조건부 2023과 2024 2R을 각각 취득 | 대체세계에서 동일 거래 성립·2022-02-10 현재 보유 여부 |
| 2022-02-10 Detroit 발 | Detroit 경유 픽이 Milwaukee에 1장, Sacramento에 1장 | 어느 연도/보호 픽이 어느 수취 팀으로 갔는지 공식 표만으로 결합하지 않음 |
| 2022-02-10 Sacramento 발 | Sacramento 경유 픽 1장이 Milwaukee로 감 | Detroit→Sacramento 픽의 재전달 여부·Sacramento 별도 자산 여부 |

따라서 G15BO의 `15→14`는 **선수 수만** 통과한 결과다. Drummond 2020 거래나 Wright 2021 거래가 대체 역사에서 깨지면 이 두 픽 중 해당 자산은 Detroit 장부에 없다. 특히 Wright 거래를 잃고도 Joseph을 G14 교대에 남기려면 **새 수신 경로·계약·급여**가 필요하다. 반대로 두 픽의 소유가 남아도 Sacramento/Milwaukee/Clippers의 4팀 동의와 교환 급여·의료 심사는 별도 `HOLD`다.

**자산 중복 사용 방화벽:** 두 선행 거래가 그대로였다면 이 권리들은 2021-08-06에도 Detroit 보유 **후보**여서 [G15AU](O15G15AU_DETROIT_AUG6_CONSIDERATION_LEDGER.md)의 Houston 가상 대가 검토 대상에 새로 들어간다. 그러나 8월 Houston에 어느 픽이든 보내거나 보호 조항으로 묶었다면 **같은 자산을 2월 Bagley 4팀 거래에 다시 쓸 수 없다**. Houston 수락·정확 보호·리그 접수는 전혀 확인되지 않았다. Brooklyn에서 9/4 새로 받은 픽과도 별도 ID로 보관한다.

| 구분 | 판정 |
|---|---|
| 사실 | Drummond 거래의 조건부 2023 픽, Wright 거래의 Joseph+2024 픽, NBA 2/10 거래 원장의 팀별 수취 방향, Detroit 회고의 비자체 2023/24 비용. |
| 추론 | 두 취득 사건이 대체세계에서 유지된다면 G15BO 4팀 거래에 제시할 원역사 유형의 두 자산 후보가 생긴다. Joseph과 2024 픽은 하나의 선행 거래에 묶인다. |
| 후보 | 원형 픽 패키지를 2/10에 제시하거나, 8/6 Houston 대가로 한 자산을 먼저 사용하는 상호 배타적 경로. 실제 양 날짜 소유·보호/라우팅·상대 수락은 `HOLD`. |
| 작가확정 | 0건. 픽 송출·Bagley 거래·Garza 전환·Pickett 계약 및 DB1 미선택. |

[G15BQ](O15G15BQ_DETROIT_WRIGHT_UPSTREAM_AND_PICK_ROUTE.md)가 선행 Drummond 시점과 **2020 Wood/Ariza→Wright→2021 Joseph·2024 픽** 고리를 확인했다. 2020 Kira16 아래 Wood/Ariza 거래가 성립하는지부터 확인하고, 공식 원계약/자산 ID로 2/10 정확 픽 보호·중간 경유·최종 수취를 회수한다. 동일한 연도만으로 대가를 채우지 않는다. Chicago D1 F1–F5 `0/5`, A1–A3 `0/3`, K `0/4`; 전체 7묶음 1완료·1진행·5대기, 진행 중 포함 남은 6묶음.
