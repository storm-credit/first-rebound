# Chicago 2019-20 Roster & Minute Baseline v0.1

- 상태: `PLAYER_GAME_CONSERVATION_PASS / SECOND_YEAR_ROLE_PROVISIONAL_LOCK`
- 기준일: 2026-09-06
- 적용 범위: O-15C4 Chicago 2019-20 실제 roster·총분·선발·부상·주인공 2년차 분 예산
- 선행 정본: 2019 lottery 7순위·Coby White 지명 `LOCKED`
- 원고 게이트: `CLOSED`

## 결론

실제 Chicago는 2019-20 정규시즌 65경기에서 22승 43패를 기록했고 재개 시즌 22개 팀에 포함되지 않았다. NBA Stats player game log를 초 단위로 합산하면 17명의 실제 출전자는 총 **15,675분 11초**, 선발 자리는 **325개**다.

대체 세계선의 1차 차이는 Chandler Hutchison이 Chicago에 없고 같은 2018 1라운드 표준계약 슬롯에 주인공이 있다는 점이다. Hutchison의 실제 28경기·10선발·526분 48초는 직접 대체 슬롯이지만, 그의 부상과 경기별 출전은 주인공에게 복사하지 않는다.

주인공 2년차의 사전 범위와 O-15C5 검산 결과는 다음과 같다.

| 항목 | LOW | BASE | HIGH | 상태 |
|---|---:|---:|---:|---|
| 출전 | 60경기 | 65경기 | 65경기 | BASE `PROVISIONAL_LOCK` |
| 선발 | 14경기 | 18경기 | 22경기 | `CANDIDATE` |
| 총분 | 1,320분 | 1,395분 | 1,470분 | BASE `PROVISIONAL_LOCK` |
| 출전 경기 평균 | 22.00분 | 21.46분 | 22.62분 | 산술값 |

BASE 1,395분은 82경기 환산 약 1,760분이다. 루키 평균 17.45분에서 약 21.46분으로 오르는 분명한 2년차 상승이지만, 주전 고정이나 공격 제1옵션을 선지급하지 않는다. O-15C5가 65경기 전수 same-date 보존을 통과했으므로 독립 원인 없는 두 경기 결장은 만들지 않는다.

## 1. 실제 시즌 경계

- 실제 최종 경기: 2020-03-10 Cleveland전
- 실제 결과: 65경기·22승 43패·동부 11위
- 전체 선수 분: 15,675:11
- 전체 선발 자리: 325 = 65경기 × 5
- 2020 재개 시즌: Chicago 불참

82경기 예정표의 취소된 17경기를 가상으로 복원하지 않는다. 대체 승수·2020 standings·lottery도 실제로 열린 65경기 안에서만 계산한다.

## 2. 실제 roster 총분

정확 행은 `simulation/CHICAGO_2019_20_ROSTER_BASELINE.csv`가 단일 원장이다.

| 선수 | G/GS | 총분 | 기능 | 대체 세계 처리 |
|---|---:|---:|---|---|
| Zach LaVine | 60/60 | 2,085:25 | 주득점원 | 0분 차감 |
| Tomas Satoransky | 65/64 | 1,877:58 | 1차 가드 | 0분 차감 |
| Coby White | 65/1 | 1,674:00 | 신인 가드 | 0분 차감 |
| Thaddeus Young | 64/16 | 1,590:39 | 베테랑 포워드 | 제한 차감 |
| Lauri Markkanen | 50/50 | 1,491:37 | 코어 슈팅 빅 | 0분 차감 |
| Kris Dunn | 51/32 | 1,268:40 | POA 수비 가드 | 0분 차감 |
| Wendell Carter Jr. | 43/43 | 1,255:49 | 코어 센터 | 0분 차감 |
| Ryan Arcidiacono | 58/4 | 929:59 | 예비 가드 | 제한 차감 |
| Daniel Gafford | 43/7 | 609:03 | 신인 센터 | 0분 차감 |
| Luke Kornet | 36/14 | 558:34 | 슈팅 센터 | 0분 차감 |
| Chandler Hutchison | 28/10 | 526:48 | 실제 윙 슬롯 | 전량 직접 대체 |
| Denzel Valentine | 36/5 | 487:55 | 슈팅 윙 | 2차 donor |
| Shaquille Harrison | 43/10 | 484:20 | 수비·에너지 윙 | 2차 donor |
| Cristiano Felicio | 22/0 | 385:43 | 예비 센터 | 0분 차감 |
| Otto Porter Jr. | 14/9 | 330:47 | 주전 윙 | 0분 차감 |
| Adam Mokoka | 11/0 | 111:40 | 투웨이 윙 | 후순위 donor |
| Max Strus | 2/0 | 6:14 | 투웨이 윙 | 후순위 donor |

