# O-15G15AY — Chicago 2021–22 투웨이 두 자리와 #39 계약 분기

- 기준: `main` `eb502e2`, [G8 계약 순서](../simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.md), [G15AW/AX Wieskamp 계약 민감도](O15G15AW_CHICAGO_WIESKAMP_CONTRACT_CLASS_GATE.md). 판정: `HISTORICAL_TWO_WAY_OCCUPANCY_IDENTIFIED / ALTERNATE_SLOT_ASSIGNMENT_HOLD`.
- 이 문서는 D2의 **조건부 명단·계약 검문**이다. Chicago #39 Wieskamp 지명·서명이나 다른 두 선수의 대체 계약, D1 시즌 결과를 확정하지 않는다.

## 시점이 붙은 원역사 증거

| 날짜 | 직접 확인한 범위 | 이 설계의 경계 |
|---|---|---|
| 2021-07-27 | [NBA 2021–22 규칙 발표](https://pr.nba.com/nba-board-of-governors-play-in-roster-rules-2021-22-season/): 일반계약 최대 15명 외 투웨이 최대 2명, 해당 시즌 투웨이 활성 명단 최대 50경기. | 동시에 세 명을 투웨이로 둘 수 없다. 50경기는 자동 출전 보장이나 분 배정이 아니다. |
| 2021-08-19 | [Chicago 구단 공동 발표](https://www.nba.com/bulls/news/bulls-sign-free-agents-bradley-green-and-dotson): 원역사 Dotson 투웨이 계약 발표. | 대체 Chicago에서도 동일 날짜·조건으로 수락했다고 추정하지 않는다. |
| 2021-10-25 | [Windy City Bulls 공식 개막 명단 발표](https://windycity.gleague.nba.com/news/windy-city-bulls-finalize-training-camp-roster-announce-basketball-operations-staff): Chicago 소속 투웨이로 **Devon Dotson·Tyler Cook**, 별도 Chicago 배정 선수로 **Marko Simonović**를 명시. Windy City의 개막 경기는 11/6 예정이라고 적었다. | 이는 **Windy City G League 개막용 10/25 공지**다. NBA Chicago의 10/20 첫 경기 명단·계약 효력일을 이 문서 하나로 인증하지 않는다. Simonović를 셋째 투웨이로 세지 않는다. |
| 2021-10-28 | [NBA 공식 Chicago–New York 경기 기록 첫 페이지](https://statsdmz.nba.com/pdfs/20211028/20211028_NYKCHI_book.pdf): Bulls 비활성 명단에 Cook·Dotson 각각 `G League - Two-Way`, Simonović `G League - On Assignment`라고 직접 표시. | 10/25 구단 발표와 독립된 **NBA 경기일 관측**이다. 10/28 계약 분류를 10/20 Chicago 첫 경기나 대체 세계 계약 날짜로 소급하지 않는다. |

원역사 10/25 공지와 10/28 NBA 경기 기록은 두 투웨이 자리를 Dotson·Cook으로 일치해 표시한다. 하지만 G8의 대체 Chicago 계약 원장은 실제 역사 명단을 복사하지 않는다. 원역사의 선수가 대체 세계에 언제·어떤 조건으로 합의했는지는 별도 사건이다. NotebookLM이 같은 Windy City 발표를 “opening-night roster”로 요약한 것은 **Windy City의 11/6 개막** 범위에서만 맞다. Chicago의 [10/20 NBA 첫 경기](https://www.nba.com/bulls/gameday/keys-game-bulls-pistons-102021) 명단 증거로 넓히지 않는다.

## 상호 배타적 대체 세계 자리 후보

아래 숫자는 [G8 SQ1의 조건부 일반계약 15명](../simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.json)에서 **Wieskamp 계약 종류 한 행만** 바꾸고 다른 일반계약 14명을 고정한 구조 시험이다. Dotson·Cook의 실제 대체 계약은 입력에 없다. `TW-D`, `TW-C`, `TW-V`는 서로 동시에 채택할 수 없다.

| 후보 | #39 Wieskamp | 다른 투웨이 자리 | 일반계약 / 투웨이 자리 | 원역사와 달라지는 선수 비용·HOLD |
|---|---|---|---:|---|
| `STD` — 현재 G8 주 경로 | 2년 일반 최소계약 제안 | Dotson+Cook이 모두 투웨이일 수도 있으나 **각각 새 대체 계약 필요** | 15 / 최대 2 | #39가 일반 마지막 자리를 사용한다. Dotson·Cook의 동의·날짜·급여는 미인증. Simonović를 이 15명에 추가할 자리는 없다. |
| `TW-D` | 투웨이 제안 | Dotson이 다른 한 자리 | 14 / 2 | Cook의 원역사 투웨이를 동시에 보존할 수 없다. 아직 계약 전이면 미취득, 이미 계약했다면 적법한 종료·전환 등 별도 사건이 필요하다. Cook의 프런트코트/개발 역할 대체는 `HOLD`. |
| `TW-C` | 투웨이 제안 | Cook이 다른 한 자리 | 14 / 2 | Dotson의 원역사 투웨이를 동시에 보존할 수 없다. 이미 계약했다면 별도 처리 필요. 가드 개발·비상 깊이의 대체는 `HOLD`. |
| `TW-V` | 투웨이 제안 | 한 자리 공석 | 14 / 1 | 공석은 합법적 구조 후보일 뿐 Dotson·Cook의 미서명·이적·방출 사실이 아니다. 두 선수의 행선과 그 역할 비용은 모두 `HOLD`. |

`STD`의 15명은 G8의 **대체 세계** 15명이며 원역사 Chicago 전체 명단이 아니다. Simonović의 Windy City 배정 표시는 투웨이 자리를 쓰지 않지만, 그를 대체 Chicago의 일반계약 선수로 살리려면 이 원장 안에 자리·급여·권리를 새로 배치해야 한다. [G1A의 정상일 10인 분표](../simulation/CHICAGO_2021_23_CONTINUATION.md)에 #39가 없다는 사실만으로 그의 계약 종류나 Dotson/Cook의 대체 NBA 출전시간을 정하지 않는다. #39 투웨이가 실제 체결되면 NBA 50경기 활성 한계·G League 체류·전환/포스트시즌 적격성을 별도 추적한다.

## 예산 순서에서 놓치기 쉬운 한 자리

[G15AW](O15G15AW_CHICAGO_WIESKAMP_CONTRACT_CLASS_GATE.md)의 첫해 `STD→TW` 알려진 **apron 예산** 차이 `−$925,258` 및 최종 일반 15→14는 그대로다. 이것을 **모든 중간 normal-cap 행이 즉시 `$925,258` 내려간다**는 뜻으로 사용하지 않는다. [G8 SQ3의 공개 산술 예시](../simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.md)는 Caruso 서명 직후 일반 11명과 12명 기준 미충원 차지 1개를 둔다. 이 예시의 #39 일반 최저급 `$925,258`은 미충원 차지 `$925,258`을 대체하므로 해당 단계 normal-cap 합계 `$101,044,029`가 같다. #39가 투웨이이면 일반 11명·미충원 1개를 유지하며 그 단계 합계 역시 `$101,044,029`이다. **다음 Bradley가 실제 일반계약에 서명**해야 12명에 닿아 미충원 차지가 없어지고, 같은 예시의 그 시점 합계는 일반 #39 경로 `$102,833,285` 대 투웨이 #39 경로 `$101,908,027`이 된다. 이는 `SQ3` 숫자 설명이지 추천 `SQ1`을 다른 경로로 바꾸는 계산이 아니다.

이후 일반명단 14명으로 끝나는 투웨이안은 평시 14명 하한에 닿는다. [당시 NBA CBA 101](https://cdn.nba.com/manage/2021/03/2018-19-CBA.pdf)의 일반명단·Team Salary/투웨이 구분을 적용하되, 미확인 FA 보류액·예외·급여 순증 `R`·방출잔액·동의가 있는 실제 팀 샐러리는 `null`이다. 다른 일반계약 한 명이 불성립하면 새 계약/명단 조정이 필요하다. 2022–23에도 투웨이 상태를 쓰려면 G15AX의 적법한 2년 계약 또는 재계약 조건을 먼저 충족해야 하며, Dotson/Cook의 2021 자리 기록을 2022로 이월하지 않는다.

## 판정과 다음 입력

- **사실:** 원역사 10/25 Windy City 발표와 10/28 NBA 공식 경기 기록의 Dotson·Cook 투웨이 및 Simonović 배정 구분, NBA 2021–22 동시 투웨이 2자리 상한.
- **추론:** #39가 투웨이이면 기존 두 선수를 **모두** 투웨이로 동시에 보존할 수 없다. G8 SQ3의 12명 미달 중간 normal-cap 차지는 #39 계약 종류만 바꾼 즉시 사라지지 않는다.
- **후보:** `STD`, `TW-D`, `TW-C`, `TW-V`. 현재 G8의 `STD` 주 비교안을 유지하되 다른 투웨이 둘의 대체 서명까지 승인한 것은 아니다.
- **작가확정:** 신규 0건. #39 지명·계약 선택, Dotson/Cook의 대체 소속·계약, 14번째 일반계약 유지, 날짜·선수 수락·2022 연속성은 `HOLD`.

Codex는 공식 NBA/Windy City/Bulls의 검색 가능한 원문과 G8/G15AW의 자리·예산을 직접 대조하고, 10/28 NBA 경기 기록의 비활성 명단을 별도로 확인했다. NotebookLM CLI에는 Windy City URL을 소스로 추가하고 그 출처와 기존 NBA 규칙 출처 두 개에만 한정 질의했다. Dotson·Cook 및 두 자리 상한은 반환했으나 원역사 10/25 자료에서 대체 계약을 만들지 못하며, 같은 원문 재독은 독립 증거 증가가 아니다. 10/28 경기 기록은 NotebookLM에 넣지 않았다. Bulls 8/19 URL의 NotebookLM 직접 추가는 실패했다. Antigravity CLI는 직전 G15AX에서 `read_url_content DONE` 뒤 429 개인 사용 한도로 본문 회수에 실패했으므로 이번 추가 원문 팩은 `NOT_RUN / NEW_EVIDENCE_0`이다. Claude CLI의 도구 없는 문서 단독 반증과 제한 source-blind는 [별도 기록](../reviews/R01_O15G15AY_TWO_WAY_SLOT_REBUTTAL_AND_BLIND.md)에 수용·기각을 분리했다. 검수 출력은 독립 원자료가 아니며 이 구간 검문은 G16 전체 독립 검수나 D1/D2 정확 실행의 PASS가 아니다.

다음은 `STD` 주 경로의 Dotson/Cook 대체 계약 가능성 및 G8 명단의 누락된 실명 일반계약 선수를 **날짜별**로 검사한다. #39에게 어떤 개발/비상 역할을 줄지도 구단 경쟁·육성 계획과 함께 따지되 분·부상·거래를 발명하지 않는다. `TW-*`는 #39 선수/대리인 선택과 상대 자리 처리의 원문이 생길 때만 전진한다. D1 F1~F5 PASS 0/5·A1~A3 0/3·K 네 묶음 0/4, K1/L2·CP2 잠정, G1A 선수 동의 `HOLD`. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, `manuscript_allowed=false` 유지.
