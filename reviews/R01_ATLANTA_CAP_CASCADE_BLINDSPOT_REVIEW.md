# R01 Atlanta cap·draft·trade 연쇄 맹점 검토

- 기준일: 2026-09-05
- 대상: `simulation/ATLANTA_2019_22_CAP_DRAFT_TRADE_CASCADE.md`
- 독립성: `NOT_INDEPENDENT`
- 판정: `CONDITIONAL_PASS / PLAYER_GAME_AND_CAP_HOLD`

## 1. 이번 검토가 뒤집은 가정

O-12C는 2022-23에 1,750~2,050분을 만들기 위해 16순위 지명 변경 또는 Bey 거래 제거를 우선 검토했다. 그러나 Griffin을 바꾸면 17순위 이하 드래프트가, Bey를 지우면 네 팀 거래가 함께 흔들린다.

따라서 인물 성장 욕구보다 역사 파급 최소화를 우선해 Griffin·Bey 기본선을 보존하고 주인공 분을 1,550~1,800으로 낮췄다. 이는 정본 하향이 아니라 계산 후보 수정이다.

## 2. 가장 강한 반대 해석

### 반대 A — 주인공이 있는데도 Bey를 데려오는 것은 비합리적이다

주인공·Hunter·Griffin·Bogdanović가 있으면 윙은 이미 많다. 실제보다 Bey 수요가 약해지는 것은 맞다.

**대응:** Bey 거래를 LOCK하지 않고 `MOTIVE_SENSITIVE`로 둔다. 2023년 2월 실제 standings, Bogdanović 가용성, Griffin 신인 변동, 주인공 shooting 한계를 player-game과 함께 검사한다. 동기가 사라지면 4팀 전체를 다시 계산한다.

### 반대 B — 역사 보존 때문에 주인공 성장을 눌렀다

5년차 1,550~1,800분은 S급 예고에 약해 보일 수 있다.

**대응:** Atlanta에서 S급 완성 금지가 기존 설계다. 고급 6맨·매치업 선발·클로징 카드는 2023 가치 트레이드 가능성을 남기며, 두 번째 팀의 권한 상승 폭을 더 크게 만든다. 단, 거래 대가는 선발급으로 과장하지 않는다.

### 반대 C — Koufos에게 room MLE를 주는 것은 과대지급이다

직전 502분의 30세 센터에게 최대 476.7만 달러를 쓰면 비효율적이다.

**대응:** 최대액은 협상액이 아니라 legality ceiling이다. 실제 사용 가능한 exception과 CSKA 선택을 뒤집을 최소액을 확인한 뒤 LOW/BASE를 정한다. 성립하지 않으면 Monroe나 2019 센터 구조안을 다시 연다.

### 반대 D — Huerter 거래는 주인공 자리 만들기다

주인공이 Huerter의 슈팅과 2차 패스를 대신하지 못하므로 이를 역할 대체 거래로 쓰면 안 된다.

**대응:** Murray 합류 뒤 가드 중복과 tax pressure를 우선 인과로 둔다. 주인공 계약은 추가 압력일 뿐 Huerter 공로·기능을 삭제하지 않는다.

## 3. 계수·자산 방화벽

| 항목 | 금지 | 허용 |
|---|---|---|
| Koufos | Jones 886.9분·27선발 복사 | 한 roster 자리 대체, exact 분 재계산 |
| 2026 GSW 2라운드 | 거래가 없는데 Atlanta 자산으로 보존 | 미수취 자산 원장 |
| Huerter | 2,188.5분 자동 상속 | 재정·가드 구조 거래 후 donor 재계산 |
| Griffin | 미래 경력을 알고 지명 회피 | 2022 당시 shooting profile로 유지 판단 |
| Bey | 628.6분 전량 이전 | 네 팀 거래 보존 뒤 일부 역할 조정 |
| 주인공 계약 | 정확 tax 계산 없이 팀 친화 선언 | LOW/BASE/HIGH 민감도 창 |
| 2023 거래 가치 | 26~29분 전제의 대가 유지 | 24~26분에 맞춰 대가 하향 |

## 4. 남은 blocker

1. Atlanta의 2019 room MLE 실제 사용 내역과 계약 체결 순서.
2. Koufos NBA 제안의 세전/보장/역할과 CSKA 세후 가치 비교.
3. 2022 protagonist LOW/BASE/HIGH별 팀 급여·tax line·15인 자리.
4. 2022-23 1,550~1,800분의 날짜별 donor와 Griffin·Bey 잔존 기능.
5. Bey 거래 당일 대체 세계 Atlanta의 동기.
6. 낮아진 2023 거래 가치에 맞춘 Indiana/Sacramento 자산 재평가.
7. R16 독립 검토.

## 5. 판정

2019 Koufos는 roster상 성립하지만 계약 mechanism은 아직 조건부다. 2022에는 Griffin과 Bey 거래를 유지하면서 주인공 분을 낮추는 안이 현재까지 최소 역사 훼손이다. 정확 cap과 player-game 원장 전에는 어느 선수·계약·분도 정본으로 승격하지 않는다.

`CONDITIONAL_PASS / NOT_CANON / R16_PENDING`
