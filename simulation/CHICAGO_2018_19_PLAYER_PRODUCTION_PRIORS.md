# Chicago 2018-19 Player Production Prior & Transfer Ledger v0.1

- 상태: `PRIOR_RANGE_PASS / TRANSFER_LEDGER_PASS / OUTCOME_INPUTS_HOLD`
- 기준일: 2026-09-06
- 상위 원장: `simulation/CHICAGO_2018_19_PLAYER_GAME_DONOR_VECTOR.md`
- 분 검산: `node tools/verify_chicago_2018_19_ledger.mjs`
- prior 검산: `node tools/verify_chicago_2018_19_priors.mjs`
- 원고 게이트: `CLOSED`

## 결론

주인공의 73경기·11선발·1,274:02를 유지하면서 루키 시즌의 개인 생산성 범위를 다음과 같이 둔다.

- 박스 생산성 중심: **9.5득점·8.5리바운드·1.7어시스트·1.3스틸·0.8블록 / 36분**
- 슈팅 중심: **TS .500·3PA 2.3·3P .280**
- 역할 해석: NBA 평균급 완성 선수가 아니라, 슛과 하프코트 판단은 약하지만 리바운드·수비 사건·전환으로 17분을 버티는 프로젝트 루키
- 영향 proxy 중심: **BPM -3.0 후보**. 단, BPM은 감사용 요약치일 뿐 승패 모델 입력으로 아직 승인하지 않는다.

따라서 정확 개인 시즌 기록과 경기별 승패는 계속 `HOLD`다. 통과시키는 것은 결과값이 아니라 **범위·비교군·분 이전 계산법**이다.

## 1. 비교군 사전 정의

성과를 본 뒤 유리한 선수만 고르지 않도록 다음 기준으로 2018-19 신인 핵심 비교군을 정한다.

1. 2018 Draft 15~48순위
2. NBA 첫 시즌의 수비 윙·저사용률 연결자·운동능력형 윙 역할
3. 정규시즌 200~1,800분
4. 주전 창조자·센터 전용 선수는 제외

| 선수 | 지명 | 분 | PTS/36 | TRB/36 | AST/36 | STL/36 | BLK/36 | TS | 3PA/36 | 3P | BPM |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Troy Brown Jr. | 15 | 730 | 12.2 | 7.2 | 3.9 | 1.0 | 0.2 | .487 | 3.4 | .319 | -2.7 |
| Josh Okogie | 20 | 1,757 | 11.7 | 4.5 | 1.9 | 1.8 | 0.7 | .492 | 4.4 | .279 | -3.1 |
| Chandler Hutchison | 22 | 895 | 9.2 | 7.4 | 1.4 | 0.9 | 0.2 | .507 | 2.0 | .280 | -3.9 |
| Jacob Evans | 28 | 204 | 7.1 | 4.4 | 4.1 | 0.9 | 0.5 | .374 | 2.6 | .267 | -8.2 |
| Rodions Kurucs | 40 | 1,294 | 14.9 | 6.8 | 1.4 | 1.1 | 0.7 | .545 | 5.1 | .315 | -2.6 |
| Bruce Brown | 42 | 1,449 | 7.9 | 4.6 | 2.3 | 1.0 | 0.9 | .469 | 2.3 | .258 | -3.3 |
| Hamidou Diallo | 45 | 526 | 13.0 | 6.6 | 1.2 | 1.4 | 0.7 | .497 | 1.6 | .167 | -4.2 |
| Svi Mykhailiuk | 47 | 440 | 10.9 | 2.9 | 3.0 | 1.1 | 0.1 | .447 | 7.3 | .326 | -5.0 |
| Keita Bates-Diop | 48 | 503 | 10.8 | 5.9 | 1.2 | 1.3 | 1.0 | .489 | 3.7 | .250 | -3.4 |

비교군 중앙값은 PTS 10.9, TRB 5.9, AST 1.9, STL 1.1, BLK 0.7, TS .489, 3PA 3.4, 3P .279, BPM -3.4다. 주인공은 득점·3점 시도를 중앙값 아래에 두고, 정본상 고유 뿌리인 리바운드를 Hutchison 7.4보다 높고 Spellman 8.7과 비슷한 범위에 둔다.

## 2. 주인공 박스 생산성 prior

| 항목 / 36분 | LOW | BASE | HIGH | 설계 이유 |
|---|---:|---:|---:|---|
| PTS | 8.0 | **9.5** | 11.0 | 하프코트 창조·점퍼 부족, 전환과 풋백으로 하한 방어 |
| TRB | 7.5 | **8.5** | 9.5 | 고유 뿌리. 동포지션 신인 중앙값보다 의도적으로 높음 |
| AST | 1.2 | **1.7** | 2.2 | 순간 공간인지가 있으나 전술 언어와 2차 판단은 미완성 |
| STL | 1.0 | **1.3** | 1.6 | 활동량·회복 운동능력 반영 |
| BLK | 0.5 | **0.8** | 1.1 | 헬프 타이밍 편차를 남김 |
| TOV | 2.2 | **1.8** | 1.4 | LOW/HIGH는 좋은 값의 방향을 반대로 읽음 |
| PF | 4.2 | **3.6** | 3.0 | 손기술·클로즈아웃 미숙 비용 |
| TS | .470 | **.500** | .530 | 림 마무리와 자유투가 점퍼 약점을 일부 상쇄 |
| 3PA | 1.5 | **2.3** | 3.1 | 스페이싱을 존중하되 공격 정체성을 점퍼로 바꾸지 않음 |
| 3P | .240 | **.280** | .320 | 1년차 약점 유지 |

