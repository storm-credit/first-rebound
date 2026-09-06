# R02-3R Dallas / Denver Cascade Contract Review

- 판정: `CASCADE_CONTRACT_PASS / GAME_OUTCOMES_HOLD`
- 대상: `simulation/DALLAS_DENVER_2018_19_CASCADE_IMPACT.md`
- 계산 파일: `simulation/ATLANTA_2018_19_CAUSALITY_LEDGER.xlsx`
- 원고 게이트: `CLOSED`

## 감사 결과

| 항목 | 판정 | 근거 |
|---|---|---|
| Dallas 계약 계층 | PASS | 실제 Spalding 표준 NBA 계약을 Metu가 대체 |
| Dallas 개발 계층 | PASS | Texas 29경기·평균 30.1분이 BASE |
| Dallas NBA 분 | PASS_WITH_TRIGGER | 1경기·1분 BASE, 초과 시 player-game 재개 |
| Dallas 1월 31일 방출 | HOLD | Metu 평가가 다르면 다른 방출 선택 가능 |
| Denver 투웨이 슬롯 | PASS | Spalding과 Akoon-Purcell 두 자리로 정확히 충족 |
| Denver NBA 분 | PASS_WITH_TRIGGER | Welsh의 11경기·36분 BASE, 초과 시 player-game 재개 |
| Welsh 역할 중복 | BLOCKED_AND_CORRECTED | Denver의 같은 투웨이 슬롯을 중복 지급할 수 없음 |
| Welsh 후속 경로 | HOLD | 미지명 자유계약 시장까지 확정, 팀 지정 금지 |
| Atlanta 직접 대결 | PASS | Dallas·Denver 네 경기의 실제 대체 슬롯 0분 |
| 승패·순위 | HOLD | Atlanta 분은 잠겼으나 개인 성과·경기 영향 미실행 |
| 원고 안전 | PASS | 대체 기록·장면·대사 미작성 |

## 레드팀 맹점

1. Metu가 San Antonio에서 실제 145.4분을 뛰었다는 이유로 Dallas에서도 같은 분을 주면 팀별 역할 원칙을 깨뜨린다.
2. Spalding이 Dallas에서 표준 계약이었다는 이유로 Denver에서도 표준 계약을 주면 실제 58번 계약 구조를 무시한다.
3. Welsh의 실제 경로를 보존한다며 같은 Denver 투웨이 슬롯을 두 번 쓰면 2018-19 로스터 규정을 위반한다.
4. Dallas가 실제 Spalding을 방출했으므로 Metu도 반드시 방출된다고 쓰면 평가 차이를 삭제한다.
5. 네 직접 대결에서 상대 팀 쪽 0분이라는 사실을 Atlanta 주인공 쪽 0영향으로 확대하면 안 된다.
6. Welsh의 새 팀을 근거 없이 지정하면 드래프트 연쇄를 닫기 위해 새 역사를 창작하는 오류가 된다.

## 계산량 통제

- 새 82경기 원장: 0팀
- 계약층에서 닫힌 팀: Dallas·Denver
- 직접 대결 확인: 4경기
- 상대 팀 실제 대체 슬롯 분: 0분
- 조건부 player-game 재개: Dallas 1분 초과, Denver 36분 초과, Dallas 다른 1월 31일 방출, Welsh 새 NBA 계약

계약층에서 실제 핵심 분 침범이 없으므로 Dallas·Denver 전 시즌 승수 모델로 확장하지 않는다.

## 최종 판정

`CASCADE_CONTRACT_PASS / GAME_OUTCOMES_HOLD`

기존 Welsh 역할 보존 후보는 슬롯 중복 때문에 폐기했고, 미지명 자유계약 시장 `HOLD`로 교정했다. 나머지 연쇄는 실제 밀려난 선수의 팀별 계약·개발 슬롯 안에서 닫힌다. Atlanta donor vector는 v0.23, 실명 수취자 183.1분은 v0.24에서 닫혔으며 다음 실행은 생산성·경기 영향 prior 사전등록이다.
