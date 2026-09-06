# Chicago 2018-19 Outcome Model v0.1

- 상태: `PROVISIONAL_RUN_PASS / EXACT_OUTCOME_HOLD`
- 기준일: 2026-09-06
- 상위 prior: `simulation/CHICAGO_2018_19_PLAYER_PRODUCTION_PRIORS.md`
- 경기 입력: `simulation/CHICAGO_2018_19_OUTCOME_LEDGER.csv`
- 검산: `node tools/verify_chicago_2018_19_outcomes.mjs`
- 원고 게이트: `CLOSED`

## 결론

82경기 전수에 같은 baseline 확률·impact 함수·latent를 적용한 첫 실행 결과는 다음과 같다.

| 시나리오 | 주인공 BPM proxy | impact 합계 | 최종 성적 | 실제 대비 | 뒤집힌 경기 |
|---|---:|---:|---:|---:|---|
| LOW | -4.2 | -5.70점 | **21-61** | -1승 | `G033` 승→패 |
| BASE | -3.0 | +26.15점 | **22-60** | 0승 | 없음 |
| HIGH | -1.8 | +57.99점 | **22-60** | 0승 | 없음 |

이는 `정확 22승 LOCK`이 아니다. 실행 재현성은 통과했지만, closing odds가 하나의 원출처 계통에 의존하고 BPM을 causal impact로 쓰는 한계가 남아 있다. 현재 정본 후보 범위는 **21~22승**, exact record는 `HOLD`다.

세 시나리오 모두 Chicago는 리그 4번째 lottery seed를 유지한다. 따라서 2019 1순위 확률 **12.5%**와 실제 7순위·Coby White 유지 방향은 흔들리지 않는다. 단, 추첨 사건과 지명은 아직 `RETENTION_STRONG_LEAN / EVENT_HOLD`다.

## 1. 입력과 provenance

### Chicago 82경기 baseline

- 원출처 계통: Sportsbook Review Online의 2018-19 NBA closing moneyline archive
- 기계 입력: `pwu97/bettingtools`의 `data/nba_odds_2019.rda`
- 원파일 SHA-256: `11339b989e5b486458c8d769dfcdbaca88b94bd0a1d68665bcdddf0970a4a560`
- 정규화된 Chicago 82경기 입력 digest: `5d384676f691b3862daeb072d7749c075ee26117a8f65a2db9e9007f082f28cc`
- 검증: 82개 날짜·상대·최종 점수를 Basketball Reference 일정표와 대조

홈·원정 closing moneyline의 내재확률을 각각 구한 뒤 합이 1이 되도록 정규화해 Chicago baseline 승률 `pB`를 만든다.

`pB = q_CHI / (q_CHI + q_OPP)`

여기서 `q`는 American moneyline을 변환한 비정규화 내재확률이다.

### logit scale 독립 교정

Chicago 2018-19 결과를 보고 scale을 맞추지 않는다. 직전 시즌인 2017-18 정규시즌 1,230경기의 closing spread와 vig-free closing moneyline을 사용한다.

- 원출처 계통: Sportsbook Review Online 2017-18 archive
- 기계 입력: `Australia-Underdog-Betting/nba odds 2017-18.xlsx`
- 원파일 SHA-256: `3aa394a83c87169f17206a0d7179d8fe540c8da2e530585e353daaf9bff73f6c`
- 정규화 교정 입력 digest: `f5caf74bde274224a024c9b11cc3bdb8b5c5cb06f5ad9421ffac7f8ad17aa98c`
- 표본: 정규시즌 1,230경기, pick'em spread는 0점
- 모형: `logit(p_favorite) = beta × closing_spread`, 절편 0
- `beta = 0.14616931588725546`
- `k = 1 / beta = 6.841381133447518`
- 확률 RMSE: `0.11847558223382366`

두 파일은 서로 다른 독립 출처가 아니라 **같은 원자료의 가공본·미러**다. 파일 일치와 경기 전수성은 검증했지만 odds 자체의 독립 교차검증은 아니므로 `SOURCE_SINGLETON`을 유지한다.

## 2. 경기별 impact

