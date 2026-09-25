# O-15G15B — Suggs 동시대 비교군과 Orlando 240분 조건부 증명

- 기반 `main` PR #182 / `75d0357`. [입력·출처](../research/O15G15B_COMPARATOR_INPUTS.json), [재현 결과](CHICAGO_2021_22_G15B_STRESS.json), [계산기](../tools/build_chicago_2021_22_g15b.py).
- 판정: `THREE_PEER_SENSITIVITY / TWO_CONDITIONAL_MINUTE_WITNESSES / G14_HOLD_UNCHANGED / NOT_INDEPENDENT`.
- 2021-10-19 이후 Suggs의 실제 NBA 경기·부상·효율을 개막 입력에 넣지 않았다. 비교 선수의 NCAA 2019–20/NBA 2020–21 시즌 결과만 쓴다. 일부 NBA 미디어 가이드는 나중에 간행됐지만 인용한 행은 개막 전에 종료된 2020–21 시즌의 회고 기록이다.

## 세 동시대 가드의 분당 변화: 묘사 자료, 예측 모형 아님

비율은 `(NBA 루키 총계 / NBA 분) ÷ (대학 마지막 시즌 총계 / 대학 분)`이다. NCAA 분·FGA/3PA/FTA/TOV는 [UNC](https://goheels.com/sports/mens-basketball/stats/2019-20) Cole Anthony, [Iowa State](https://cyclones.com/sports/mens-basketball/stats/2019/) Tyrese Haliburton, [Georgia](https://georgiadogs.com/sports/mens-basketball/stats/2019-20) Anthony Edwards 공식 누적표에서 읽었다. NBA 루키 총계는 [Orlando 미디어 가이드의 Cole](https://magicweb.blob.core.windows.net/resources/communications/orlando-magic-media-guide-2024-25.pdf), [Sacramento 미디어 가이드의 Haliburton](https://cdn.nba.com/teams/uploads/sites/1610612758/2022/07/kings_media_guide_2021-22_FINAL.pdf), [Minnesota 미디어 가이드의 Edwards](https://cdn.nba.com/teams/uploads/sites/1610612750/2022/03/2021-22_Timberwolves_Media_Guide.pdf) 행에서 읽었다. 대학 시즌의 나이·포지션·사용률, NBA 팀의 분과 역할이 서로 다르다.

| 선수 | 대학→NBA 분당 FGA | 3PA | FTA | TOV | 비교상 차이 |
|---|---:|---:|---:|---:|---|
| Cole Anthony | 0.965 | 0.736 | 0.617 | 0.831 | 대학 22경기·무릎 수술, NBA 47경기·34선발 |
| Tyrese Haliburton | 1.173 | 1.103 | 0.575 | 0.697 | 대학 2년차 연결형, NBA 58경기·다른 공격 역할 |
| Anthony Edwards | 1.095 | 0.970 | 0.727 | 0.840 | 대학·NBA 모두 높은 슛 사용량, NBA 72경기 |

Georgia의 공식 누적 페이지는 Edwards 1,057분, 별도 학교 PDF의 검색 렌더링은 1,059:54를 보여 준다. 본 계산은 누적 페이지 1,057분을 사용했고 **출처 간 3분 미만 차이를 HOLD**로 남긴다. 비교군 세 명은 무작위 표본도 동일 역할군도 아니다. 비율의 중앙값은 각 항목에서 다른 선수를 뽑을 수 있어 **하나의 실존 선수 시즌을 구성하지 않는다**.

| Suggs의 조건부 DET 24분 | 무보정 대학 분당 노출 | 비교군 최소~최대 스트레스 | 항목별 중앙값 스트레스 |
|---|---:|---:|---:|
| FGA | 8.497 | 8.202~9.963 | 9.307 |
| 3PA | 2.869 | 2.111~3.165 | 2.781 |
| FTA | 3.145 | 1.809~2.285 | 1.942 |
| 선수 TOV | 2.428 | 1.692~2.039 | 2.016 |

이 범위는 **세 선택된 사례의 관측 범위**다. 신뢰구간·리그 전환계수·Suggs 실력 예측이 아니다. 효율·득점·어시스트·리바운드·승패는 계산하지 않았다. 원역사 Detroit의 슛/자유투/실책을 주인공이 영향을 준 새 팀의 실제 총량으로 취급하지 않는다.

## G14 Detroit 네 정책에 다시 투입한 반례

[G14](CHICAGO_2021_22_PAIRED_REVIEW.md)의 기존 24팀·정책 결과는 **숫자16/PRIOR_HOLD4/ROLE_HOLD4 그대로**다. 별도 G15B 스트레스에서 세 선수별 묶음 × 네 정책 12개만 계산했다. 경기의 역사적 **선수 합산** FGA90·FTA13·TOV16을 공통 예산으로 고정했으며 공식 팀 총 포제션과 다르다.

| 정책 | 세 묶음 중 숫자 | 스트레스 선수 수 | 핵심 결과 |
|---|---:|---:|---|
| B14A Grant 원시 기회 고정 | 3/3 | 각 9명 | Suggs FTA 0.709~0.874로 압축 |
| B14B Grant·Suggs·Patrick 고정 | 3/3 | 각 7명 | 비코어가 FTA 잔여를 분담 |
| B14C 모두 비례 조정 | 3/3 | 각 10명 | Suggs FTA 0.962~1.193으로 압축 |
| B14D 비코어 고정 | **0/3** | 해당 없음 | 비코어 원시 FTA만으로 예산 초과 `BUDGET_HOLD` |

세 묶음의 원시 FTA 총합은 24.431~24.907인데 역사적 선수 FTA 예산은 13이다. B14A/B/C의 숫자 출력은 **고정 예산의 산술 배분**이며 농구 현실성 통과가 아니다. 0.75~1.25의 스트레스 표식도 G14가 정한 수동 경계다. Suggs의 24분과 Detroit의 다른 선수 분/역할, 팀 자유투 총량을 하나의 실제 경기로 확정하려면 포제션·수비·드라이브/파울 구조와 팀 예산 자체를 새로 판단해야 한다. 그러므로 기존 네 `PRIOR_HOLD`를 자동 해제하지 않는다.

## Orlando: 12분을 채운 두 수학적 증명

[G14의 12분 부족](CHICAGO_2021_22_PAIRED_REVIEW.md)은 Cole 36분 상한과 매분 지정 주 가드 규칙의 결과다. O15A는 [NBA의 2021 드래프트 전 Herbert Jones 평가](https://www.nba.com/draft/2021/prospects/herbert-jones)에 기록된 Alabama 주 전개자 경험을 근거로 **NBA에서도 12분 PG를 맡길 수 있는지 시험하는 후보**다. 그 대학 경험은 NBA 2022-01-23 수행·의료 허가의 증명이 아니다. O15C는 [Orlando의 실제 2021-12-17 Gravett 단기 계약](https://www.nba.com/magic/orlando-magic-sign-ford-gravett-johnson-and-schofield-10-day-contracts-20211217)을 참고한 **새 계약 분기**다. 실제 계약이 1/23까지 유지됐다고 가정하지 않는다.

| 4×12분 동시 5명 증명 | PG 48분 | 전체 | 남은 조건 |
|---|---|---|---|
| O15A Herbert 내부 전개 | Cole36·Herbert12 | 9명·240분, 각 선수≤36, 포지션별48 | G7 DB1의 Herbert33/Mobley3, Schofield·Brazdeikis 등 등록·당일 가용, Herbert NBA PG 역할·공간/수비 비용 |
| O15C Gravett 계약 | Cole36·Gravett12 | 10명·240분, 각 선수≤36, 포지션별48 | 1/23 이전 Gravett의 **새 적법 계약·자리/급여·당일 활동**, 나머지 등록·가용, 상대 분 비용 |

두 조합은 **순서 없는 네 12분 블록**이다. 실제 교대·의료·계약·전력 동등성·성적은 증명하지 않는다. Franz/Suggs/Hampton/Carter를 ORL 명단에 복원하지 않았고, 공식 1/23 보고서의 MCW/Fultz/Harris/Isaac/Moore/Ross 결장 사유를 채택하는 조건에서도 이들을 분 수신자로 쓰지 않았다. O15B Okeke 주 가드와 O15D Cole48은 이번 240분 증명에 넣지 않았다. A는 추가 가드 계약이 없다는 점에서 **다음 역할 감사 우선 후보**지만, Herbert의 36분 다중 역할과 기존 선수 분·슛 공간 비용이 크다. C는 명시적 계약·등록 감사를 통과하기 전까지 차선 조건부안이다. 둘 다 작가확정이 아니다.

## 다음 게이트

1. DET는 90/13/16 역사 예산을 그대로 고정할 근거를 먼저 재검토하고, 당시 포제션·파울·FGA/FTA 상관과 대체 로스터 비용을 연결한다. 세 비교군의 중앙값을 공식 환산계수로 승격하지 않는다.
2. ORL은 2021 여름부터 2022-01-23까지 조건부 15+2 등록·두 계약·실제 활동 가능성을 일자별로 닫고, O15A의 주 전개 수비/공간 비용과 O15C의 실명 계약 비용을 비교한다.
3. 그 뒤에만 새 날짜별 양팀 공격기회·생산성·시즌 경로를 계산한다. G14 원본은 덮어쓰지 않는다.

`PROJECT_FREEZE v0.30 PARTIAL`; 설계/원고 `CLOSED`; `author_locked=false`, `season_selected=false`, `exact_execution_cleared=false`, `manuscript_allowed=false`. G16 전체 독립 검수는 미실시다.
