# O-15G15Y — 2022-01-23 세 경기 선수 이동·기회 원장

- 기준: G15W의 `CHI@ORL`·`DET@DEN`, G15X의 Denver 수신자 X1과 기존 2020 정본·2021 DB1 비교안.
- 판정: `THIRD_GAME_AND_BEY_OPPONENT_COLLISION_IDENTIFIED / ROSTER_MINUTES_HOLD`. 원역사 경기 기록을 대체세계 점수로 선택하지 않는다.
- `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`; 새 작가확정 0건, `author_locked=false`, `season_selected=false`, `exact_execution_cleared=false`, `manuscript_allowed=false`.

## 1. 원역사 세 경기와 여섯 선수의 팀 변경 조건

미국 현지 2022-01-23에는 [CHI@ORL `0022100701`](https://www.nba.com/game/chi-vs-orl-0022100701/box-score), [ATL@CHA `0022100703`](https://www.nba.com/game/atl-vs-cha-0022100703/box-score), [DET@DEN `0022100707`](https://www.nba.com/game/det-vs-den-0022100707/box-score)가 있었다. [당일 19:30 ET NBA 부상 보고서](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2022-01-23_07PM.pdf)는 이 세 매치업을 따로 기재한다. 역사적 박스의 선수 분은 **그 팀·상대·코치 아래 실제 관측**이며 팀을 바꾸어 복사할 1인 목표치가 아니다.

| 원역사 1/23 행 | 이 프로젝트에서 다른 팀으로 이동하는 경로 | 지위·1/23 처리 |
|---|---|---|
| DET Bey `30:42`, 11 FGA, 11점 | [2020 정본](../canon/PROJECT_FREEZE.md)은 **Denver 22순위 지명**을 작가 확정. [2021 조건부 계속안](../simulation/NBA_2021_FIRST_ROUND_CONTINUATION.md)은 Bey의 Denver 잔류를 입력한다. | 지명 팀은 확정, 2022-01-23 Denver 계약·등록·출전 분은 `HOLD`. Detroit 원역사 분/슛은 제거하고 Denver로 그대로 복사하지 않는다. |
| DET Hayes `24:42`, 5 FGA, 8점 | [2020 정본](../canon/PROJECT_FREEZE.md)은 **New Orleans 13순위 지명**을 작가 확정한다. | 원역사 Detroit `Available`·실제 양수 분도 New Orleans로 이월하지 않는다. 기존 이 표에서 빠진 세 번째 선수 이동이다. |
| DET Cade `36:14`, 15 FGA, 18점 | [2021 DB1](../simulation/NBA_2021_FULL_DRAFT_COMPARISON.json)의 **Charlotte 1순위 후보**. | DB1은 최종 지명이 아니다. 이 분기에서는 Detroit 원역사 분/슛이 없고 Charlotte가 아래 LaMelo 공백과 함께 검토해야 한다. |
| CHA LaMelo `33:58`, 17 FGA, 19점 | [2020 정본](../canon/PROJECT_FREEZE.md)은 **Chicago 4순위 지명**을 작가 확정. | 원역사 Charlotte 분/슛은 Charlotte에 남지 않는다. Chicago의 기존 G14 1/23 조건부 분은 별도이며, 원역사 33:58을 덧셈하지 않는다. Charlotte는 이미 확정된 Anthony Edwards 3순위와 DB1 Cade 후보의 볼 권한을 함께 봐야 한다. |
| ORL Suggs `32:46`, 10 FGA, 8 FTA, 15점 | [2021 DB1](../simulation/NBA_2021_FULL_DRAFT_COMPARISON.json)의 **Detroit 5순위 후보**. | Orlando의 G15B 240분에는 원역사 Suggs를 복원하지 않는다. Detroit는 Suggs의 대체세계 계약·의료·분과 Cade 공백을 같은 원장에 넣어야 한다. |
| DEN Nnaji `16:45`, 5 FGA, 12점 | 승인된 Gordon A 선수 방향에서는 Orlando 반환 자산; 정확 거래 실행은 `HOLD`. | Denver 원역사 분은 이 거래 조건에서 사용할 수 없다. G15X X1 또는 아래 X2처럼 이름 있는 수신자와 다른 포지션 비용이 필요하다. |

**자체 산술:** Detroit 원역사 Bey+Cade 두 행은 `66:56`, `26 FGA`, `29점`, `9 TOV`다. 이 값은 **원역사에서 사라지는 선수 관측 행의 크기**다. 대체 Detroit에서 그만큼의 분·슛이 비고 같은 점수를 누구에게 나눠 주면 된다는 뜻이 아니다. 두 선수의 분은 원역사에서 다른 선수와 동시 출전했으며, 대체세계는 Patrick Williams 7·Kira Lewis Jr. 16·Stewart 19의 [2020 정본](../canon/PROJECT_FREEZE.md)과 Suggs5 후보를 가진다. Stewart의 원역사 `26:42·18점·8 FGA`도 그가 대체 Detroit에 남는다는 이유만으로 자동 보존하지 않는다.

**G15AA 정정:** 위 Bey+Cade 합은 계산상 맞지만 이탈 집합 전체가 아니다. [세 번째 Hayes 이탈](O15G15AA_DETROIT_HAYES_THIRD_EXIT_AND_MEDICAL_BOUNDARY.md)을 더하면 2020 정본만으로 Bey+Hayes `55:24`·16 FGA·19점, DB1까지 조건부 적용 시 세 명 `91:38`·31 FGA·37점의 **원역사 관측 행**이 사라진다. 이 값 역시 대체 Detroit의 빈 분/슛 목표가 아니다.

## 2. Bey는 Denver 수신자 후보와 맞대결 상대를 동시에 바꾼다

G15X X1은 JaMychal Green을 PF `16:45`로 기용한다. 그런데 Bey가 2020 지명 후 Denver에 잔류했다면, 원역사 Detroit의 **상대 선수 Bey**가 대체세계에서는 Denver의 윙/포워드 후보가 된다. 기존 두 경기 원장에서 이 같은 날짜의 **팀 방향 전환**을 명시하지 않았다.

| 비교 분기 | 앞코트 96분의 조건부 수학 | 아직 지불해야 할 비용 |
|---|---|---|
| X1 JaMychal | PF Gordon31:15+JaMychal16:45; C Jokić36:06+Cousins11:54 | JaMychal의 실제 DNP를 바꾸는 코치 결정, 계약·건강, Bey가 Denver에 있으면 그의 별도 윙 분/자리 또는 0분 결정 |
| X2 Bey | PF Gordon31:15+Bey16:45; C Jokić36:06+Cousins11:54 | Bey의 2022 Denver 보유·당일 출전, PF 기용 적합성, 원역사 Detroit 30:42·11 FGA를 **이월하지 않는** 새 역할, JaMychal 0분 결정 |

두 분기 모두 다른 선수의 `0:05`를 Cousins에게 옮겨 팀240분을 맞추는 **분 합계 시험**일 뿐이다. X2에서 Bey의 원역사 Detroit `30:42`를 PF에 추가하면 PF48분을 초과한다. 윙에 추가할 때도 기존 윙 분을 별도로 빼지 않으면 팀240분을 넘는다. X1/X2를 동시에 선택하거나 Bey에게 원역사 Detroit 11 FGA와 Nnaji의 5 FGA를 합쳐 주지 않는다. PF 적합성·실제 동시 5인·Bey 신인 계약의 대체세계 2년차 유효성·상대 매치업은 미검증이다.

## 3. 다음 검증 순서

1. Detroit의 원역사 1/23 양수 분 중 **Bey/Hayes 제외**, DB1에서는 **Cade까지 제외**한 집합과 대체 Patrick/Kira/Suggs의 계약·당일 가용성을 같은 명단으로 대조한다. 원역사 Chicago의 Patrick 부상과 원역사 New Orleans의 Kira 부상, Orlando의 Suggs 가용성을 새 팀 의무 의료사건으로 복사하지 않는다.
2. Denver의 Bey22 잔류와 JaMychal·Cousins 계약을 날짜별로 확인한 뒤 X1/X2 각각에 대해 **5인 교대와 포지션별 48분**을 검증한다. 기존 Gordon A의 정확 거래·픽·급여 `HOLD`는 별도다.
3. Charlotte의 LaMelo 상실, Edwards3 정본, DB1 Cade1 후보를 ATL@CHA에 연결하고 Charlotte/Atlanta 공격 기회와 Chicago/Orlando·Detroit/Denver의 상호 상대 변화를 분리한다. 세 원역사 점수·승패를 대체세계 결과로 고정하지 않는다.

**사실:** 세 공식 경기의 원역사 선수 행과 일정, 2020 작가 확정 지명권. **추론:** 2021 DB1·Gordon A 조건이 성립하면 팀 간 선수 이동으로 세 경기의 기회 비용이 연쇄된다. **후보:** DB1 Cade/Suggs, Denver X1/X2 및 세 경기 새 분. **작가확정:** 이번 0건. Chicago 2020–21 정확 시즌, G14 DET `PRIOR_HOLD`·ORL `ROLE_HOLD`, G16/G17 독립/작가 게이트는 열린 상태다. 전체 7개 매크로 게이트는 1완료·1진행·5대기, 진행 중 포함 6개가 남는다.

[Claude 제한 source-blind 검토](../reviews/R01_O15G15Y_CLAUDE_SOURCE_BLIND.md)는 원역사 분의 팀 간 무단 복사와 세 경기 연결을 확인했다. Bey의 새 Denver 역할을 이미 확정된 것으로 가정해 X2를 불가능하다고 한 부분은 기각했다. NBA 원문을 Claude가 독립 확인한 것은 아니다.

### 후속 — G15Z의 추상 5인 동시 배치

[G15Z](O15G15Z_DENVER_FIVE_MAN_AND_BEY_CONTRACT_BRIDGE.md)는 X1/X2 각각에 대해 5자리를 전 시간 피복하는 **수학적 증명**을 추가했다. 같은 선수의 동시 중복과 240분 불일치는 없다. 이 증명은 긴 연속 출전과 실험적인 포지션을 쓰므로 실제 쿼터 교대·선수 적합성·의료·계약·공격 기회는 여전히 `HOLD`다. Bey22가 2020 표준 신인 계약에 서명했다면 2021–22는 계약 2년차이나, 지명 사실만으로 2022-01-23 Denver 등록을 확정하지 않는다.
