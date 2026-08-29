# R02-3O Atlanta 2018-19 Causality Ledger Review

- 판정: `BASELINE_PASS / SECOND_TEAM_IMPACT_HOLD`
- 대상: `simulation/ATLANTA_2018_19_CAUSALITY_LEDGER.md`
- 계산 파일: `simulation/ATLANTA_2018_19_CAUSALITY_LEDGER.xlsx`

## 검증 결과

| 게이트 | 판정 | 근거 |
|---|---|---|
| G0 Spellman 새 팀 파급 | PARTIAL | Spurs 49번은 확정, 2018-19 분·승패 파급 미실행 |
| G1 82경기 기준선 | PASS | 82경기·29-53·9,294득점·연장분 재현 |
| G2 사전등록 | HOLD | 시즌 범위만 잠겼고 날짜별 출전·assignment 미확정 |
| G3 분 보존 | HOLD | 시즌 상한은 통과했으나 player-game donor vector 미작성 |
| G4 접촉 범위 | PASS | 82경기 전부 최소 ROSTER |
| G5 승패 모델 | HOLD | 방법은 선택했으나 pB·영향 prior·game hash 실행 전 |
| G6 시간순 파급 | HOLD | 피로·부상·거래·휴식 순차 실행 전 |
| G7 작가 개입 방지 | PASS | 대체 점수·승패·수동 flip 없음 |
| G8 리그 전체 보존 | HOLD | 상대팀 승패·타이브레이커·Spellman 팀 파급 미실행 |
| G9 재현성 | PARTIAL | 원장·생성기·검증기 존재, run manifest는 사전등록 뒤 생성 |

## 핵심 맹점과 통제

| 맹점 | 실패 처리 | 통제 |
|---|---|---|
| 공짜 출전시간 | 새 선수를 기존 총분 위에 추가 | Spellman 805분을 1차 상한으로 사용 |
| DNP=비접촉 오류 | 주인공 미출전 경기를 실제 결과로 자동 고정 | Spellman 부재가 남으므로 최소 ROSTER |
| 접전 골라잡기 | 1~5점 경기만 주인공 승리로 변경 | 82경기 전수·시간순·고정 hash |
| 미래정보 누출 | 실제 점수와 승패를 보고 영향치 조정 | 경기 전 pB와 사전등록 prior만 허용 |
| OT 자동 복사 | 실제 연장과 25분을 대체 세계에 그대로 적용 | CF OT는 별도 민감 판정, 실제 OT는 baseline 전용 |
| Atlanta 단독 확정 | 상대팀과 Spellman 새 팀을 무시하고 lottery 확정 | 리그 전체 W/L와 두 번째 팀 파급까지 FINAL 차단 |
| 실제 픽 강제 | #8·#10과 Hunter/Reddish를 자동 유지 | 새 lottery·보호픽 뒤 거래·선택 재판정 |
| 실제 부상 복제 | Spellman 발목 부상을 주인공 결장 장치로 사용 | 주인공 고유 일정·행동 비용 필요 |

## 판정 이유

- 사용자가 요구한 경기별 고증과 승수·드래프트 연결의 첫 데이터층은 완성됐다.
- 주인공의 신인 분은 실제 교체 대상의 805분 안에서 성립하므로 핵심 젊은 선수의 시간을 억지로 빼앗지 않는다.
- 대체 승패는 아직 증거와 사전등록이 부족하므로 생성하지 않았다.
- 2018년 후반 드래프트가 크더라도 30~60을 무조건 모두 장편 서술하지 않는다. 팀 선택이 실제와 달라지는 지점만 깊게 검토하되, 모든 픽은 원장상 통과시킨다.
- 1차 스캔은 각 픽당 실제 선택·Spellman/연쇄 이탈자·동시대 비교 후보 한 명으로 제한하고, `CHANGED/CASCADE`에서만 심층 조사한다.
- 원고 게이트는 계속 `CLOSED`다.

## 다음 실행

1. San Antonio의 실제 Metu 145분과 G League 이동을 날짜별로 수집한다.
2. Spellman의 Spurs 계약·assignment·출전 안전선을 결과 보기 전에 잠근다.
3. Atlanta 경기별 availability와 주인공 donor vector를 만든다.
4. Atlanta와 Spurs의 영향 prior를 만들고 직접 대결 두 경기를 포함해 시간순으로 실행한다.
5. 그 뒤에만 승패·상대팀 기록·2019 lottery를 실행한다.