`LOW/BASE/HIGH`는 한 줄의 완성 기록이 아니라 사전 범위다. TS·3P·PTS를 독립적으로 최고값끼리 조합하지 않는다. 정확한 FGA·FTA·ORB/DRB와 경기별 정수 박스는 결과 모델 뒤에도 별도 검산한다.

### 1,274:02 환산 참고선

| 항목 | LOW | BASE | HIGH |
|---|---:|---:|---:|
| 총 득점 | 283 | **336** | 389 |
| 경기당 득점 | 3.88 | **4.61** | 5.33 |
| 총 리바운드 | 265 | **301** | 336 |
| 경기당 리바운드 | 3.64 | **4.12** | 4.61 |
| 총 어시스트 | 42 | **60** | 78 |
| 경기당 어시스트 | 0.58 | **0.82** | 1.07 |
| 총 스틸 | 35 | **46** | 57 |
| 총 블록 | 18 | **28** | 39 |

이는 반올림 참고선이다. exact season line은 `HOLD`다.

## 3. 실제 선수 생산성 이전량

실제 Chicago 소속 구간의 per-36을 해당 이동분에 선형 적용한다. 이 값은 누구의 실제 기록을 주인공에게 복사하는 것이 아니라, 이후 정수 박스 원장에서 보존해야 할 **1차 사건량**이다.

### 후반 33경기 — 476분 차감

| 선수 | 차감 분 | PTS | TRB | AST | STL | BLK |
|---|---:|---:|---:|---:|---:|---:|
| Wayne Selden Jr. | 137 | 47.6 | 19.0 | 10.3 | 3.0 | 1.1 |
| Shaquille Harrison | 119 | 39.3 | 18.5 | 11.6 | 7.3 | 2.6 |
| Antonio Blakeney | 61 | 30.8 | 7.8 | 3.0 | 0.8 | 0.7 |
| Timothé Luwawu-Cabarrot | 73 | 26.2 | 10.5 | 3.0 | 2.0 | 1.0 |
| Rawle Alkins | 27 | 8.3 | 5.8 | 2.9 | 0.2 | 0.0 |
| Brandon Sampson | 35 | 11.6 | 2.6 | 1.7 | 1.3 | 0.5 |
| JaKarr Sampson | 24 | 15.1 | 6.1 | 0.7 | 0.7 | 0.6 |
| 합계 | **476** | **178.9** | **70.4** | **33.2** | **15.4** | **6.6** |

### 주인공 결장 4경기 — 96:35 반환

| 선수 | 추가 분 | PTS | TRB | AST | STL | BLK |
|---|---:|---:|---:|---:|---:|---:|
| Wayne Selden Jr. | 22:00 | 7.6 | 3.1 | 1.7 | 0.5 | 0.2 |
| Shaquille Harrison | 27:00 | 8.9 | 4.2 | 2.6 | 1.7 | 0.6 |
| Antonio Blakeney | 15:00 | 7.6 | 1.9 | 0.8 | 0.2 | 0.2 |
| Jabari Parker | 15:44 | 8.4 | 3.6 | 1.3 | 0.3 | 0.2 |
| Bobby Portis | 16:51 | 9.8 | 5.1 | 0.9 | 0.3 | 0.2 |
| 합계 | **96:35** | **42.4** | **17.9** | **7.2** | **3.0** | **1.4** |

실제 Hutchison 894:37의 229득점·185리바운드·34어시스트·23스틸·6블록은 기준선에서 제거된다. BASE 주인공 참고선과 위 이동량을 단순 합치면 선수 박스 귀속은 약 `-29득점, +64리바운드, -1어시스트, +11스틸, +18블록` 방향이다.

이 값은 팀 총득점·총리바운드의 변화가 아니다. 고정된 슛·리바운드 기회를 동료가 다시 점유하므로, 팀 결과에 이 수치를 직접 더하는 것은 금지한다.

## 4. 승패 영향 prior

비교군의 2018-19 BPM 분포는 P25 -4.2, 중앙값 -3.4, P75 -3.1이다. 주인공은 다음 감사 범위를 둔다.

| 시나리오 | BPM proxy | 의미 |
|---|---:|---|
| LOW | -4.2 | 공격 결함과 파울·턴오버가 수비 장점을 대부분 상쇄 |
| BASE | **-3.0** | 비교군 상위사분위 부근. 리바운드·전환으로 정상 로테이션 유지 |
| HIGH | -1.8 | 수비·리바운드가 예상보다 빠르게 번역된 상한, 평균급 선수 아님 |

