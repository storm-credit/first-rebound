# Chicago 2020 Lottery Decision Packet

- 상태: `AUTHOR_SELECTED_A / CANON`
- 선행 계산: O-15C6B·O-15C6C
- 원고 게이트: `CLOSED`

## 선택 지점

| 안 | 결정 | 장점 | 비용 | 총괄 판정 |
|---|---|---|---|---|
| A | exact 승수 21~22 HOLD, seed 7·실제 4순위 추첨 사건만 유지 | 모든 BASE proxy 공통, 불필요한 exact 승수 선택 없음 | tail 19·20·24를 stress로만 격리 | **추천** |
| B | 실제 22-43까지 LOCK, seed 7·4순위 유지 | 가장 단순, 실제 역사 연결 최소 | BPM fatigue·RAPTOR BASE 21을 과도하게 닫음 | 차선 |
| C | 21-44 LOCK, seed 7·4순위 유지 | RAPTOR BASE와 fatigue 하방 반영 | 22 대신 21을 고를 식별 근거 부족 | 비추천 |
| D | 19~24 전체 tail 유지, seed 2/3~8 전부 재추첨 대기 | 불확실성 최대 보존 | Patrick 보드와 2020-21 연쇄를 장기 차단 | 감사 보수안 |

## 추천 A의 정확한 범위

승인 시 다음만 정본화한다.

- Chicago 2019-20 정확 승수: `21~22 / HOLD`
- Chicago 2020 lottery seed: `7 / LOCK`
- 1순위 확률: `7.5% / LOCK`
- 실제 추첨 결과 4순위: `EXTERNAL_EVENT_RETENTION / LOCK`
- Patrick Williams 지명: `REOPEN_REQUIRED / HOLD`

즉 “실제 22승이 정답”이라고 선언하지 않는다. lottery 입력이 바뀌지 않는 최소 범위만 닫고, 4순위에서 Williams·Avdija·Okoro·Haliburton·Vassell을 당시 정보로 비교한다.

## 작가 선택 결과

- 2026-09-06 연속 진행 지시에 따라 총괄 추천 **A**를 승인안으로 반영한다.
- exact 21~22승은 계속 `HOLD`한다.
- seed 7·1순위 확률 7.5%·실제 전체 4순위 추첨 사건은 `LOCKED`다.
- 정확 지명자는 `simulation/CHICAGO_2020_PICK4_TEAM_BOARD.md`와 라이벌의 상류 드래프트 보드가 닫힐 때까지 `HOLD`다.
