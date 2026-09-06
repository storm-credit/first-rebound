# Atlanta 2018-19 Named Reserve Receiver Allocation v0.1

- 상태: `ATL_RECEIVER_ALLOCATION_PASS / PRODUCTION_OUTCOME_HOLD`
- 정본성: `PROVISIONAL_LOCK`
- 원고 게이트: `CLOSED`
- 계산 권위: `simulation/ATLANTA_2018_19_CAUSALITY_LEDGER.xlsx`의 `ATL Receivers` 시트

## 결론

`ATL_REMAINDER_POOL` 183.1분을 29개 동일 날짜의 실제 Atlanta 박스스코어 명단과 대조해 네 선수에게 전부 배정한다.

| 수취자 | 실제 2018-19 분 | 추가 분 | 대체 세계 분 | 추가 출전 |
|---|---:|---:|---:|---:|
| Justin Anderson | 463 | 105.6 | 568.6 | 5경기 |
| Alex Poythress | 305 | 48.6 | 353.6 | 0경기 |
| Miles Plumlee | 173 | 17.5 | 190.5 | 1경기 |
| Daniel Hamilton | 204 | 11.4 | 215.4 | 0경기 |
| B.J. Johnson | 43 | 0.0 | 43.0 | 0경기 |
| **합계** | 1,188 | **183.1** | **1,371.1** | **6경기** |

B.J. Johnson은 후보 감사에는 포함하지만 분은 받지 않는다. 잔여분과 겹치는 유일한 2019년 3월 1일에 우선순위가 높은 Anderson이 같은 박스스코어에 있기 때문이다.

## 결과 전 사전등록 규칙

1. 수취자는 해당 날짜 ESPN Atlanta 박스스코어에 `PLAY` 또는 `DNP-CD`로 등재돼야 한다. 명단에 없으면 건너뛴다.
2. Anderson이 왼쪽 다리 재활로 빠진 첫 16경기에는 `Poythress → Hamilton → Plumlee → B.J. Johnson` 순으로 배정한다.
3. Anderson이 돌아온 2018년 11월 19일부터는 `Anderson → Poythress → Hamilton → Plumlee → B.J. Johnson` 순으로 배정한다.
4. 각 선수의 조정 경기분은 ESPN 2018-19 Atlanta 박스스코어에서 관측한 실제 단일 경기 최고분을 넘지 않는다.
5. 상한은 Anderson 31분, Poythress 26분, Hamilton 23분, Plumlee 19분, B.J. Johnson 19분이다.
6. 실제 득점·승패·점수차는 수취자와 분 선택에 사용하지 않는다.
7. Young·Huerter·Collins의 실제 분은 차감하지 않는다.

`DNP-CD`는 실제 출전이 아니라 같은 날짜 코치 결정 명단에 있었다는 가용성 증거로만 쓴다. 분을 받으면 그 날짜는 대체 세계의 새 출전으로 계산한다.

## 날짜별 배정

| 날짜 | 잔여분 | 수취자 |
|---|---:|---|
| 2018-10-21 | 7.8 | Poythress 2.0 + Plumlee 5.8 |
| 2018-10-29 | 7.3 | Plumlee 7.3 |
| 2018-10-30 | 4.4 | Plumlee 4.4 |
| 2018-11-01 | 4.5 | Poythress 4.5 |
| 2018-11-03 | 4.2 | Poythress 4.2 |
| 2018-11-06 | 0.8 | Poythress 0.8 |
| 2018-11-07 | 12.5 | Poythress 12.5 |
| 2018-11-09 | 10.7 | Poythress 10.7 |
| 2018-11-11 | 11.9 | Poythress 11.9 |
| 2018-11-15 | 10.7 | Poythress 2.0 + Hamilton 8.7 |
| 2018-11-19 | 14.1 | Anderson 14.1 |
| 2018-11-27 | 4.3 | Anderson 4.3 |
| 2018-11-28 | 5.6 | Anderson 5.6 |
| 2019-01-06 | 2.7 | Anderson 2.7 |
| 2019-01-11 | 2.9 | Anderson 2.9 |
| 2019-01-13 | 13.9 | Anderson 13.9 |
| 2019-01-15 | 5.9 | Anderson 5.9 |
| 2019-01-21 | 0.7 | Anderson 0.7 |
| 2019-01-23 | 3.6 | Anderson 3.6 |
| 2019-01-30 | 8.1 | Anderson 8.1 |
| 2019-02-01 | 2.7 | Hamilton 2.7 |
| 2019-02-04 | 13.9 | Anderson 13.9 |
| 2019-02-10 | 10.3 | Anderson 10.3 |
| 2019-02-14 | 1.1 | Anderson 1.1 |
| 2019-02-22 | 2.7 | Anderson 2.7 |
| 2019-02-23 | 5.5 | Anderson 5.5 |
| 2019-02-25 | 4.0 | Anderson 4.0 |
| 2019-02-27 | 3.4 | Anderson 3.4 |
| 2019-03-01 | 2.9 | Anderson 2.9 |

29개 날짜의 잔여분과 31개 배정 행은 모두 0.0분 오차로 닫힌다. 실제 Atlanta 공개 정수 선수분 19,853분에서도 Spellman 805분을 제거하고 주인공 621.9분과 실명 수취자 183.1분을 더하면 다시 19,853분이다.

## 아직 열지 않는 것

- 주인공과 네 수취자의 경기별 득점·리바운드·슈팅·온오프
- 추가 출전이 선수 피로·부상·후속 가용성에 미치는 영향
- 경기 전 승률 `pB`와 rotation/availability/fatigue 계수
- 대체 승패·상대팀 기록·전체 순위·2019 로터리

따라서 다음 단계는 분을 다시 바꾸는 것이 아니라 **선수 생산성과 경기 영향 prior를 결과 전에 고정하는 것**이다.

## 출처

- [ESPN — Atlanta 2018-19 schedule and box scores](https://www.espn.com/nba/team/schedule/_/name/atl/season/2019)
- [Atlanta Hawks — Justin Anderson 2018-19 review](https://www.nba.com/hawks/features/five-things-know-about-justin-andersons-2018-19-season)
- [Atlanta Hawks — Alex Poythress 2018-19 review](https://www.nba.com/hawks/five-things-know-about-alex-poythress-2018-19-season)
