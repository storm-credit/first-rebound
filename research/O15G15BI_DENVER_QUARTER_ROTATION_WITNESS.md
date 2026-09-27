# O-15G15BI — Denver 1/23 쿼터별 조건부 교대 증명

- 기준: [G15Z의 추상 5인 배정](O15G15Z_DENVER_FIVE_MAN_AND_BEY_CONTRACT_BRIDGE.md). [NBA 원역사 DET@DEN 경기](https://www.nba.com/game/det-vs-den-0022100707/box-score)의 선수별 분은 **비교 기준**이며 대체세계 교대 시각이 아니다.
- 산출물: [2분 단위 4쿼터 5인 원장](../simulation/O15G15BI_DENVER_QUARTER_ROTATION.json), [재현 검사기](../tools/check_o15g15bi_denver_quarters.py).
- 판정: `QUARTER_AND_REST_MATH_PASS / CONTRACT_MEDICAL_ROLE_OFFENSE_HOLD`. X1 JaMychal Green과 X2 Saddiq Bey는 상호 배타적이며 작가확정은 이번 0건이다.

## 쿼터 교대의 비용

G15Z는 Jokić을 처음 `36:06`, Gordon을 처음 `31:15` 연속 뛰게 했다. 이번 원장은 각 쿼터를 여섯 개 2분 구간으로 나누고 실제 교체 시각이라는 주장 없이 휴식 구간을 배치했다. 아래 `RX`는 X1에서 JaMychal, X2에서 Bey다. 표의 각 행은 해당 쿼터의 왼쪽부터 `0–2 / 2–4 / … / 10–12분` 순서다. 각 구간의 포지션은 JSON에서 PG·SG·SF·PF·C 순서로 고정한다.

| 쿼터 | PG 순서 | SG 순서 | SF 순서 | PF 순서 | C 순서 |
|---|---|---|---|---|---|
| 1 | Morris×3, Campazzo×3 | Forbes×2, Campazzo, Rivers×3 | Barton, Barton, Barton, Barton, Barton, Barton | Gordon×5, RX | Jokić×6 |
| 2 | Campazzo×2, Morris×4 | Forbes×3, Rivers×3 | Rivers×2, Barton×4 | RX×4, Gordon×2 | Cousins×5, Jokić |
| 3 | Morris×2, Campazzo×4 | Rivers×3, Forbes×3 | Reed×6 | Gordon×4, RX×2 | Jokić×5, Cousins |
| 4 | Morris×6 | Forbes×2, Rivers×4 | Rivers×2, Barton×4 | RX, Gordon×5 | Jokić×6 |

`×n`은 연속된 2분 칸 `n`개다. 1쿼터의 Campazzo는 SG 4–6분을 마친 뒤 PG 6–12분을 맡는다. Rivers는 2쿼터 SF 0–4분과 SG 6–12분 등 서로 다른 **시간**의 역할만 맡는다. 어느 2분 칸에도 한 사람이 두 자리에 없다. 4쿼터 마지막 8분은 Morris·Rivers·Barton·Gordon·Jokić 조합으로 끝나며 이 조합의 실제 상대 전술상 성공을 주장하지 않는다.

| 선수 | 조건부 분 | G15Z의 원역사 분 기준과 차이 |
|---|---:|---:|
| Morris / Campazzo | `30:00 / 20:00` | `+0:09 / −0:36` |
| Forbes / Rivers / Barton / Reed | `20:00 / 34:00 / 28:00 / 12:00` | `−0:44 / +0:15 / +1:04 / −0:08` |
| Gordon / RX | `32:00 / 16:00` | `+0:45 / −0:45` |
| Jokić / Cousins | `36:00 / 12:00` | `−0:06 / +0:06` |

RX `16:00`과 G15Z의 원역사 Nnaji `16:45`의 45초 차이는 Gordon으로 옮긴다. 이 분안은 원역사 분을 2분 칸에 맞춘 **산술적 근접안**이지 역사적 경기의 보존이나 가능한 유일 교대가 아니다. Barton의 `+1:04`가 최대 차이다. 각 쿼터 60 선수분, 전체 240 선수분, 모든 순간 5명, 모든 선수의 최장 연속 출전 12분을 검사했다. 쿼터 경계를 이어도 최장 연속 출전은 12분이다. 이 값은 의료적 허용 시간이나 코치의 실제 활용 상한이 아니다.

## 아직 닫히지 않은 연결

| 구분 | 현재 판정 |
|---|---|
| 사실 | 원역사 경기·선수분, 2020 정본 Denver Bey22. [NBA 게임 노트](https://cdn.nba.com/teams/uploads/sites/1610612743/2022/01/nuggetsPistons.pdf)의 원역사 명단은 대체세계 등록 증명이 아니다. |
| 추론 | X1 또는 X2의 계약·당일 가용성이 따로 성립하면, 같은 10명의 분을 쿼터·5인 중복 없이 나눌 수 있다. |
| 후보 | X1 JaMychal PF16, Bey 0분 또는 X2 Bey PF16, JaMychal 0분. X2의 Bey PF와 두 분기의 다른 수신자 0분에는 코치·성장 비용이 든다. |
| 작가확정 | 이번 0건. Bey 서명·2021–22 보유/등록·PF 적합성, JaMychal 계약/건강, 실제 교대·공격기회·수비/파울·점수/승패·Gordon A 정확 거래는 모두 `HOLD`. |

따라서 G15Z의 **긴 무휴식 교대**라는 산술 맹점은 개선됐지만 Denver 경기 자체는 미완료다. 다음은 날짜별 계약·15인 자리/의료, Detroit의 이탈한 Bey/Hayes 및 DB1 Cade와 새 Patrick/Kira/Suggs의 당일 기회 비용이다. D1 Chicago 2020–21 정확 실행, G14 Detroit `PRIOR_HOLD`·Orlando `ROLE_HOLD`, G16/G17은 그대로다. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, `author_locked=false`, `season_selected=false`, `exact_execution_cleared=false`, `manuscript_allowed=false`. 전체 7묶음은 1완료·1진행·5대기, 진행 중 포함 6묶음이 남는다.
