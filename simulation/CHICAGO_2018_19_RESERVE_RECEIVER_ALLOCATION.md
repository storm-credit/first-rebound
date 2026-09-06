# Chicago 2018-19 Reserve Receiver Allocation v1.0

- 상태: `RECEIVER_ALLOCATION_PASS / SEASON_LINE_PROVISIONAL_LOCK / OUTCOMES_HOLD`
- 상위 원장: `simulation/CHICAGO_2018_19_PLAYER_GAME_DONOR_VECTOR.md`
- 검산: `node tools/verify_chicago_2018_19_ledger.mjs`
- 원고 게이트: `CLOSED`

## 결론

Hutchison이 Chicago에서 사라지는 894:37과 주인공 1,274:02의 차이는 실제 선수들의 순차감 **379:25**와 맞는다.

```text
실제 Hutchison 894:37
+ 실제 선수 순차감 379:25
= 주인공 1,274:02
```

시즌선은 **73경기·11선발·1,274:02·평균 17.45분**을 `PROVISIONAL_LOCK`으로 올린다. 개인 득점·리바운드·효율·승패는 잠그지 않는다.

## A. 주인공이 빠진 네 경기 — 실존 선수 수취 96:35

| 날짜 | 사유 | 반환 슬롯 | 같은 날짜 수취 |
|---|---|---:|---|
| 2018-12-07 | 자기관리 실패 | 11:35 | Harrison +5:00 · Parker +6:35 |
| 2019-01-09 | Windy City 배정으로 서부 원정 제외 | 30:24 | Harrison +7:00 · Selden +7:00 · Blakeney +8:00 · Portis +8:24 |
| 2019-01-11 | Windy City 홈 경기와 NBA 원정 충돌 | 29:27 | Harrison +7:00 · Selden +7:00 · Blakeney +7:00 · Portis +8:27 |
| 2019-01-12 | Windy City 홈 경기와 NBA 원정 충돌 | 25:09 | Harrison +8:00 · Selden +8:00 · Parker +9:09 |
| 합계 | — | **96:35** | **96:35** |

이는 실존 선수의 실제 성과를 주인공에게 넘기는 차감이 아니라, 주인공이 NBA 경기에 없어서 생긴 분을 실제 당일 출전 선수에게 돌려주는 수취다. 추가 생산과 피로는 승패 원장에서 별도로 계산한다.

## B. Hutchison 부상 뒤 33경기 — 주인공 수취 476분

규칙:

1. 그 날짜 Chicago 경기에 실제 출전한 선수만 donor가 된다.
2. 한 선수의 단일 경기 차감은 6분 이하이다.
3. 차감 뒤 해당 경기 실제 출전분을 최소 6분 남긴다.
4. 핵심 9인의 분은 차감하지 않는다.
5. 2월 22일과 3월 5일은 안전한 donor가 두 명뿐이므로 12분으로 낮춘다. 2월 25일·3월 3·10·12일은 donor가 넓어 15분으로 보완한다. 결과·점수차는 선택 근거가 아니다.

