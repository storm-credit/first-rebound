# Chicago 2019-20 Player-Game Donor & Starter Vector v0.1

- 상태: `PLAYER_GAME_CONSERVATION_PASS / SECOND_YEAR_ROLE_PROVISIONAL_LOCK / PRODUCTION_HOLD`
- 기준일: 2026-09-06
- 적용 범위: O-15C5 Chicago 2019-20 65경기 same-date 분·18선발 원장
- 원고 게이트: `CLOSED`

## 결론

주인공의 2년차 BASE는 **65경기·18선발·1,395분**으로 잠정 고정한다. 경기당 평균은 21분 27.7초다. O-15C4의 `63경기`는 독립적인 결장 원인이 없는 계산 후보였고, 65경기 전수 보존이 성립하므로 새 DNP 두 경기를 만들지 않는다.

이 결정은 개인 박스스코어·효율·온오프·승패를 잠그지 않는다. 경기 결과를 보지 않고 roster 역할, 실제 당일 출전자, 시즌 총분, 실제 선발 자리만 사용했다.

## 단일 원장

- `CHICAGO_2019_20_PLAYER_GAME_MINUTE_LEDGER.csv`: 65경기 주인공 분·선발·팀 총초
- `CHICAGO_2019_20_PLAYER_GAME_DONOR_VECTOR.csv`: 실제 선수별 당일 actual→alternate 분 변화
- `CHICAGO_2019_20_ROSTER_BASELINE.csv`: 실제 17명 시즌 총계
- `CHICAGO_2019_20_PROTAGONIST_MINUTE_BUDGET.csv`: 선수별 시즌 순차감 예산

NBA Stats `PlayerGameLogs`와 `BoxScoreTraditionalV3`를 2026-09-06에 조회했다. `actual_wl`은 후속 outcome join을 위한 식별값일 뿐 이번 분·선발 배정 규칙에는 사용하지 않았다.

## 주인공 65경기 역할선

| 항목 | 값 | 판정 |
|---|---:|---|
| 출전 | 65 | 실제 열린 Chicago 경기 전부 |
| 선발 | 18 | 실제 같은 날짜 선발 자리 18개 이전 |
| 총분 | 1,395:00 | O-15C4 BASE 예산과 일치 |
| 평균 | 21:27.7 | 루키 17.45분에서 제한적 상승 |
| 경기 최소~최대 | 16~31분 | bench→injury-window starter 상승 |
| bench 범위 | 16~23분 | 주전 고정 선지급 금지 |
| starter 범위 | 24~31분 | 48분 주전 역할 복사 금지 |

경기별 분은 초반 bench, Porter 이탈 뒤 11월 선발창, 12~1월 bench 성장, 2월 부상창, 시즌 말 혼합 역할의 순서로 배치했다. 전 경기 분은 정수 분으로 두어 초 단위 pseudo-precision을 만들지 않았다.

## 18선발 보존

새 선발 자리를 만들지 않았다.

| source | 경기 | 날짜 규칙 |
|---|---:|---|
| Chandler Hutchison 실제 선발 | 10 | 실제 Hutchison 선발 10경기 전부 |
| Shaquille Harrison 실제 선발 | 8 | 실제 Harrison 선발 10경기 중 시간순 최초 8경기 |
| 합계 | **18** | 경기별 Chicago 선발 5자리 유지 |

Harrison source 날짜는 2019-11-20·22·23·25, 2020-02-29, 03-02·04·06이다. 마지막 두 Harrison 선발인 03-08·10은 실제 역할 표본으로 남긴다. 이는 승패를 보고 고른 것이 아니라 시간순 규칙이다.

## 시즌 순차감과 gross 이동

O-15C4의 시즌 순차감은 그대로다.

| 선수 | actual | alternate | 시즌 순차감 |
|---|---:|---:|---:|
| Hutchison | 526:48 | 0:00 | 526:48 |
| Valentine | 487:55 | 227:55 | 260:00 |
| Harrison | 484:20 | 244:20 | 240:00 |
| Arcidiacono | 929:59 | 789:59 | 140:00 |
| Mokoka | 111:40 | 21:40 | 90:00 |
| Strus | 6:14 | 0:00 | 6:14 |
| Young | 1,590:39 | 1,458:41 | 131:58 |
| 합계 | — | — | **1,395:00** |

`0분 차감 보호`는 시즌 순감 0을 뜻한다. donor가 없는 날짜에도 65경기 출전을 성립시키려면 당일 분을 앞뒤 경기와 교환해야 한다. 최소 재배열 해에서 보호 선수 gross bridge는 다음뿐이며 시즌 총분은 모두 실제와 같다.

| 보호 선수 | 당일 차감 합 | 다른 날 반환 합 | 시즌 순감 |
|---|---:|---:|---:|
| Lauri Markkanen | 14:34 | 14:34 | 0:00 |
| Kris Dunn | 5:00 | 5:00 | 0:00 |
| 합계 | **19:34** | **19:34** | **0:00** |

LaVine·Satoransky·Coby·Porter는 시즌뿐 아니라 이번 최소 해에서 경기별 분도 변경하지 않았다. Carter·Gafford·Kornet·Felicio의 센터 분은 모든 경기에서 실제와 동일하다. Markkanen·Dunn의 19:34는 주인공에게 순차감한 생산성으로 계산하지 않고, 같은 시즌 안에서 날짜만 옮긴 receiver/debit bridge다.

## 경기별 보존

- 실제 팀 총분: **15,675:11**
- alternate 실제 선수 합 + 주인공: **15,675:11**
- 62개 regulation 경기와 3개 overtime 경기 모두 당일 총초 일치
- real-player gross debit 1,514:51 - gross credit 119:51 = 주인공 1,395:00
- 실제 없던 선수 출전일을 만들지 않음
- 각 실제 선수는 실제 출전한 날짜 안에서만 분을 이동
- 주인공은 실제 65경기 일정 안에서만 출전

## 역할 보존 방화벽

1. Valentine은 227:55, Harrison은 244:20을 남겨 슈팅 윙과 POA 수비 역할을 삭제하지 않는다.
2. Arcidiacono의 140분 순차감은 3가드 라인업 감소다. 주인공에게 포인트가드 권한을 주지 않는다.
3. Young의 131:58 순차감은 제한적인 4번 중첩이다. 그의 베테랑 리더십과 1,458:41은 유지한다.
4. Mokoka는 3경기·21:40의 NBA 표본을 남긴다. Strus의 NBA 6:14는 0이지만 two-way 계약과 ACL 사건은 삭제하지 않는다.
5. Coby의 65경기·1,674분과 LaVine의 60경기·2,085:25는 그대로다. 주인공의 성장 때문에 두 사람의 실제 분을 선취하지 않는다.

## HOLD와 다음 실행

- 주인공 2년차 공격·수비 생산성 prior
- 실제 선수의 생산성 이전량과 bridge fatigue
- 정확 개인 박스·TS·BPM proxy·온오프
- 65경기 승패·최종 standings·2020 lottery
- Patrick Williams 유지·대체 보드
- Boylen 해임과 새 프런트 오피스의 대체 세계 인과

다음은 O-15C6 생산성 prior다. 분 원장만으로 실제 22승 43패나 2020 lottery 4순위를 자동 보존하지 않는다.

## 출처

- [NBA Stats — Chicago 2019-20 선수 기록](https://www.nba.com/stats/team/1610612741/players-traditional?Season=2019-20&SeasonType=Regular%20Season)
- [NBA Stats — Box Scores](https://www.nba.com/stats/teams/boxscores?Season=2019-20&SeasonType=Regular%20Season&TeamID=1610612741)
