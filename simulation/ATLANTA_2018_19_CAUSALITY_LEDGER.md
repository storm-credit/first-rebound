# Atlanta 2018-19 Causality Ledger v0.4

- 상태: `ATL_DONOR_VECTOR_PASS / COUNTERFACTUAL_OUTCOMES_HOLD`
- 정본성: `PROVISIONAL`
- 원고 게이트: `CLOSED`
- 계산 파일: `simulation/ATLANTA_2018_19_CAUSALITY_LEDGER.xlsx`
- 재현 스크립트: `tools/build_atlanta_2018_19_ledger.mjs`
- 검증 스크립트: `tools/verify_atlanta_ledger.mjs`

## 이번 단계에서 확정한 것

Atlanta의 실제 2018-19 정규시즌 82경기를 시간순으로 원장화했다.

| 검산 | 값 | 판정 |
|---|---:|---|
| 경기 | 82 | PASS |
| 승패 | 29승 53패 | PASS |
| Atlanta 득점 | 9,294 | PASS |
| 연장 포함 경기 총 선수분 | 19,855 | PASS |
| 공개 로스터 정수 선수분 합계 | 19,853 | PASS_WITH_2_MIN_ROUNDING_DELTA |

경기 총 선수분은 `240 + 25 × 연장 횟수`로 계산한다. 실제 시즌에는 1연장 3경기와 4연장 1경기가 있어 총 19,855분이다. 공개 선수별 정수 분의 2분 차이는 원자료 반올림 오차로만 보며 새 출전시간으로 사용하지 않는다.

## 로테이션 방화벽

주인공은 실제 30순위 Omari Spellman을 대신해 Atlanta에 들어간다. 따라서 공짜 로스터 자리나 공짜 출전시간을 만들지 않는다.

| 항목 | 실제 기준선 | R09 안전선 |
|---|---:|---:|
| Spellman | 46경기·11선발·805분 | 대체 슬롯 상한 805분 |
| 주인공 | 없음 | **43경기·621.9분·14.46 MPG·0선발** |
| Erie | Spellman 3경기 | **2018-12-07~22, 6경기·24~30 MPG** |

경기별 가용성은 `Spellman donor ≥7.0분 → MIN(16.0, donor)` 규칙으로 잠갔다. 2018년 11월 19일은 밤샘 게임 뒤 아침 일정 지각으로 예정된 14.1분을 잃는다. 결과를 보지 않고 적용한 뒤 43경기·621.9분이 된다.

1차 donor는 Spellman 한 명이다. 805.0분은 주인공 621.9분과 `ATL_REMAINDER_POOL` 183.1분으로 날짜별 완전 분할한다. 회계 브리지는 가상 선수가 아니며, Justin Anderson·Alex Poythress·B.J. Johnson 등 실명 수취자는 같은 날짜 가용성 증거가 있을 때만 배정한다. Trae Young·Kevin Huerter·John Collins의 핵심 육성 분은 보호한다.

Spellman의 실제 11선발, 3월 1일 발목 부상, 시즌 종료 결장은 주인공에게 자동 복사하지 않는다.

## 82경기 접촉 판정

주인공이 DNP이거나 Erie에 있어도 그 경기가 자동 비접촉이 되지 않는다. 주인공의 지명으로 Spellman이 Atlanta에 없고, 그의 실제 분은 누군가에게 재배분되기 때문이다.

| contact_type | 뜻 |
|---|---|
| `DIRECT` | 주인공이 NBA 경기에 출전 |
| `ROSTER` | 주인공은 미출전이지만 Spellman 부재·분 재배분이 존재 |
| `CASCADE` | 앞선 출전·피로·부상·거래·휴식 변화가 현재 경기에 도달 |
| `IDENTICAL` | 모든 선수 상태와 분이 실제와 동일하다는 증명이 있을 때만 허용 |

현재 분류는 `DIRECT 43 / ROSTER 39`다. 82경기 모두 donor 또는 로스터 부재 접촉이 있으므로 `IDENTICAL`은 없다.

## 승패 계산 사전등록

현 단계에서는 대체 점수와 승패를 만들지 않았다. 접전만 골라 뒤집는 방식은 금지한다.

향후 한 방식만 사용한다.

```text
logit(pCF) = logit(pB) + Δμ / k
Δμ = rotation + availability + delta-fatigue + validated interaction
```

- `pB`는 경기 전 정보만 사용하는 사전 승률이다.
- 실제 최종 점수나 승패를 보고 계수를 조정하지 않는다.
- 실제 결과에 조건부인 고정 latent `u`를 game hash로 만들고 low/base/high가 같은 `u`를 공유한다.
- 입력이 불변이면 실제 82경기를 전부 재현해야 한다.
- 시나리오별 결과가 갈리면 `SENSITIVE/HOLD`로 둔다.
- possession/PBP 모델 없이 정확한 대체 점수는 쓰지 않는다.

## 2019 Draft 연결부

실제 기준선은 Atlanta 29승 53패, 자체픽 사전 역순위 5번 확률군, 실제 로터리 8번이다. Dallas는 33승 49패, 사전 9번 슬롯, 실제 10번이었고 2019 top-5 보호를 벗어나 Atlanta로 양도됐다.

두 팀의 2018-19 직접 대결은 1승 1패다.

- 2018-10-24: Atlanta 111-104 Dallas
- 2018-12-12: Dallas 114-107 Atlanta