| 날짜 | 주인공 분 | 같은 날짜 실제 donor 차감 |
|---|---:|---|
| 2019-01-27 | 12 | Selden -4 · Harrison -3 · Blakeney -5 |
| 2019-01-29 | 12 | Selden -6 · Harrison -5 · Blakeney -1 |
| 2019-01-30 | 12 | Selden -4 · Harrison -3 · Brandon Sampson -5 |
| 2019-02-02 | 12 | Selden -4 · Harrison -3 · Brandon Sampson -5 |
| 2019-02-06 | 12 | Selden -5 · Harrison -4 · Luwawu-Cabarrot -3 |
| 2019-02-08 | 14 | Selden -6 · Harrison -4 · Luwawu-Cabarrot -4 |
| 2019-02-09 | 14 | Selden -5 · Harrison -5 · Luwawu-Cabarrot -4 |
| 2019-02-11 | 14 | Selden -6 · Harrison -4 · Luwawu-Cabarrot -4 |
| 2019-02-13 | 14 | Selden -5 · Harrison -5 · Luwawu-Cabarrot -4 |
| 2019-02-22 | 12 | Selden -6 · Harrison -6 |
| 2019-02-23 | 14 | Selden -5 · Harrison -5 · Luwawu-Cabarrot -4 |
| 2019-02-25 | 15 | Selden -4 · Harrison -3 · Blakeney -5 · Luwawu-Cabarrot -3 |
| 2019-02-27 | 14 | Selden -6 · Harrison -6 · Luwawu-Cabarrot -2 |
| 2019-03-01 | 14 | Selden -5 · Harrison -5 · Luwawu-Cabarrot -4 |
| 2019-03-03 | 15 | Selden -4 · Harrison -3 · Blakeney -5 · Luwawu-Cabarrot -3 |
| 2019-03-05 | 12 | Selden -6 · Harrison -6 |
| 2019-03-06 | 14 | Selden -6 · Harrison -4 · Luwawu-Cabarrot -4 |
| 2019-03-08 | 14 | Selden -5 · Harrison -5 · Luwawu-Cabarrot -4 |
| 2019-03-10 | 15 | Selden -4 · Harrison -3 · Blakeney -5 · Luwawu-Cabarrot -3 |
| 2019-03-12 | 15 | Selden -4 · Harrison -3 · Blakeney -5 · Luwawu-Cabarrot -3 |
| 2019-03-15 | 14 | Selden -5 · Harrison -5 · Luwawu-Cabarrot -4 |
| 2019-03-17 | 16 | Selden -4 · Harrison -4 · Blakeney -5 · Luwawu-Cabarrot -3 |
| 2019-03-18 | 16 | Selden -4 · Harrison -4 · Blakeney -5 · Luwawu-Cabarrot -3 |
| 2019-03-20 | 16 | Selden -4 · Harrison -4 · Blakeney -5 · Luwawu-Cabarrot -3 |
| 2019-03-23 | 16 | Selden -3 · Harrison -3 · Blakeney -4 · Luwawu-Cabarrot -2 · Brandon Sampson -4 |
| 2019-03-26 | 16 | Selden -3 · Harrison -3 · Blakeney -4 · Luwawu-Cabarrot -2 · Brandon Sampson -4 |
| 2019-03-27 | 16 | Selden -2 · Harrison -2 · Blakeney -3 · Luwawu-Cabarrot -1 · Alkins -5 · Brandon Sampson -3 |
| 2019-03-30 | 16 | Selden -2 · Harrison -2 · Blakeney -3 · Luwawu-Cabarrot -1 · Alkins -5 · Brandon Sampson -3 |
| 2019-04-01 | 16 | Selden -2 · Harrison -2 · Blakeney -3 · Luwawu-Cabarrot -1 · Brandon Sampson -2 · JaKarr Sampson -6 |
| 2019-04-03 | 16 | Selden -2 · Harrison -1 · Luwawu-Cabarrot -1 · Alkins -4 · Brandon Sampson -2 · JaKarr Sampson -6 |
| 2019-04-06 | 16 | Selden -2 · Harrison -1 · Luwawu-Cabarrot -1 · Alkins -4 · Brandon Sampson -2 · JaKarr Sampson -6 |
| 2019-04-09 | 16 | Selden -2 · Harrison -1 · Luwawu-Cabarrot -1 · Alkins -4 · Brandon Sampson -2 · JaKarr Sampson -6 |
| 2019-04-10 | 16 | Selden -2 · Harrison -2 · Blakeney -3 · Luwawu-Cabarrot -1 · Alkins -5 · Brandon Sampson -3 |
| 합계 | **476** | **476** |

## C. 선수별 순변화

| 선수 | A 수취 | B 차감 | 순변화 | 실제 역할 보존 |
|---|---:|---:|---:|---|
| Wayne Selden Jr. | +22:00 | -137:00 | -115:00 | 868.8분 수준, 후반 주요 윙 유지 |
| Shaquille Harrison | +27:00 | -119:00 | -92:00 | 1,338.0분 수준, 수비 가드/윙 유지 |
| Antonio Blakeney | +15:00 | -61:00 | -46:00 | 783.0분 수준, 벤치 득점원 유지 |
| Timothé Luwawu-Cabarrot | — | -73:00 | -73:00 | 473.4분 수준, 후반 윙 실험 유지 |
| Rawle Alkins | — | -27:00 | -27:00 | 93.4분 수준, 투웨이 기회 유지 |
| Brandon Sampson | — | -35:00 | -35:00 | 179.3분 수준, 투웨이 기회 유지 |
| JaKarr Sampson | — | -24:00 | -24:00 | 103.3분 수준, 10일 계약 기회 유지 |
| Jabari Parker | +15:44 | — | +15:44 | 거래 전 역할·자산 유지 |
| Bobby Portis | +16:51 | — | +16:51 | 거래 전 역할·자산 유지 |
| 합계 | **+96:35** | **-476:00** | **-379:25** | player-minutes 보존 |

## 남은 HOLD

- 주인공과 수취자·donor의 같은 날짜 생산성·피로·승패 영향
- 정확한 득점·리바운드·슈팅·온오프
- 22승 60패, Hoiberg 해임, Holiday·Porter 거래가 유지되는지 여부
- Windy City 두 경기 개인 박스와 G League 승패

## 자료 기준

- NBA Stats의 2018-19 Chicago 선수 총계와 player game log
- Basketball Reference의 Chicago 팀 총계와 Hutchison game log
- 실제 경기 결과·점수차는 allocation 선택에 사용하지 않았다.