주인공과 실제 선수의 해당 경기 분을 실제 Chicago 구간 BPM proxy로 가중한다.

`delta = Σ[(BPM_PROTAGONIST - BPM_DONOR) × moved_minutes / 48]`

역할은 네 종류다.

| mode | 경기 수 | 의미 |
|---|---:|---|
| `HUTCH` | 40 | 주인공이 Hutchison의 실제 분을 대체 |
| `RETURN` | 4 | 주인공 결장, receiver가 Hutchison 분을 재수령 |
| `POST` | 33 | 부상 뒤 주인공이 후순위 donor의 476분을 수령 |
| `NONE` | 5 | 이동분 없음 |

사용한 실제 Chicago BPM proxy는 Hutchison -3.9, Selden -5.9, Harrison -1.3, Blakeney -5.2, Luwawu-Cabarrot -4.7, Alkins -7.3, Brandon Sampson -4.7, JaKarr Sampson +3.7, Parker -2.1, Portis -1.9다.

이 값은 선수 가치의 정본 평가가 아니다. 작은 표본과 역할·라인업 효과를 포함한 박스 기반 proxy이므로 이번 단계에서는 outcome sensitivity를 찾는 감사 입력으로만 사용한다.

## 3. counterfactual 확률과 동일 latent

경기별 counterfactual 승률은 다음처럼 계산한다.

`logit(pCF) = logit(pB) + delta / k`

결과를 시나리오마다 다시 추첨하지 않는다. 고정 seed와 event ID로 만든 하나의 latent `u`를 실제와 counterfactual에 함께 쓴다.

- seed: `FIRST_REBOUND|R09|CHI_2018_19|PRIOR_v1`
- seed SHA-256: `a327dfbb38ff2f8cfb25f1abc03a892cee1704613aa81053a8721806f04666e2`
- event ID: `CHI_2018_19_G001`~`CHI_2018_19_G082`
- 실제 승리: `u = h × pB`
- 실제 패배: `u = pB + h × (1 - pB)`
- `h`: `SHA256(seed|event_id)`의 첫 8바이트를 53비트 균등수로 변환
- counterfactual 승리 판정: `u < pCF`

이 조건부 latent는 실제 결과를 정확히 재현하면서, impact가 임계치를 넘을 때만 승패를 바꾼다. close game을 사후 선택하지 않는다.

## 4. 유일한 민감 경기

| 항목 | 값 |
|---|---|
| event | `CHI_2018_19_G033` |
| 날짜 | 2018-12-21 |
| 경기 | Orlando @ Chicago |
| 실제 결과 | Chicago 90-80 승 |
| protagonist/Hutchison slot | 16:44 |
| `pB` | 0.40372671 |
| `u` | 0.401877463873 |
| LOW delta | -0.10458333점 |
| LOW `pCF` | 0.40005216 |
| LOW 판정 | 패 |

BASE와 HIGH에서는 그대로 승리다. LOW만 Chicago가 21-61, Orlando가 43-39가 된다.

이 변화는 Chicago의 lottery seed를 바꾸지 않지만 Orlando와 Brooklyn의 동부 6·7번 seed를 바꿀 수 있다. 실제 두 팀은 42-40이었고 Brooklyn이 6위, Orlando가 7위였다. Orlando가 43승이면 Orlando 6위·Brooklyn 7위가 되어 1라운드 상대가 서로 교환된다. 따라서 LOW 선택은 Chicago 한 팀의 숫자 수정으로 끝나지 않으며, 2019 플레이오프 분기를 함께 여는 선택이다.

## 5. standings와 2019 lottery

| 시나리오 | Chicago | 다음 lottery 팀 Atlanta | Chicago seed | 1순위 확률 |
|---|---:|---:|---:|---:|
| LOW | 21-61 | 29-53 | 4 | 12.5% |
| BASE | 22-60 | 29-53 | 4 | 12.5% |
| HIGH | 22-60 | 29-53 | 4 | 12.5% |

이 모델이 허용하는 전 범위에서 4번째 seed는 구조적으로 안전하다. 그러므로 lottery 조합을 실제와 동일하게 유지하는 원칙을 택하면 실제 추첨의 Chicago 7순위를 보존할 수 있다.

