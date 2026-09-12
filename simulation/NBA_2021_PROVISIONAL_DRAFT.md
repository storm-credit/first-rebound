# O-15F14-M — 2021 잠정 추첨·픽 결산

- 상태: `PROVISIONAL_CONDITIONAL_RESULT / CP2_WORKFLOW_APPROVED`.
- [계산 JSON](NBA_2021_PROVISIONAL_DRAFT.json), [실행 전 기록](NBA_2021_DRAW_PREREGISTRATION.md), [승인 권위](../canon/CHICAGO_2020_21_CP2_APPROVAL.json).
- 최종 작가·시즌·정확 실행 잠금 false, v0.30 PARTIAL·설계/원고 CLOSED. 새 선수 지명은 아직 없다.

## 실행 증거

입력·알고리즘을 GitHub 커밋 [2f77a4e](https://github.com/storm-credit/first-rebound/commit/2f77a4eac597dc7eaab0127ec4d83123e42b5c85)에 먼저 게시했다. 원격 tree `3c78b28d053b71353a827caf04803698a6e6d12f`가 사전 검증 tree와 일치한 뒤 첫 작품 seed를 실행했다. 동일 입력 재생성만 허용했고 결과 선택을 위한 seed 탐색은 없다.

| 시도 | 네 공 | 원소유 팀 | 판정 |
|---|---|---|---|
| 1 | 5·8·10·11 | CHA | 1순위 |
| 2 | 1·3·6·10 | HOU | 2순위 |
| 3 | 1·10·12·13 | ORL | 3순위 |
| 4 | 1·4·7·8 | HOU | 이미 당첨돼 제외 |
| 5 | 2·6·10·11 | OKC | 4순위 |

전체 조합 1,001개 중 팀 배정 1,000개·미배정 1개. CHI/NOP 동률은 NOP→CHI, 조합은 38/37이다. 상위4 당첨 후 원소유 순서를 기준으로 2R 동률을 역전했다. 플레이인 승패는 K의 정규시즌 계산값이 아니라 L2 사건안이고, 이번 추첨이 그 사실 지위를 바꾸지 않는다.

## 전체 원소유 순번

아래 팀은 **픽 발생 원소유 팀**이다. 모든 현재 보유 구단을 뜻하지 않는다. 실제 2021 지명 선수와 후대 성공을 붙이지 않는다.

| 1R 순번 | 원소유 | 2R 순번 | 원소유 |
|---|---|---|---|
| 1 | CHA | 31 | HOU |
| 2 | HOU | 32 | DET |
| 3 | ORL | 33 | ORL |
| 4 | OKC | 34 | CLE |
| 5 | DET | 35 | OKC |
| 6 | CLE | 36 | MIN |
| 7 | MIN | 37 | TOR |
| 8 | TOR | 38 | CHA |
| 9 | NOP | 39 | CHI |
| 10 | CHI | 40 | NOP |
| 11 | SAC | 41 | SAC |
| 12 | WAS | 42 | WAS |
| 13 | SAS | 43 | IND |
| 14 | GSW | 44 | SAS |
| 15 | IND | 45 | BOS |
| 16 | BOS | 46 | MEM |
| 17 | MEM | 47 | MIA |
| 18 | MIA | 48 | GSW |
| 19 | ATL | 49 | POR |
| 20 | NYK | 50 | NYK |
| 21 | POR | 51 | ATL |
| 22 | LAL | 52 | DAL |
| 23 | DAL | 53 | LAL |
| 24 | MIL | 54 | MIL |
| 25 | LAC | 55 | DEN |
| 26 | DEN | 56 | LAC |
| 27 | BKN | 57 | PHI |
| 28 | PHI | 58 | BKN |
| 29 | PHX | 59 | PHX |
| 30 | UTA | 60 | UTA |

## Chicago·Minnesota 자산

| 자산 | 조건부 결산 | 이후 의미 |
|---|---|---|
| CHI 자체1R | 10순위 유지 | 승인된 Vučević 미영입 경로. ORL에 넘기지 않음 |
| CHI/NOP 2R | CHI39·NOP40, 스왑 미행사 추천 | CHI가 더 앞선 자체 픽 보유. 실제 Ayo38 복사 금지 |
| MIN 자체1R | 7순위→GSW | 기존 top3 보호 채무가 유지되는 조건. 전달 시 해당 2022 대체채무 종료 |
| MIN 자체2R | 36순위→OKC | 보도된 이전 자산 경로 유지 조건 |

보호 근거는 [원출처 목록](../research/NBA_2021_PROVISIONAL_DRAFT_SOURCES.json)에 있다. 2021 전 구단의 전체 이전 계약 감사를 완료한 것은 아니다. BOS16→OKC 같은 여름 거래를 추첨 결과만으로 새 세계에 넣지 않는다. CHI의 10·39에서 거래/선수를 정하려면 새 보드의 상위 지명과 당시 팀 수요를 연결한다.

## 시즌 처리와 후속

CP2 작업 분기는 `K1: CHI31–41/MIN24–48 → L2: CHI Washington전 승리·Indiana 원정 패배 → 위 잠정 추첨`으로 이어진다. 정확 건강·등록·charge HOLD는 [채택 준비 색인](CHICAGO_2020_21_ADOPTION_READINESS.md)에 남는다. 이제 [2021–23 거래·계약 작업안](CHICAGO_2021_23_CONTINUATION.md)을 실행할 수 있으며 CP2 승인 반복 질문은 없다.
