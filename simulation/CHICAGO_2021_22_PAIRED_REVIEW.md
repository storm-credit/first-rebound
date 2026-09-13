# O-15G14 — 세 경기 양 팀 분과 공격기회 비교

- 기반: PR #180 main `109a488c5c508a9f47a79c1f12991b9d162a1720`.
- 판정: `PARTIAL_PAIRED_CONTROL_NOT_SEASON_EXECUTION / NOT_INDEPENDENT`.
- [입력](CHICAGO_2021_22_PAIRED_INPUTS.json), [기계 결과](CHICAGO_2021_22_PAIRED_REVIEW.json), [선수별 기회 배분](CHICAGO_2021_22_OPPORTUNITY_ALLOCATIONS.csv), [출처](../research/CHICAGO_2021_22_PAIRED_SOURCES.json).
- G12 개막 prior·G13 P21A/D21A를 사용하는 **사후 공통 예산 비교**다. 실제 경기의 FGA/FTA/선수 실책 합계는 개막 시점에 알 수 없으므로 예측 입력이라고 부르지 않는다. 추천은 계산용이며 날짜·거래·생산성·시즌의 최종 선택은 없다.

## 확보한 관측과 분 증명

고정 mirror 세 원본의 SHA256을 다시 확인하고 목표 세 경기 양 팀 선수행 **78개**, 상대 베테랑 **17명·2020–21 관측 1,087개**를 추출했다. G12의 리그 1,230행을 다시 수집하지 않았다. [원본 계보](CHICAGO_2021_22_PAIRED_PROVENANCE.json)와 [상대 prior](CHICAGO_2021_22_OPPONENT_PRIORS.json)에 원본 버전과 개막 이전 범위를 저장했다. 숫자 박스는 공개 mirror이고 신규 공식 숫자 박스 대조는 **0건**이다. 공식 경기 페이지는 날짜·ID·팀 확인 범위다.