실제 Chicago 구간 BPM을 그대로 꽂은 감사용 plug-in에서는 player-minute 가중 팀 점수차가 약 `-6 / +26 / +58점`이다. 이는 대략 한 시즌 `0~+2승` 규모를 가리키는 방향성 검사일 뿐이다.

다음 이유로 이 숫자를 경기별 승패에 아직 넣지 않는다.

1. BPM은 박스 기반 요약치이며 같은 날짜 라인업·상대·garbage time의 인과효과가 아니다.
2. JaKarr Sampson 127분, Alkins 120분 등 소표본 극단값이 donor 평균을 흔든다.
3. 현재 `pB` closing probability와 독립 교정한 logit scale이 없다.
4. 결과를 보고 close game만 고르는 방식은 `DRAFT_CAUSALITY_PROTOCOL`과 충돌한다.

따라서 77개 영향 경기 전부에 대해 사전확률·동일 latent를 적용하기 전에는 정확한 23승 또는 24승을 선택하지 않는다.

## 5. standings·lottery에 대한 현재 안전 결론

- 실제 Chicago는 22승 60패, 리그 4번째 최저 승률이었다.
- 다음 팀 Atlanta는 29승이었다.
- 현재 prior가 가리키는 `0~+2승` 범위에서는 Chicago가 22~24승이므로 **4번째 lottery seed가 변하지 않는다**.
- 2019 제도에서 4번째 seed의 1순위 확률은 **12.5%**다.
- seed와 조합 배정이 그대로면 실제 추첨 결과인 Chicago 7순위를 유지한다.
- 다만 exact 경기 승패와 상대팀 순위 원장이 닫히기 전에는 `LOTTERY_RESULT_FINAL`로 승격하지 않는다.

## 6. Coby White·Patrick Williams 연결

### 2019 Coby White

주인공은 1차 볼 운반자가 아니라 저사용률 SF/PF다. Chicago가 실제로 찾던 포인트가드 업그레이드와 역할이 겹치지 않는다. 따라서 7순위가 유지되면 Coby White는 **`RETENTION_STRONG_LEAN / EVENT_HOLD`**다.

금지:

- 주인공의 장기 BQ 상한을 근거로 2019년에 이미 주전 포인트포워드라고 가정
- Coby의 실후대 성과를 알고 지명 여부를 역선택
- 22~24승 범위를 근거 없이 정확 23승으로 잠금

### 2020 Patrick Williams

Patrick Williams는 실제로 4순위에서 뽑힌 다포지션 포워드라 주인공의 성장 위치와 직접 겹친다. 따라서 실제 지명을 자동 보존하지 않는다.

- 구조 검토: `REOPEN_REQUIRED`
- 필요한 선행값: 2019-20 주인공 분·선발·볼 운반·Markkanen/Porter 역할, Chicago 성적과 lottery
- 비교 보드 후보: Williams 유지 / Avdija / Okoro / Haliburton / Vassell
- exact pick과 선택: `HOLD`

## 다음 실행

1. 77개 영향 경기의 양방향 closing moneyline 출처·마감 시각을 하나로 잠근다.
2. 2018-19 비접촉 리그 표본으로 logit scale을 교정한다.
3. 같은 event ID·latent로 LOW/BASE/HIGH를 실행한다.
4. Chicago와 상대팀 승수를 동시에 한 번만 갱신한다.
5. 4번째 seed가 유지되면 실제 2019 추첨·7순위·Coby White 보드를 조건부 통과시킨다.

## 출처

- [NBA — Chicago 2018-19 22승 60패·팀 효율](https://www.nba.com/news/powerrankings-2019-20-summer-east)
- [NBA — 2019 Draft lottery odds/order](https://www.nba.com/news/draft-lottery-odds-order-decided-official-release)
- [NBA — 2019 Draft lottery result](https://www.nba.com/news/pelicans-win-nba-draft-lottery)
- [NBA — 2019 Draft results](https://www.nba.com/news/2019-nba-draft-results-picks-1-60)
- [Chicago Bulls — Coby White와 포인트가드 경쟁](https://www.nba.com/bulls/news/can-coby-white-translate-his-game-create-one-most-explosive-backcourts-nba)
- [NBA — 2020 Draft results](https://www.nba.com/news/2020-nba-draft-results-picks-1-60)
- [Chicago Bulls — Patrick Williams 선택 이유](https://www.nba.com/bulls/features/arturas-karnisovas-details-why-bulls-targeted-patrick-williams-marko-simonovic-2020-draft)
- [Basketball Reference — Chicago 2018-19 로스터·per-36·advanced](https://www.basketball-reference.com/teams/CHI/2019.html)
- [Basketball Reference — 2018-19 league per-36](https://www.basketball-reference.com/leagues/NBA_2019_per_minute.html)
- [Basketball Reference — 2018-19 league advanced](https://www.basketball-reference.com/leagues/NBA_2019_advanced.html)