## 3. 2019 여름 roster 사건

2019 Draft에서 Coby White 7순위와 Daniel Gafford 38순위는 유지한다. 이후 Chicago의 실제 주요 보강 기능도 현재 단계에서는 유지한다.

| 사건 | 기능 | 판정 |
|---|---|---|
| Tomas Satoransky sign-and-trade | 장신 1차 볼 운반·LaVine 보조 | `RETENTION_PASS` |
| Thaddeus Young 계약 | 베테랑 포워드·프런트코트 깊이 | `RETENTION_PASS` |
| Luke Kornet 계약 | 슈팅 가능한 예비 센터 | `RETENTION_PASS` |
| Ryan Arcidiacono 재계약 | 안정적 예비 가드 | `RETENTION_PASS` |
| Shaquille Harrison 재계약 | 수비·에너지 윙 깊이 | `RETENTION_LEAN` |

주인공은 2019년 아직 주된 가드도 센터도 아니다. 따라서 Satoransky·Kornet 영입을 제거할 직접 인과가 없다. Harrison은 역할이 가장 겹치지만 최소계약급 깊이와 POA 수비 기능이 달라 자동 방출하지 않는다.

## 4. 실제 부상으로 생긴 역할 창

| 선수 | 실제 사건 | 설계 의미 |
|---|---|---|
| Otto Porter Jr. | 2019-11-06 뒤 왼발 부상, 이후 작은 골절 확인; 14경기 출전 | 주인공의 윙 분 확대 창이지만 Porter의 330:47은 보호 |
| Wendell Carter Jr. | 2020-01-06 오른발목 염좌, 4~6주 예상 | 센터 분을 주인공에게 직접 주지 않음 |
| Lauri Markkanen | 2020-01-23 오른쪽 골반 조기 스트레스 반응, 4~6주 예상 | 제한적 4번 분 가능, 실제 코어 분은 보호 |
| Kris Dunn | 2020-01-31 오른쪽 MCL 염좌, 남은 시즌 결장 | POA 수비 필요가 커지지만 가드 분 자동 상속 금지 |
| Chandler Hutchison | 2020-02-11 오른어깨 악화, 이후 수술 결정 | 활성 세계선에는 선수가 없으므로 부상 자체는 비접촉 사건 |

부상은 주인공 성장 버튼이 아니다. 실제 선수의 출전분은 우선 보존하고, 당시 저·중역할 윙의 같은 날짜 분을 재배분한다.

## 5. BASE 1,395분 예산

`simulation/CHICAGO_2019_20_PROTAGONIST_MINUTE_BUDGET.csv`의 합계가 단일 산술 권위다.

| 출처 | 이전량 | 남는 실제 분 | 보호 기능 |
|---|---:|---:|---|
| Hutchison 직접 슬롯 | 526:48 | 0 | 선수를 삭제하는 것이 아니라 변경 팀 경로에 둠 |
| Valentine | 260:00 | 227:55 | 슈팅 윙 표본 유지 |
| Harrison | 240:00 | 244:20 | POA·에너지 수비 표본 유지 |
| Arcidiacono | 140:00 | 789:59 | 예비 볼 운반·조직 기능 유지 |
| Mokoka | 90:00 | 21:40 | roster·투웨이 존재 유지 |
| Strus | 6:14 | 0 | roster·부상 사건은 유지, NBA 출전만 0 후보 |
| Young | 131:58 | 1,458:41 | 베테랑 포워드·리더십·프런트코트 기능 유지 |
| **합계** | **1,395:00** |  |  |