| 경기 | 역사적 선수 박스 합계: PTS / FGA / FTA / TOV | 원본 초 합계·잔차 | 대체세계 조건부 분안 |
|---|---|---|---|
| [10/20 CHI@DET](https://www.nba.com/game/chi-vs-det-0022100004) | CHI 94/86/15/17; DET 88/90/13/16 | 양 팀 14,401초·각 +1초 | CHI 코비 공백; DET 10명 240분 |
| [1/23 CHI@ORL](https://www.nba.com/game/chi-vs-orl-0022100701) | CHI 95/76/32/21; ORL 114/80/23/12 | CHI 14,401초·+1; ORL 14,400초·0 | CHI 복합56분 대체; ORL 지정 가드 12분 HOLD |
| [2/16 SAC@CHI](https://www.nba.com/game/sac-vs-chi-0022100878) | CHI 125/94/20/11; SAC 118/84/22/13 | CHI 14,401초·+1; SAC 14,400초·0 | CHI 복합70분 대체; SAC S14A 스트레스 240분 |

위 수치는 [고정 선수 관측](NBA_2021_22_THREE_GAME_OBSERVATIONS.csv)에서 합산했다. TOV는 **선수행 실책 합계**이며 별도 팀 실책을 포함한 공식 팀 총실책·포제션이 아니다. 역사적 점수는 원본 대조에만 쓰고 대체세계 득점으로 이전하지 않는다. 표시 초의 +1을 임의 선수에게서 차감하지 않는다.

Chicago 세 분안은 [G12 코비 예시](CHICAGO_2021_22_INPUT_REVIEW.json)와 [G13 복합 공백](CHICAGO_2021_22_GROWTH_REVIEW.json)의 저장된 5인 증명을 그대로 연결했다. G1A/SQ1 등록·수신자 가용성·해당 결장 조건이 모두 성립할 때만 쓴다. 10/20 코비 예시는 앞선 13경기 전체 채택이 아니다. 1/23 Markkanen의 다음 날 사유를 당일 결장으로 옮기지 않으며 2/16 Green Probable은 의료 허가가 아니다.

## 상대 구단의 연쇄

### Detroit — 분은 성립, Suggs 생산성은 미확보

[2020 정본](../canon/PROJECT_FREEZE.md)의 Patrick7·Kira16·Stewart19, [G7 DB1](NBA_2021_FULL_DRAFT_COMPARISON.json)의 Suggs5를 조건으로 한다. Hayes/Bey/Cade를 실제 Detroit 명단에서 자동 복사하지 않는다. G7에서 실행하지 않은 실제 Plumlee/37 거래는 이번 대조에서도 보류한다. 이는 거래 거절의 작가 확정이 아니다.

| 위치 | 조건부 분 |
|---|---|
| PG | Kira24·Cory Joseph24 |
| SG | Suggs24·Josh Jackson16·Diallo8 |
| SF | Patrick28·Josh Jackson8·Diallo12 |
| PF | Grant30·Olynyk18 |
| C | Stewart24·Plumlee24 |

포지션별48분·총240분·개인36분 이하와 매 조합의 지정 가드를 확인했다. 모든 선수의 등록/가용성, Olynyk 취득, Plumlee 유지가 비교 조건이다. 전체 15자리·급여·계약 감사 완료가 아니며 큰 라인업의 공간·수비 비용도 미계산이다. Suggs의24분을 0 생산성으로 처리하거나 미래 NBA 기록을 넣지 않아 네 공격기회 정책 모두 `PRIOR_HOLD`다.

### Orlando — 지정 가드 규칙 아래 최소12분 부족

G7 DB1에서 Mobley3·Herbert33, Suggs DET·Hampton DAL, Carter CHI와 Vucevic ORL/Nnaji Gordon A를 따른다. [1/23 17:30 공식 보고서](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2022-01-23_05PM.pdf)의 MCW·Fultz·Harris·Isaac·Moore·Ross 결장을 조건으로 채택하면, 현재 이름이 지정된 주 가드는 Cole Anthony 한 명이다. 원래 ORL 소속 Hampton의 사유를 대체세계 ORL 인원에 넣지 않는다.

개인 설계 상한36분과 매분 지정 주 가드 규칙 아래 **48−36=12분**이 부족하다. 이는 해당 역할 규칙의 하한이며 NBA 법규상 출전 불가 또는 ORL 전체 명단 불능 판정이 아니다. 추가 가드의 등록·가용성 또는 새 전개자 역할을 지정하기 전에는 240분 증명과 생산성 네 조건을 만들지 않는다. 가짜 가드 영입이나 무근거 Cole48분으로 빈칸을 지우지 않는다.

### Sacramento — 실제 두 거래와 대조 조건을 분리

역사적 2/8 Indiana 교환은 [NBA 거래 기사](https://www.nba.com/news/pacers-agree-to-trade-domantas-sabonis-to-kings), 2/10 네 구단 교환은 [Milwaukee Bucks 명의 보도자료](https://urbanmilwaukee.com/pressrelease/milwaukee-bucks-acquire-serge-ibaka-from-los-angeles-clippers-in-four-team-trade/)로 구분했다. 정확 픽·현금·급여 조항과 대체세계 합의는 미확보다.

| 조건 | 2/8 Sabonis 패키지 | 2/10 네 구단 패키지 | 이번 처리 |
|---|---|---|---|
| S14A | 보류 | 보류 | 거래 전 코어를 남기는 중립 대조 분안만 계산 |
| S14B | 진행 조건 | 보류 | Indiana 자산·등록 연쇄 HOLD |
| S14C | 보류 | 진행 조건 | Hood 선행 등록·픽·등록 연쇄 HOLD |
| S14D | 진행 조건 | 진행 조건 | 양 패키지 연쇄 HOLD |

S14A는 추천·정본·거래 거절이 아니다. G7의 Indiana는 실제 Duarte 대신 Trey Murphy 조건이다. [T4 승인](../canon/CHICAGO_2020_21_DIRECTION_APPROVAL.json)의 Hood POR 잔류는 **2020–21 방향**이다. 이후 방출·FA·MIL 등록을 확인하지 않았다는 뜻이며 2022 MIL 보유가 영구 불가능하다는 주장이 아니다. Metu도 2018 DAL 이후 후속 등록이 닫히지 않아 실제 SAC 출전을 자동 이전하지 않는다.

| 위치 | S14A의 추가 결장 조건 아래 분 |
|---|---|
| PG | Fox36·Haliburton12 |
| SG | Haliburton24·Hield24 |
| SF | Hield12·Barnes36 |
| PF | Harkless28·Bagley20 |
| C | Bagley8·Holmes28·Len12 |

위 8명의 등록·가용성과 Mitchell 미출전·Queta0분을 가정한다. [2/16 공식 보고서](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2022-02-16_05PM.pdf)의 Mitchell은 **Questionable**이다. 이 비교의 미출전 가정이 역사적 확정 Out을 뜻하지 않는다. Fox/Haliburton/Hield/Barnes 모두36분, Hield SF12·Harkless PF28은 부담 큰 스트레스안이며 정상 추천 로테이션이 아니다.

## 같은 예산에서 네 공격기회 정책 비교

선수별 원시 가중치는 `2020–21 per36 × 조건부 분 / 36`이며 주인공/Duarte만 G13 수동 후보를 쓴다. 베테랑 기록 역시 다른 팀·역할에서 나온 역사적 prior로, 대체세계 실력 확정치가 아니다. FGA·FTA·TOV를 각각 배분하며 3PA/FGA 구성비는 prior를 유지한다. 실책은 성과 보상이 아니라 비용이고, 실책에 같은 비례식을 적용하는 것도 통제 비교일 뿐이다.

| 정책 | 원시 기회를 고정할 선수 | 잔여 조정 |
|---|---|---|
| B14A 주 비교 추천 | CHI 주인공 / SAC Fox | 나머지 선수에 비례 배분 |
| B14B | CHI 주인공·LaMelo·출전 LaVine / SAC Fox·Haliburton·Barnes | 비코어가 분담 |
| B14C | 없음 | 모두 비례 조정 |
| B14D | 비코어 | 출전 코어가 분담 |

고정분이 예산을 넘거나 잔여를 받을 가중치가 없으면 `BUDGET_HOLD`다. 부호가 음수인 시도·실책을 만들지 않는다. 합계 오차 허용은 부동소수점 `1e-7`이다. 추천 B14A에서도 선수별 조정량은 원시 가중치 대비 차이이며 **주인공 성장만의 인과적 양도량이 아니다**.

| B14A | 원시 FGA / FTA / TOV | 공통 관측 예산 | 주인공 외 조정 비율 FGA / FTA / TOV |
|---|---|---|---|
| CHI 10/20 | 93.426 / 23.227 / 17.253 | 86 / 15 / 17 | 0.908 / 0.578 / 0.983 |
| CHI 1/23 | 91.128 / 19.776 / 15.900 | 76 / 32 / 21 | 0.807 / 1.762 / 1.375 |
| CHI 2/16 | 89.968 / 20.145 / 15.410 | 94 / 20 / 11 | 1.052 / 0.991 / 0.663 |

B14A는 주인공32분의 FGA12.772·FTA3.733·TOV2.311을 세 경기 모두 유지한다. 10/20 동료 자유투 가중치−42.2%, 1/23 +76.2%, 2/16 동료 실책 가중치−33.7%는 **고정 예산이 강요하는 조정**이다. 실제 역할 변화로 그 조정이 가능한지 검증하지 않았다. 비율0.75~1.25 밖을 수동 스트레스 표식으로 남겼으며 통계적 허용 범위·신뢰구간이 아니다. SAC B14A는 이 표식0명이지만 현실성 인증을 뜻하지 않는다.

총 **24팀·정책 조건 = 숫자16 + Suggs prior HOLD4 + ORL 역할 HOLD4**, 배분 CSV164행이다. 세 경기×네 정책의12양팀 조건 중 숫자가 양쪽 모두 있는 것은 **S14A SAC 경기의4조건**뿐이다. 전체 세 경기 양 팀 생산성이 완성됐다고 보고하지 않는다.

## 검증과 다음 사용 지점

[재현 도구](../tools/build_chicago_2021_22_paired.py)는 저장된 관측만으로 prior·분·예산·HOLD를 재생성한다. 신규11검사는 중복 선수·결장 수신자·전개자 부재·미래 자료·Suggs 누락·고정분 초과·0 가중치·비율과 합계·조건부 ORL 하한·점수/승수 미선택을 확인한다. 별도 해시 시드로 재현해 집합 순회 순서에 따른 float 출력 차이도 막았다. [자체 검토](../reviews/R01_O15G14_PAIRED_OPPORTUNITY_REVIEW.md)는 독립 검수가 아니다.

다음은 **Suggs의 개막 이전 대학 환산 후보와 ORL 가드12분 대안**을 비교해 두 상대의 보류 사유를 먼저 줄이는 작업이다. SAC S14B~D는 후속 등록·자산 필드를 확보할 때 확장한다. 새 82/1,230경기 전량 수집은 필요 없다. 팀 수비·리바운드·어시스트·포제션 상호작용과 승패, 실제 교대 순서·시즌/2022 계약·픽은 미완료다.

전체1완료·6진행, 남은 큰 작업6개. `PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 `CLOSED`, author/season/exact/manuscript false를 유지한다. CP2 절차 승인으로 검증된 PR→main 후속은 진행하되 최종 작가 선택으로 승격하지 않는다.
