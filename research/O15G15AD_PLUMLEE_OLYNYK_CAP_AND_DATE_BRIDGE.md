# O-15G15AD — Plumlee 잔류의 계약·Olynyk 취득 비용

- 시작 권위: `main` `45e6924`, [G15AC](O15G15AC_PLUMLEE_2021_DRAFT_ASSET_COLLISION.md)의 P0/P1. 판정: `2021_22_PLUMLEE_CONTRACT_BRIDGE / OLYNYK_ACQUISITION_COLLISION / JAN23_HOLD`.
- `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`; `author_locked=false`, `season_selected=false`, `exact_execution_cleared=false`, `manuscript_allowed=false`. 신규 작가확정 0건.

## 1. 날짜와 직접 근거

| 날짜 | 원역사 사실 | 대체 P0에 넘길 수 있는 범위 |
|---|---|---|
| 2020–21 시작 | Detroit가 Plumlee와 계약했다. [NBA 계약·거래 분석](https://www.nba.com/news/numbers-to-know-breaking-down-the-big-draft-week-trades)은 첫 두 해 합계 약 `$16.1m` 보장, 3년차 비보장이라고 설명한다. | 2021–22는 원계약의 보장된 두 번째 해라는 **계약 출발점**. 선수별 정확 연봉·옵션 조항 원문은 미확보. |
| 2021-07-29 드래프트 / 08-06 공식화 | [Charlotte 발표](https://www.nba.com/hornets/press-releases/charlotte-hornets-acquire-mason-plumlee-and-draft-rights-jt-thor)는 DET→CHA Plumlee+37 Thor 권리, CHA→DET 57 Koprivica 권리다. | P0는 **이 거래를 실행하지 않는 조건**일 뿐, 대체 DB1의 Thor 권리를 Detroit에 되돌리지 않는다. [미선택 DB1 비교안](../simulation/NBA_2021_FULL_DRAFT_COMPARISON.md)의 Thor는 Utah30 제안, Detroit37은 Aldama 제안이다. |
| 2021-08-06 | [Detroit 구단 발표](https://www.nba.com/pistons/features/detroit-pistons-sign-free-agents-kelly-olynyk-trey-lyles-and-restricted-free-agent-saben)는 Olynyk·Trey Lyles·Saben Lee 계약을 확인하나 금액은 공개하지 않는다. [Detroit 당시 분석](https://www.nba.com/pistons/features/olynyk-deal-made-possible-stewarts-rapid-progress-opens-pistons-offense)과 [구단 후속 회고](https://www.nba.com/pistons/news/decisions-decisions-a-critical-few-weeks-ahead-for-pistons-gm-troy-weaver)는 Plumlee를 보내 만든 cap space를 Olynyk 추구·영입에 썼다고 설명한다. | P0에서 Plumlee를 보유하면서 **원역사 Olynyk 서명을 비용 0으로 복사할 수 없다.** 다른 급여 이탈·예외·거래·조건 변경 중 구체 경로와 상대 비용을 증명해야 한다. 그렇다고 두 선수의 동시 보유가 모든 경로에서 불가능하다고 단정하지 않는다. |
| 2021–22 개막 → 2022-01-23 | [G14의 2021-10-20 Detroit 추상 조합](../simulation/CHICAGO_2021_22_PAIRED_REVIEW.md)은 `Grant PF30 + Olynyk PF18`, `Stewart C24 + Plumlee C24`다. G15AB의 1/23 원역사 박스와 원역사 부상 보고는 대체 명단·건강을 보장하지 않는다. | G14는 계약/명단 증명이 아닌 조건부 분 계산이다. 8월 거래 미실행과 2020 계약만으로 10월·1월 소유·등록·건강·출전이 확정되지 않는다. 후속 거래/방출·15인 명단·당일 의료·앞코트 96분 재검산이 필요하다. |

## 2. G14 동시 기용을 위한 상호 배타적 시험

| 시험 | 추가 사건과 비용 | G14와 1/23 판정 |
|---|---|---|
| P0-A: Plumlee 유지, Olynyk 미취득 | Olynyk의 다른 팀 경로와 Detroit의 대체 PF/C 수신자를 정한다. 원역사 Lyles·Lee 계약도 동일하게 가능했는지 별도 확인한다. Charlotte의 Plumlee/Thor 수신은 없음. | `Plumlee C24`의 계약 출발점만 있고 `Olynyk PF18`은 불성립. G14 원안을 통과시키지 않는다. |
| P0-B: Plumlee와 Olynyk 동시 보유 | Plumlee 보장 계약의 2021–22 Team Salary와 **표준 자리 +1**을, 동일한 나머지 명단에서 원역사 거래 실행 분기와 비교해 기록한다. Olynyk를 얻을 별도 cap room/예외/사인앤트레이드와 이를 가능하게 할 선수·권리·현금/급여 변화를 이름·날짜·상대별로 제시한다. | 경로를 증명하기 전 `CAP_AND_SLOT_HOLD`. 다른 선수의 분/계약/역사 비용도 필수. 두 선수 보유를 가능하다고 확정하지 않는다. |
| P0-C: 8월 거래는 미실행, 1/23 전 Plumlee 이탈 | 후속 거래/방출일·상대·반대급부·보장급여/캡 처리와 Charlotte의 센터 경로를 제시한다. | 1/23 Plumlee 분은 0; G14의 10/20 조합도 **이탈일이 10/20 전이면** 불성립. |

`+1`은 다른 14명·계약 사건을 같게 둔 **한 선수의 상대적 자리 비용**이며 Detroit가 절대 `16/15`라는 주장도, 정확 cap 차이가 `$16.1m`라는 주장도 아니다. `$16.1m`은 두 해 합계다. 팀 전체 급여·2021–22 Plumlee 개별 연봉·Olynyk 정확 첫해 연봉/예외·대체 roster 총수는 확인 전 `HOLD`다. 비보장 2022–23은 **2021–22 보장**을 지우지 않는다. 상대 Charlotte가 원역사에서 잃은 센터 수신과 픽 권리를 다른 선수에게 자동 보전하지 않는다.

## 3. 근거 지위와 다음 빈칸

| 지위 | 결론 |
|---|---|
| 사실 | 원역사 Plumlee 계약의 2021–22 보장 구간; 8/6 거래와 Olynyk·Lyles·Lee 서명; 구단이 설명한 Plumlee 처분→Olynyk 영입 cap 경로; 기존 DB1 미선택 보드. |
| 추론 | P0의 Plumlee 보유와 원역사 Olynyk 취득을 같은 사건 목록으로 복사하면 cap/자리와 거래 자산 연쇄가 누락된다. |
| 후보 | P0-A/B/C는 비교 시험이며 추천이나 정본이 아니다. 기존 P1은 신규 거래 자산/수락 근거가 나올 때까지 HOLD. |
| 작가확정 | 이번 0건. 대체 Olynyk 계약 여부, Plumlee의 1/23 Detroit 보유·활동·분, DB1 최종 지명/거래 모두 HOLD. |

다음은 **2021-07-29→08-06→10-20→2022-01-23 Detroit의 이름별 계약·급여·표준 자리 원장**을 만들고 P0-B의 실제 cap 경로가 있는지 판정하는 것이다. Charlotte의 센터 대체와 G14의 Grant/Olynyk 의료·PF/C 분도 함께 추적한다. Chicago 2020–21 정확 시즌, G14 Detroit `PRIOR_HOLD`·Orlando `ROLE_HOLD`, G16/G17은 미완료다. 7개 매크로 게이트는 1완료·1진행·5대기, 진행 중 포함 6개가 남는다.

[CLI·제한 맹점 검토](../reviews/R01_O15G15AD_CAP_CLI_AND_SOURCE_BLIND.md)는 각 도구의 실제 원문 접근 여부와 잘못된 권리 이월을 분리한다.
