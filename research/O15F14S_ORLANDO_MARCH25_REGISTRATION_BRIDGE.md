# O-15F14-S — Orlando 3/24→3/27 Fournier 거래 등록 연결

- 기준: `main` `4bcb41f` / PR #274 병합 뒤.
- 판정: `PUBLIC_REGISTRATION_COUNT_PASS / MARCH25_27_CHARGE_AND_F2_HOLD`.
- 범위: F2의 **Orlando 일반계약·투웨이 자리 수**. 거래일 Team Salary, 정확 charge, Boston TPE·픽 의무, F1/F3/F4/F5는 별도다.

## 공식 관측과 거래 연속성

| 시점 | 1차 근거 | 원역사에서 확인한 것 |
|---|---|---|
| 3/21 | [NBA ORL–BOS 경기책 첫 장](https://statsdmz.nba.com/pdfs/20210321/20210321_ORLBOS_book.pdf) | Orlando 박스 명단 12명 + inactive 5명 = 계약 명단 관측 17명. Randle·Mané는 투웨이이므로 일반 15 + 투웨이 2. |
| 3/24 | [NBA PHX–ORL 경기책 첫 장](https://statsdmz.nba.com/pdfs/20210324/20210324_PHXORL_book.pdf) | Orlando 박스 명단 13명 + inactive 4명 = 17명. Randle·Mané가 박스에 함께 있고, Anthony·Fultz·Isaac·Ross가 inactive다. 일반 15 + 투웨이 2의 **거래 직전 재관측**이다. |
| 2/15→3/25 | [Orlando 2022–23 공식 미디어 가이드, 인쇄 229쪽 거래 연혁](https://cdn.nba.com/teams/uploads/sites/1610612753/2022/11/orlando-magic-media-guide-2022-23.pdf) | 공개 거래 목록은 2/15 Randle 투웨이 서명 다음 사건을 3/25 세 거래로 기록한다. 3/21~24 사이 별도 명단 거래가 이 목록에 없다. |
| 3/25 | [Orlando Fournier 발표](https://www.nba.com/magic/orlando-magic-acquire-two-future-second-round-draft-picks-boston-celtics-evan-fournier-trade-20210325), [Denver 거래 발표](https://www.nba.com/magic/orlando-magic-acquire-rj-hampton-garry-harris-draft-pick-denver-nuggets-aaron-gordon-gary-clark-trade-20210325) | 원역사에서 Fournier→Teague와 Gordon·Clark→Harris·Hampton은 각각 1:1, 2:2. 미디어 가이드는 별도의 Vučević·Aminu→Carter·Porter 2:2도 같은 날 기록한다. |
| 3/27 | [NBA Teague 방출 발표](https://www.nba.com/news/magic-waive-veteran-guard-jeff-teague), 위 미디어 가이드 | Teague는 Orlando에 합류하지 않았지만 3/25 거래로 취득했고 3/27 방출됐다. 불참을 3/25–26 등록·비용 0으로 처리할 수 없다. |

[Orlando의 Randle 투웨이 설명](https://www.nba.com/magic/news/magic-beat-knicks-behind-big-scoring-night-from-terrence-ross-tenacious-team-defense-20210217)과 [Mané 투웨이 확인](https://www.nba.com/magic/orlando-magic-waive-karim-mane-20210413)을 두 경기책의 선수 분류에 사용했다. 경기책은 그날 계약서 원본은 아니지만, 3/24 17명 관측과 구단 거래 연혁을 합치면 공개 자료상 3/25 직전 자리 수를 더 이상 3/21 단면에만 의존하지 않는다.

## 승인된 대체 경로의 자리 산술

아래는 기존 작가 승인 방향의 **조건부 실행 검사**다. 3/25 대체 세계에서 Vučević·Aminu가 남아 원역사의 Chicago 2:2 거래가 없고, Gordon·Clark를 Harris·Nnaji로 바꾸는 2:2와 Fournier를 Teague로 바꾸는 1:1을 실행한다. Boston 쪽 Fournier 계약·두 2R은 기존 방향 그대로 둔다. Nnaji는 실제 Denver의 [2020 22순위 지명](https://www.nba.com/nuggets/news/nuggets-pick-zeke-rj-202011) 사실을 대체 세계에 그대로 옮기는 선수가 아니다. 이 경로는 [기존 Orlando 급여안](../simulation/ORLANDO_2020_21_PAYROLL_BOUND.md)의 **대체 24순위 120% 일반 신인계약**을 조건으로 한다. 그 계약이 체결되지 않거나 투웨이 등 다른 종류라면 이 행의 `2:2` 결과를 재판정한다.

| 사건 뒤 | 일반 | 투웨이 | 계산 |
|---|---:|---:|---|
| 3/24 거래 전 | 15 | 2 | 공식 경기책의 13+4명 중 투웨이 2명 |
| 3/25 Gordon/Clark 대체 거래 뒤 | 15 | 2 | 일반 2명 송출·2명 수취. 원역사 Hampton 대신 Nnaji 수취는 작가 승인 방향 |
| 3/25 Fournier 거래 뒤 | 15 | 2 | Fournier 송출·Teague 수취. 두 거래의 순서를 바꿔도 중간 일반 수는 15 |
| 3/27 Teague 방출 뒤 | 14 | 2 | 방출은 명단 자리 −1. 잔여 계약 부담을 지우지 않음 |

**사실:** 두 공식 경기책의 17명과 Orlando 거래 연혁·발표·방출 날짜. **추론:** 위 대체 거래를 실제와 같은 날짜·계약 자격으로 실행할 때 자리 수가 15를 넘지 않는다는 것. **후보:** 그 사건 순서와 등록을 대체 세계에 적용하는 실행안. **작가확정:** 기존 T1~T4 사건 *방향* 및 Draft/Chicago 관련 승인만 재사용하며, 정확 거래·급여·건강·시즌 결과는 여기서 새로 확정하지 않는다.

F2 조건 4의 **공개 등록 자리 산술**은 위 조건에서 통과했다. 팀의 3/25–27 누적 부담·Teague 잔여 보수·대체 Gordon 대가와 Vučević 잔류의 apron/예외 영향은 미확인이다. 경기책과 미디어 가이드가 거래 승인서나 계약 charge 원장을 대체하지 않는다. F2 전체 및 `K_TRANSACTIONS`는 `HOLD`; F 전체 `0/5`, A 최종 `0/3`, K 종료 `0/4`다. K1/L2·CP2는 잠정이며 `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`를 유지한다. [Claude 문서 단독 반증](../reviews/R01_O15F14S_REGISTRATION_REBUTTAL.md)은 계약 종류 조건 명시만 수용했다. 독립 원문 조사는 아니다.
