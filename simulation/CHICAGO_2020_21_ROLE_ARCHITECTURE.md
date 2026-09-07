# Chicago 2020-21 Opening Role Architecture

- 상태: `ROSTER_STRUCTURE_PASS / STAGED_STARTING_SEQUENCE_PROVISIONAL_BASE / PLAYER_GAME_REQUIRED`
- 기준선: 표준 15 + 투웨이 2, LaMelo와 주인공의 1대1 roster 치환
- 정확 개인 기록·승수·거래: `HOLD`
- 원고 게이트: `CLOSED`

## 1. 첫날 역할

Billy Donovan 체제의 실제 preseason 구상은 Coby White에게 point guard 역할을 먼저 시험하고 Patrick Williams를 선발 포워드로 세우는 것이었다. 현재 세계에서는 Patrick 대신 3년차 주인공이 있으며, LaMelo라는 더 높은 1차 창출 후보가 추가된다.

가장 적은 약속 파괴와 수비 비용으로 시작하는 provisional five는 다음이다.

| 자리 | 선수 | 첫 역할 |
|---|---|---|
| PG | Coby White | 실제처럼 첫 PG 시험 기회 유지 |
| SG | Zach LaVine | 주득점원·클로징 공격 보호 |
| SF | 주인공 | 가장 어려운 윙 수비·리바운드 뒤 전환 시동 |
| PF | Lauri Markkanen | spacing·계약연도 평가 기회 유지 |
| C | Wendell Carter Jr. | 센터 수비·스크린 역할 유지 |

LaMelo는 첫날부터 25분 이상을 받는 **첫 가드 교체이자 두 번째 유닛 1차 창출자**로 시작한다. 이는 4순위 가치를 bench player로 낮추는 것이 아니라 Coby의 기존 시험을 짧게 보존하면서 세 가드 수비 붕괴를 피하는 시작점이다.

## 2. 단계적 전환

`게임 10~20` 구간에 LaMelo의 압박 대응·turnover·수비 조합과 Coby의 half-court 조직을 비교한다. exact 날짜는 player-game 뒤에만 정한다.

- LaMelo가 1차 창출을 획득하면: `LaMelo–LaVine–주인공–Markkanen–Carter`가 주 선발 후보
- Coby는 2차 득점·약한 수비 매치업 공격으로 역할을 재정의하되 1,500분 아래로 자동 축소하지 않음
- 주인공은 LaMelo의 수비 약점을 모두 지우는 만능 stopper가 아니라, 큰 윙 매치업과 리바운드 종료를 담당
- LaVine의 실제 All-Star급 득점 볼륨은 첫 donor 대상에서 제외

## 3. 폐기할 즉시 해법

| 안 | 문제 | 처리 |
|---|---|---|
| LaMelo·Coby·LaVine 3가드 + 주인공 벤치 | 최고 수비 포워드를 빼고 약한 POA 조합을 상시화 | `REJECTED_AS_BASE` |
| LaMelo 입단 즉시 Coby PG 실험 종료 | 2019 7순위의 실제 개발 선택을 평가 없이 삭제 | `REJECTED_AS_BASE` |
| 주인공이 상시 point forward | 3년차 grab-and-go·숏롤 패스를 완성형 주도자로 과장 | `REJECTED_AS_BASE` |
| Charlotte의 LaMelo 51경기·신인왕 복사 | 팀·동료·상대·부상 사건이 다른 결과를 선지급 | `PROHIBITED` |

## 4. provisional minute prior

`simulation/CHICAGO_2020_21_ROLE_MINUTE_PRIOR.csv`의 BASE는 주인공 1,938분, LaMelo 1,760분이다. 이는 결과가 아니라 player-game 원장 제작 목표다.

- 주인공: 2019-20 1,395분에서 약 39% 증가. 3년차 선발 포워드 상승이지만 30 MPG 상한을 둔다.
- LaMelo: 27.5 MPG 기준. 실제 Charlotte의 28.8 MPG를 참고하되 Chicago의 가드 중복 비용을 반영한다.
- 합산 3,698분에서 Patrick·Hutchison 실제 2,047분을 빼면 추가 donor가 1,651분 필요하다.
- 정확 GP·GS·분은 부상 사건과 same-date 보존 뒤 `PROVISIONAL_LOCK` 여부를 다시 판정한다.

## 5. 다음 게이트

다음은 작가 선택이 아니라 계산 단계다. O-15F1에서 마감일 전 실제 경기 원장을 만들고, staged sequence가 같은 날짜 분과 선발 5자리 보존을 통과하는지 검증한다. 통과하지 못하면 BASE 총분 또는 선발 전환 시점을 낮춘다.
