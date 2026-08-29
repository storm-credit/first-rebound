# Atlanta 2018-19 Player-Game Donor Vector v0.1

- 상태: `ATL_DONOR_VECTOR_PASS / OUTCOME_HOLD`
- 정본성: `PROVISIONAL_LOCK`
- 원고 게이트: `CLOSED`
- 계산 권위: `simulation/ATLANTA_2018_19_CAUSALITY_LEDGER.xlsx`

## 결론

주인공의 NBA 신인 기준선은 **43경기·621.9분·평균 14.46분·0선발**로 잠근다. 실제 Omari Spellman의 46경기·805.0분을 그대로 복사하지 않고, 경기 전 공개 정보만으로 재현 가능한 다음 규칙을 사용했다.

1. 실제 Spellman 분이 7.0분 이상인 날짜만 1차 출전 후보로 둔다.
2. 후보 경기의 주인공 분은 `MIN(16.0, Spellman 실제 분)`이다.
3. 2018년 11월 19일은 자기관리 실패로 예정된 14.1분 로테이션 기회를 잃어 0분이다.
4. 실제 결과·점수차·승패는 날짜나 분 선택에 사용하지 않는다.
5. Spellman의 실제 선발 11회와 부상은 주인공에게 복사하지 않는다.

이 규칙은 44개 후보·636.0분을 만든다. 11월 19일의 직접 비용 14.1분을 빼면 43경기·621.9분이다.

## 805분 보존

| 항목 | 분 | 기능 |
|---|---:|---|
| 실제 Spellman donor | 805.0 | Atlanta에서 사라진 1차 슬롯 |
| 주인공 | 621.9 | 날짜별 `DIRECT` 출전 |
| `ATL_REMAINDER_POOL` | 183.1 | 아직 이름을 붙이지 않은 동일 날짜 Atlanta 수취 분 |
| 차이 | 0.0 | 82경기 전부 분 보존 |

`ATL_REMAINDER_POOL`은 가상 선수가 아니라 감사용 회계 브리지다. Justin Anderson·Alex Poythress·B.J. Johnson 등 실제 수취자를 날짜별로 확정하기 전까지 개인 박스스코어를 만들지 않는다. Young·Huerter·Collins의 실제 육성 분은 보호한다.

접촉 분류는 `DIRECT 43 / ROSTER 39`다. `ROSTER` 경기에도 Spellman 부재와 잔여분 재배분이 있으므로 `IDENTICAL`은 없다.

## 자기관리 비용

- 날짜: **2018-11-19, Atlanta 홈 vs Los Angeles Clippers**
- 선택 기준: 다구간 원정 뒤 첫 홈 경기이며 아침 영상·컨디셔닝 일정이 성립하는 날짜
- 예정 분: 14.1분
- 실제 배정: 0분, `MISSED_ROTATION`
- 원인: 전날 밤 게임 뒤 일정 지각
- 금지: 경기 결과를 보고 접전·승리·패배를 골라 비용을 조정하는 것

직접 비용은 이 한 경기의 NBA 기회 상실이다. 감동 연설이나 게임 삭제로 해결하지 않고, 이후 준비 순서를 회복하는 성장 근거로만 쓴다.

## Erie 개발 배정

- 배정 창: **2018-12-07 ~ 2018-12-22**
- 계약: Atlanta 1라운드 rookie-scale 계약 유지
- 기능: 닫힌 NBA 자리 대신 실전 반복을 주는 개발 결정
- 경기: 6경기
- 분 안전선: 경기당 24~30분
- 정확한 G League 개인 박스스코어: `HOLD`

| 날짜 | 장소 | 상대 |
|---|---|---|
| 2018-12-08 | 원정 | South Bay Lakers |
| 2018-12-10 | 원정 | Stockton Kings |
| 2018-12-13 | 원정 | Agua Caliente Clippers |
| 2018-12-15 | 원정 | Santa Cruz Warriors |
| 2018-12-19 | 홈 | Texas Legends |
| 2018-12-21 | 원정 | Northern Arizona Suns |

동일 날짜 Atlanta 경기에서는 주인공 NBA 분이 모두 0이므로 NBA/Erie 이중 출전은 없다. 이 배정은 11월 19일의 직접 징계가 아니며, 실제 Spellman의 12월 오른쪽 엉덩이 부상·컨디셔닝 배정을 복사하지 않는다.

## 아직 열지 않는 것

- 주인공의 경기별 득점·리바운드·슈팅·온오프
- `ATL_REMAINDER_POOL` 183.1분의 실명 수취자
- 경기 전 승률과 영향 prior
- 대체 승패·상대팀 기록·전체 순위
- 2019 로터리·Dallas 보호픽·대안 드래프트

다음 단계는 183.1분을 동일 날짜 실제 가용 포워드에게 배분하는 것이다. 그 검산이 끝난 뒤에만 사전등록된 경기 영향 모델을 실행한다.

## 출처

- [HoopsStats — Omari Spellman 2018-19 game log](https://www.hoopsstats.com/basketball/fantasy/nba/atlanta-hawks/players/omari-spellman/gamelog/19/1/16)
- [RealGM — Omari Spellman profile](https://basketball.realgm.com/player/Omari-Spellman/Summary/74078)
- [Peachtree Hoops — Spellman Erie assignment context](https://www.peachtreehoops.com/2018/12/30/18161520/omari-spellman-alex-poythress-atlanta-hawks-g-league-erie-bayhawks-assignment-transfer-roster)
- [Basketball-Reference — Erie 2018-19 schedule](https://www.basketball-reference.com/gleague/schedules/HAW/2019.html)
- [Atlanta Hawks — Spellman ankle injury update](https://www.nba.com/hawks/news/omari-spellman-injury-update)