두 번째 경기가 바뀌면 Atlanta에 1승을 더하는 것만으로 끝나지 않는다. Dallas에도 1패를 더해 동률·로터리 조합·top-5 보호 가능성을 다시 계산해야 한다.

## 최종 판정을 막는 선행조건

Atlanta 단독 계산만으로 2019 standings와 lottery를 `FINAL`로 만들 수 없다.

1. 2018 Draft 30~60의 27개 유지·4개 변경 보드를 보존한다.
2. Spellman의 Spurs, Metu의 Dallas, Spalding의 Denver 계약·로스터 기준선은 연결 완료했다.
3. Spurs 145.4분·Dallas 1분·Denver 36분을 넘거나 경쟁 구간 출전이 생길 때만 해당 팀 경기별 파급을 연다.
4. 모든 바뀐 경기에서 승자·패자의 승패를 함께 갱신한다.
5. 비플레이오프 14팀, 동률, 조합 배분, 별도 동률 추첨을 재계산한다.
6. 로터리 입력이 바뀌면 잠긴 seed로 재추첨한다.
7. Dallas pick의 top-5 보호·양도 여부를 판정한다.
8. 그 뒤에만 Atlanta의 지명·거래 보드를 다시 연다.

따라서 현재 판정은 `ATL_DONOR_VECTOR_PASS / COUNTERFACTUAL_OUTCOMES_HOLD`다. Atlanta 날짜별 주인공 분은 닫혔지만 183.1분의 실명 수취자·개인 성과·승패·상대팀 기록 전에는 시즌 결과를 선언하지 않는다.

## Atlanta player-game 실행 기준선

- 주인공: 43경기·621.9분·14.46 MPG·0선발
- 자기관리 비용: 2018-11-19 Clippers전 예정 14.1분 → 0분
- Erie: 2018-12-07~22, 실제 일정 6경기, NBA 동일 날짜 출전 0
- Atlanta remainder: 183.1분, 실명 수취자 `HOLD`
- 상세 권위: `simulation/ATLANTA_2018_19_PLAYER_GAME_DONOR_VECTOR.md`

## Spurs 두 번째 팀 기준선

- 실제 Metu: NBA 29경기·145.4분, Austin 26경기·710.4분
- Spellman BASE: 29경기·145.4분·0선발
- 허용 범위: 24~31경기·120~180분
- 145.4분 초과: 날짜별 donor와 경쟁 구간 검토 필수
- Atlanta 직접 대결 2경기: Metu 0분, Spurs 쪽 `NO_DIRECT_MINUTES`
- 상세 권위: `simulation/SPURS_2018_19_SECOND_TEAM_IMPACT.md`

## Dallas·Denver 연쇄 계약 기준선

- Dallas Metu BASE: 표준 NBA 계약·Texas assignment, NBA 1경기·1분, Texas 29경기
- Denver Spalding BASE: Welsh 투웨이 슬롯, NBA 11경기·36분, G League 20경기
- Denver의 다른 투웨이 자리: DeVaughn Akoon-Purcell 유지
- Welsh: Denver 투웨이 중복 금지, 미지명 자유계약 시장 `HOLD`
- Atlanta 직접 대결 네 경기: 실제 Spalding/Welsh 0분, 상대 팀 쪽 `NO_DIRECT_MINUTES`
- Dallas 1월 31일 방출 선택: `HOLD`
- 상세 권위: `simulation/DALLAS_DENVER_2018_19_CASCADE_IMPACT.md`

## 출처

- [NBA Stats — Atlanta 2018-19 schedule](https://www.nba.com/stats/team/1610612737/schedule?Season=2018-19)
- [NBA Stats — Atlanta 2018-19 player totals](https://www.nba.com/stats/players/traditional?Season=2018-19&SeasonType=Regular%20Season&TeamID=1610612737&PerMode=Totals)
- [Atlanta Hawks — Omari Spellman injury update](https://www.nba.com/hawks/news/omari-spellman-injury-update)
- [NBA G League — Omari Spellman](https://gleague.nba.com/player/1629016)
- [Atlanta Hawks — 2019 lottery odds and Dallas pick protection](https://www.nba.com/hawks/features/hawks-lottery-odds-explained)
- [NBA Communications — 2019 draft tiebreakers](https://pr.nba.com/2019-nba-draft-tiebreakers/)
- [NBA — actual 2019 lottery result](https://www.nba.com/news/pelicans-win-nba-draft-lottery)
- [Atlanta Hawks — 2018-10-24 Dallas game](https://www.nba.com/hawks/game/0021800052-mavericks-vs-hawks-atlanta-ga-10-24-2018)
- [Dallas Mavericks — 2018-12-12 Atlanta game](https://www.nba.com/mavs/mavs-get-a-spark-from-carlisle-and-rallied-for-a-114-107-victory-over-the-hawks)
- [HoopsStats — Omari Spellman 2018-19 game log](https://www.hoopsstats.com/basketball/fantasy/nba/atlanta-hawks/players/omari-spellman/gamelog/19/1/16)
- [RealGM — Omari Spellman profile](https://basketball.realgm.com/player/Omari-Spellman/Summary/74078)
- [Basketball-Reference — Erie 2018-19 schedule](https://www.basketball-reference.com/gleague/schedules/HAW/2019.html)