현재 처리 원칙은 다음과 같다.

1. lottery seed가 실제와 같으면 실제 추첨 조합·결과를 기본 baseline으로 유지한다.
2. 주인공 때문에 seed 또는 lottery 참가팀 순서가 바뀔 때만 추첨 사건을 다시 연다.
3. 이번 LOW의 Orlando 변화는 playoff seed 변화이지 lottery 참가 순서 변화가 아니다.
4. 다만 exact 정규시즌 결과가 `HOLD`이므로 Chicago 7순위도 아직 `LOCK`으로 승격하지 않는다.

## 6. Coby White 보드

7순위가 보존되는 경우 Coby White 유지가 가장 강한 후보다.

- Chicago의 실제 필요: 주전급 포인트가드와 속도·볼 운반 보강
- 주인공의 2018-19 역할: 저사용률 SF/PF, 리바운드·수비·전환 중심
- 직접 중복: 낮음
- 공존 구조: White가 1차 전진·픽앤롤, 주인공이 수비 리바운드 뒤 직접 전환 또는 2차 러너
- 1년차 충돌 위험: 두 선수 모두 의사결정과 슈팅이 미완성이라 하프코트 spacing이 좁아질 수 있음

판정은 `COBY_RETENTION_STRONG_LEAN / EVENT_HOLD`다. 주인공의 장기 포인트포워드 상한을 2019년의 완성 역할로 당겨와 Coby를 지우지 않는다.

## 7. Patrick Williams 연결

2020 실제 4순위 Patrick Williams는 포워드 수비·성장 자원을 주인공과 직접 공유한다. 2019 Coby와 달리 자동 보존할 수 없다.

- 현재 판정: `REOPEN_REQUIRED / HOLD`
- 선행 조건: 2019-20 주인공의 분·선발·온볼 비중, Porter·Markkanen의 역할과 건강, Chicago 성적·lottery
- 비교 보드: Williams / Avdija / Okoro / Haliburton / Vassell

이번 실행은 2020 보드를 닫지 않는다.

## 8. 남은 blocker와 다음 실행

1. 독립 odds archive로 최소한 Chicago 82경기의 closing moneyline을 교차검증한다.
2. BPM proxy 대신 가능한 lineup/on-off·RAPM 계열의 방향 일치 여부를 확인한다.
3. 주인공의 17.45분 역할에서 fatigue를 0으로 둘지, 후반 연속 경기만 미세 감산할지 사전 규칙을 정한다.
4. LOW를 선택할 경우 Orlando–Brooklyn playoff opponent cascade를 별도 분기로 연다.
5. 위 검증 전에는 21승과 22승 중 하나를 정본화하지 않는다.

## 출처

- [NBA — Chicago 2018-19 22승 60패·팀 효율](https://www.nba.com/news/powerrankings-2019-20-summer-east)
- [NBA — 2019 Draft lottery odds/order](https://www.nba.com/news/draft-lottery-odds-order-decided-official-release)
- [NBA — 2019 Draft lottery result](https://www.nba.com/news/pelicans-win-nba-draft-lottery)
- [NBA — 2019 Draft results](https://www.nba.com/news/2019-nba-draft-results-picks-1-60)
- [Chicago Bulls — Coby White 지명 당시 포인트가드 보강 맥락](https://www.nba.com/bulls/news/can-coby-white-translate-his-game-create-one-most-explosive-backcourts-nba)
- [NBA — 2020 Draft results](https://www.nba.com/news/2020-nba-draft-results-picks-1-60)
- [Chicago Bulls — Patrick Williams 선택 이유](https://www.nba.com/bulls/features/arturas-karnisovas-details-why-bulls-targeted-patrick-williams-marko-simonovic-2020-draft)
- [Sportsbook Review Online — NBA odds archive](https://www.sportsbookreviewsonline.com/scoresoddsarchives/nba/nbaoddsarchives.htm)
- [pwu97/bettingtools — odds archive 가공본](https://github.com/pwu97/bettingtools)
- [Basketball Reference — Chicago 2018-19 일정·로스터](https://www.basketball-reference.com/teams/CHI/2019.html)