직접 슬롯 밖의 추가 이전은 868분 12초다. LaVine·Satoransky·Coby·Markkanen·Dunn·Carter·Porter·Gafford·Kornet·Felicio의 시즌 순감은 BASE에서 0이다. O-15C5에서 donor가 희박한 날짜를 연결하기 위해 Markkanen·Dunn의 19:34를 다른 경기로 옮겼지만, 두 선수의 시즌 총분은 전부 반환한다.

## 6. 2년차 역할과 성장 기능

2019-20의 핵심 신기술은 기존 성장 사다리대로 **약한 손 운반과 클로즈아웃 돌파**다. 보조 연결 기술은 감속 뒤 짧은 패스까지만 허용한다.

- 수비 리바운드 뒤: 열린 길이면 두세 번 직접 전진
- 첫 벽이 서면: Coby 또는 Satoransky에게 조기 이양
- 하프코트: 코너 대기만 반복하지 않고 클로즈아웃을 약한 손으로 공격
- 도움수비가 두 번째로 오면: 아직 공격이 자주 끝나는 결함 유지
- 2020-21 핵심인 완성형 grab-and-go·숏롤 첫 패스를 앞당기지 않음

공존 우선순위는 `주인공 리바운드 → 직접 전진 가능 여부 판단 → Coby/Satoransky 조기 이양 → LaVine 1차 마무리`다. 주인공을 포인트가드로 만들거나 Coby의 신인 개발 possession을 빼앗지 않는다.

## 7. O-15C5 player-game 연결

- 주인공: 65경기·18선발·1,395:00 `PROVISIONAL_LOCK`
- 65경기 팀 총분 15,675:11 전수 보존
- 선발 source: 실제 Hutchison 10자리 + 실제 Harrison 시간순 최초 8자리
- 보호 10인 시즌 순감 0; 센터 4인과 LaVine·Satoransky·Coby·Porter 경기별 분 변경 0
- 권위: `simulation/CHICAGO_2019_20_PLAYER_GAME_DONOR_VECTOR.md`

## 8. 다음 계산 전 HOLD

- 개인 박스·TS·BPM proxy·온오프
- 정확 승수와 2020 standings·lottery
- Patrick Williams 유지·대체 지명
- Boylen 해임과 새 프런트 오피스 인과 변화

O-15C6A의 생산성 prior 권위는 `simulation/CHICAGO_2019_20_PLAYER_PRODUCTION_PRIORS.md`다.

## 출처

- [NBA Stats — Chicago 2019-20 선수 기록](https://www.nba.com/stats/team/1610612741/players-traditional?Season=2019-20&SeasonType=Regular%20Season)
- [Chicago Bulls — Satoransky 영입](https://www.nba.com/bulls/news/release-title)
- [Chicago Bulls — Thaddeus Young 계약](https://www.nba.com/bulls/news/bulls-sign-thaddeus-young)
- [Chicago Bulls — Arcidiacono 재계약](https://www.nba.com/bulls/bulls-re-sign-arcidiacono)
- [Chicago Bulls — Kornet·Harrison 2019 역할](https://www.nba.com/bulls/features/luke-kornet-bring-high-basketball-iq-and-three-point-shooting-bulls)
- [NBA — Otto Porter Jr. 왼발 골절](https://www.nba.com/news/bulls-otto-porter-injury-update)
- [Chicago Bulls — Carter 발목 부상](https://www.nba.com/bulls/news/keys-game-bulls-vs-pacers-01102020)
- [Chicago Bulls — Markkanen 골반 스트레스 반응](https://www.nba.com/bulls/news/chucks-daily-check-12520)
- [NBA — Kris Dunn MCL 염좌](https://www.nba.com/news/kris-dunn-mcl-sprain-out-least-4-6-weeks)
- [Chicago Bulls — Hutchison 2019-20 시즌 회고](https://www.nba.com/bulls/features/bulls-2019-2020-season-recap-chandler-hutchison)
